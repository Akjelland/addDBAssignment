from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask import flash,redirect,url_for

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///saveData.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "supersecretkey"  

db = SQLAlchemy(app)


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie1 = db.Column(db.String(50), nullable=False)
    movie2 = db.Column(db.String(50), nullable=False)
    movie3 = db.Column(db.String(50), nullable=False)
    



with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/page1', methods=['GET', 'POST'])
def page1():
    if request.method == 'POST':
        movie1 = request.form.get('form1FirstInput')
        movie2 = request.form.get('form1SecondInput')
        movie3 = request.form.get('form1ThirdInput')

        try:
            new_profile = Profile(
                movie1=movie1,
                movie2=movie2,
                movie3=movie3,
            )
            db.session.add(new_profile)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            error = "An error occurred while saving your profile. Please try again."
            return render_template('page1.html', error=error)

        return render_template('success/page1Success.html',movie1=movie1,movie2=movie2,movie3=movie3)


    return render_template('page1.html')




@app.route('/PreviousResponses', methods=['GET', 'POST'])
def prevResp1():
    items = Profile.query.all() 
    id=db.session.query(Profile.id).all()

    if request.method == 'POST': 
        for item in items:
            print(item)

        return render_template('page1PreviousResp.html')
    return render_template('page1PreviousResp.html',items=items,id=id,)

@app.route('/delete/<int:item_id>', methods=['POST'])
def delete_entry(item_id):
    try:
        item= Profile.query.get(item_id)
        db.session.delete(item)
        db.session.commit()
        flash(f" '{item_id}' deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting entry: {str(e)}", "danger")
    return redirect(url_for('prevResp1'))
@app.route('/edit/<int:item_id>', methods=['POST'])
def edit_entry(item_id):
    try:
        item = Profile.query.get_or_404(item_id)

        new_text1 = request.form.get('movie1_edit')
        new_text2 = request.form.get('movie2_edit')
        new_text3 = request.form.get('movie3_edit')

        if new_text1:
            item.movie1 = new_text1

        if new_text2:
            item.movie2 = new_text2

        if new_text3:
            item.movie3 = new_text3

        db.session.commit()

    except Exception as e:
        db.session.rollback()
        flash(f"Error editing entry: {str(e)}", "danger")

    return redirect(url_for('prevResp1'))


@app.route('/page2', methods=['GET', 'POST'])
def page2():
    if request.method == 'POST':
        game = request.form.get('game', '').strip()
        year = request.form.get('release', '').strip()
        star1 = request.form.get('rating1star', '').strip()
        star2 = request.form.get('rating2star', '').strip()
        star3 = request.form.get('rating3star', '').strip()
        star4 = request.form.get('rating4star', '').strip()
        star5 = request.form.get('rating5star', '').strip()
        fstar = 0
        if(star5):
            fstar = 5
        elif(star4):
            fstar = 4
        elif(star3):
            fstar = 3
        elif(star2):
            fstar = 2
        elif(star1):
            fstar = 1
        else:
            fstar = 0
        return render_template('success/page2Success.html', gameName=game, gameYear=year, stars=fstar)
    return render_template('page2.html')

@app.route('/page3', methods=['GET', 'POST'])
def page3():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        weapon = request.form.get('weapon', '').strip()
        amount = request.form.getlist('fromAmount')
        number = len(amount)
        playstyle = request.form.get('playstyle','').strip()
        return render_template('success/page3Success.html',name=name, weapon=weapon, fromAmount=amount, fromNumber=number, playstyle=playstyle)
    return render_template('page3.html')

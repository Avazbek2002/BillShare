import os
from functools import reduce
from flask import Flask, jsonify, render_template, request, redirect, session, url_for, flash
from itsdangerous import json
from werkzeug import security
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from database import db, User, Bill, SharedBill, Image, dbinit

app = Flask(__name__)
app.secret_key = 'My name is Avazbek'
UPLOAD_FOLDER = 'static/uploads/'

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///billshare.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

db.init_app(app)


with app.app_context():
    # drop everything, create all the tables, then put some data into the tables
    db.drop_all()
    db.create_all()
    dbinit()

#route to the index
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        household = request.form['household']
        password = request.form['user_password']
        email_database = [k.email for k in User.query]
        household_database = [k.household for k in User.query]
        user = User.query.filter_by(email = email).first()
        
        if (email.lower() in email_database) and (household in household_database) and security.check_password_hash(user.password, password):
            session['email']=email
            session['household'] = household
            session['userid'] = user.id

            return redirect('/Bills')
        else:
            return redirect('/badlogin')
        #hashed_password = password_database[username]
    return render_template('index.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        household = request.form['household']
        hashed_password = security.generate_password_hash(request.form['user_password'])
        db.session.add(User(name, email.lower(), hashed_password, household, 100))
        db.session.commit()
        return redirect('/welcome')
    
    return render_template('register.html')

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/Bills', methods = ["POST", "GET"])
def Bills():
    user_id = session['userid']
    all_users = len(User.query.all())
    balance = User.query.filter_by(id=user_id).first().balance
    if request.method == 'POST':
        name = request.form["name"]
        amount = request.form["amount"]
        date = str(request.form["deadline"])
        if 'file' not in request.files:
            flash('No file part')
            return redirect (request.url)
        
        file = request.files["file"]
        
        if file.filename == '':
            flash('No image selected for uploading')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            flash('Allowed image types are - png, jpg, jpeg, gif')
            return redirect(request.url)

        db.session.add_all([Bill(name, amount, date, user_id)])
        bill_id = Bill.query.filter_by(name=name, user_id=user_id).first().bill_id
        db.session.add_all([SharedBill(bill_id = bill_id, paid = False, user_id=user.id) for user in User.query.all()])
        image = Image(filename=file.filename, bill_id=bill_id)
        db.session.add(image)
        db.session.commit()
        flash(message="New bill added "+amount+"£", category="warning")
        return redirect('/Bills')
    
    dict = {k.name : [round(k.amount/all_users, 2), k.deadline, User.query.filter_by(id=k.user_id).first().name, k.bill_id, SharedBill.query.filter_by(user_id=user_id, bill_id=k.bill_id).first().paid] for k in Bill.query.all()}
    overall = sum([k.amount/all_users for k in Bill.query.all()])
    username=User.query.filter_by(id=user_id).first().name
    return render_template('Bills.html', value = dict, overall = overall, balance = balance, name=username)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/paid', methods = ["POST", "GET"])
def paid():
    user_id = session['userid']
    all_users = len(User.query.all())
    balance = User.query.filter_by(id=user_id).first().balance
    print(balance)
    if request.method == "POST":
        paidBill = request.get_json()['bill']
        amount=Bill.query.filter_by(bill_id=paidBill).first().amount/all_users
        print(amount)
        if (balance - amount) >= 0:
            update = SharedBill.query.filter_by(bill_id=paidBill, user_id=user_id).first()
            update.paid=True
            db.session.commit()
            update = User.query.filter_by(id=user_id).first()
            update.balance = round(balance - amount, 2)
            db.session.commit()
            results = {'processed': 'true',
                       'balance' : str(round(balance - amount, 2))}
            temp = True
            for sh in SharedBill.query.all():
                temp = temp and sh.query.filter_by(bill_id=paidBill).first().paid
            if temp:
                Bill.query.filter_by(bill_id=paidBill).delete()
                db.session.commit()
            return jsonify(results)

        else:
            results = {'processed': 'false',
                       'balance' : balance}
            return jsonify(results)

@app.route('/badlogin')
def badlogin():
    return render_template('badlogin.html')

@app.route('/topUp', methods=["GET", "POST"])
def topUp():
    if request.method == "POST":
        amount = request.get_json()['amount']
        user_id = session['userid']
        update = User.query.filter_by(id=user_id).first()
        update.balance += float(amount)
        db.session.commit()
        result = {'processed': 'true',
                  'balance' : update.balance}
        return jsonify(result)

@app.route('/remove', methods=["GET", "POST"])
def remove():
    user_id=session['userid']
    if request.method=="POST":
        bill_id = request.get_json()['bill']
        SharedBill.query.filter_by(user_id=user_id, bill_id =bill_id).delete()
        db.session.commit()
        result = { 'processed' : 'true'}
        return result


@app.route('/logout')
def logout():
    session.pop('userid', None)
    return redirect('/')

@app.route('/display', methods=['GET', 'POST'])
def display():
    if request.method=='POST':
        bill_id = request.form['bill']
        image = Image.query.filter_by(bill_id=bill_id).first()
        return redirect(url_for('static', filename='uploads/' + image.filename), code=301) 


from flask import render_template, request, flash, redirect, session
from flask_app import app
from flask_app.models.user import User
from flask_app.models.post import Post
from flask_app import bcrypt


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login/page')
def login_page():
    return render_template('login_page.html')

@app.route('/register/page')
def register_page():
    return render_template('register_page.html')

@app.route('/register', methods =['POST'])
def register():
    if not User.validate(request.form):
        return redirect('/register/page')
    data ={ 
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['user_id'] = id
    return redirect('/homepage')


@app.route('/login', methods = ['POST'])
def login():
    user = User.get_email(request.form)
    if not user:
        flash("Invalid Email", "login")
        return redirect('/login/page')
    if not bcrypt.check_password_hash(user.password,request.form['password']):
        flash("Invalid Password", "login")
        return redirect('/login/page')
    session['user_id'] = user.id
    print("Session Data:", session)
    return redirect('/homepage')






@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')







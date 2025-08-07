from flask import Blueprint,render_template,redirect,url_for,flash,request
from forms import Login,Registration
from app import db
from models import User
from flask_login import login_user,logout_user,login_required
from werkzeug.security import generate_password_hash,check_password_hash
auth_route=Blueprint('auth_route',__name__)

@auth_route.route('/register',methods=['GET','POST'])
def register():
    form=Registration()
    if form.validate_on_submit():
        print(form.password.data)
        password=generate_password_hash(form.password.data)
        data=User(name=form.username.data,email=form.email.data,hash_password=password)
        db.session.add(data)
        db.session.commit()
        flash("Register sucessfully",'success')
        return redirect(url_for('auth_route.login'))
    else:
        if request.method == 'POST':
            print(form.errors)  # 👈 Show what's wrong with input
    return render_template('register.html',form=form)

@auth_route.route('/login',methods=['GET','POST'])
def login():
    form=Login()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.hash_password,form.password.data):
            login_user(user) #Logs the user in (creates a session using Flask-Login).
            flash("Successfully logedin!",'success')
            return redirect(url_for('home_route.dashboard'))
        flash("Invalid credentials ",'danger')   
            
    return render_template('login.html',form=form)

@auth_route.route('/logout')
@login_required
def logout():
    logout_user()
    flash("LogOut successfully",'success')
    return redirect(url_for('auth_route.login'))



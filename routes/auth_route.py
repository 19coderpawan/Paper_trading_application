from flask import Blueprint,render_template,redirect,url_for
from forms import Login,Registeration
from app import db
from models import User
from werkzeug.security import generate_password_hash,check_password_hash
auth_main=Blueprint('auth_main',__name__)

@auth_main.route('/register',methods=['GET','POST'])
def register():
    form=Registeration()
    if form.validate_on_submit():
        password=generate_password_hash(form.password.data)
        data=User(name=form.name.data,email=form.email.data,hash_password=password)
        db.session.add(data)
        db.session.commit()
        redirect(url_for('home'))
    return render_template('register.html',form=form)

@auth_main.route('/login',methods=['GET','POST'])
def login():
    form=Login()
    if form.validate_on_submit():
        pass
    return render_template('login',form=form)

from flask import Blueprint,render_template
from forms import Login,Registeration
auth_main=Blueprint('auth_main',__name__)

@auth_main.route('/register',methods=['GET','POST'])
def register():
    form=Registeration()
    if form.validator_on_submit():
        pass
    return render_template('register.html',form=form)

@auth_main.route('/login',methods=['GET','POST'])
def login():
    form=Login()
    if form.validator_on_submit():
        pass
    return render_template('login',form=form)

from flask import Blueprint

auth_main=Blueprint('auth_main',__name__)

@auth_main.route('/register',methods=['GET','POST'])
def register():
    pass

@auth_main.route('/login',methods=['GET','POST'])
def login():
    pass

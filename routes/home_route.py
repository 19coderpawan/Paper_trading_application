from flask import Blueprint, render_template,redirect

main=Blueprint('home_route',__name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/dashboard')
def dashboard():
    pass

@main.route('/trade')
def trade():
    pass

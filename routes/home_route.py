from flask import Blueprint, render_template,redirect
from flask_login import login_required
main=Blueprint('home_route',__name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@main.route('/trade')
def trade():
    pass

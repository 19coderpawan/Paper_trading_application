from flask import Blueprint, render_template,redirect
from flask_login import login_required,current_user
from models import Transaction,Portfolio
main=Blueprint('home_route',__name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/dashboard')
@login_required
def dashboard():
    portfolio=Portfolio.query.filter_by(user_id=current_user.id).all()
    transaction=Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.timestamp.desc()).limit(10).all()
    
    return render_template('dashboard.html',transaction=transaction)


from flask import Blueprint, render_template,redirect
from flask_login import login_required,current_user
from models import Transaction,Portfolio
from sqlalchemy import func
main=Blueprint('home_route',__name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/dashboard')
@login_required
def dashboard():
    portfolio=Portfolio.query.filter_by(user_id=current_user.id).all()
    # totalInvested=Portfolio.query.with_entities(func.sum(Portfolio.quantity*Portfolio.avg_price)).filter_by(user_id=current_user.id).scalar()
    transaction=Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.timestamp.desc()).limit(10).all()
    
    totalInvested=sum(item.avg_price*item.quantity for item in portfolio)
    net_worth=totalInvested+current_user.balance

    return render_template('dashboard.html',transaction=transaction,total_invested=totalInvested,net_worth=net_worth)


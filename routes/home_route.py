from flask import Blueprint, render_template,redirect
from flask_login import login_required,current_user
from models import Transaction
main=Blueprint('home_route',__name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/dashboard')
@login_required
def dashboard():
    # transaction=Transaction.query.filter_by(user_id=current_user.id).first()
    # transactions=None
    # if(transaction!=None):
    #    transactions=transaction
    #    return render_template('dashboard.html',transactions=transactions)
    return render_template('dashboard.html')


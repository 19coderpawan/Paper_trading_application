from flask import Blueprint,redirect,render_template,url_for,request,flash
from forms import Trade
from app import db
from models import Portfolio,Transaction
from flask_login import login_required,current_user
from datetime import datetime,timezone

trade_route=Blueprint('trade_route','__name__')

@trade_route.route('/trade',methods=["GET","POST"])
@login_required
def trade():
    form=Trade()
    if form.validate_on_submit():
        symbol=form.symbol.upper.data
        quantity=float(form.quantity.data)
        trade_type=form.trade_type.data

        price=100 #temperory later wil fetch usin API.
        total_cost=quantity*price

        # check for curr user portfolio
        portfolio_item=Portfolio.query.filter_by(user_id=current_user.id ,symbol=symbol).first()

        if trade_type =='buy':
            #check if user has enough balace to buy.
            if current_user.balance<total_cost:
                flash("Insufficient Balance!",'danger')
                return redirect(url_for('trade_route.trade'))
            # if have suffienct balance .
            current_user.balance-=total_cost

            # if user_portfolio exists
            if portfolio_item:
                old_total_value = portfolio_item.avg_price * portfolio_item.quantity
                new_total_value = old_total_value + total_cost
                portfolio_item.quantity += quantity
                portfolio_item.avg_price = new_total_value / portfolio_item.quantity
            else:
                portfolio_item=Portfolio(user_id=current_user.id,symbol=symbol,quantity=quantity,avg_price=price)
                db.session.add(portfolio_item)  

        elif trade_type=='sell':
            if not portfolio_item or portfolio_item.quantity < quantity:
                flash("Not enough quantity to sell.", "danger")
                return redirect(url_for('trade_route.trade')) 
               
            # Increase balance from sale
            current_user.balance += total_cost

            # Reduce quantity or delete portfolio entry
            portfolio_item.quantity -= quantity
            if portfolio_item.quantity == 0:
                db.session.delete(portfolio_item)   

        # ✅ Record transaction
        transaction=Transaction(
            user_id=current_user.id,
            symbol=symbol,
            quantity=quantity if trade_type=="buy" else -quantity,
            price=price,
            transaction_type=trade_type,
            timestamp=datetime.now(timezone.utc)
        )           
        db.session.add(transaction)
        db.session.commit()
        flash(f"{trade_type.capitalize()} order executed for {symbol} at ${price}.", "success")
        return redirect(url_for('home_route.dashboard'))
    
    return render_template('trade.html',form=form)



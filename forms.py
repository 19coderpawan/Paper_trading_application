from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,DecimalField,SelectField
from wtforms.validators import DataRequired ,EqualTo,Email,NumberRange


class Registration(FlaskForm):
    username=StringField("UserName",validators=[DataRequired()])
    email=StringField("Email",validators=[DataRequired(),Email()])
    password=PasswordField("Password",validators=[DataRequired()])
    confirm_password=PasswordField("Confirm_Password",validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField("Register")

class Login(FlaskForm):
    email=StringField("Email",validators=[DataRequired(),Email()])
    password=PasswordField("Password",validators=[DataRequired()])
    submit=SubmitField("LogIn")    

class Trade(FlaskForm):
    symbol=StringField("Stock/Crypto Symbol", validators=[DataRequired()])
    quantity=DecimalField("Quantity",validators=[DataRequired(),NumberRange(min=0.0001)])
    trade_type=SelectField("Type",choices=[('buy','Buy'),('sell','Sell')],validators=[DataRequired()])
    submit=SubmitField("Trade Submit")

    

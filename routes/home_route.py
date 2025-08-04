from flask import Blueprint, render_template,redirect

main=Blueprint('main',__name__)

@main.route('/')
def home():
    pass

@main.route('/dashboard')
def dashboard():
    pass

@main.route('/trade')
def trade():
    pass

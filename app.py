from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from instance.config import Config

db=SQLAlchemy()

def create_app():
    app=Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    from models import User,Trade
    with app.app_context():
        db.create_all()
    
    from routes import main
    app.register_blueprint(main)

    return app

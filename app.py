from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from instance.config import Config
from extension import db

def create_app():
    app=Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    from models import User    
    with app.app_context():
        print("🧪 SQLAlchemy tables:", db.metadata.tables.keys())  # debug pri
        db.create_all()
    
    from routes.home_route import main
    app.register_blueprint(main)
    from routes.auth_route import auth_route
    app.register_blueprint(auth_route)

    return app

if __name__=="__main__":
    app=create_app()
    app.run(debug=True)
    


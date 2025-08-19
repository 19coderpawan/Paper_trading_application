from flask import Flask
from instance.config import Config
from extension import db
from flask_login import LoginManager
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
load_dotenv() # take environment variables from .env
login_manager=LoginManager()
migrate=Migrate()
def create_app():
    app=Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app,db)
    login_manager.login_view = 'auth_route.login'  # 👈 Redirects to login page if @login_required fails
    login_manager.login_message_category = 'info'  # 👈 Flash category for login message

    from models import User    
    # with app.app_context():
    #     # print("🧪 SQLAlchemy tables:", db.metadata.tables.keys())  # debug pri
    #     db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    from routes.home_route import main
    app.register_blueprint(main)
    from routes.auth_route import auth_route,google_bp
    # app.register_blueprint(auth_route)
    app.register_blueprint(auth_route, url_prefix="/auth")
    app.register_blueprint(google_bp, url_prefix="/login")  # for Google OAuth
    from routes.trade_route import trade_route
    app.register_blueprint(trade_route)
    

    return app

if __name__=="__main__":
    app=create_app()
    app.run(debug=True)
    


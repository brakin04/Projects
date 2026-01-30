from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask import render_template, request
import os
from app.logging_config import logger 
from flask_cors import CORS
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'main.login'

def create_app():
    logger.info("Finance program started") 
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'super-secret-key'

    if os.environ.get("DOCKER") == "1":
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////instance/finance.db'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = True

    db.init_app(app)
    migrate = Migrate(app, db)
    login_manager.init_app(app)
    CORS(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        logger.debug(f"load_user called with ID: {user_id}")
        return User.query.get(int(user_id))

    from . import routes
    app.register_blueprint(routes.bp)
    # app.register_blueprint(status_api)

    @app.errorhandler(500)
    def handle_internal_error(error):
        logger.error(f"HTTP 500 error: {error}")
        return render_template("500.html"), 500
    
    @app.errorhandler(404)
    def handle_not_found_error(error):
        logger.error(f"HTTP 500 error: {error}")
        return render_template("500.html"), 404

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        logger.critical(f"Unexpected critical error: {error}", exc_info=True)
        return render_template("500.html"), 500
    
    @app.before_request
    def log_request():
        logger.info(f"Request: {request.method} {request.path}")

    @app.after_request
    def log_response(response):
        logger.info(f"{request.method} {request.path} returned {response.status}")
        return response

    return app
import atexit

def log_exit():
    logger.critical("Finance program exited unexpectedly or was terminated.")
atexit.register(log_exit)

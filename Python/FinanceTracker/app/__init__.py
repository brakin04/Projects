from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import HTTPException
from flask_login import LoginManager
from flask import render_template, request
import os
from .logging_config import logger 
from flask_cors import CORS
from flask_migrate import Migrate
from datetime import datetime
import shutil

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login' # maybe main.login
def create_app(test_config=None):
    logger.info("Finance program started") 
    app = Flask(__name__)
    if test_config:
        app.config.from_object(test_config)
    else:
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

    from .routes import finance_bp, auth_bp, main_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(finance_bp)
    app.register_blueprint(main_bp)
    # app.register_blueprint(status_api)

    @app.errorhandler(HTTPException)
    def handle_internal_error(error):
        logger.error(f"HTTP {error.code} error: {error}")
        description = error.description if error.description else None
        return render_template("error.html", errorNumber=error.code, description=description), error.code

    # @app.errorhandler(404)
    # def handle_not_found_error(error):
    #     logger.error(f"HTTP 404 error: {error}")
    #     return render_template("error.html", errorNumber=404), 404

    # @app.errorhandler(403)
    # def handle_forbidden_error(error):
    #     logger.error(f"HTTP 403 error: {error}")
    #     return render_template("error.html", errorNumber=403), 403

    @app.errorhandler(Exception)
    def handle_error(error):
        logger.critical(f"Unexpected critical error: {error}", exc_info=True)
        return render_template("error.html", errorNumber=500, description=None), 500

    @app.before_request
    def log_request():
        logger.info(f"Request: {request.method} {request.path}")

    @app.after_request
    def log_response(response):
        logger.info(f"{request.method} {request.path} returned {response.status}")
        return response

    return app
import atexit

# Backup database and log exit
def log_backup_exit():
    logger.critical("Finance program exited unexpectedly or was terminated.")
    try:
        source = '../instance/finance.db'
        backup_dir = '../backups'
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dest = f"{backup_dir}/backup_{timestamp}.db"
        
        shutil.copy2(source, dest)
        logger.info(f"Database backed up to {dest}")
    except Exception as e:
        logger.error(f"Backup failed: {e}")

atexit.register(log_backup_exit)

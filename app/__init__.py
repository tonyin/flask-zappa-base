import os
from flask import Flask
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from flask_login import LoginManager
from flask_mail import Mail
from flask_s3 import FlaskS3

from config import config

basedir = os.path.abspath(os.path.dirname(__file__))

# Extensions
db = SQLAlchemy(metadata=MetaData())
csrf = CSRFProtect()
mail = Mail()
s3 = FlaskS3()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'account.login'

def create_app(config_name='development'):
    if config_name == 'development': print("App is in DEV MODE!")
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Set up extensions
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    s3.init_app(app)
    migrate = Migrate(app, db)

    # Blueprints
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .account import account as account_blueprint
    app.register_blueprint(account_blueprint, url_prefix='/account')

    return app

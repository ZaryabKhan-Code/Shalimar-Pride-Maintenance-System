from flask_sqlalchemy import SQLAlchemy
from flask_login import *
from flask_mail import *

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
def init_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:zaryab@localhost/SPM'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = "SPMSYSTEM_UNBREABLE_21132__=++II9900"
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = 'your_email_address_here'
    app.config['MAIL_PASSWORD'] = 'your_email_password_here'
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)


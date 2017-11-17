from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///VegaWeb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 1


db = SQLAlchemy(app)

Base = declarative_base()
Base.query = db.session.query_property()
from app.models import User,Crowdfund
from app import views
db.init_app(app)

Base.metadata.create_all(bind=db.engine)
db.create_all()

BCRYPT_LOG_ROUNDS = 12
bcrypt = Bcrypt(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(userid):
    return Crowdfund.query.filter(Crowdfund.id == userid).first()

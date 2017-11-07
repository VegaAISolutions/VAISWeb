from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

app = Flask(__name__)

dbloc = app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///VegaWeb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 0


db = SQLAlchemy(app)
engine = create_engine("sqlite:///VegaWeb.db")
db_session = scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()
from app.models import User,Crowdfund
db.init_app(app)

Base.metadata.create_all(bind=engine)
db.create_all()

BCRYPT_LOG_ROUNDS = 12
bcrypt = Bcrypt(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(userid):
    return Crowdfund.query.filter(Crowdfund.id == userid).first()

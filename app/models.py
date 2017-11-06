from sqlalchemy import Column, Integer, String, Boolean
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app import app

db = SQLAlchemy(app)

db_session = scoped_session(sessionmaker(autocommit=True,autoflush=False,bind=db))
#Base = declarative_base()
#Base.query = db_session.query_property()


class User(db.Model):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True)
    email = Column(String(80))
    fname = Column(String(80))
    lname = Column(String(80))
    msg = Column(String(300))
    email_confirmed = Boolean(0)

    def __repr__(self):
        """docstring for __repr__"""
        return self.email


with app.app_context():
    db.init_app(app)
    db.create_all()

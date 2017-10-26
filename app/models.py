from sqlalchemy import Column, Integer, String
from flask_sqlalchemy import SQLAlchemy
from app import app

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True)
    email = Column(String(80))
    fname = Column(String(80))
    lname = Column(String(80))
    msg = Column(String(300))

    def __repr__(self):
        """docstring for __repr__"""
        return self.email


with app.app_context():
    db.init_app(app)
    db.create_all()

from sqlalchemy import Column, Integer, String
from VegaWeb import db

class User(db.model):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True)
    email = Column(String(80))

    def __repr__(self):
        """docstring for __repr__"""
        return self.email

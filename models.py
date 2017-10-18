from VegaWeb import db_session,Base
from sqlalchemy import Column, Integer, String, Boolean

class User(Base):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True)
    email = Column(String(80))



    def __repr__(self):
        """docstring for __repr__"""
        return self.email

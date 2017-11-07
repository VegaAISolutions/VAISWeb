
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from app import db_session,Base,app,db
from sqlalchemy import Column, Integer, String, Boolean, BLOB
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql.expression import Executable, ClauseElement
import flask_bcrypt as bcrypt


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String(80), nullable=True)
    fname = Column(String(80), nullable=True)
    lname = Column(String(80), nullable=True)
    msg = Column(String(300), nullable=True)

    def __repr__(self):
        """docstring for __repr__"""
        return self.id


class Crowdfund(Base,UserMixin):
    __tablename__ = 'cf'
    id = Column(Integer, primary_key=True)
    email = Column(String(80), nullable=True)
    confirmed = Boolean()
    _password = Column(String(128), nullable=True)

    def __repr__(self):
        """docstring for __repr__"""
        return self.id



    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def _set_password(self, plaintext):
        self._password = bcrypt.generate_password_hash(plaintext)

    def is_correct_password(self, plaintext):
        return bcrypt.check_password_hash(self._password.encode('utf-8'), plaintext)

    @staticmethod
    def get_or_create(session, model, defaults=None, **kwargs):
        instance = session.query(model).filter_by(**kwargs).first()
        if instance:
            return instance
        else:
            params = dict((k, v) for k, v in kwargs.iteritems() if not isinstance(v, ClauseElement))
            if defaults:
                params.update(defaults)
            instance = model(**params)
            return instance

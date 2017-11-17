from flask_login import UserMixin
from app import Base,db
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql.expression import ClauseElement
import flask_bcrypt as bcrypt


class User(db.Model,Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(80), nullable=True)
    fname = Column(String(80), nullable=True)
    lname = Column(String(80), nullable=True)
    msg = Column(String(300), nullable=True)


class Crowdfund(db.Model,Base,UserMixin):
    __tablename__ = 'cf'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(80), nullable=True)
    confirmed = Boolean()
    _password = Column(String(128), nullable=True)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def _set_password(self, plaintext):
        self._password = bcrypt.generate_password_hash(plaintext)

    def is_correct_password(self, plaintext):
        enc = self._password
        return bcrypt.check_password_hash(enc, plaintext)

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

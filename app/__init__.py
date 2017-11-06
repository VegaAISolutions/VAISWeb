from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from sqlalchemy import create_engine
from pandas import DataFrame, Series
app = Flask(__name__)


class CustomSeries(Series):
    @property
    def _constructor(self):
        return CustomSeries

    def custom_series_function(self):
        return 'OK'
class CustomDataFrame(DataFrame):
    """
    Subclasses pandas DF, fills DF with simulation results, adds some
    custom plotting functions.
    """

    def __init__(self, *args, **kw):
        super(CustomDataFrame, self).__init__(*args, **kw)

    @property
    def _constructor(self):
        return CustomDataFrame

    _constructor_sliced = CustomSeries

    def custom_frame_function(self):
        return 'OK'



sql_engine = create_engine('sqlite:///test.db', echo=False)
connection = sql_engine.raw_connection()
#df = CustomDataFrame.to_sql('data', 'sql_engine',index=False, if_exists='append')
from app.models import db, User

bcrypt = Bcrypt(app)



login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(userid):
    return User.query.filter(db.id == userid).first()

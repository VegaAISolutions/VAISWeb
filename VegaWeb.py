from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
import feedparser
# from models import User //to be used later
from html.parser import HTMLParser


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):

        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

app = Flask(__name__)

app.jinja_env.filters['strip_tags'] = strip_tags

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///VegaWeb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 0
db = SQLAlchemy(app)

db.create_all()


medium = feedparser.parse('https://medium.com/feed/@VegaAISolutions')
twitter = feedparser.parse('https://twitrss.me/twitter_user_to_rss/?user=VegaAISolutions')


@app.route('/')
def index():
    output = render_template('index/index.html', medium=medium, twitter=twitter, strip_tags=strip_tags)
    return output

@app.route('/crowdfund')
def crowdfund():
    output = render_template('crowdfund/index.html')
    return output

@app.route('/whitepaper')
def whitepaper():
    output = render_template('index/whitepaper.html')
    return output


app.run(debug=True,host='0.0.0.0',port=1900,threaded=True)

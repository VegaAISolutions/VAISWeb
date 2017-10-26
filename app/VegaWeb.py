from app import app
from flask import render_template
from flask import request
import feedparser
from html.parser import HTMLParser
import flask_mailgun as mailgun
from app import models
from app.models import db




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

medium = feedparser.parse('https://medium.com/feed/@VegaAISolutions')
twitter = feedparser.parse('https://twitrss.me/twitter_user_to_rss/?user=VegaAISolutions')

def email(text):
    mailgun.MailgunApi('vegais.com', '2e5bf1dda730f83f65727d0163c4b6b7')
    mailgun.MailgunApi.send_email(text)


@app.route('/', methods=['GET', 'POST'])
def index():

    submission = models.User(lname=request.form.get('lname'), email=request.form.get('email'), msg=request.form.get('msg'), fname=request.form.get('fname'))
    db.session.add(submission)
    db.session.commit()
    output = render_template('index/index.html', medium=medium, twitter=twitter, strip_tags=strip_tags)
    try:
        test = request.form.get('msg')
        try:
            print(test + "\n From: \n" + request.form.get('email'))
            email(test + "\n From: \n" + request.form.get('email'))
        except:
            print("email could not be sent")
            print(test)
    except:
        print("no user found")

    return output

@app.route('/crowdfund')
def crowdfund():
    output = render_template('crowdfund/index.html')
    return output

@app.route('/whitepaper')
def whitepaper():
    output = render_template('index/whitepaper.html')
    return output


@app.route('/deposit')
def deposit():
    output = render_template('crowdfund/deposit.html')
    return output

app.run(debug=True,host='0.0.0.0',port=1900,threaded=True)

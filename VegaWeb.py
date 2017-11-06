from app import app
import feedparser
from html.parser import HTMLParser
from app.models import db, db_session, User
from flask import Flask, redirect, url_for, render_template, flash, request, session, g
from flask_login import LoginManager, login_user, logout_user, current_user
from itsdangerous import URLSafeTimedSerializer
from subprocess import PIPE, Popen
app.config['SECRET_KEY'] = 'Everything in the world is either a potato, or not a potato.'
ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])


## Useful if you need to access os cmd's ##
def cmd(command):
  return Popen(command, shell=True, stdout=PIPE)

def email(msg):
    cmd("curl -s --user 'api:2e5bf1dda730f83f65727d0163c4b6b7'"
        "\ https://api.mailgun.net/v3/vegais.com/messages "
        "\ -F from='noreply <noreply@vegais.com>' "
        "\ -F to=cryptsmith@gmail.com "
        "\ -F subject='Hello' "
        "\ -F text=" + msg + "")


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


@app.route('/', methods=['GET', 'POST'])
def index():

    submission = User(lname=request.form.get('lname'), email=request.form.get('email'), msg=request.form.get('msg'), fname=request.form.get('fname'))
    #db_session.add(submission)
    #db_session.commit()
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


@app.route("/register")
def register():

    output = render_template('dashboard/register.html')
    return output

@app.route('/register/create', methods=["GET", "POST"])
def create_account():
    output = render_template("dashboard/register.html")
    if request.form.get("email"):
        output = redirect(url_for("index"))
        email = request.form.get("email")
        if request.form.get("password") is not None:
            password = request.form.get("password")
        else:
            password = "test"
        exists = User.query.filter_by(email=email).first()
        if current_user.is_authenticated():
            user = User(nickname=request.form.get("username"), email=email, password=password, email_confirmed=0)
        else:
            user = User(nickname=request.form.get("username"), email=email, password=password, email_confirmed=0)

        # Now we'll send the email confirmation link
        subject = "Confirm your email"

        token = ts.dumps(user.email, salt='email-confirm-key')

        confirm_url = url_for(
            'confirm_email',
            token=token,
            _external=True)

        html = render_template(
            'dashboard/email/activate.html',
            confirm_url=confirm_url)

        if exists == None:
            db_session.add(user)
            db_session.commit()
            login_user(user, True)
            #drill(user.email, subject, html)
        else:
            db_session.merge(user)
            db_session.commit()
            login_user(user, True)
            output = redirect(url_for("index"))
    return output


@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = ts.loads(token, salt="email-confirm-key", max_age=86400)
    except:
        return "404"

    user = User.query.filter_by(email=email).first()

    user.email_confirmed = True
    session['user'] = user.id
    db_session.commit()
    return redirect('/')


@app.route("/lostpw")
def lostpw():
    return render_template('dashboard/lostpw.html')


@app.route('/logout')
def logout():
    logout_user()
    session.pop('user', None)
    return redirect(url_for('index'))


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.form.get("email"):
        user = User.query.filter_by(email=request.form.get("email")).first()
        if user.is_correct_password(request.form.get("password")):
            login_user(user, True)

            session['user'] = user.id
            return redirect(url_for('index'))
        else:

            return redirect(url_for('login'))

    return render_template('dashboard/login.html')


app.run(debug=True,host='0.0.0.0',port=1900,threaded=True)

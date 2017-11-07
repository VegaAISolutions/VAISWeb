from app import app
import feedparser
from html.parser import HTMLParser
from app import db_session, db
from app.models import User
from app.models import Crowdfund
from flask import redirect, url_for, render_template, request, session, g
from flask_login import login_user, logout_user, current_user
from itsdangerous import URLSafeTimedSerializer
from flask_login import LoginManager
import requests


### Give darrel a hand ###
app.config['SECRET_KEY'] = 'Everything in the world is either a potato, or not a potato.'
msg = None
### Password Salt Key ###
ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])

#### MailGun Key ####
api_key = 'key-5c140fd81223a56d283edc025a523a0e'



@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = User.query.get(session['user_id'])


@app.after_request
def after_request(response):
    db_session.remove()
    return response


lm = LoginManager(app)

@lm.user_loader
def load_user(id):
    if id is None or id == 'None':
        id = -1
    return Crowdfund.query.get(int(id))



        #its a lie, this method IS abstracted
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


def send(msg,subject,to):
    if msg is not None:
        payload = {'from': 'noreply <noreply@vegais.com>', 'to': to, 'subject': subject,
                   "text": strip_tags(msg)}
        ## kuro's ghetto auth and curl ##
        r1 = requests.get('https://api:' + api_key + '@api.mailgun.net/v3/samples.mailgun.org/log')
        r2 = requests.post("https://api:" + api_key + "@api.mailgun.net/v3/m.vegais.com/messages",params=payload)
        print(r2.text, r2.url)
    return print(r2.status_code)

@app.route('/', methods=['GET', 'POST'])
def index():
    if "@" not in request.url:
        if request.form.get('email') is not None:
            #try:
            usr = User(email=request.form.get('email'), lname=request.form.get('lname'), fname=request.form.get('fname'),msg=request.form.get('message'))
            em = request.form.get("email")
            exists = User.query.filter_by(email=em).first()
            if exists == None:
                db_session.add(usr)
                #db_session.commit()
            else:
                db_session.merge(usr)
                #db_session.commit()
            sub = "Thanks for reaching out!"
            send(request.form.get('msg'), sub, request.form.get('email'))
            #except:
                #print("email could not be sent")
                #print(sys.exc_info()[0])
        else:
            render_template('index/index.html', medium=medium, twitter=twitter, strip_tags=strip_tags)

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


@app.route('/deposit')
def deposit():
    output = render_template('crowdfund/deposit.html')
    return output


@app.route("/register")
def register():
    output = render_template('crowdfund/register.html')
    return output

@app.route('/register/create', methods=["GET", "POST"])
def create_account():
    output = render_template("crowdfund/register.html")
    if request.form.get("email-reg"):
        output = redirect(url_for("index"))
        email = request.form.get("email-reg")
        if request.form.get("password-reg") is not None:
            password = request.form.get("password-reg")
        else:
            password = "test"
        exists = Crowdfund.query.filter_by(email=email).first()
        user = Crowdfund(email=email, password=password, confirmed=0)
        db_session.add(user)
        db_session.commit()


        # Now we'll send the email confirmation link
        subject = "Confirm your email"

        token = ts.dumps(user.email, salt='email-confirm-key')

        confirm_url = url_for(
            'confirm_email',
            token=token,
            _external=True)

        html = render_template(
            'crowdfund/activate.html',
            confirm_url=confirm_url)

        if exists == None:
            db_session.add(user)
            db_session.commit()
            login_user(user, True)
            send(html, subject, user.email)
        else:
            db_session.merge(user)
            db_session.commit()
            login_user(user, True)
            output = redirect(url_for("crowdfund"))
    return output


@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = ts.loads(token, salt="email-confirm-key", max_age=86400)
        print(email)
    except:
        return "404"

    user = Crowdfund.query.filter_by(email=email).first()

    user.email_confirmed = True
    session['user'] = user.id
    db_session.commit()
    return redirect('/crowdfund')


@app.route("/lostpw")
def lostpw():
    return render_template('crowdfund/lostpw.html')


@app.route('/logout')
def logout():
    logout_user()
    session.pop('user', None)
    return redirect(url_for('index'))


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.form.get("email"):
        user = Crowdfund.query.filter_by(email=request.form.get("email-login")).first()
        if user.is_correct_password(request.form.get("password-login")):
            login_user(user, True)

            session['user'] = user.id
            return redirect(url_for('crowdfund'))
        else:

            return redirect(url_for('login'))

    return render_template('crowdfund/login.html')

sauce = "rfgJHUJHG657YHjhjhmhugy6453678gjgf"
@app.route('/join')
def join():
    output = render_template('crowdfund/join.html',ethaddy=sauce)
    return output

app.run(debug=True,host='0.0.0.0',port=1900,threaded=True)

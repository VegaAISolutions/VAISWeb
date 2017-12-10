import feedparser
from app import db
from app.models import User
from app.models import Crowdfund
from flask import redirect, url_for, render_template, request, session, g, send_from_directory
from flask_login import login_user, logout_user
from itsdangerous import URLSafeTimedSerializer
from flask_login import LoginManager
import requests,sys
from html.parser import HTMLParser
from app import app
from etherscan.accounts import Account
from etherscan.stats import Stats

### Give darrel a hand ###
app.config['SECRET_KEY'] = 'Everything in the world is either a potato, or not a potato.'
eth_addy = "0x7ee3032a81c998c9f38de324e848f187722e3edf"
### Password Salt Key ###
ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])

#### MailGun Key ####
mailgun_key = 'key-5c140fd81223a56d283edc025a523a0e'

#### Etherscan Key ####
etherscan_key = 'UG4SAB8DV97VX7V15Y43GIUCKZCCP4BCU2'


def price():
    api = Stats(api_key=etherscan_key)
    last_price = api.get_ether_last_price()
    return float(last_price['ethusd'])


def scan():
    api = Account(address=eth_addy, api_key=etherscan_key)
    balance = api.get_balance()
    return int(balance[:-15]) / 1000


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


@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = User.query.get(session['user_id'])


@app.after_request
def after_request(response):
    db.session.remove()
    return response


lm = LoginManager(app)


@lm.user_loader
def load_user(id):
    if id is None or id == 'None':
        id = -1
    return Crowdfund.query.get(int(id))


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

medium = feedparser.parse('https://medium.com/feed/@VegaAISolutions')
twitter = feedparser.parse('https://twitrss.me/twitter_user_to_rss/?user=VegaAISolutions')
youtube = feedparser.parse('https://www.youtube.com/feeds/videos.xml?channel_id=UCh0VfuCPgW88Y-N1vyNjinA')
soundcloud = feedparser.parse('http://feeds.soundcloud.com/users/soundcloud:users:112453360/sounds.rss')


def send(msg,subject,to):
    if msg is not None:
        payload = {'from': 'noreply <noreply@vegais.com>', 'to': to + ',contact@m.vegais.com', 'subject': subject,
                   "text": strip_tags(msg)}
        r1 = requests.get('https://api:' + mailgun_key + '@api.mailgun.net/v3/samples.mailgun.org/log')
        r2 = requests.post("https://api:" + mailgun_key + "@api.mailgun.net/v3/m.vegais.com/messages",params=payload)
        print(r2.text, r2.url)
    return print(r2.status_code)


@app.route('/', methods=['GET', 'POST'])
def index():
    if "@" not in request.url:
        if request.form.get('email') is not None:
            try:
                usr = User(email=request.form.get('email'), lname=request.form.get('lname'),
                           fname=request.form.get('fname'), msg=request.form.get('message'))
                em = request.form.get("email")
                exists = User.query.filter_by(email=em).first()
                if exists is not None:
                    db.session.add(usr)
                    db.session.commit()
                else:
                    db.session.merge(usr)
                    db.session.commit()
                sub = "Thanks for reaching out!"
                send(request.form.get('msg'), sub, request.form.get('email'))
            except:
                print("email could not be sent")
                print(sys.exc_info()[0])
    output = render_template('index/index.html', medium=medium, twitter=twitter, youtube=youtube,
                             soundcloud=soundcloud, strip_tags=strip_tags)
    return output



def inject():
    eth = scan()
    usdtotal = 2000 * price()
    usd = int(eth) * price()
    return [eth,usd,usdtotal]

@app.route('/crowdfund')
def crowdfund():
    output = render_template('crowdfund/index.html', eth=inject()[0],usd=inject()[1],usdtotal=inject()[2])
    return output


@app.route('/whitepaper')
def show_static_pdf():
    return send_from_directory(app.config['UPLOAD_FOLDER'], 'Vega-WhitePaper.pdf')

@app.route('/toc')
def toc():
    return send_from_directory(app.config['UPLOAD_FOLDER'], 'toc.pdf')

@app.route('/privacy')
def privacy():
    return send_from_directory(app.config['UPLOAD_FOLDER'], 'privacy.pdf')



# @app.route('/deposit')
# def deposit():
#     output = render_template('crowdfund/deposit.html')
#     return output
#
#
# @app.route("/register")
# def register():
#     output = render_template('crowdfund/register.html')
#     return output


@app.route('/register/create', methods=["GET", "POST"])
def create_account():
    output = render_template("crowdfund/register.html")
    if request.form.get("email-reg"):
        output = redirect(url_for("login"))
        email = request.form.get("email-reg")
        if request.form.get("password-reg") is not None:
            password = request.form.get("password-reg")
        else:
            password = "test"
        exists = Crowdfund.query.filter_by(email=email).first()
        user = Crowdfund(email=email, password=password, confirmed=0)


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

        if exists is not None:
            db.session.add(user)
            db.session.commit()
            login_user(user, True)
            send(html, subject, user.email)
        else:
            db.session.merge(user)
            db.session.commit()
            login_user(user, True)
            output = redirect(url_for("login"))
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
    db.session.commit()
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
    email = request.form.get("email-login")
    if email is not None:
        user = Crowdfund.query.filter_by(email=email).first()
        print(user)
        if user is not None:
            encodes = str(request.form.get("password-login"))
            if user.is_correct_password(encodes):
                login_user(user, True)
                session['user'] = user.id
                return redirect(url_for('crowdfund'))
            else:
                print(user)
                return redirect(url_for('login'))

    return render_template('crowdfund/login.html')


@app.route('/join')
def join():
    output = render_template('crowdfund/join.html',ethaddy=eth_addy)
    return output


@app.route('/thankyou')
def thankyou():
    output = render_template('crowdfund/thankyou.html')
    return output

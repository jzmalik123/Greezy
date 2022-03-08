from flask import Flask, request, flash, url_for, redirect, render_template, session
from werkzeug.routing import RequestRedirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///greezy_db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = "my_secret"

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    phone = db.Column(db.String(50))
    street_address = db.Column(db.String(200))
    zip_code = db.Column(db.String(50))
    city = db.Column(db.String(50))
    cryptocurrency = db.Column(db.String(50))
    wallet = db.Column(db.String(100))
    cb_credentials = db.relationship("CBCredentials", backref="user", uselist=False)
    strategy = db.relationship('Strategy', backref='user', uselist=False)

    def __init__(self, username, email, phone, password):
        self.username = username
        self.phone = phone
        self.email = email
        self.password = password


class CBCredentials(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    cb_key = db.Column(db.String(100))
    cb_secret = db.Column(db.String(100))
    cb_password = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Strategy(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    currency_id = db.Column('currency_id', db.Integer, default=1)
    aggressiveness = db.Column('aggressiveness', db.Integer, default=1)
    stop_loss = db.Column('stop_loss', db.Integer, default=1)
    audacity = db.Column('audacity', db.Integer, default=1)
    minimum_gains = db.Column('minimum_gains', db.Float, default=0.0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


def sessionExists():
    return session['user_id'] is not None


def redirectIfSessionExists():
    if sessionExists():
        raise RequestRedirect(url_for('home'))


def redirectIfSessionNotExists():
    if not sessionExists():
        flash("You must be logged in to access this page", "danger")
        raise RequestRedirect(url_for('login'))


@app.route('/admin')
def hello_admin():
    return 'Hello Admin'


@app.route('/guest/<guest>')
def hello_guest(guest):
    return 'Hello %s as Guest' % guest


@app.route('/user/<name>')
def hello_user(name):
    if name == 'admin':
        return redirect(url_for('hello_admin'))
    else:
        return redirect(url_for('hello_guest', guest=name))


@app.route('/')
def index():
    return redirect(url_for('home')) if sessionExists() else redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    redirectIfSessionExists()
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email, password=password).first()
        if user is None:
            flash("Invalid email or password", "danger")
        else:
            session['user_id'] = user.id
            return redirect(url_for('home'))
    return render_template('login.html', pageTitle='Login', cssFile='login')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    redirectIfSessionExists()
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']

        if User.query.filter_by(email=email).count() > 0:
            flash("User with email already exists", "danger")
        elif User.query.filter_by(username=username).count() > 0:
            flash("User with username already exists", "danger")
        else:
            user = User(username, email, phone, password)
            user.strategy = Strategy()
            user.cb_credentials = CBCredentials()
            db.session.add(user)
            db.session.commit()
            flash("User registered successfully", "success")
            return redirect(url_for('login'))
    return render_template('signup.html', pageTitle='Signup', cssFile='login')


@app.route('/home')
def home():
    redirectIfSessionNotExists()
    current_user = User.query.filter_by(id=session['user_id']).first()
    return render_template('home.html', pageTitle='Home', cssFile='dashboard', current_user=current_user)


@app.route('/logout')
def logout():
    if sessionExists():
        session["user_id"] = None
        flash("Logged out successfully", "success")
    return redirect("/")


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    redirectIfSessionNotExists()
    current_user = User.query.filter_by(id=session['user_id']).first()
    if request.method == 'POST':
        current_user.first_name = request.form['first_name']
        current_user.last_name = request.form['last_name']
        current_user.email = request.form['email']
        current_user.phone = request.form['phone']
        current_user.street_address = request.form['street_address']
        current_user.zip_code = request.form['zip_code']
        current_user.city = request.form['city']
        current_user.cryptocurrency = request.form['cryptocurrency']
        current_user.wallet = request.form['wallet']
        try:
            db.session.commit()
            flash("Profile updated successfully", "success")
        except:
            flash("Error in updating profile", "danger")
    return render_template('profile.html', cssFile="dashboard", current_user=current_user, pageTitle="Profile")


@app.route('/connect_greezy', methods=['GET', 'POST'])
def connect_greezy():
    redirectIfSessionNotExists()
    current_user = User.query.filter_by(id=session['user_id']).first()
    if request.method == 'POST':
        current_user.cb_credentials.cb_key = request.form['cb_key']
        current_user.cb_credentials.cb_password = request.form['cb_password']
        current_user.cb_credentials.cb_secret = request.form['cb_secret']
        try:
            db.session.commit()
            flash("Coinbase Credentials updated successfully", "success")
        except:
            flash("Error in updating Coinbase Credentials", "danger")
    return render_template('connect_greezy.html', cssFile="dashboard", current_user=current_user, pageTitle="Connect Greezy")


@app.route('/strategy', methods=['GET', 'POST'])
def strategy():
    redirectIfSessionNotExists()
    current_user = User.query.filter_by(id=session['user_id']).first()
    if request.method == 'POST':
        current_user.strategy.currency_id = request.form['currency_id']
        current_user.strategy.aggressiveness = request.form['aggressiveness']
        current_user.strategy.stop_loss = request.form['stop_loss']
        current_user.strategy.minimum_gains = request.form['minimum_gains']
        current_user.strategy.audacity = request.form['audacity']
        try:
            db.session.commit()
            flash("Strategy updated successfully", "success")
        except:
            flash("Error in updating Strategy", "danger")
    return render_template('strategy.html', cssFile="dashboard", current_user=current_user, pageTitle="Strategy")


@app.route('/affiliation', methods=['GET', 'POST'])
def affiliation():
    redirectIfSessionNotExists()
    current_user = User.query.filter_by(id=session['user_id']).first()
    if request.method == 'POST':
        current_user.strategy.currency_id = request.form['currency_id']
        current_user.strategy.aggressiveness = request.form['aggressiveness']
        current_user.strategy.stop_loss = request.form['stop_loss']
        current_user.strategy.minimum_gains = request.form['minimum_gains']
        current_user.strategy.audacity = request.form['audacity']
        try:
            db.session.commit()
            flash("Strategy updated successfully", "success")
        except:
            flash("Error in updating Strategy", "danger")
    return render_template('affiliation.html', cssFile="dashboard", current_user=current_user, pageTitle="Affiliation")


@app.route('/support', methods=['GET', 'POST'])
def support():
    redirectIfSessionNotExists()
    current_user = User.query.filter_by(id=session['user_id']).first()
    if request.method == 'POST':
        current_user.strategy.currency_id = request.form['currency_id']
        current_user.strategy.aggressiveness = request.form['aggressiveness']
        current_user.strategy.stop_loss = request.form['stop_loss']
        current_user.strategy.minimum_gains = request.form['minimum_gains']
        current_user.strategy.audacity = request.form['audacity']
        try:
            db.session.commit()
            flash("Strategy updated successfully", "success")
        except:
            flash("Error in updating Strategy", "danger")
    return render_template('support.html', cssFile="dashboard", current_user=current_user, pageTitle="Support")


@app.context_processor
def context_processor():
    return dict(logoURL=url_for('static', filename='images/logo.png'))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

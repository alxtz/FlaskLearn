from flask_sqlalchemy import SQLAlchemy

from flask import Flask
from flask import render_template
from flask import request, redirect, url_for

from flask_security import Security, SQLAlchemyUserDatastore
from flask_security import UserMixin, RoleMixin, login_required


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://flaskserver@localhost:5432/flaskdb'
app.config['SECRET_KEY'] = 'super-secret'
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_PASSWORD_SALT'] = 'SecretSalt'
app.debug = True # turn on server debug mode

# we want to pass our app as an argument
db = SQLAlchemy(app)

# Define models
roles_users = db.Table( 'roles_users', db.Column('user_id', db.Integer(), db.ForeignKey('user.id')), db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id          = db.Column(db.Integer(), primary_key=True)
    name        = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id           = db.Column(db.Integer, primary_key=True)
    email        = db.Column(db.String(255), unique=True)
    password     = db.Column(db.String(255))
    active       = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles        = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# the @ is a python decorater, they're wrappers around python functions
# to exec the function for particular event
# a router for index page, default is only for get
@app.route('/')
def index():
    return render_template('index.html')

# a router for user profile page
@app.route('/profile/<email>')
@login_required
# pass the argument of the router into view
def getProfile(email):
    user = User.query.filter_by(email=email).first()
    # you can redirect if you user is queried null/None
    return render_template('profile.html', user=user)

# a router spec for posting
@app.route('/post_user', methods=['POST'])
def post_user():
    newUser = User(request.form['username'], request.form['email'])
    db.session.add(newUser)
    db.session.commit()
    # when done, redirect, call url_for and pass in a view
    return redirect(url_for('index'))


# if the app.py is runned directly
# if this code was imported, the __name__ would not be __main__
if __name__ == '__main__':
    app.run()

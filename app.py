from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask import render_template
from flask import request, redirect, url_for

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://flaskserver@localhost:5432/flaskdb'
app.debug = True # turn on server debug mode

# we want to pass our app as an argument
db = SQLAlchemy(app)

class User(db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email    = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

# a router for index page, default is only for get
@app.route('/')
def index():
    userList = User.query.all()
    oneItem = User.query.filter_by(username="Alxtz").first()
    # we're never going to pass just static HTML
    # flask uses a template engine call Jinja2
    return render_template('add_user.html', userList=userList, oneItem=oneItem)

# a router spec for posting
@app.route('/post_user', methods=['POST'])
def post_user():
    newUser = User(request.form['username'], request.form['email'])
    db.session.add(newUser)
    db.session.commit()
    # when done, redirect, call url_for and pass in a view
    return redirect(url_for('index'))

# a router for user profile page
@app.route('/profile/<username>')
# pass the argument of the router into view
def getProfile(username):
    user = User.query.filter_by(username=username).first()
    # you can redirect if you user is queried null/None
    return render_template('profile.html', user=user)

# if the app.py is runned directly
# if this code was imported, the __name__ would not be __main__
if __name__ == '__main__':
    app.run()

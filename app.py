from flask import Flask, render_template, request
# from flask.ext.sqlalchemy import SQLAlchemy   # NB was this
from flask_sqlalchemy import SQLAlchemy             # now this (as of 25/3/19)
from send_email import send_email
from sqlalchemy.sql import func

app = Flask(__name__)           # use whatever is the name of this script cf 10-143
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/height_collector'
# in URI args postgres: user-name:password@server-address/database-name
# URI string would have to be populated from 'heroku config myappname' if deploying to Heroku
db = SQLAlchemy(app)


# ORM model for SQLAlchemy
# NB underscores for variable names in ORM object
class Data(db.Model):
    """ ORM model for SQLAlchemy """
    __tablename__ = "data"
    id = db.Column(db.Integer, primary_key=True)
    email_ = db.Column(db.String(120), unique=True)       # max length 120 characters
    height_ = db.Column(db.Integer)

    def __init__(self, email_, height_):
        self.email_ = email_
        self.height_ = height_





@app.route("/")
def index():
    return render_template("index.html")

# NB have to add form POST processing route to mappings - also action="{{url_for('success')}}" in markup
# must explicitly declare POST not GET
@app.route("/success", methods=['POST'])
def success():
    if request.method == 'POST':
        email = request.form['email_name']
        height = request.form['height_name']
        # print(email)
        print(request.form)
        return render_template('success.html')

if __name__ == '__main__':
    app.debug = True
    app.run()             # could have port = 5001 &c here


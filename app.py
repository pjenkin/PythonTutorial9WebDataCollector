from flask import Flask, render_template, request, send_file
# from flask.ext.sqlalchemy import SQLAlchemy   # NB was this
from flask_sqlalchemy import SQLAlchemy             # now this (as of 25/3/19)
from send_email import send_email
from sqlalchemy.sql import func
#from werkzeug import secure_filename
import werkzeug


app = Flask(__name__)           # use whatever is the name of this script cf 10-143
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/height_collector'
# in URI args postgres: user-name:password@server-address/database-name
# URI string would have to be populated from 'heroku config myappname' if deploying to Heroku
db = SQLAlchemy(app)


# NB underscore suffixes for variable names in ORM object
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

# working ok - commented-out only to facilitate 21-240 file upload/download
# NB have to add form POST processing route to mappings - also action="{{url_for('success')}}" in markup
# must explicitly declare POST not GET
# @app.route("/success", methods=['POST'])
# def success():
#     if request.method == 'POST':
#         email = request.form['email_name']      # NB variable from POST'd data - *without* underscore suffix REMmed 21-240 files
#         height = request.form['height_name']
#         # print(email)
#         print(request.form)
#         print(request.form)
#         print(db.session.query(Data).filter(Data.email_ == email))
#         print(db.session.query(Data).filter(Data.email_ == email).count())
#         if db.session.query(Data).filter(Data.email_ == email).count() == 0:
#             # query class variable - check whether email already present
#             # need to map string fields to database
#             data = Data(email, height)
#             db.session.add(data)        # pass instance of Data ORM class to this PostGreSQL session
#             db.session.commit()
#             average_height = db.session.query(func.avg(Data.height_)).scalar()       # NB underscore to get object property
#             average_height = round(average_height, 2)
#             count = db.session.query(Data.height_).count()
#             print('average height: ' + str(average_height))
#             email_feedback = send_email(email, height, average_height, count)
#             # email formerly REMmed out as security/payment issue with Gmail
#             return render_template('success.html', email_feedback_text = email_feedback)
#         return render_template('index.html',
#                                feedback_text='We seem to have received data from that email address registered already.')
#         # if fail - e.g. if not unique email, go back to start

# success route if file upload used 21-240
@app.route("/success", methods=['POST'])
def success():
    global file         # make global to be accessible in download function
    if request.method == 'POST':
        file = request.files['file_name']      # NB variable from POST'd data - *without* underscore suffix REMmed 21-240 files
        # print(email)
        file.save('uploaded_' + werkzeug.secure_filename(file.filename))        # strip slashes/unsafe characters from name
        with open('uploaded_' + werkzeug.secure_filename(file.filename), 'a') as write_file:
            write_file.write('\n- this being added later!')
        content = file.read()
        print(content)
        # return render_template('success.html', email_feedback_text='')
        return render_template('index.html', btn='download.html')

@app.route('/download')
def download():
    """ function to avoid 'missing endpoint' error """
    return send_file('uploaded_' + werkzeug.secure_filename(file.filename), attachment_filename="Download_height_file.csv", as_attachment=True)
    # pass


if __name__ == '__main__':
    app.debug = True        # useful for dev (take out in production)
    app.run()             # could have port = 5001 &c here


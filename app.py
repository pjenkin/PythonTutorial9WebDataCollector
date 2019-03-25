from flask import Flask, render_template, request

app = Flask(__name__)           # use whatever is the name of this script cf 10-143

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.debug = True
    app.run()             # could have port = 5001 &c here


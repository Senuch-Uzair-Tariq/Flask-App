from flask import Flask,render_template
from content_management import Content

TOPIC_DICT=Content()

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("main.html")

@app.route('/dashboard/')
def dashboard():
    return render_template("dashboard.html",CONTEXT=TOPIC_DICT)


if __name__ == '__main__':
    app.run(debug=True)

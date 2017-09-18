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

@app.route('/slashboard/')
def slashboard():
    try:
        return render_template("dashboard.html",CONTEXT=TOPIC_DICT)
    except Exception as e:
        return render_template("500.html",CONTEXT=e)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

if __name__ == '__main__':
    app.run(debug=True)

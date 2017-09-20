from flask import Flask,render_template,flash
from content_management import Content

TOPIC_DICT=Content()

app = Flask(__name__)

app.secret_key="Senuch Uzair Tariq"

@app.route('/')
def hello_world():
    return render_template("main.html")

@app.route('/dashboard/')
def dashboard():
    flash("Okay this is the flask message")
    return render_template("dashboard.html",CONTEXT=TOPIC_DICT)

@app.route('/slashboard/')
def slashboard():
    try:
        return render_template("dashboard.html",CONTEXT=TOPIC_DICT)
    except Exception as e:
        return render_template("500.html",CONTEXT=e)

@app.route('/login/',methods=['POST'])
def login():
    return render_template("login.html")

@app.errorhandler(404)
@app.errorhandler(405)
def page_not_found(e):
    return render_template("404.html")

if __name__ == '__main__':
    app.run(debug=True)

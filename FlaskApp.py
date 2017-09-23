from flask import Flask,render_template,flash,request,url_for,redirect
from content_management import Content
from dbconnect import connection

TOPIC_DICT=Content()

app = Flask(__name__)

app.secret_key="Senuch Uzair Tariq"

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

@app.route('/login/',methods=['GET','POST'])
def login():

    error=None;
    try:

        if request.method=='POST':
            attempted_username=request.form['username']
            attempted_password=request.form['password']

            #flash(attempted_username)
            #flash(attempted_password)

            if attempted_username=="admin" and attempted_password == "password":
                return redirect(url_for('dashboard'))
            else:
                error="Invalid! Credentials."
        return render_template('login.html',CONTEXT=error)

    except Exception as e:
        #flash(e)
        return render_template("login.html",CONEXT=error)

@app.route('/register/',methods=['GET','POST'])
def register():
    try:
        c,conn = connection()
        return "Okay"
    except Exception as e:
        return str(e)

@app.errorhandler(404)
@app.errorhandler(405)
def page_not_found(e):
    return render_template("404.html")

if __name__ == '__main__':
    app.run(debug=True)

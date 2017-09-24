from flask import Flask,render_template,flash,request,url_for,redirect,session
from content_management import Content
from wtforms import StringField,PasswordField,BooleanField,Form,validators,form
from dbconnect import connection
from passlib.hash import sha256_crypt
import gc


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
        form=RegistrationFroms(request.form)

        if request.method=='POST' and form.validate():
            username=form.username.data
            email=form.email.data
            password=sha256_crypt.encrypt(str(form.password.data))
            c,conn=connection()

            c.execute("SELECT * FROM users WHERE username='"+username+"'")

            if len(c.fetchall())>0:
                flash("This username is already taken,please choose a different one.")
                return render_template('register.html',form=form)
            else:
                c.execute("INSERT INTO users (username,password,email,tracking) VALUES (%s,%s,%s,%s)",
                          (username,password,email,"/introduction-to-python-programming/"))

                conn.commit()
                c.close()
                conn.close()
                flash("Registration Successful")
                gc.collect()

                session['logged_in']=True
                session['username']=username

                return redirect(url_for('dashboard'))
        return render_template('register.html',form=form)

    except Exception as e:
        return str(e)

class RegistrationFroms(Form):
    username=StringField("Username",[validators.Length(min=4,max=20)])
    email=StringField("Email",[validators.length(min=6,max=20)])
    password=PasswordField('Password',[validators.DataRequired(),validators.EqualTo('confirm',message="Password must match.")])
    confirm = PasswordField('Password')
    accept_tos=BooleanField("I accept the <a href='/tof/'> Terms Of Service</a>",[validators.DataRequired()])

@app.errorhandler(404)
@app.errorhandler(405)
def page_not_found(e):
    return render_template("404.html")

if __name__ == '__main__':
    app.run(debug=True)

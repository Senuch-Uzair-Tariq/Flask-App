from flask import Flask,render_template,flash,request,url_for,redirect,session
from functools import wraps
from content_management import Content
from wtforms import StringField,PasswordField,BooleanField,Form,validators,form
from dbconnect import connection
from passlib.hash import sha256_crypt
import gc


TOPIC_DICT=Content()

app = Flask(__name__)

app.secret_key="Senuch Uzair Tariq"

def login_required(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            flash('You need to login first')
            return redirect(url_for('login'))
    return wrap

@app.route('/')
def homepage():
    return render_template("main.html")

@app.route('/dashboard/')
@login_required
def dashboard():
    return render_template("dashboard.html",CONTEXT=TOPIC_DICT)

@app.route('/slashboard/')
def slashboard():
    try:
        return render_template("dashboard.html",CONTEXT=TOPIC_DICT)
    except Exception as e:
        return render_template("500.html",CONTEXT=e)

@app.route('/logout/')
@login_required
def logout():
    session.clear()
    flash('You have been logged out')
    gc.collect()
    return redirect(url_for('homepage'))

@app.route('/login/',methods=['GET','POST'])
def login():

    error=None;
    try:
        c,conn=connection()
        if request.method=='POST':
            data=c.execute("SELECT * from users WHERE username='"+request.form['username']+"'")
            data=c.fetchone()[2]


            if  not data == None and sha256_crypt.verify(request.form['password'],data):
                session['logged_in']=True
                session['username']=request.form['username']

                flash("You are logged in")

                return redirect(url_for('dashboard'))
            else:
                error="Invalid credentials, try again."

            c.close()
            conn.close()
            gc.collect()

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

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

@app.route('/dashboard/',methods=['GET','POST'])
@login_required
def dashboard():
    try:
        try:
            client_name, setting, tracking, rank = userinformation()
            if len(tracking)<10:
                tracking="/introduction-to-python-programming/"
            gc.collect()

            if client_name=="Guest":
                flash("Welcome Guest, Feel free to look around.")
                tracking=['None']
            update_user_tracking()

            completed_percentages=topic_completion_percent()

            return render_template("dashboard.html", CONTEXT=TOPIC_DICT,TRACKING=tracking,COMPLETE=completed_percentages)

        except:
            pass

    except:
        pass


@app.route('/logout/')
@login_required
def logout():
    session.clear()
    flash('You have been logged out')
    gc.collect()
    return redirect(url_for('homepage'))

@app.route('/login/',methods=['GET','POST'])
def login():

    error=None
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

def userinformation():
    try:
        client_name=(session['username'])
        guest=False
    except:
        guest=True
        client_name='Guest'
    if not guest:
        try:
            c,conn=connection()
            c.execute("SELECT * FROM users WHERE username='"+client_name+"'")
            data=c.fetchone()
            setting=data[4]
            tracking=data[5]
            rank=data[6]

        except Exception,e:
            pass
    else:
        setting=[0,0]
        tracking=[0,0]
        rank=[0,0]

    c.close()
    conn.close()
    gc.collect()

    return client_name,setting,tracking,rank

def update_user_tracking():
    try:
        completed=str(request.args['completed'])

        if completed in str(TOPIC_DICT.values()):
            client_name,setting,tracking,rank=userinformation()

            if tracking == None:
                tracking=completed
            else:
                if completed not in tracking:
                    tracking=tracking+","+completed
            c,conn = connection()
            c.execute("UPDATE users SET tracking='"+tracking+"' WHERE username='"+client_name+"'")
            conn.commit()
            c.close()
            conn.close()
            client_name, setting, tracking, rank = userinformation()
        else:
            pass
    except:
        pass

def topic_completion_percent():
    client_name, setting, tracking, rank = userinformation()
    try:
        try:
            tracking=tracking.split(',')
        except:
            pass
        if tracking==None:
            tracking=[]

        completed_percentage={}

        for each_topic in TOPIC_DICT:
            total=0
            total_complete=0

            for each in TOPIC_DICT[each_topic]:
                total+=1
                for done in tracking:
                    if done==each[1]:
                        total_complete+=1

            percent_complete = int((total_complete*100)/total)

            completed_percentage[each_topic]=percent_complete

        return completed_percentage
    except:
        for each_topic in TOPIC_DICT:
            total=0
            total_complete=0

            completed_percentage[each_topic]=0.0
        return completed_percentage


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


#CMS-Contents Begin

@app.route(TOPIC_DICT["Basics"][0][1], methods=['GET', 'POST'])
def Python_Introduction():
    update_user_tracking()
    completed_percentages = topic_completion_percent()
    return render_template("/Basics/introduction-to-python-programming.html",completed_percentages=completed_percentages, curLink = TOPIC_DICT["Basics"][0][1], curTitle=TOPIC_DICT["Basics"][0][0],  nextLink = TOPIC_DICT["Basics"][1][1], nextTitle = TOPIC_DICT["Basics"][1][0])




@app.route(TOPIC_DICT["Basics"][1][1], methods=['GET', 'POST'])
def Print_Function_and_Strings():
    update_user_tracking()
    completed_percentages = topic_completion_percent()
    return render_template("/Basics/python-tutorial-print-function-strings.html",completed_percentages=completed_percentages, curLink = TOPIC_DICT["Basics"][1][1], curTitle=TOPIC_DICT["Basics"][1][0],  nextLink = TOPIC_DICT["Basics"][2][1], nextTitle = TOPIC_DICT["Basics"][2][0])




@app.route(TOPIC_DICT["Basics"][2][1], methods=['GET', 'POST'])
def Sockets_with_Python_Intro():
    update_user_tracking()
    completed_percentages = topic_completion_percent()
    return render_template("/Basics/python-sockets.html",completed_percentages=completed_percentages, curLink = TOPIC_DICT["Basics"][2][1], curTitle=TOPIC_DICT["Basics"][2][0],  nextLink = TOPIC_DICT["Basics"][3][1], nextTitle = TOPIC_DICT["Basics"][3][0])




@app.route(TOPIC_DICT["Basics"][3][1], methods=['GET', 'POST'])
def Simple_Port_Scanner_with_Sockets():
    update_user_tracking()
    completed_percentages = topic_completion_percent()
    return render_template("/Basics/python-port-scanner-sockets.html",completed_percentages=completed_percentages, curLink = TOPIC_DICT["Basics"][3][1], curTitle=TOPIC_DICT["Basics"][3][0],  nextLink = TOPIC_DICT["Basics"][4][1], nextTitle = TOPIC_DICT["Basics"][4][0])




@app.route(TOPIC_DICT["Basics"][4][1], methods=['GET', 'POST'])
def Threaded_Port_Scanner():
    update_user_tracking()
    completed_percentages = topic_completion_percent()
    return render_template("/Basics/python-threaded-port-scanner.html",completed_percentages=completed_percentages, curLink = TOPIC_DICT["Basics"][4][1], curTitle=TOPIC_DICT["Basics"][4][0],  nextLink = TOPIC_DICT["Basics"][5][1], nextTitle = TOPIC_DICT["Basics"][5][0])




@app.route(TOPIC_DICT["Basics"][5][1], methods=['GET', 'POST'])
def Binding_and_Listening_with_Sockets():
    update_user_tracking()
    completed_percentages = topic_completion_percent()
    return render_template("/Basics/python-binding-listening-sockets.html",completed_percentages=completed_percentages, curLink = TOPIC_DICT["Basics"][5][1], curTitle=TOPIC_DICT["Basics"][5][0],  nextLink = TOPIC_DICT["Basics"][6][1], nextTitle = TOPIC_DICT["Basics"][6][0])




@app.route(TOPIC_DICT["Basics"][6][1], methods=['GET', 'POST'])
def Client_Server_System_with_Sockets():
    update_user_tracking()
    completed_percentages = topic_completion_percent()
    return render_template("/Basics/client-server-python-sockets.html",completed_percentages=completed_percentages, curLink = TOPIC_DICT["Basics"][6][1], curTitle=TOPIC_DICT["Basics"][6][0],  nextLink = TOPIC_DICT["Basics"][7][1], nextTitle = TOPIC_DICT["Basics"][7][0])




@app.route(TOPIC_DICT["Basics"][7][1], methods=['GET', 'POST'])
def Python_2to3_for_Converting_Python_2_scripts_to_Python_3():
    update_user_tracking()
    completed_percentages = topic_completion_percent()
    return render_template("/Basics/converting-python2-to-python3-2to3.html",completed_percentages=completed_percentages, curLink = TOPIC_DICT["Basics"][7][1], curTitle=TOPIC_DICT["Basics"][7][0],  nextLink = TOPIC_DICT["Basics"][8][1], nextTitle = TOPIC_DICT["Basics"][8][0])




#CMS-Contents End

if __name__ == '__main__':
    app.run(debug=True)

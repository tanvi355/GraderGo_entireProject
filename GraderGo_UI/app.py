from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from flask import *
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_info.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///essays.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "abc"
db=SQLAlchemy(app)

class user_info(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    username=db.Column(db.String(length=30),nullable=False)
    email=db.Column(db.String(length=30),nullable=False,unique=True)
    password=db.Column(db.String(length=30),nullable=False)

class essays(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    essay_name = db.Column(db.String(length=30), nullable=False)
    email=db.Column(db.String(length=30),nullable=False)
    Score=db.Column(db.Integer(),nullable=False)


global essay


global score




@app.route("/")
def hello_world():
    return render_template('index.html',msg=None,error=None)

@app.route("/login_page",methods=['GET','POST'])
def login_page():


    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')

        users = user_info.query.all()
        for user in users:
            if user.email==email:
                if user.password==password:
                    session['username']=user.username
                    session['email']=email
                    return render_template('login_page.html',essay=None,score=None,username=user.username, save_msg=None)
                else:
                    return render_template('index.html',msg=None,error='Incorrect Password ')

        else:
            return render_template('index.html', msg=None, error='Incorrect Email-id')

    else:
        return 'Login from the form'



@app.route("/create_user",methods=['GET','POST'])
def create_user():
    global email
    if request.method=='POST':
        username=request.form.get('username')
        email=request.form.get('email')
        password=request.form.get('pass')
        confirm_pass=request.form.get('cpass')

        users = user_info.query.all()
        for user in users:
            if user.email==email:
                return render_template('index.html',msg=None,error='Email already exists! try logging in')


        if(password !=confirm_pass):
            return render_template('index.html',msg=None,error='Password confirmation failed')

        else:
            new_user = user_info(username=username,email=email,password=password)
            db.session.add(new_user)
            db.session.commit()
            return render_template('index.html',msg='User Created Successfully! Login to Continue',error=None)





@app.route('/grader',methods=['GET','POST'])
def grader():

    global essay
    global score
    print(session['username'])
    if request.method=='POST':
        essay=request.form.get('essay')
        data={}
        data['essay']=essay
        score = requests.post('http://127.0.0.1:51/predict', data=data)#url of api
        final = (score.json()['pred_score'])
        print(final)



    else:
        score=None
    return render_template('login_page.html',essay=essay,score=final,username=session['username'], save_msg=None)


@app.route('/logout', methods=['GET','POST'])
def logout():
    global essay

    global score

    essay=score=None
    session.pop('username')
    session.pop('email')
    return render_template('logout.html')


@app.route('/save',methods=['GET','POST'])
def save():
    global essay
    global score
    global username


    if request.method=='POST':
        essay=request.form.get('essay')
        score=essay
        essay_name=request.form.get('essayapp_name')
        print(essay_name)
        if (essay_name == ""):
            # print("heeeeloo")

            essay_name = 'essay'
        ess = essays(essay_name=essay_name, email=session['email'], Score=score)
        db.session.add(ess)
        db.session.commit()
        print("here")
        #return 'Saved essay!'
        save_msg = "Score saved"
        return render_template('login_page.html',essay=None,score=None,username=session['username'], save_msg=save_msg)

if  __name__=='__main__':
    db.create_all()
    port=5000
    app.run(debug=True, port=port)

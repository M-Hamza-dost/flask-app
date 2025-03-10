from flask import Flask,render_template,request,url_for,redirect,session
from flask_mysqldb import MySQL
import MySQLdb.cursors
from datetime import *
import requests
url="https://jsonplaceholder.typicode.com/users"


today=datetime.now().strftime('%d-%m-%y  %I:%M')

app=Flask(__name__)
app.config["MYSQL_HOST"]='172.31.94.201'
app.config["MYSQL_PORT"] = 3300
app.config["MYSQL_USER"]='hamzadost'
app.config["MYSQL_PASSWORD"]='mysqlHamza'
app.config["MYSQL_DB"]='mydata'
app.secret_key="123Qwe"
mysql=MySQL(app)

@app.route("/login", methods= ['POST','GET'])
def login():
    msg=''
    if request.method=="POST":
        username=request.form['username']
        password=request.form['password']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select * from users where username= %s and password= %s',(username,password))
        account = cursor.fetchone()
        if account:
            session['loggedin']=True
            session['id']=account['id']
            session['username']=account['username']
            session['password']=account['password']
            return render_template("home.html", username=session['username'])
        else:
            msg="Invalid Username or Password"
    return render_template('login.html',msg=msg)


@app.route("/register")
def register_page():
    return render_template('register.html')

@app.route("/register_method",methods=['POST','GET'])
def register_method():
    msg=''
    if request.method=='POST':
        username=request.form['username']
        email=request.form['email']
        password=request.form["password"]
        cursor=mysql.connection.cursor()
        cursor.execute("select * from users where username=%s",(username,))
        user=cursor.fetchone()  
        if user:
            msg="user alredy exist"
            return render_template('register.html',msg=msg)
    
        else:
            sql="INSERT INTO users (username,email,password) VALUES (%s,%s,%s)"
            val=(username,email,password)
            cursor.execute(sql,val)
            mysql.connection.commit()
            cursor.close()
        msg="User Registered, Please login"
        return render_template('login.html', msg=msg)

@app.route("/")
def home():
    if 'loggedin' in session:
        return render_template('home.html',username=session['username'])
    return redirect(url_for('login'))

@app.route("/AddRecord")
def add_rec():
    if 'loggedin' in session:
        return render_template('addrec.html',username=session['username'])
    return redirect(url_for('login'))

@app.route("/trainer_create", methods=['POST','GET'])
def trainer_create():
    if request.method=="POST":
        fname=request.form['fname']
        lname=request.form['lname']
        email=request.form['email']
        region=request.form['region']
        c_name=request.form['c_name']
        cdate=today
        sql = "INSERT INTO trainer (f_name,lname,email,region,course,date_and_time) VALUES (%s,%s,%s,%s,%s,%s)"
        val = (fname,lname,email,region,c_name,cdate)

        cur=mysql.connection.cursor()
        cur.execute(sql,val)
        mysql.connection.commit()
        cur.close()
        return render_template("addrec.html")

@app.route("/ShowRecords", methods=['GET','POST'])
def show_rec():
    if 'loggedin' in session:
        data = []
        if request.method=="POST":
            cursor=mysql.connection.cursor()
            cource=request.form['filter']
            if cource=="'all'":
                sql="select * from trainer"
            else:
                sql="select * from trainer where course=" + cource
            cursor.execute(sql)
            data=cursor.fetchall()
        return render_template('showrec.html',username=session['username'],row=data)
    return redirect(url_for('login'))


response=requests.get(url)
data=response.json()
client=[]
@app.route("/Clients")
def clients():
    if 'loggedin' in session:
        for i in range (len(data)):
           cl=(data[i]['name'], data[i]['company']['name'])
           client.append(cl)
        return render_template('company.html',username=session['username'],row=client)
    return redirect(url_for('login'))

@app.route("/logout")
def logout():
    session.pop('loggedin',None)
    session.pop('id',None)
    session.pop('username',None)
    session.pop('password',None)
    return redirect(url_for('login'))

if __name__=="__main__":
    app.run(debug=True,host="0.0.0.0")
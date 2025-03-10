from flask import Flask,render_template,request,url_for,session,redirect
import MySQLdb.cursors
from flask_mysqldb import MySQL

app=Flask(__name__)

app.config["MYSQL_HOST"]='172.31.94.201'
app.config["MYSQL_USER"]='hamzadost'
app.config["MYSQL_PASSWORD"]='mysqlHamza'
app.config["MYSQL_DB"]='mydata'
mysql=MySQL(app)
app.secret_key="qwert1234"


@app.route("/")
def login_page():
   return render_template('login.html')


@app.route("/register")
def register_page():
   return render_template('register.html')


@app.route("/login",methods=["POST","GET"])
def login():
    msg= ''
    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('select * from users where username = %s and password = %s', (username,password))
        account=cur.fetchone()
        if account:
            session['loggedin']=True
            session['id']=account['id']
            session['username']=account['username']
            session['password']=account['password']
            return render_template("home.html",username=session['username'])
        else:
            msg="Incorrect username or password"
    return render_template('login.html',msg=msg)
    print(msg)


@app.route("/register_method",methods=["POST","GET"])
def register_method():
    msg =''
    if request.method=="POST":
        username=request.form['username']
        email=request.form['email']
        password=request.form['password']
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('select * from users where email = %s',(email,))
        account=cur.fetchone()
        if account:
            msg = "Email Already Exists"
            return render_template('register.html',msg=msg)
        else:
            cur.execute('INSERT INTO users(username,email,password) VALUES(%s,%s,%s)',(username,email,password))
            mysql.connection.commit()
            cur.close()
    return render_template('login.html')


@app.route("/logout")
def logout():
    session.pop('loggedin',None)
    session.pop('id',None)
    session.pop('username',None)
    session.pop('password',None)
    return redirect(url_for('login_page'))

@app.route("/home")
def home():
    if 'loggedin' in session:
        return render_template("home.html",username=session['username'])
    return redirect(url_for('login_page'))


@app.route("/addRecord")
def add_rec():
    if 'loggedin' in session:
        return render_template("addrec.html",username=session['username'])
    return redirect(url_for('login_page'))


@app.route("/showRecord")
def show_rec():
    if 'loggedin' in session:
        return render_template("showrec.html",username=session['username'])
    return redirect(url_for('login_page'))
    


if __name__=="__main__":
 app.run(debug=True,host='0.0.0.0')
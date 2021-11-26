# Store this code in 'app.py' file

from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

app.secret_key = 'your secret key'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin123'
app.config['MYSQL_DB'] = 'covidlogin'

mysql = MySQL(app)

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            return render_template('register.html', msg=msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg=msg)


@app.route('/vaccine', methods=['GET', 'POST'])
def vaccine():
    msg = ''
    if request.method == 'POST' and 'uniqueId' in request.form:
        uniqueId = request.form['uniqueId']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE uniqueId = % s', (uniqueId,))
        account = cursor.fetchone()
        if account:
            #session['loggedin'] = True
            session['uniqueid'] = account['uniqueid']
            #session['username'] = account['username']
            msg = 'UniqueId is validated'
            return render_template('index.html', msg=msg)
        else:
            msg = 'Incorrect UniqueId'
    return render_template('vaccine.html', msg=msg)

@app.route('/testresult', methods=['GET', 'POST'])
def testresults():
    msg = ''
    if request.method == 'POST' and 'uniqueId' in request.form:
        uniqueId = request.form['uniqueId']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE uniqueId = % s', (uniqueId,))
        account = cursor.fetchone()
        if account:
            #session['loggedin'] = True
            session['uniqueid'] = account['uniqueid']
            #session['username'] = account['username']
            msg = 'UniqueId is validated'
            return render_template('index.html', msg=msg)
        else:
            msg = 'Incorrect UniqueId'
    return render_template('testresults.html', msg=msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'name' in request.form and 'email' in request.form and ('testresults' or 'vaccinedetails') in request.form:
        name = request.form['name']
        email = request.form['email']
        test_result = request.form['testresults']
        vaccinedetails = request.form['vaccinedetails']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE name = % s', (name,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (name, email, test_result, vaccinedetails,))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg=msg)

if __name__ == '__main__':
   app.run()

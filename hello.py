from flask import Flask, redirect, url_for, render_template, request, session
import os
import psycopg2
from os.path import exists
from os import makedirs
from config import config

import numpy as np

from flask import Flask, session
from flask_session import Session


SESSION_TYPE = 'memcache'

app = Flask(__name__)
sess = Session()

nextId = 0

def verifySessionId():
    global nextId

    if not 'username' in session:
        session['username'] = nextId
        nextId += 1
        sessionId = session['username']
        print ("set username[" + str(session['username']) + "]")
    else:
        print ("using already set userid[" + str(session['username']) + "]")
    sessionId = session.get('username', None)
    return sessionId

import datetime
date_time = datetime.datetime.now()



params = config()
conn = psycopg2.connect(**params)
cur = conn.cursor()


# Initialize the Flask application
app = Flask(__name__)
app.secret_key = "super secret key"

SESSION_TYPE = 'memcache'

@app.route('/list')
def list():
    suname= []
    suname[0] = session.username
    sql = """ select * from qregswimmer where email = %s """
    cur.execute(sql, (suname[0]))
    rows = cur.fetchall()
    return render_template("list.html", rows=rows)

@app.route('/')
def index():
    try:
        userId = verifySessionId()
        session_userId =  str(userId)
        cur = conn.cursor()
        sql = " select username, passwordsalt from logins where username = %s "
        cur.execute(sql, (session_userId))
        rows = cur.fetchall()
        return render_template("list.html")

    except:

        msg = "Failed : error in query operation"
        return render_template("result.html", msg=msg)

    finally:
        return render_template("list.html", msg=rows)


@app.route('/login', methods=['POST', 'GET'])
def login_page():
    cur = conn.cursor()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur.execute("select username, passwordsalt from logins where username = %s and passwordsalt = %s;", (username, password))
        rows = cur.fetchall()
        if cur.rowcount > 0:
            for rows in rows:
                if (request.form['username'] == rows[0] and request.form['password'] == rows[1]) :
                    session['username'] = rows[0]
                    return redirect(url_for('list'))
                else:
                    msg = "Login credentials are not correct"
                    return render_template('login_new.html', msg=msg)

        else:
            msg = "Login credentials are not correct"
            return render_template('login_new.html', msg=msg)

    else:
        msg = "Please login"
        return render_template('login_new.html', msg=msg)

@app.route('/success')
def success():
    return 'logged in successfully'

@app.route('/home_page')
def home_page():
    return render_template('home.html')

@app.route('/fixture_page')
def fixture_page():
    return render_template('fixtures.html')

@app.route('/signup_page')
def signup_page():
   return render_template('signup.html')

@app.route('/performance_page')
def performance_page():
    # data to plot
    n_groups = 4
    means_frank = (90, 55, 40, 65)
    means_guido = (85, 62, 54, 20)


    return render_template('performance.html')


@app.route('/addrec', methods=['POST', 'GET'])
def addrec():

    if request.method == 'POST':
        try:

            fname = request.form['fname']
            lname = request.form['lname']
            email = request.form['email']
            today = date_time.date()  # Gives the date

            cur = conn.cursor()
            cur.execute("INSERT INTO qregswimmer(email, firstname, lastname, regdate) VALUES (%s, %s, %s, %s)" , (email, fname, lname, today))
            conn.commit()
            msg = "Success : Record successfully added"
            return render_template('home.html', msg=msg)

        except:
           conn.rollback()
           msg = "Failed : error in insert operation"

        finally:
           return render_template("result.html", msg=msg)


@app.route('/update_swimmer', methods=['POST', 'GET'])
def update_swimmer():
    cur = conn.cursor()
    fname = request.form['firstname']
    userid = request.form['userid']
    sql = """ UPDATE qregswimmer
                SET firstname = '%s'
                WHERE userid = '%s'"""

    updated_rows = 0
    try:
        cur.execute(sql, tuple(fname, userid))
        # get the number of updated rows
        updated_rows = cur.rowcount
        # Commit the changes to the database
        conn.commit()
        # Close communication with the PostgreSQL database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return updated_rows



def progress():
    # data to plot
    n_groups = 4
    means_frank = (90, 55, 40, 65)
    means_guido = (85, 62, 54, 20)





@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
    conn.close()
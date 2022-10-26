#!/usr/bin/env python3

import os
from flask import Flask, render_template, request, session, redirect, url_for, make_response
from dotenv import dotenv_values

import pymongo
import datetime
from bson.objectid import ObjectId
import sys

# instantiate the app
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# load credentials and configuration options from .env file
# if you do not yet have a file named .env, make one based on the template in env.example
config = dotenv_values(".env")

# turn on debugging if in development mode
if config['FLASK_ENV'] == 'development':
    # turn on debugging, if in development
    app.debug = True # debug mnode


# connect to the database
cxn = pymongo.MongoClient(config['MONGO_URI'], serverSelectionTimeoutMS=5000)
try:
    # verify the connection works by pinging the database
    cxn.admin.command('ping') # The ping command is cheap and does not require auth.
    db = cxn[config['MONGO_DBNAME']] # store a reference to the database
    print(' *', 'Connected to MongoDB!') # if we get here, the connection worked!
except Exception as e:
    # the ping command failed, so the connection is not available.
    print(' *', "Failed to connect to MongoDB at", config['MONGO_URI'])
    print('Database connection error:', e) # debug

@app.route('/')
def home():
    """
    Route for the home page
    """ 
    return render_template('home.html') # render the home template 


@app.route('/home.html', methods=['POST'])
def home_post():
    decision = request.form['home_choice']

    if decision == 'login':
        return redirect(url_for('login'))
    elif decision == 'signup':
        return redirect(url_for('signup'))


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/login', methods=['POST'])
def process_login():
    us = request.form['us']
    psw = request.form['psw']

    existing = db.users.find_one({ "username": us, "password": psw})

    if (existing != None):
        session['username'] = us
        return redirect(url_for('show_Boptions'))

    else:
        error = 1
        return render_template("login.html", error = error)


@app.route('/login/<error>')
def show_issue(error):
    error = error
    return redirect (url_for('login'))


@app.route('/signup')
def signup():
    return render_template("signup.html")


@app.route('/signup', methods=['POST'])
def process_signup():
    fn = request.form['firstName']
    ln = request.form['lastName']
    email = request.form['email']

    us = request.form['us']
    psw = request.form['psw']
    psw2 = request.form['psw-repeat']

    if (psw != psw2):
        error = 1
        return render_template("signup.html", error = error)
    
    else:
        existing = db.users.find_one({ "username": us})
        if (existing != None):
            error = 2
            return render_template("signup.html", error = error)
        else:
            check_email = db.users.find_one({ "email": email})
            if (check_email != None):
                error = 3
                return render_template("signup.html", error = error)
            else:
                db.users.insert_one({ "username": us, "password": psw, "first": fn, "last": ln, "email": email})
                return redirect(url_for('login'))


@app.route('/buildings')
def show_Boptions():
    return render_template('buildings.html')


@app.route('/buildings', methods=['POST'])
def get_choice():
    bName = request.form['buildings']

    if (bName == "kimmel"):
        b = "Kimmel Center for University Life"
    elif (bName == "bobst"):
        b = "Elmer Holmes Bobst Library"
    elif (bName == "slc-manhattan"):
        b = "Student Link Center (Manhattan)"
    elif (bName == "silver"):
        b = "Silver Center for Arts and Science"
    elif (bName == "meyer"):
        b = "Meyer Hall"
    elif (bName == "tandon"):
        b = "Tandon School of Engineering"
    else:
        b = "Student Link Center - Brooklyn"

    session['bName'] = b

    return redirect(url_for('show_Foptions'))


@app.route('/floors')
def show_Foptions():
    return render_template("floors.html")


@app.route('/floors', methods=['POST'])
def get_choice2():
    fNum = request.form['floorNum']

    if (fNum == "floor-1"):
        f = 1
    elif (fNum == "floor-2"):
        f = 2
    elif (fNum == "floor-3"):
        f = 3
    elif (fNum == "floor-4"):
        f = 4
    elif (fNum == "floor-5"):
        f = 5
    elif (fNum == "floor-6"):
        f = 6
    else:
        f = 7

    session['fNum'] = f

    return redirect(url_for('show_rest'))


@app.route('/restroom')
def show_rest():
    bName = session.get('bName')
    fNum = session.get('fNum')
    comments = db.comments.find({ "building": bName, "floor": fNum })
    current_restroom = db.restrooms.find_one({ "building": bName,  "floor": fNum})
    return render_template("restroom.html", b = bName, f = fNum, coms = comments, cr = current_restroom )


@app.route('/addRestroom')
def add_new():
    return render_template("addRestroom.html")


@app.route('/addRestroom', methods=['POST'])
def analyze_new():
    loc_b = request.form['loc_b']
    loc_f = request.form['loc_f']
    description = request.form['description']
    available = request.form['available']

    if (loc_b == "kimmel"):
        loc_b = "Kimmel Center for University Life"
    elif (loc_b == "bobst"):
        loc_b = "Elmer Holmes Bobst Library"
    elif (loc_b == "slc-manhattan"):
        loc_b = "Student Link Center (Manhattan)"
    elif (loc_b == "silver"):
        loc_b = "Silver Center for Arts and Science"
    elif (loc_b == "meyer"):
        loc_b = "Meyer Hall"
    elif (loc_b == "tandon"):
        loc_b = "Tandon School of Engineering"
    else:
        loc_b = "Student Link Center - Brooklyn"

    if (loc_f == "floor-1"):
        loc_f = 1
    elif (loc_f == "floor-2"):
        loc_f = 2
    elif (loc_f == "floor-3"):
        loc_f = 3
    elif (loc_f == "floor-4"):
        loc_f = 4
    elif (loc_f == "floor-5"):
        loc_f = 5
    elif (loc_f == "floor-6"):
        loc_f = 6
    else:
        loc_f = 7

    doc = {
        "building": loc_b,
        "floor": loc_f, 
        "desc": description,
        "available": available
    }

    db.restrooms.insert_one(doc)
    return render_template("addRestroom.html", success = 1)


@app.route('/addRestroom/<success>')
def show_success(success):
    success = success
    return redirect (url_for('add_new'))


@app.route('/addComment')
def add_comment():
    return render_template("addComment.html")


@app.route('/addComment', methods=['POST'])
def analyze_comment():
    bName = session.get('bName')
    fNum = session.get('fNum')
    us = session.get('username')
    comText = request.form['comment']

    doc = {
        "username": us,
        "building": bName,
        "floor": fNum,
        "text": comText
    }

    db.comments.insert_one(doc)
    return redirect (url_for('show_rest'))


@app.route('/profile')
def get_profile():
    us = session.get('username')
    user = db.users.find_one({ "username": us})
    user_coms = db.comments.find({ "username": us})
    return render_template("profile.html", user = user, coms = user_coms)

@app.route('/delete/<comment_id>')
def delete(comment_id):
    """
    Route for GET requests to the delete page.
    Deletes the specified record from the database, and then redirects the browser to the home page.
    """
    db.comments.delete_one({"_id": ObjectId(comment_id)})
    return redirect(url_for('get_profile')) # tell the web browser to make a request for the / route (the home function)


# route to handle any errors
@app.errorhandler(Exception)
def handle_error(e): 
    """
    Output any errors - good for debugging.
    """
    return render_template('error.html', error=e) # render the edit template


# run the app
if __name__ == "__main__":
    #import logging
    #logging.basicConfig(filename='/home/ak8257/error.log',level=logging.DEBUG)
    app.run(debug = True)


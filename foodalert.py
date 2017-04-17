import os
import sys
import pymongo
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask_cas import CAS
from flask_cas import login_required

# sanitize the input string
def sanitize(pref):
    if len(pref) > 40:
        return pref[:40]
    else: 
        return pref

# set up CAS
app = Flask(__name__)
CAS(app)

app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'foodalert.db'),
                       SECRET_KEY='development key',
                       USERNAME='admin',
                       PASSWORD='default'))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

# set CAS settings
app.config['CAS_SERVER'] = 'https://fed.princeton.edu/cas'
app.config['CAS_AFTER_LOGIN'] = 'show_entries'

uri = 'mongodb://foodpref:hungry67@ds153730.mlab.com:53730/heroku_b3r535zh'

client = None
db = None
users = None
try:
    client = pymongo.MongoClient(uri)
    db = client.get_default_database()
    users = db.get_collection("Users")
except Exception as e:
    print(str(e))

# Main display page: show the entries the user currently has in the system
@app.route('/')
@login_required
def show_entries():
    entries = []
    usr = None
    # retrieve user's food preferences. show empty table if anything goes wrong
    if users != None:
        try:
            usr = users.find_one({'netid':session['CAS_USERNAME']})
        except Exception:
            pass
        if (usr != None): 
            try:
                entries = usr['foodpref']
                entries.reverse()
            except Exception:
                pass
    return render_template('show_entries.html', entries=entries)

# Add a new entry to the database
@app.route('/add', methods=['POST'])
def add_entry():
    new_entry = "Something went wrong"
    try:
        new_entry = request.form['title']
    except Exception as e:
        print(str(e))
        return redirect(url_for('show_entries'))
    new_entry = sanitize(new_entry)
    if (len(new_entry) > 0):
        try:
            users.update_one({'netid':session['CAS_USERNAME']}, {'$push' : {'foodpref':new_entry}}, upsert=True)
        except Exception as e:
            print(str(e))
    return redirect(url_for('show_entries'))

# Remove and entry from the database
# To be connected with a "X" button on the user interface next to each food preference
def rem_entry():
    entry = request.form['title']
    try:
        users.update_one({'netid':session['CAS_USERNAME']}, {'$pull' : {'foodpref':entry}})
    except Exception as e:
        print(str(e))
    return redirect(url_for('show_entries'))

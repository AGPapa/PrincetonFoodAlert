import os
import sys
import pymongo
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask_cas import CAS
from flask_cas import login_required
#import ldap
import datetime

# sanitize the input string
def sanitize(pref):
    val = pref.replace("{", "?")
    val = val.replace("}", "?")
    val = val.replace(":", "?")
    if len(val) > 40:
        return val[:40]
    else: 
        return val

def is_valid(pref):
    if (len(pref) <= 0):
        return False
    if (len(pref) >= 50):
        return False
    #if (not pref.isalpha()):
    #    return False
    return True

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
topten = None
netids = None
l = None
try:
    client = pymongo.MongoClient(uri)
    db = client.get_default_database()
    users = db.get_collection("Users")
    topten = db.get_collection("Top_Ten")
    netids = db.get_collection("NetIDs").find()[0]
except Exception as e:
    print(str(e))

netid = "student"
name = "Student"

# Main display page: show the entries the user currently has in the system
@app.route('/')
@login_required
def show_entries():
    global netid
    global name
    print("In show entries")
    entries = []
    usr = None
    try:
        netid = session['CAS_USERNAME']
    except:
        pass
    if netids != None:
        if netid in netids:
            try: 
                name = netids[netid]
            except:
                name = netid
    # retrieve user's food preferences. show empty table if anything goes wrong
    if users != None:
        try:
            usr = users.find_one({'netid':netid})
        except Exception as e:
            print(str(e))
        if (usr != None): 
            try:
                entries = usr['foodpref']
                entries.reverse()
            except Exception:
                pass
    return render_template('show_entries.html', entries=entries, name=name)

# top ten foods
@app.route('/topten')
@login_required
def show_topten():
    print("In topten")
    entries = []
    usr = None
    full_date = datetime.datetime.utcnow()
    date = full_date.strftime("%Y-%m-%d")
    try:
        netid = session['CAS_USERNAME']
    except:
        pass
    if netids != None:
        if netid in netids:
            try: 
                name = netids[netid]
            except:
                name = netid
    # retrieve top ten foods. show empty table if anything goes wrong
    if topten != None:
        try:
            today = topten.find_one({'date':date})
        except Exception:
            print("No topten entry found for today's date")
        if (today != None): 
            try:
                entries = today['topten']
            except Exception:
                print("No topten list found in today's entry")
    return render_template('topten.html', entries=entries, name=name)

    # top ten foods
@app.route('/about')
@login_required
def about():
    print("In about")
    try:
        netid = session['CAS_USERNAME']
    except:
        pass
    if netids != None:
        if netid in netids:
            try: 
                name = netids[netid]
            except:
                name = netid
    return render_template('AboutUs.html', name=name)

# Add a new entry to the database
@app.route('/add', methods=['POST'])
def add_entry():
    try:
        netid = session['CAS_USERNAME']
    except:
        pass
    if netids != None:
        if netid in netids:
            try: 
                name = netids[netid]
            except:
                name = netid
    new_entry = "Something went wrong"
    try:
        new_entry = request.form['title']
    except Exception as e:
        print(str(e))
        return redirect(url_for('show_entries'))
    new_entry = sanitize(new_entry)
    if (is_valid(str(new_entry))):
        try:
            usr = users.find_one({'netid': netid})
            if (usr != None):
                if ("foodpref" in usr):
                    if (new_entry in usr["foodpref"]):
                        flash("Entry already exists.", "danger")
                        return redirect(url_for('show_entries'))
            users.update_one({'netid': netid}, {'$push' : {'foodpref':new_entry}}, upsert=True)
            flash("New entry added!", "success")
        except Exception as e:
            print(str(e))
    else:
        flash("Invalid string.", "danger")
    return redirect(url_for('show_entries'))

# Remove an entry from the database
@app.route('/rem_entry', methods=['POST'])
def rem_entry():
    print("in remove entry")
    try:
        netid = session['CAS_USERNAME']
    except:
        pass
    entry = request.form['item']
    print(entry)
    try:
        users.update_one({'netid':netid}, {'$pull' : {'foodpref':entry}})
        flash("Entry Removed.", "info")
        print("Item Removed")
    except Exception as e:
        print(str(e))
    return redirect(url_for('show_entries'))

@app.route('/delete')
def delete_account():
    print("in delete account")
    try:
        netid = session['CAS_USERNAME']
    except:
        pass
    try:
        users.delete_one({'netid':netid})
        print("User Deleted")
    except Exception as e:
        print(str(e))
    return redirect(url_for('cas.logout'))

@app.route('/apply_pref', methods=['GET', 'POST'])
def apply_pref():
    print("in apply preferences")
    try:
        netid = session['CAS_USERNAME']
    except:
        pass
    if (request.method == 'POST'):
        if (request.form.get("day_before")):
            if (request.form.get("week_before")):
                try:
                    users.update_one({'netid':netid}, {'$set' : {'accountpref':'dw'}}, upsert=True)
                except Exception as e:
                    print(str(e))
            else:
                try:
                    users.update_one({'netid':netid}, {'$set' : {'accountpref':'d'}}, upsert=True)
                except Exception as e:
                    print(str(e))
        else:
            if (request.form.get("week_before")):
                try:
                    users.update_one({'netid':netid}, {'$set' : {'accountpref':'w'}}, upsert=True)
                except Exception as e:
                    print(str(e))
            else:
                try:
                    users.update_one({'netid':netid}, {'$set' : {'accountpref':''}}, upsert=True)
                except Exception as e:
                    print(str(e))
        dhall_preferences = ""
        if (request.form.get("butler_wilson")):
            dhall_preferences += "b"
        if (request.form.get("forbes")):
            dhall_preferences += "f"
        if (request.form.get("rocky_mathey")):
            dhall_preferences += "r"
        if (request.form.get("whitman")):
            dhall_preferences += "w"
        if (request.form.get("cjl")):
            dhall_preferences += "c"
        if (request.form.get("grad")):
            dhall_preferences += "g"
        try:
            users.update_one({'netid':netid}, {'$set' : {'dhallpref':dhall_preferences}}, upsert=True)
        except Exception as e:
            print(str(e))
    return redirect(url_for('show_entries'))

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    print("in settings")
    try:
        netid = session['CAS_USERNAME']
    except:
        pass
    if netids != None:
        if netid in netids:
            try: 
                name = netids[netid]
            except:
                name = netid
    daily = True
    weekly = True
    butler_wilson = True
    forbes = True
    rocky_mathey = True
    whitman = True
    cjl = True
    grad = True
    usr = None
    try:
        usr = users.find_one({'netid':netid})
    except Exception as e:
        print(str(e))
    if (usr != None):
        if "accountpref" in usr:
            try:
                daily = usr['accountpref'].startswith("d")
                weekly = usr['accountpref'].endswith("w")
            except Exception as e:
                    print(str(e))
        if "dhallpref" in usr:
            try:
                print(usr['dhallpref'])
                butler_wilson = ("b" in usr['dhallpref'])
                rocky_mathey = ("r" in usr['dhallpref'])
                forbes = ("f" in usr['dhallpref'])
                whitman = ("w" in usr['dhallpref'])
                cjl = ("c" in usr['dhallpref'])
                grad = ("g" in usr['dhallpref'])
            except Exception as e:
                    print(str(e))
    return render_template('settings.html', daily=daily, weekly=weekly, butler_wilson=butler_wilson, 
        rocky_mathey=rocky_mathey, forbes=forbes, whitman=whitman, cjl=cjl, grad=grad, name=name)



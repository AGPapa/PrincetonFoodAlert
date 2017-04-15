import os
import sys
import pymongo
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask_cas import CAS
from flask_cas import login_required

app = Flask(__name__)
CAS(app)

app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'foodalert.db'),
                       SECRET_KEY='development key',
                       USERNAME='admin',
                       PASSWORD='default'))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

uri = 'mongodb://foodpref:hungry67@ds153730.mlab.com:53730/heroku_b3r535zh'
client = pymongo.MongoClient(uri)
# hardcode db name
db = client.get_default_database()
users = db.get_collection("Users")

app.config['CAS_SERVER'] = 'https://fed.princeton.edu/cas'
app.config['CAS_AFTER_LOGIN'] = 'show_entries'

# def connect_db():
#     rv = sqlite3.connect(app.config['DATABASE'])
#     rv.row_factory = sqlite3.Row
#     return rv

# def get_db():
#     if not hasattr(g, 'sqlite_db'):
#         g.sqlite_db = connect_db()
#     return g.sqlite_db

# @app.teardown_appcontext
# def close_db(error):
#     if hasattr(g, 'sqlite_db'):
#         g.sqlite_db.close()

# def init_db():
#     db = get_db()
#     with app.open_resource('schema.sql', mode='r') as f:
#         db.cursor().executescript(f.read())
#     db.commit()

# @app.cli.command('initdb')
# def initdb_command():
#     init_db()
#     print('Initialized the database.')

@app.route('/')
@login_required
def show_entries():
    # db = get_db()
    # cur = db.execute('select title from entries order by id desc')
    # entries = cur.fetchall()
    # return render_template('show_entries.html', entries=entries)
    entries = []
    try:
        usr = users.find_one({'netid':session['CAS_USERNAME']})
    except Exception, e:
        print(str(e))
        return render_template('show_entries.html', entries=[])
    entries = usr['foodpref']
    entries.reverse()
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    # db = get_db()
    # new_entry = request.form['title'] + " : " + session['CAS_USERNAME']
    # db.execute('insert into entries (title) values (?)',
    #            [new_entry])
    # db.commit()
    # flash('Your food preference has been recorded')
    # print (session[app.config['CAS_USERNAME_SESSION_KEY']])
    # return redirect(url_for('show_entries'))
    new_entry = request.form['title']
    try:
        users.update_one({'netid':session['CAS_USERNAME']}, {'$push' : {'foodpref':new_entry}}, upsert=True)
    except Exception, e:
        print(str(e))
    return redirect(url_for('show_entries'))

#@app.route('/login', methods=['GET', 'POST'])
#def login():
    # error = None
    # netid = C.Authenticate()
    # session['logged_in'] = True
    # print("BLABLABLA")
    # if request.method == 'POST':
    #  if request.form['username'] != app.config['USERNAME']:
    #      error = 'Invalid username'
    #  elif request.form['password'] != app.config['PASSWORD']:
    #      error = 'Invalid password'
    #  else:
    #      session['logged_in'] = True
    #      flash('You were logged in')
    #      return redirect(url_for('show_entries'))
    # return render_template('login.html', error=error)
#    session['logged_in'] = True
#    return redirect(url_for('show_entries'))

# @app.route('/logout')
# def logout():
#      session.pop('logged_in', None)
#      flash('You were logged out')
#      return redirect(url_for('show_entries'))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
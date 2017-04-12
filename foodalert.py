import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'foodalert.db'),
                       SECRET_KEY='development key',
                       USERNAME='admin',
                       PASSWORD='default'))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    init_db()
    print('Initialized the database.')

@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select title from entries order by id desc')
    entries = cur.fetchall()
    return render_template('index.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    db = get_db()
    db.execute('insert into entries (title) values (?)',
               [request.form['title']])
    db.commit()
    flash('Your food preference has been recorded')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
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
    session['logged_in'] = True
    return redirect(url_for('show_entries'))

@app.route('/logout')
def logout():
     session.pop('logged_in', None)
     flash('You were logged out')
     return redirect(url_for('show_entries'))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

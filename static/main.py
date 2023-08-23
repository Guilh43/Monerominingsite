from flask import Flask, render_template, request, redirect, url_for, session, g
import sqlite3
import time

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Não é uma boa prática; defina uma chave secreta mais segura
DATABASE = 'database.db'


def get_db():
  db = getattr(g, '_database', None)
  if db is None:
    db = g._database = sqlite3.connect(DATABASE)
    db.execute(
      'CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)')
    db.commit()
  return db


@app.teardown_appcontext
def close_connection(exception):
  db = getattr(g, '_database', None)
  if db is not None:
    db.close()


@app.route('/')
def index():
  if 'username' in session:
    return render_template('index.html', username=session['username'])
  return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    db = get_db()
    cursor = db.execute('SELECT * FROM users WHERE username=? AND password=?',
                        (username, password))
    user = cursor.fetchone()
    if user is not None:
      session['username'] = username
      return redirect(url_for('index'))
  return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    db = get_db()
    db.execute('INSERT INTO users (username, password) VALUES (?, ?)',
               (username, password))
    db.commit()
    return redirect(url_for('login'))
  return render_template('register.html')


@app.route('/logout')
def logout():
  session.pop('username', None)
  return redirect(url_for('index'))


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=81)
# import function from os to get the environmental variables from .flaskenv
from os import environ
# import all necessary functions from flask
from flask import Flask, render_template, url_for, redirect, request, flash, session, abort, g
# import the database module
import sqlite3

app = Flask(__name__)
# get the sercet key for the session from .flaskenv
app.secret_key = environ.get('SECRET_KEY')

# DATABASE_PATH = Path(__file__).parent / '/database/flask_login.db'
DATABASE_PATH = 'database/flask_login.db'


# building a connection to database before each request
@app.before_request
def dbConn():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    # pass the connection in the g variable to use it in all view functions
    g.conn = conn


# destroy the connection after a request is over
@app.teardown_appcontext
def closeConn(exception):
    if conn := g.pop('conn', None):
        conn.close()


@app.route('/')
def home():
    return render_template('index.html')


@app.get('/login/')
def login():
    # if you are already login, redirect to your profile
    if 'username' in session:
        app.logger.debug(session['username'])
        return redirect(url_for('profile', username=session['username']))
    else:
        return render_template('login.html')


@app.post('/login/')
def loginAuth():
    # get the credentials from the login form
    username = request.form.get('username')
    password = request.form.get('password')
    # use cursor to help me execute a query to the database
    cursor = g.conn.cursor()
    user = cursor.execute(
        '''
        SELECT [id], [username]
        FROM [users]
        WHERE [username] = :username AND [password] = :password
        ''',
        {'username': username, 'password': password}).fetchone()
    # close the cursor after the query return the data
    cursor.close()
    # if the query returns 0 result
    if not user:
        flash('Username or password invalid')
        return redirect(url_for('login'))
    # easter egg
    elif user['username'] == 'nbilalis':

        cursor = g.conn.cursor()
        user = cursor.execute(
            '''
            SELECT [username], [firstname], [lastname], [email]
            FROM [users]
            WHERE [username] = :username
            ''',
            {'username': username}).fetchone()
        cursor.close()
        session['username'] = user['username']
        session['firstname'] = user['firstname']
        return redirect(url_for('easterEgg', username=session['username']))
    # if the query returns with data
    elif user is not None:
        session['username'] = username
        return redirect(url_for('profile', username=username))


# destroy the session
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/profile/<username>')
def profile(username=None):
    # if someone tries to view another profile than the one is connected gets error 401
    if 'username' not in session or username != session['username']:
        abort(401)
    else:
        cursor = g.conn.cursor()
        user = cursor.execute(
            '''
            SELECT [username], [firstname], [lastname], [email]
            FROM [users]
            WHERE [username] = :username
            ''',
            {'username': username}).fetchone()
        cursor.close()
        # pass the firstname into session so I can use it all pages
        session['firstname'] = user['firstname']
        username = session['username']
        return render_template('profile.html', user=user)


# Handles the error when a path doesn't exist
@ app.errorhandler(404)
def page_not_found(e):
    app.logger.debug(e)
    return render_template('errors/404.html'), 404


# Handles the errors when something is restricted
@ app.errorhandler(401)
def page_forbidden(e):
    app.logger.debug(e)
    return render_template('errors/401.html'), 401


# easter egg
@ app.route('/easteregg')
def easterEgg():
    if 'username'not in session or session['username'] != 'nbilalis':
        abort(401)
    return render_template('easteregg.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=environ.get('SERVER_PORT', 5000))

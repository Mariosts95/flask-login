from os import environ
from flask import Flask, render_template, url_for, redirect, request, flash, session, abort

app = Flask(__name__)
# get the sercet key for the session from .flaskenv
app.secret_key = environ.get('SECRET_KEY')


@app.route('/')
def home():
    return render_template('index.html')


@app.get('/login/')
def login():
    return render_template('login.html')


@app.post('/login/')
def loginAuth():
    username = request.form.get('username')
    password = request.form.get('password')

    if username == 'admin' and password == 'admin':
        session['logged_in'] = username
        return redirect(url_for('profile', username=username))
    else:
        flash('Username or password invalid')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))


@app.route('/profile')
@app.route('/profile/<username>')
def profile(username):
    if not session['logged_in'] == username:
        abort(401)
    else:
        return render_template('profile.html', username=username)


# Handles the error when a path doesn't exist
@app.errorhandler(404)
def page_not_found(e):
    app.logger.debug(e)
    return render_template('errors/404.html'), 404


@app.errorhandler(401)
def page_forbidden(e):
    app.logger.debug(e)
    return redirect(url_for('login')), 401


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=environ.get('SERVER_PORT', 5000))

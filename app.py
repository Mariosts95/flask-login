from os import environ
from flask import Flask

app = Flask(__name__)


@app.get('/')
def home():
    return 'Hello world!'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=environ.get('SERVER_PORT', 5000))

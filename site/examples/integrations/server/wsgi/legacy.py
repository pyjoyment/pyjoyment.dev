from flask import Flask, url_for


app = Flask(__name__)


@app.get('/')
def index():
    return f'<a href="{url_for("hello", name="Sara")}">Hello</a>'


@app.get('/hello/<name>')
def hello(name):
    return {'hello': name, 'from': 'Flask'}

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/<name>')
def index(name):
    items = ['Nasta', True, 110]
    return render_template('index.html', name=name, items=items)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('404.html'), 500
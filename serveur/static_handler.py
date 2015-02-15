from flask import redirect
from flask import render_template
from flask import request
from serveur import app


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/', methods=['GET'])
def page_home():
    """Home page any language."""
    return render_template('home.html')

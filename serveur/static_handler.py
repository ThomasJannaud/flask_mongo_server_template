from flask import redirect
from flask import render_template
from flask import request
from serveur import app
from serveur import Constants


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/', methods=['GET'])
def page_home():
    """Home page any language."""
    return render_template('home.html', stripe_publishable_key=app.config[Constants.STRIPE_PUBLISHABLE_KEY])


@app.route('/dashboard', methods=['GET'])
def page_dashboard():
    """Dashboard page."""
    return render_template('sorry.html')

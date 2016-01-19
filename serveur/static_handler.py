from flask import redirect
from flask import render_template
from flask import request
from serveur import app
from serveur import Constants
from serveur.utils import user as user_util


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/', methods=['GET'])
def page_home():
    """Home page."""
    user_pb = user_util.getCurrentUserPb()
    return render_template('home.html',
      stripe_publishable_key=app.config[Constants.KEY_STRIPE_PUBLISHABLE_KEY],
      logged_in_name="" if user_pb is None else user_pb.info.email)

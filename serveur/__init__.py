from flask import Flask
from flask.ext.babel import Babel
app = Flask(__name__)
babel = Babel(app)

class Constants:
    # Most constants act as keys in app.config[]
    PROD, BETA, DEBUG = range(3)  # value, not key
    MODE = 'mode'  # app.config[MODE] = one of the constants above
    ALLOW_ANYONE = 'allow_anyone'  # to let freelancers work on beta version (html+js+css only) without any login
    UPLOAD_DIR = 'upload_dir'
    DB_NAME = 'db_name'
    STRIPE_PUBLISHABLE_KEY = "stripe publishable key"
    STRIPE_SECRET_KEY = "stripe secret key"
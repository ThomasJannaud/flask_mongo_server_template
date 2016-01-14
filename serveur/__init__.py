from flask import Flask
from flask.ext.babel import Babel
app = Flask(__name__)
babel = Babel(app)

class Constants:
    # Most constants act as keys in app.config[]
    APP_NAME = 'REPLACEME_NAME'
    PROD, BETA, DEBUG = range(3)  # value, not key
    MODE = 'mode'  # app.config[MODE] = one of the constants above
    ALLOW_ANYONE = 'allow_anyone'  # to let others work on beta version (html+js+css only) without any login
    UPLOAD_DIR = 'upload_dir'
    DB_NAME = 'REPLACEME_DBNAME'
    STRIPE_PUBLISHABLE_KEY = "stripe publishable key"
    STRIPE_SECRET_KEY = "stripe secret key"
    STRIPE_PUBLISHABLE_KEY_LIVE = "REPLACEME_stripe publishable key"
    STRIPE_SECRET_KEY_LIVE = "REPLACEME_stripe secret key"
    STRIPE_PUBLISHABLE_KEY_TEST = "REPLACEME_stripe publishable key"
    STRIPE_SECRET_KEY_TEST = "REPLACEME_stripe secret key"
    FLASK_SECRET_KEY = "REPLACEME_ksdfmkjmaozijdaziodj"
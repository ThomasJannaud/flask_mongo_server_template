from flask import Flask
from flask.ext.babel import Babel
app = Flask(__name__)
babel = Babel(app)

class Constants:
    # Constants that act as keys in app.config[] have prefix KEY_
    APP_NAME = 'REPLACEME_NAME'
    KEY_MODE = 'mode'  # app.config[MODE] = one of the constants PROD, BETA, DEBUG
    PROD, BETA, DEBUG = range(3)
    KEY_ALLOW_ANYONE = 'allow_anyone'  # to let others work on beta version (html+js+css only) without any login
    KEY_UPLOAD_DIR = 'upload_dir'
    DB_NAME = 'REPLACEME_DBNAME'
    KEY_STRIPE_PUBLISHABLE_KEY = "stripe publishable key"
    KEY_STRIPE_SECRET_KEY = "stripe secret key"
    STRIPE_PUBLISHABLE_KEY_LIVE = "REPLACEME_stripe publishable key"
    STRIPE_SECRET_KEY_LIVE = "REPLACEME_stripe secret key"
    STRIPE_PUBLISHABLE_KEY_TEST = "REPLACEME_stripe publishable key"
    STRIPE_SECRET_KEY_TEST = "REPLACEME_stripe secret key"
    FLASK_SECRET_KEY = "REPLACEME_ksdfmkjmaozijdaziodj"
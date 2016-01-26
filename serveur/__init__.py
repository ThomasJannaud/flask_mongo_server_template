from flask import Flask
from flask.ext.babel import Babel
app = Flask(__name__)
babel = Babel(app)

class Constants:
    # Constants that act as keys in app.config[] have prefix KEY_
    APP_NAME = 'REPLACEME_NAME'
    KEY_MODE = 'mode'  # app.config[MODE] = one of the constants PROD, BETA, DEBUG
    PROD, BETA, DEBUG = range(3)
    KEY_UPLOAD_DIR = 'upload_dir'
    DB_NAME = 'REPLACEME_DBNAME'
    FLASK_SECRET_KEY = "REPLACEME_ksdfmkjmaozijdaziodj"
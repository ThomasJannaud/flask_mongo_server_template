#!/usr/bin/python

"""
Main of the server. Run with
    python main.py [--local|--beta|--prod]

--debug : for debugging, localhost
--beta : beta server, real conditions, on beta.xxx.com
--prod : real server, on xxx.com
"""

from logging import Formatter
from logging.handlers import RotatingFileHandler
from serveur import app
from serveur import Constants
import logging
import sys
import datetime

if __name__ == '__main__':
    is_debug = ('--debug' in sys.argv)
    is_beta = ('--beta' in sys.argv)
    is_prod = ('--prod' in sys.argv)
    assert((is_debug or is_beta or is_prod) and len(sys.argv) == 2)
    app.secret_key = Constants.FLASK_SECRET_KEY
    app.debug = is_debug
    if is_debug:
        app.config[Constants.KEY_MODE] = Constants.DEBUG
        app.config[Constants.KEY_UPLOAD_DIR] = "upload_debug"
    elif is_beta:
        app.config[Constants.KEY_MODE] = Constants.BETA
        app.config[Constants.KEY_UPLOAD_DIR] = "upload_beta"
    else:
        app.config[Constants.KEY_MODE] = Constants.PROD
        app.config[Constants.KEY_UPLOAD_DIR] = "upload_prod"
    from serveur.utils import jinja_filters
    from serveur.utils import session_mongo
    from serveur.utils import utils
    jinja_filters.setupFilters(app)
    app.url_map.converters['regex'] = utils.RegexConverter
    handler = RotatingFileHandler('/tmp/app.log' if is_debug else '/var/log/%s.log' % Constants.APP_NAME.lower().replace(' ', '_'), maxBytes=10000000, backupCount=10)
    # log level of the file logger
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.addHandler(handler)
    # log level of the console log
    app.logger.setLevel(logging.INFO)
    # max total upload files : 12 Mo
    app.config['MAX_CONTENT_LENGTH'] = 12 * (2 ** 20)
    # Loads the urls routing
    from serveur import api_handler
    from serveur import debug_handler
    from serveur import product_handler
    from serveur import static_handler
    from serveur import user_handler
    from serveur import utils_handler
    # Run !
    if is_debug:
        # sessions are stored in the db instead of internal variables
        # This makes it easier for debugging.
        app.session_interface = session_mongo.MongoSessionInterface()
        app.run()
    else:
        from tornado.wsgi import WSGIContainer
        from tornado.httpserver import HTTPServer
        from tornado.ioloop import IOLoop
        http_server = HTTPServer(WSGIContainer(app))
        http_server.listen(8001 if is_beta else 80)
        IOLoop.instance().start()

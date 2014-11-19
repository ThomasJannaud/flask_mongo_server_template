#!/usr/bin/python

"""
Main of the server. Run with
    python main.py [--debug]
"""

from datetime import datetime
from datetime import timedelta
from flask import Flask
from flask import request
from logging import Formatter
from logging.handlers import RotatingFileHandler
from serveur import app
from serveur.utils import jinja_filters
from serveur.utils import session_mongo
from serveur.utils import utils
import logging
import sys


if __name__ == '__main__':
    jinja_filters.setupFilters(app)
    app.url_map.converters['regex'] = utils.RegexConverter
    app.secret_key = "dsfdsf"
    is_debug = (len(sys.argv) == 2 and sys.argv[1] == '--debug')
    handler = RotatingFileHandler('/tmp/app.log' if is_debug else '/var/log/test_server.log',
                                  maxBytes=10000000, backupCount=10)
    # log level of the file logger
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.addHandler(handler)
    # log level of the console log
    app.logger.setLevel(logging.INFO)
    # Loads the urls routing
    from serveur import debug_handler
    from serveur import user_handler
    from serveur import listener_handler
    # Run !
    if is_debug:
        app.debug = True
        # sessions are stored in the db instead of internal variables -> easier for debugging.
        app.session_interface = session_mongo.MongoSessionInterface()
        app.run()
    else:
        from tornado.wsgi import WSGIContainer
        from tornado.httpserver import HTTPServer
        from tornado.ioloop import IOLoop
        http_server = HTTPServer(WSGIContainer(app))
        http_server.listen(8001)
        IOLoop.instance().start()
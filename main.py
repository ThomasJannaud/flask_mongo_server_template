#!/usr/bin/python

"""
Main of the server. Run with
    python main.py [--debug]
"""

from datetime import datetime
from datetime import timedelta
from flask import Flask
from flask import request
from flask.ext.login import LoginManager
from serveur import debug_handler
from serveur import listener_handler
from serveur import user_handler
from serveur.utils import session_mongo
from serveur.utils import jinja_filters
from werkzeug.routing import BaseConverter
import sys



class RegexConverter(BaseConverter):
    """Used to define regexes in app routing."""
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


if __name__ == '__main__':
    app = Flask(__name__)
    app.jinja_env.filters['time_period'] = jinja_filters.time_period
    app.url_map.converters['regex'] = RegexConverter

    @app.before_request
    def log_request():
        app.logger.debug(request.url)

    # ------------------------------------------------------------------------------------------
    # Debug Handler    
    debug_handl = debug_handler.DebugHandler()
    @app.route('/debug/<regex(".*"):al>', methods=['GET'])
    def debug_special(al):
        return debug_handl.Special(al)

    @app.route('/debug', methods=['GET'])
    def debug_get():
        return debug_handl.Get()

    @app.route('/debug', methods=['POST'])
    def debug_post():
        return debug_handl.Post()

    # ------------------------------------------------------------------------------------------
    # User Handler
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(userid):
        return user_handler.load_user(userid)

    @app.route('/register')
    def register():
        return user_handler.register()

    @app.route('/login')
    def logme():
        return user_handler.login()

    @app.route('/logout')
    def logout():
        return user_handler.logout()

    @app.route('/test_user')
    def testpage():
        return user_handler.test()

    # ------------------------------------------------------------------------------------------
    # Misc
    listener_handl = listener_handler.ListenerHandler()
    @app.route('/listener', methods=['POST'])
    def listener():
        return listener_handl.Post()


    app.secret_key = "dsfdsf"
    is_debug = (len(sys.argv) == 2 and sys.argv[1] == '--debug')
    if is_debug:
        app.debug = True
        app.session_interface = session_mongo.MongoSessionInterface()
        app.run()
    else:
        from tornado.wsgi import WSGIContainer
        from tornado.httpserver import HTTPServer
        from tornado.ioloop import IOLoop
        http_server = HTTPServer(WSGIContainer(app))
        http_server.listen(8001)
        IOLoop.instance().start()
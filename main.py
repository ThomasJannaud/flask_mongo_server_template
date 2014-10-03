#!/usr/bin/python

"""Main of the server. run with "python main.py [--debug]" depending if you are debugging locally or if it is the prod server."""

import data_models
import jinja_filters
import listener_handler

from flask import Flask, request
from flask.ext import login
from flask.ext.login import LoginManager
 

class FLUser:
  def __init__(self, user_pb):
    self.user_pb = user_pb
  def is_authenticated(self):
    return True
  def is_active(self):
    return True
  def is_anonymous(self):
      return False
  def get_id(self):
    return self.user_pb.id


if __name__ == '__main__':
  app = Flask(__name__)
  app.jinja_env.filters['time_period'] = jinja_filters.time_period

  login_manager = LoginManager()
  login_manager.init_app(app)
  login_manager.login_view = 'login'


  @app.before_request
  def log_request():
    app.logger.debug(request.url)


  listener_handl = listener_handler.ListenerHandler()
  @app.route('/listener', methods=['POST'])
  def listener():
    return listener_handl.Post()


  @app.route('/test')
  def testpage():
    if login.current_user.is_anonymous():
      return 'anonyme'
    else:
      return 'salut' + login.current_user.user_pb.prenom


  @app.route('/testlog')
  @login.login_required
  def testlog():
    return 'une page'

  @login_manager.user_loader
  def load_user(userid):
    table = data_models.GetTable(data_models.RW_USERS)
    user_pb = data_models.ToProto(table.find_one({"_id": userid}), data_models.RW_USERS)
    if not user_pb: return None
    return FLUser(user_pb)

  @app.route('/raz')
  def raz():
    data_models.GetTable(data_models.RW_USERS).drop()
    return 'razed'


  @app.route('/register')
  def register():
    user_pb = data_models.all_pbs.User()
    user_pb.id = '1234'
    user_pb.prenom = 'thomas'
    data_models.SaveProto(user_pb, data_models.RW_USERS)
    return 'ok, registered'


  @app.route('/login')
  def logme():
    table = data_models.GetTable(data_models.RW_USERS)
    user_pb = data_models.ToProto(table.find_one({"_id": "1234"}), data_models.RW_USERS)
    user = FLUser(user_pb)
    login.login_user(user, remember=True)
    return 'log in success'


  @app.route('/logout',methods=['GET'])
  def logout():
    login.logout_user()
    return 'logged out'

  app.debug = True
  app.secret_key = "sdflkdsmflk"
  app.run()

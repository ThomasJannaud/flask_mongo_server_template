from flask import request
from flask import session
from flask.ext import login as flogin
from flask.ext.login import LoginManager
from serveur import app
from serveur import Constants
from serveur.db import all_pb2 as all_pbs
from serveur.db import data_models
import protobuf_json


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
@login_manager.user_loader
def load_user(userid):
    """Used by Flask to make a FLUser from our user id, for auto login sessions from cookie etc."""
    try:
        user_id = int(userid)
        table = data_models.GetTable(data_models.RW_USERS)
        user_pb = data_models.ToProto(table.find_one({"_id": user_id}), data_models.RW_USERS)
        if not user_pb: return None
        return FLUser(user_pb)
    except:
        return None


class FLUser:
    """Wrapper class around our User datamodel in the protobuf.
    Flask needs this class to save cookie for session auto-login, ...
    All the info about the user (first name, ...) is saved in the proto, and all the info
    about anonymous user, logged in, ... is in the wrapper layer."""
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


def doesEmailExist(email):
    """Returns true if a user exist with this email."""
    table = data_models.GetTable(data_models.RW_USERS)
    user_pb = data_models.ToProto(table.find_one({"info.email": email}), data_models.RW_USERS)
    return user_pb is not None


def isAdmin():
    """Returns True if the user is logged in as admin or if debug and &admin=1."""
    if app.debug and request.args.get('admin', False):
        return True
    if flogin.current_user.is_anonymous():
        return False
    return flogin.current_user.user_pb.admin


def getCurrentUserPb():
    """Returns the loggedin user's protobug or None if no user is logged in"""
    if flogin.current_user.is_anonymous():
        return None
    return flogin.current_user.user_pb
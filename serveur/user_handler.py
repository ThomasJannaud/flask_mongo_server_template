from flask import session
from flask.ext import login as flogin
from flask.ext.login import LoginManager
from serveur import app
from serveur.db import data_models


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


@app.route('/api/v1/register')
def register():
    """Creates the user in the database. For users, don't use mongodb's id, you must create our own (email, ...).
    TODO: Should of course use the request params, not harcoded values."""
    user_pb = data_models.all_pbs.User()
    user_pb.id = 1234
    user_pb.email = "test@mail.com"
    data_models.SaveProto(user_pb, data_models.RW_USERS)
    return 'ok, registered'


@app.route('/api/v1/login')
def login():
    """ login as our user.
    TODO: in practice, check request login/password."""
    table = data_models.GetTable(data_models.RW_USERS)
    user_pb = data_models.ToProto(table.find_one({"_id": 1234}), data_models.RW_USERS)
    user = FLUser(user_pb)
    flogin.login_user(user, remember=True)
    return 'log in success'


@app.route('/api/v1/logout')
def logout():
    flogin.logout_user()
    return 'logged out'


@app.route('/test_user')
def test():
    """This is for playing with session/login/logout. Sessions exist for anonymous users. Ex: buying goods in an ecommerce
    -> you need session to know what is in the shopping cart.
    TODO: in practice, check request login/password."""
    KEY_USER_IN_CREATION = 'user_in_creation'
    if KEY_USER_IN_CREATION not in session:
        user_in_creation = data_models.all_pbs.User()
        user_in_creation.email = 'anonymous@session'
        session[KEY_USER_IN_CREATION] = data_models.protobuf_json.pb2json(user_in_creation)
    if flogin.current_user.is_anonymous():
        user_in_creation = data_models.protobuf_json.json2pb(data_models.all_pbs.User(), session[KEY_USER_IN_CREATION])
        return 'anonyme ; current user in creation :' + user_in_creation.email
    else:
        user_in_creation = data_models.protobuf_json.json2pb(data_models.all_pbs.User(), session[KEY_USER_IN_CREATION])
        return 'logged in / not anononymous ; user:%s, current user in creation:%s' % (
            flogin.current_user.user_pb.email, user_in_creation.email)


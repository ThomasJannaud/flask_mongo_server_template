from flask import session
from flask.ext import login as flogin
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


def load_user(userid):
    """Used by Flask to make a FLUser from our user id, for auto login sessions from cookie etc."""
    table = data_models.GetTable(data_models.RW_USERS)
    user_pb = data_models.ToProto(table.find_one({"_id": userid}), data_models.RW_USERS)
    if not user_pb: return None
    return FLUser(user_pb)


def register():
    """Creates the user in the database. For users, don't use mongodb's id, e create our own (email, ...).
    TODO: Should of course use the request params, not harcoded values."""
    user_pb = data_models.all_pbs.User()
    user_pb.id = '1234'
    user_pb.prenom = 'thomas'
    data_models.SaveProto(user_pb, data_models.RW_USERS)
    return 'ok, registered'


def login():
    """ login as our user.
    TODO: in practice, check request login/password."""
    table = data_models.GetTable(data_models.RW_USERS)
    user_pb = data_models.ToProto(table.find_one({"_id": "1234"}), data_models.RW_USERS)
    user = FLUser(user_pb)
    flogin.login_user(user, remember=True)
    session['toto'] = 0  # this is for playing in /test_user only
    return 'log in success'


def logout():
    flogin.logout_user()
    return 'logged out'


def test():
    """This is for playing with session/login/logout. Sessions exist for anonymous users. Ex: buying goods in an ecommerce
    -> you need session to know what is in the shopping cart.
    TODO: in practice, check request login/password."""
    if 'toto' not in session:
        us = data_models.all_pbs.User()
        us.prenom = 'skfjldkjf'
        session['toto'] = data_models.protobuf_json.pb2json(us)
    if flogin.current_user.is_anonymous():
        us = data_models.protobuf_json.json2pb(data_models.all_pbs.User(), session['toto'])
        return 'anonyme' + us.prenom
    else:
        us = data_models.protobuf_json.json2pb(data_models.all_pbs.User(), session['toto'])
        return 'salut' + flogin.current_user.user_pb.prenom + us.prenom


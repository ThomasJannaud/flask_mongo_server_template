from flask import session
from flask.ext import login as flogin
from serveur.db import data_models


class FLUser:
    """Wrapper class around our User datamodel in the protobuf.
    Flask needs this class to save cookie for session auto-login, ...
    All the info about the user is saved there."""
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
    table = data_models.GetTable(data_models.RW_USERS)
    user_pb = data_models.ToProto(table.find_one({"_id": userid}), data_models.RW_USERS)
    if not user_pb: return None
    return FLUser(user_pb)


def register():
    user_pb = data_models.all_pbs.User()
    user_pb.id = '1234'
    user_pb.prenom = 'thomas'
    data_models.SaveProto(user_pb, data_models.RW_USERS)
    return 'ok, registered'


def login():
    table = data_models.GetTable(data_models.RW_USERS)
    user_pb = data_models.ToProto(table.find_one({"_id": "1234"}), data_models.RW_USERS)
    user = FLUser(user_pb)
    flogin.login_user(user, remember=True)
    session['toto'] = 2
    return 'log in success'


def logout():
    flogin.logout_user()
    return 'logged out'


def test():
    if 'toto' not in session:
        us = data_models.all_pbs.User()
        us.prenom = 'skfjldkjf'
        session['toto'] = data_models.protobuf_json.pb2json(us)
    if flogin.current_user.is_anonymous():
        us = data_models.protobuf_json.json2pb(data_models.all_pbs.User(), session['toto'])
        return 'anonyme' + us.prenom
    else:
        import pdb; pdb.set_trace()
        us = data_models.protobuf_json.json2pb(data_models.all_pbs.User(), session['toto'])
        return 'salut' + flogin.current_user.user_pb.prenom + us.prenom


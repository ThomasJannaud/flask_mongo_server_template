"""
We want to allow anyone using the server to have their own rest interface for quick testing.
Ex: you want /debug/values to return {'email': 'aa@a.com', 'password': 'abcd'}.
On /debug, you can see what the server will return for various urls of your choice, and set this.
"""

from flask import abort
from flask import render_template
from flask import request
from flask import session
from flask.ext import login as flogin
from serveur import app
from serveur import Constants
from serveur.db import all_pb2 as all_pbs
from serveur.db import data_models
from serveur.utils import user as user_util
import glob
import json
import os
import shutil

urls = {}
debug_input_as_json = ''


@app.route('/api/debug/<regex(".*"):args>', methods=['GET', 'POST'])
def Special(args):
    """Returns the debug value for the debug url, specified in the /debug UI."""
    return json.dumps(urls.get("/debug/%s" % args, 'error'))


@app.route('/debug', methods=['GET'])
def Get():
    """Show the debug dashboard."""
    return render_template('debug.html', text=debug_input_as_json)


@app.route('/api/debug', methods=['POST'])
def Post():
    """Saves debug url -> json info. Used in the debug dashboard."""
    global urls, debug_input_as_json
    debug_input_as_json = request.form['urls']
    urls = json.loads(debug_input_as_json)
    return 'ok'


@app.route('/api/debug/login', methods=['GET'])
def debug_login():
    """Auto login with no password.

    ?user_id=2
    """
    if app.config[Constants.KEY_MODE] == Constants.PROD:
        abort(401)
    table = data_models.GetTable(data_models.RW_USERS)
    user_pb = data_models.ToProto(table.find_one({"_id": int(request.args.get('user_id'))}), data_models.RW_USERS)
    if not user_pb:
        return "error"
    user = user_util.FLUser(user_pb)
    flogin.login_user(user, remember=True)
    return 'ok'


@app.route('/api/trashbin', methods=['POST'])
def toTrashbin():
    """Post to here if you want to see what has been posted.

    Always returns 'ok'."""
    print request.data
    inp = request.get_json()
    print json.dumps(inp, indent=4, sort_keys=True)
    return 'ok'


@app.route('/raz', methods=['GET'])
def raz():
    """Empties the database and puts back all the fake data."""
    if app.config[Constants.KEY_MODE] == Constants.PROD or (app.config[Constants.KEY_MODE] == Constants.BETA and request.args.get("admin", "0") != "1"):
        abort(401)
    data_models.Raz()
    server_dir = os.path.dirname(os.path.realpath(__file__))
    # The filenames in the directory must match the collection names in data_models
    for table in (data_models.RW_USERS, data_models.RW_PRODUCTS, ):
        with open('%s/../fake_data/%s.json' % (server_dir, table)) as f:
            datas = json.loads(f.read())
            for data in datas:
                pb = data_models.DictToProto(data_models.ProtoForTable(table), data)
                data_models.SaveProto(pb, table)
    upload_dir = "%s/static/%s" % (server_dir, app.config[Constants.KEY_UPLOAD_DIR])
    shutil.rmtree(upload_dir, ignore_errors=True)
    os.mkdir(upload_dir)
    return 'ok'


@app.route('/debug/test_user')
def testUser():
    """Returns 'logged in as email' or 'logged out'. This is for debug/test/show off mainly."""
    if flogin.current_user.is_anonymous():
        return 'logged out'
    return 'logged in as %s' % flogin.current_user.user_pb.info.email


@app.route('/debug/test_session')
def testSession():
    """This is for playing with session/login/logout. Sessions exist for anonymous users. Ex: buying goods in an ecommerce
    -> you need session to know what is in the shopping cart.
    In practice, check request login/password."""
    KEY_USER_IN_CREATION = 'user_in_creation'
    if KEY_USER_IN_CREATION not in session:
        user_in_creation = data_models.all_pbs.User()
        user_in_creation.info.email = 'anonymous@session'
        session[KEY_USER_IN_CREATION] = data_models.protobuf_json.pb2json(user_in_creation)
    if flogin.current_user.is_anonymous():
        user_in_creation = data_models.protobuf_json.json2pb(data_models.all_pbs.User(), session[KEY_USER_IN_CREATION])
        return 'anonyme ; current user in creation :' + user_in_creation.info.email
    else:
        user_in_creation = data_models.protobuf_json.json2pb(data_models.all_pbs.User(), session[KEY_USER_IN_CREATION])
        return 'logged in / not anononymous ; user:%s, current user in creation:%s' % (
            flogin.current_user.user_pb.info.email, user_in_creation.info.email)

from flask import abort
from flask import redirect
from flask import render_template
from flask import request
from flask.ext import login as flogin
from flask.ext.login import LoginManager
from serveur import app
from serveur import Constants
from serveur.db import all_pb2 as all_pbs
from serveur.db import data_models
from serveur.utils import user as user_util
from serveur.utils import utils
import json
import protobuf_json
import stripe


@app.route('/api/v1/forgot_password', methods=["GET"])
def forgot_password():
    """Sends an email.

    output: "ok".

    Request
        ?email=xxx@yy.com
    """
    table = data_models.GetTable(data_models.RW_USERS)
    user_pb = data_models.ToProto(table.find_one({"info.email": request.args.get("email", "")}), data_models.RW_USERS)
    if not user_pb:
        abort(401)
    utils.SendMail(email_from="no-reply", to=user_pb.info.email, obj="Credentials", body="Your login credentials :\n%s\n%s" % (user_pb.info.email, user_pb.info.password))
    return "ok"


@app.route('/api/v1/check-new-email', methods=["GET"])
def check_email():
    """Checks that an email can be used for registration, i.e that
    it is not used by someone else.

    output: "ok" or "error"

    Request
        ?email=xxx@xx.com
    """
    email = request.args.get("email", "")
    if not email or user_util.doesEmailExist(email):
        abort(400)
    return "ok"


@app.route('/api/v1/register', methods=["POST"])
def register():
    """Creates an account + the user in the database + auto login.

    input: RegistrationRequest
    output: "ok".
    """
    registration_req_pb = data_models.DictToProto(all_pbs.RegistrationRequest(), request.get_json())
    user_info_pb = registration_req_pb.user_info
    if not user_info_pb.email or \
            not registration_req_pb.stripe_token or \
            user_util.doesEmailExist(user_info_pb.email):
        abort(400)
    user_pb = all_pbs.User()
    user_pb.info.MergeFrom(user_info_pb)
    user_pb.id = data_models.GetUniqueId()
    customer = stripe.Customer.create(
        card=registration_req_pb.stripe_token,
        description='%s %s - %d' % (user_info_pb.first_name, user_info_pb.last_name, user_pb.id),
        email=user_info_pb.email,
        metadata={"user_id": user_pb.id},
    )
    if not customer:
        abort(400)
    timestamp_secs = utils.getTimestampSecs()
    user_pb.timestamp_creation_secs = timestamp_secs
    user_pb.stripe_customer_id = customer.id
    data_models.SaveProto(user_pb, data_models.RW_USERS)
    flogin.logout_user()
    user = user_util.FLUser(user_pb)
    flogin.login_user(user, remember=False)
    return 'ok'


@app.route('/api/v1/login', methods=['POST', 'GET'])
def login():
    """login as our user.
    input: LoginRequest (if POST)
    output: ok.

    Request:
        ?email=xx&password=xx[&remember_me=1] (if GET, else arguments in LoginRequest)
    """
    if request.method == "POST":
        input_pb = protobuf_json.json2pb(all_pbs.LoginRequest(), request.get_json())
    else:
        input_pb = all_pbs.LoginRequest()
        input_pb.email = request.args.get("email", "")
        input_pb.password = request.args.get("password", "")
        input_pb.remember = request.args.get("remember", "") == "1"
    table = data_models.GetTable(data_models.RW_USERS)
    user_pb = data_models.ToProto(table.find_one({"info.email": input_pb.email}), data_models.RW_USERS)
    if not user_pb or user_pb.info.password != input_pb.password:
        abort(400)
    user = user_util.FLUser(user_pb)
    flogin.login_user(user, remember=input_pb.remember)
    return 'ok'


@app.route('/api/v1/logout', methods=['GET'])
def logout():
    """log out."""
    flogin.logout_user()
    return 'ok'

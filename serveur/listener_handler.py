from flask import request
from serveur import app
from serveur.db import data_models
from serveur.db import test_pb2 as all_pbs
import protobuf_json
import json


@app.route('/listener', methods=['GET'])
def listener():
	inp = request.get_json()
	pb = protobuf_json.json2pb(all_pbs.ObjA(), inp)
	data_models.SaveProto(pb, data_models.RW_NAMES)
	return 'ok'

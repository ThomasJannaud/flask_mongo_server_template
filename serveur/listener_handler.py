from flask import request
import protobuf_json
import json
from serveur.db import data_models
from serveur.db import test_pb2 as all_pbs


class ListenerHandler:
	def Post(self):
		inp = request.get_json()
		pb = protobuf_json.json2pb(all_pbs.ObjA(), inp)
		data_models.SaveProto(pb, data_models.RW_NAMES)
		return 'ok'

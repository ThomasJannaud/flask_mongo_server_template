import data_models
import proto.test_pb2 as all_pbs

from flask import request
import protobuf_json
import json

class ListenerHandler:
  def Post(self):
    import pdb; pdb.set_trace()
    inp = request.get_json()
    pb = protobuf_json.json2pb(all_pbs.ObjA(), inp)
    data_models.SaveProto(pb, data_models.RW_NAMES)
    return 'ok'

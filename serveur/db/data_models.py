from bson.son import SON
from serveur import Constants
from serveur.db import all_pb2 as all_pbs
import protobuf_json    # protobuf <-> dict, not json
import pymongo
import random



# Collection names in mongo. We decide that a collection will hold only one type of object.
# Collections are read-write (RW_... = 'raw_...') or read-only (RO_... = 'out_...').
# _ read-write collections are written by /listener
# _ read-only collections are the results of background mapreduces. (see pipelines/)
#     Mapreduce objects have internally in mongo only 2 fields : _id and value
#     so protobuf fields will be scattered in those two.
#
# N.B: read-write and read-only is only a formalism for us not to mix up collections in this code
# and elsewhere. Mongo doesn't implement such a mechanism.
# WARNING: we want this server to have read-write access to the rw collections and
# read-only access to the ro collections, but the most important collections are the RW ones !
# RO collections are results of RW collections. If a RO collection is deleted we can recover it
# very easily. RW collections are the real stuff, if they are deleted we are screwed.

RW_USERS = 'users'
RW_PRODUCTS = 'products'
RW_SALES = 'sales'
RW_SESSIONS = 'sessions'
RW_UNIQUE_IDS = 'unique_ids'


# Implements collection -> protobuf type uniqueness.
_COLLECTION_TO_PB_CLASS = {
    RW_SESSIONS: None,
    RW_PRODUCTS: all_pbs.Product,
    RW_USERS: all_pbs.User,
    RW_SALES: all_pbs.Sale,
}

client = pymongo.MongoClient()
mongo_db = client[Constants.DB_NAME]


def Raz():
    """Empties the database."""
    client.drop_database(Constants.DB_NAME)


def GetTable(collection):
    """Returns the Python object that mirrors the MongoDB collection.
    On it you can call .find(), ... Cf pymongo documentation."""
    assert(collection in _COLLECTION_TO_PB_CLASS)
    return mongo_db[collection]


def ProtoForTable(table):
    """Returns a new proto object for the given table."""
    return _COLLECTION_TO_PB_CLASS[table]()


def ProtoToKVS(pb, collection_name):
    kvs = protobuf_json.pb2json(pb)
    if collection_name in (RW_USERS,) and pb.id:
        kvs['_id'] = pb.id
        del kvs['id']
    return kvs


def SaveProto(obj, collection_name):
    """Saves the protobuf 'obj' into the mongodb collection collection_name.
    A protobuf is like a dictionary and mongo likes dictionaries.
    However, there might be some subtleties on both sides and this function is responsible
    for interfacing with mongo correctly (cf '_id' field present in mongo but not in protobufs,
    or eventual indexes, ...).
    SaveProto and ToProto are meant to be reciprocal."""
    assert(obj.__class__ == _COLLECTION_TO_PB_CLASS[collection_name])
    kvs = ProtoToKVS(obj, collection_name)
    mongo_db[collection_name].save(kvs)


def ToProto(cursor, collection_name=None):
    """Transforms a cursor result (collection.find(...) into the associated protobuf.
    Data in mongo is not exactly proto -> dictionary -> mongo, e.g results of mapreduce
    are of the form {_id:, value:}, so this interfaces    mongo and our protobuf data model.
    This is the reciprocal function of SaveProto plus it enables to read 'read-only' collections
    (SaveProto doesn't handle them)."""
    # example : ToProto(table.find_one()) -> None.
    if not cursor: return None
    col_name = cursor.collection.name if collection_name is None else collection_name
    cls = _COLLECTION_TO_PB_CLASS[col_name]
    if col_name in (RW_USERS, ):
        pb = protobuf_json.json2pb(cls(), cursor)
        pb.id = cursor['_id']
        return pb
    return protobuf_json.json2pb(cls(), cursor)


def SaveProtos(objs, collection_name):
    """Saves the array of protobuf 'obj' into the mongodb collection collection_name.
    See notes in SaveProto.
    SaveProtos and ToProtos are meant to be reciprocal."""
    all_kvs = []
    for obj in objs:
        assert(obj.__class__ == _COLLECTION_TO_PB_CLASS[collection_name])        
        kvs = ProtoToKVS(obj, collection_name)
        all_kvs.append(kvs)
    mongo_db[collection_name].insert(all_kvs)


def ToProtos(cursor):
    """Transforms the result of a collection.find() (multiple) into an array of protobuf."""
    return [ToProto(x, cursor.collection.name) for x in cursor]


def ToDict(pb):
    """protobuf -> dictionary.
    Wrapper around protobuf_json module so that other modules in our project don't use it."""
    return protobuf_json.pb2json(pb)


def DictToProto(pb, json_data):
    """dictionary -> protobuf."""
    return protobuf_json.json2pb(pb, json_data)


def ArrayToProto(pb_class, json_array):
    """json array -> list of protobuf."""
    return [protobuf_json.json2pb(pb_class(), x) for x in json_array]


def ToArray(pbs):
    """[protobuf] -> [dictionary].
    Wrapper around protobuf_json module so that other modules in our project don't use it."""
    return [ToDict(pb) for pb in pbs]


def GetUniqueId():
    """Returns unique id uint64."""
    table = mongo_db[RW_UNIQUE_IDS]
    while True:
        # 100 : this is to avoid collisions with fake data ids.
        _id = 100 + random.getrandbits(30)
        x = table.find_one({"_id": _id})
        if x == None:
            table.insert({"_id": _id})
            return _id
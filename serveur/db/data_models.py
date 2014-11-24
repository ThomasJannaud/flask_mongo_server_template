import pymongo
import protobuf_json    # protobuf <-> dict, not json

import test_pb2 as all_pbs


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

RW_NAMES = 'raw_all'
RW_USERS = 'raw_users'
RW_SESSIONS = 'raw_sessions'

# Implements collection -> protobuf type uniqueness.
_COLLECTION_TO_PB_CLASS = {
        RW_NAMES: all_pbs.ObjA,
        RW_USERS: all_pbs.User,
        RW_SESSIONS: None,
}

client = pymongo.MongoClient()
mongo_db = client.test_db


def GetTable(collection):
    """Returns the Py object that mirrors the MongoDB collection.
    On it you can call .find(), ... cf pymongo documentation."""
    assert(collection in _COLLECTION_TO_PB_CLASS)
    return mongo_db[collection]


def SaveProto(obj, collection_name):
    """Saves the protobuf 'obj' into the mongodb collection collection_name.
    A protobuf is like a dictionary and mongo likes dictionaries.
    However, there might be some subtleties on both sides and this function is responsible
    for interfacing with mongo correctly (cf '_id' field present in mongo but not in protobufs,
    or eventual indexes, ...).
    SaveProto and ToProto are meant to be reciprocal."""
    assert(obj.__class__ == _COLLECTION_TO_PB_CLASS[collection_name])
    kvs = protobuf_json.pb2json(obj)
    if collection_name == RW_USERS and obj.id:
        kvs['_id'] = obj.id
        del kvs['id']
    mongo_db[collection_name].save(kvs)


def ToProto(cursor, collection_name=None):
    """Transforms a cursor result (collection.find(...) into the associated protobuf.
    Data in mongo is not exactly proto -> dictionary -> mongo, e.g results of mapreduce
    are of the form {_id:, value:}, so this interfaces    mongo and our protobuf data model.
    This is the reciprocal function of SaveProto plus it enables to read 'read-only' collections
    (SaveProto doesn't handle them)."""
    # example : ToProto(table.findOne()) -> None.
    if not cursor: return None
    col_name = cursor.collection.name if collection_name is None else collection_name
    cls = _COLLECTION_TO_PB_CLASS[col_name]
    if col_name == RW_USERS:
        pb = protobuf_json.json2pb(cls(), cursor)
        pb.id = cursor['_id']
        return pb
    return protobuf_json.json2pb(cls(), cursor)


def ToProtos(cursor):
    """Transforms the result of a collection.find() (multiple) into an array of protobuf."""
    return [ToProto(x, cursor.collection.name) for x in cursor]


def ToDict(pb):
    """protobuf -> dictionary.
    Wrapper around protobuf_json module so that other modules in our project don't use it."""
    return protobuf_json.pb2json(pb)

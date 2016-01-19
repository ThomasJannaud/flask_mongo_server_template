from flask import abort
from flask import render_template
from flask import request
from serveur import app
from serveur.db import data_models
from serveur.db import all_pb2 as all_pbs
import json
import protobuf_json


@app.route('/products', methods=['GET'])
def page_products():
    """Products page."""
    return render_template("products.html")
    

@app.route('/api/v1/products/all', methods=['GET'])
def get_all_product():
    """Gets all products in the db.

    output: [Product] as json.
    """
    table = data_models.GetTable(data_models.RW_PRODUCTS)
    product_pbs = data_models.ToProtos(table.find())
    return json.dumps(data_models.ToArray(product_pbs))


@app.route('/api/v1/products/save', methods=['POST'])
def save_product():
    """Takes an array of Product as json and saves them all in the db, overwriting the existing ones.

    input: [Product]
    output: 'ok'
    """
    inp = request.get_json()
    pbs = data_models.ArrayToProto(all_pbs.Product, inp)
    data_models.GetTable(data_models.RW_PRODUCTS).drop()
    data_models.SaveProtos(pbs, data_models.RW_PRODUCTS)
    return 'ok'

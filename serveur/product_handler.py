from flask import abort
from flask import render_template
from flask import request
from serveur import app
from serveur.db import data_models
from serveur.db import test_pb2 as all_pbs
import protobuf_json


@app.route('/products', methods=['GET'])
def page_products():
    """Products page."""
    return render_template("products.html")
    

@app.route('/api/v1/product/all', methods=['GET'])
def get_all_product():
    """Gets all products in the db.

    output: [ObjA] as json.
    """
    table = data_models.GetTable(data_models.RW_PRODUCTS)
    product_pbs = data_models.ToProto(table.find())
    return json.dumps(data_models.ToArray(product_pbs))


@app.route('/api/v1/product/save', methods=['POST'])
def save_product():
	"""Takes an object of type ObjA as json and saves it in the db."""
	inp = request.get_json()
	pb = protobuf_json.json2pb(all_pbs.ObjA(), inp)
	data_models.SaveProto(pb, data_models.RW_PRODUCTS)
	return 'ok'

from flask import abort
from flask import render_template
from flask import request
from serveur import app
from serveur import babel
from serveur import Constants
from serveur.db import all_pb2 as all_pbs
from serveur.db import data_models
from serveur.utils import user as user_utils
from serveur.utils import utils
import json
import os


@app.before_request
def log_request():
    app.logger.debug(request.url)


@babel.localeselector
def get_locale():
    for lang in ('en', 'fr'):
        if ('/%s/' % lang) in request.url:
            return lang
    return 'en'


IMAGE_TYPE_AND_MIMES = {
    'png': 'image/png',
    'jpg': 'image/jpg',
    'jpg': 'image/jpeg',
    'm4v': 'video/mp4',
    'wmv': 'video/x-ms-wmv',
    'mov': 'video/quicktime',
}

def getImageTypeAndBytes(image_64):
    """image_64: "data:image/png;base64....."."""
    BAD_RESPONSE = None, None
    a = image_64.find("base64")
    if a < 0: return BAD_RESPONSE
    first_bytes = image_64[:a-1]
    last_bytes = image_64[a+len("base64,"):]
    for image_type, mime_type in IMAGE_TYPE_AND_MIMES.iteritems():
        if mime_type in first_bytes:
            return image_type, last_bytes
    return BAD_RESPONSE


@app.route('/api/v1/save-image', methods=['POST'])
def save_image():
    """Saves picture or movie.
    
    Request:
        ?account_id=xxx
        image or movie as base64

    output: '/static/upload/ad-129343297.jpg'
    """
    has_permission, account_id = user_utils.checkAccountAccess()
    if not has_permission:
        abort(401)
    image_64 = request.data
    # file input checking
    if len(image_64) > 10 * (2 ** 20):  # 10 Mo
        abort(400)
    image_type, b64bytes = getImageTypeAndBytes(image_64)
    if image_type not in IMAGE_TYPE_AND_MIMES:
        abort(400)
    # saving new file with unique id
    server_dir = os.path.dirname(os.path.realpath(__file__))
    file_id = data_models.GetUniqueId()
    filename = "ad-%d.%s" % (file_id, image_type)
    full_filename = "static/%s/%s" % (app.config[Constants.UPLOAD_DIR], filename)
    with open(server_dir + "/" + full_filename, "wb") as f:
        f.write(b64bytes.decode('base64'))
    return utils.FileToImageUrl(filename)

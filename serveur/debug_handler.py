from flask import render_template
from flask import request
from serveur import app
import json


@app.before_request
def log_request():
    app.logger.debug(request.url)


@app.route('/debug/<regex(".*"):args>', methods=['GET'])
def Special(args):
    return json.dumps(self.urls.get("/debug/%s" % args, '"error"'))


@app.route('/debug', methods=['GET'])
def Get():
    return render_template('debug.html', text=json.dumps(self.urls))


@app.route('/debug', methods=['POST'])
def Post():
    inp = request.form['urls']
    self.urls = json.loads(inp)
    return self.Get()

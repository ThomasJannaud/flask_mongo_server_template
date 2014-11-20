"""
We want to allow anyone using the server to have their own rest interface for quick testing.
Ex: you want /debug/values to return {'email': 'aa@a.com', 'password': 'abcd'}.
On /debug, you can see what the server will return for various urls of your choice, and set this.
"""


from flask import render_template
from flask import request
from flask import session
from serveur import app
import json

urls = {}

@app.before_request
def log_request():
    app.logger.debug(request.url)


@app.route('/api/debug/<regex(".*"):args>', methods=['GET'])
def Special(args):
    return json.dumps(urls.get("/debug/%s" % args, 'error'))


@app.route('/debug', methods=['GET'])
def Get():
    return render_template('debug.html', text=json.dumps(urls))


@app.route('/api/debug', methods=['POST'])
def Post():
    inp = request.form['urls']
    urls = json.loads(inp)
    return 'ok'

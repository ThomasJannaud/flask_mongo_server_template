from flask import render_template
from flask import request
import json


class DebugHandler:
    def __init__(self):
    	self.urls = {}

    def Special(self, args):
        return json.dumps(self.urls.get("/debug/%s" % args, '"error"'))


    def Get(self):
        return render_template('debug.html', text=json.dumps(self.urls))


    def Post(self):
        inp = request.form['urls']
        self.urls = json.loads(inp)
        return self.Get()

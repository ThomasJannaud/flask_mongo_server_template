"""This intends to replicate what swaggers does:
it lists all apis and url routes in the project."""

from flask import abort
from flask import render_template
from flask import request
from flask import session
from flask.ext import login as flogin
from serveur import app
from serveur.db import all_pb2 as all_pbs
from serveur.db import data_models
import glob
import json
import os
import sys


class Method:
    def __init__(self, route_line):
        self.description = ""  # will come later when parsing first big comment
        self.url = self.ParseUrl(route_line)
        self.methods = self.ParseMethods(route_line)  # POST, GET, ...

    def pushDescription(self, l):
        self.description += ("\n" if self.description else "") + l.strip('"""')

    @staticmethod
    def ParseUrl(l):
        # l = @app.route('/api/v1/login', methods=['POST'])
        a = l.find('(')
        b = l.find(',')
        return l[a+2:b-1] 
    
    @staticmethod
    def ParseMethods(l):
        """l = @app.route('/api/v1/login', methods=['POST'])
        or l = @app.route('/api/v1/login')"""
        a = l.find('methods=')
        if a < 0:
            return []
        l = l[a:]
        a = l.find('[')
        b = l.find(']')
        l = l[a+1:b]
        s = l.split(',')
        return [x.strip(' ').strip("'").strip('"').strip(' ') for x in s]


def parseHandler(filename):
    is_parsing = False
    is_comment_on = False
    methods = []
    indent = 0
    f = open(filename, 'rb')
    for l in f.readlines():
        l = l.strip('\r\n')
        if l.startswith('@app.route'):
            method = Method(l)
            is_parsing = True
        if not is_parsing:
            continue
        if '"""' in l:
            if not is_comment_on:
                is_comment_on = True
                indent = l.find('"""')
            else:
                is_comment_on = False
        if is_comment_on:
            if l.startswith(' ' * indent):
                l = l[indent:]
            method.pushDescription(l)
        # check for last comment or a 1 line description.
        a = l.find('"""')
        b = -1
        if a >= 0: b = l.find('"""', a+3)
        if '"""' in l and not is_comment_on or b > 0:
            is_parsing = False
            is_comment_on = False
            methods.append(method)
    return methods


@app.route('/api')
def page_api():
    """Lists all apis in the project."""
    pwd = os.path.dirname(__file__)
    server_handlers = glob.glob("%s/*_handler.py" % pwd)
    handler_methods = []
    apis = []  # [(file_name, [Method])]
    for handler in server_handlers:
        methods = parseHandler(handler)
        apis.append((handler[len(pwd)+1:], methods))
    return render_template('api.html', apis=apis)
from datetime import date, datetime, timedelta
from flask import current_app
from flask import make_response
from flask import request
from functools import update_wrapper
from multiprocessing import Process
from serveur import app
from serveur import Constants
from serveur.db import all_pb2 as all_pbs
from werkzeug.routing import BaseConverter
import os
import random
import smtplib
import time


class RegexConverter(BaseConverter):
    """Used to define regexes in app routing."""
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


def getTimestampSecs():
    return int(time.time())


def getFilenameExtension(filename):
    return filename.split(".")[-1]


def getFileSize(ffile):
    ffile.seek(0, os.SEEK_END)
    size = ffile.tell()
    ffile.seek(0, os.SEEK_SET)
    return size


def ImageUrlToFile(image_url):
    """images are stored as ad-213213.png in the db. We get them from the website as
    /static/upload-debug/ad-213213.png so we trim them.
    Returns True, filepath"""
    BAD_RETURN = False, ''
    prefix = request.url_root + "static/%s/" % app.config[Constants.KEY_UPLOAD_DIR]
    if not image_url.startswith(prefix):
        return BAD_RETURN
    a = image_url.split('/')
    if not a or (image_url != prefix + a[-1]):
        return BAD_RETURN
    return True, a[-1]


def FileToImageUrl(image_file):
    return request.url_root + "static/%s/%s" % (app.config[Constants.KEY_UPLOAD_DIR], image_file)


def SendMail(email_from, to, obj, body):
    def send_mail(email_from, to, obj, body):
        # TODO: implement your own email depending on your server
        print email_from, to, obj, body
    Process(target=send_mail, args=(email_from, to, obj, body)).start()
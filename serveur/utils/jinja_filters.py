"""Custom filters for jinja templates"""

from datetime import timedelta
from jinja2 import evalcontextfilter, Markup, escape
import re

_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')

def nl2br(value):
    return value.replace('\n','<br/>\n')


def time_period(time_delta):
    """Display a time interval nicely: 2 min, 3h, 1.3 jours, ... depending on its order of magnitude"""
    if time_delta < timedelta(minutes=1):
        return "%d s" % int(time_delta.total_seconds())
    elif time_delta < timedelta(hours=1):
        return "%d min" % int(time_delta.total_seconds() / 60)
    elif time_delta < timedelta(days=1):
        return "%d h" % int(time_delta.total_seconds() / 3600)
    else:
        return "%.1f jours" % (time_delta.total_seconds() / (3600 * 24))


def setupFilters(app):
    # Executed before server is running
    app.jinja_env.filters['time_period'] = time_period
    app.jinja_env.filters['nl2br'] = nl2br

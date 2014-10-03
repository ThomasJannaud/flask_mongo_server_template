"""Custom filters for jinja templates"""

from datetime import timedelta


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


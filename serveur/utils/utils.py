from werkzeug.routing import BaseConverter

class RegexConverter(BaseConverter):
    """Used to define regexes in app routing."""
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

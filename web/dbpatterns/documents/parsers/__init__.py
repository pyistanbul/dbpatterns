class BaseParser(object):
    parsed = None

    def __init__(self, text):
        self.text = text

    def is_valid(self):
        try:
            self.parsed = list(self.parse(self.text))
        except ParseError as e:
            return False
        return True

    def parse(self, text):
        raise NotImplementedError


class ParseError(StandardError):
    pass
from documents.parsers import BaseParser

class DummyParser(BaseParser):

    def parse(self, text):
        return text
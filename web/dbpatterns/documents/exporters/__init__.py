class BaseExporter(object):
    """
    The base class of all exporters.
    """

    def __init__(self, document):
        self.document = document

    def export(self):
        raise NotImplementedError

    def as_text(self):
        return "\n".join(list(self.export()))


class ExporterError(Exception):
    pass
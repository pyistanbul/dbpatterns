from documents.constants import TYPES_BOOLEAN, TYPES_INTEGER, TYPES_TEXT
from documents.exporters import BaseExporter

class SqlExporter(BaseExporter):

    TYPE_MAPPING = {
        TYPES_INTEGER: "integer",
        TYPES_BOOLEAN: "bool",
        TYPES_TEXT: "text"
    }

    DEFAULT_TYPE = "varchar(255)"

    def export(self):
        yield 'BEGIN;'
        for entity in self.document.entities:
            yield 'CREATE TABLE "%s" ('
            yield ','.join(self.get_attributes(entity.get("attributes", [])))
            yield ');'
        yield 'COMMIT;'

    def get_attributes(self, attributes):
        for attribute in attributes:
            yield '"%s" %s %s %s' % (
                attribute.get("name"),
                self.get_attribute_type(attribute.get("type")),
                "NOT NULL",
                "PRIMARY KEY" if attribute.get("is_primary_key") else "")

    def get_attribute_type(self, attribute_type):
        return self.TYPE_MAPPING.get(attribute_type, self.DEFAULT_TYPE)
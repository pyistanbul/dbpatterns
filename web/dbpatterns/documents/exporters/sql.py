from documents.constants import *
from documents.exporters import BaseExporter


class SQLExporter(BaseExporter):
    """
    A base class of all sql exporters.
    """
    TYPE_MAPPING = {
        TYPES_INTEGER: "int",
        TYPES_BOOLEAN: "bool",
        TYPES_TEXT: "longtext",
        TYPES_TIME: "time",
        TYPES_DATETIME: "datetime",
        TYPES_DATE: "date",
    }
    DEFAULT_TYPE = "varchar"
    COMMA_LITERAL = ","
    QUOTATION_LITERAL = '"'
    WHITE_SPACE = "\t"
    DEFAULT_VARCHAR_SIZE = 255

    INLINE_FOREIGN_KEYS = True

    def quote(self, text):
        return self.QUOTATION_LITERAL + text + self.QUOTATION_LITERAL

    def export(self):

        for entity in self.document.get("entities") or []:

            yield 'CREATE TABLE %s (' % self.quote(entity.get("name"))
            if entity.get("attributes"):
                yield self.WHITE_SPACE + ('%(comma_literal)s\n%(tab)s' % {
                    "comma_literal": self.COMMA_LITERAL,
                    "tab": self.WHITE_SPACE
                }).join(list(self.build_columns(entity.get("attributes"))))

            yield ');'

    def build_columns(self, attributes):
        for attribute in attributes:
            yield " ".join(list(
                self.column_for_attribute(attribute)))

        if not self.INLINE_FOREIGN_KEYS:
            for attribute in attributes:
                if attribute.get("is_foreign_key"):
                    yield " ".join(list(
                        self.foreign_key_for_attribute(attribute)))

    def column_for_attribute(self, attribute):

        yield self.quote(attribute.get("name"))

        size = attribute.get("size") or self.DEFAULT_VARCHAR_SIZE if \
            attribute.get("type") == TYPES_STRING else None
        column_type = self.TYPE_MAPPING.get(attribute.get("type"),
                                            self.DEFAULT_TYPE)

        yield "%s(%s)" % (column_type, size) if size else column_type

        if attribute.get("is_primary_key"):
            yield "PRIMARY KEY"

        if attribute.get("is_not_null"):
            yield "NOT NULL"

        if attribute.get("is_unique"):
            yield "UNIQUE"

        if self.INLINE_FOREIGN_KEYS and attribute.get("is_foreign_key"):
            for line in self.foreign_key_for_attribute(attribute):
                yield line

    def foreign_key_for_attribute(self, attribute):
        yield "FOREIGN KEY(%s)" % self.quote(attribute.get("name", ""))
        yield "REFERENCES"
        yield "%s (%s)" % (self.quote(attribute.get("foreign_key_entity", "")),
                           self.quote(
                               attribute.get("foreign_key_attribute", "")))


class SQLiteExporter(SQLExporter):
    pass


class MysqlExporter(SQLExporter):
    INLINE_FOREIGN_KEYS = False
    QUOTATION_LITERAL = "`"


class PostgresExporter(SQLExporter):
    INLINE_FOREIGN_KEYS = False


class OracleExporter(SQLExporter):
    def foreign_key_for_attribute(self, attribute):
        yield "CONSTRAINT %s_%s" % (attribute.get("foreign_key_entity", ""),
                                    attribute.get("foreign_key_attribute", ""))
        yield "REFERENCES"
        yield "%s(%s)" % (attribute.get("foreign_key_entity", ""),
                          attribute.get("foreign_key_attribute", ""))
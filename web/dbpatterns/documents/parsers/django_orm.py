import ast
from _ast import Call, Attribute, Name

from documents.constants import *
from documents.parsers import BaseParser, ParseError

MODEL_BASE_CLASS = "Model"

MANY_TO_MANY_FIELD = "many-to-many"
FOREIGN_KEY_FIELD = "foreign-key"

FIELD_TYPE_MAP = {
    "PositiveIntegerField": TYPES_INTEGER,
    "IntegerField": TYPES_INTEGER,
    "CharField": TYPES_STRING,
    "EmailField": TYPES_STRING,
    "BooleanField": TYPES_BOOLEAN,
    "DateTimeField": TYPES_DATETIME,
    "DateField": TYPES_DATE,
    "TimeField": TYPES_TIME,
    "FileField": TYPES_STRING,
    "ForeignKey": FOREIGN_KEY_FIELD,
    "ManyToManyField": MANY_TO_MANY_FIELD,
    "OneToOneField": FOREIGN_KEY_FIELD
}

DEFAULT_FIELD_TYPE = "string"


class FieldVisitor(ast.NodeVisitor):
    """
    A visitor that inspects model fields.
    """
    def __init__(self):
        self.fields = []

    def add_field(self, field_name, field_type, relationship):
        field = {
            "name": field_name,
            "type": field_type
        }
        if relationship is not None:
            field["relationship"] = relationship
        self.fields.append(field)

    def visit_Assign(self, node):
        field_name = None
        field_type = None
        relationship = None

        if not isinstance(node.value, Call):
            return

        try:
            field_name = node.targets[0].id
        except AttributeError:
            return

        if isinstance(node.value.func, Attribute):
            field_type = FIELD_TYPE_MAP.get(node.value.func.attr,
                DEFAULT_FIELD_TYPE)

            if field_type in [MANY_TO_MANY_FIELD, FOREIGN_KEY_FIELD]:
                relationship = node.value.args[0].id

        if field_type is not None:
            self.add_field(field_name, field_type, relationship=relationship)



class ModelVisitor(ast.NodeVisitor):
    """
    A visitor that detects django models.
    """
    def __init__(self):
        self.models = {}

    def visit_ClassDef(self, node):
        base_class = None
        for base in node.bases:
            if isinstance(base, Attribute):
                base_class = base.attr
            if isinstance(base, Name):
                base_class = base.id

        if base_class == MODEL_BASE_CLASS:
            visitor = FieldVisitor()
            visitor.visit(node)
            self.models[node.name] = visitor.fields


class DjangoORMParser(BaseParser):

    def parse(self, text):

        try:
            node = ast.parse(text)
        except SyntaxError:
            raise ParseError
        else:
            visitor = ModelVisitor()
            visitor.visit(node)
            return self.normalize_models(visitor.models)

    def normalize_models(self, models):
        """
        The normalization process for django models.

            - Adds `id` field
            - Separates many-to-many fields
            - Converts foreign-key-fields to integer

        """
        position_top = 0
        position_left = 0

        for model, fields in models.items():
            attributes = [{
                "name": "id",
                "type": TYPES_INTEGER,
                "is_primary_key": True
            }]
            for field in fields:

                if field.get("type") == MANY_TO_MANY_FIELD:

                    position_left += ENTITY_POSITION_LEFT_INCREASE
                    position_top += ENTITY_POSITION_TOP_INCREASE

                    yield self.m2m_to_entity(model, field, position_top, position_left)

                    continue # skip the field addition

                elif field.get("type") == FOREIGN_KEY_FIELD:

                    field["name"] += "_id"
                    field["type"] = TYPES_INTEGER

                attributes.append(field)

            position_left += ENTITY_POSITION_LEFT_INCREASE
            position_top += ENTITY_POSITION_TOP_INCREASE

            yield {
                "name": model.lower(),
                "attributes": attributes,
                "position": {
                    "top": position_top,
                    "left": position_left
                }
            }

    def m2m_to_entity(self, model, field, position_top, position_left):
        """
        Returns an entity that consist of provided m2m field.
        """
        return {
            "name": model.lower() + "_" + field.get("name"),
            "position": {
                "top": position_top,
                "left": position_left
            },
            "attributes": [
                {
                    "name": "id",
                    "type": TYPES_INTEGER,
                    },
                {
                    "name": model.lower() + "_id",
                    "type": TYPES_INTEGER,
                    "is_foreign_key": True,
                    "foreign_key_entity": model.lower(),
                    "foreign_key_attribute": "id"
                },
                {
                    "name": field.get("relationship").lower() + "_id",
                    "type": TYPES_INTEGER,
                    "is_foreign_key": True,
                    "foreign_key_entity": field.get("relationship").lower(),
                    "foreign_key_attribute": "id"
                }
            ]
        }
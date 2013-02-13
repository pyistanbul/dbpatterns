ENTITY_POSITION_TOP_INCREASE = 100
ENTITY_POSITION_LEFT_INCREASE = 300

TYPES_INTEGER = "integer"
TYPES_STRING = "string"
TYPES_BOOLEAN = "boolean"
TYPES_DATETIME = "datetime"
TYPES_DATE = "date"
TYPES_TIME = "time"
TYPES_CURRENCY = "currency"
TYPES_TEXT = "text"

FIELD_TYPES = (
    (TYPES_INTEGER, "integer"),
    (TYPES_STRING, "string"),
    (TYPES_TEXT, "text"),
    (TYPES_BOOLEAN, "boolean"),
    (TYPES_DATETIME, "datetime"),
    (TYPES_DATE, "date"),
    (TYPES_TIME, "time"),
    (TYPES_CURRENCY, "currency"),
)

EXPORTER_MYSQL = "mysql"
EXPORTER_POSTGRES = "postgres"
EXPORTER_ORACLE = "oracle"
EXPORTER_SQLITE = "sqlite"

EXPORTERS = (
    (EXPORTER_MYSQL, "MySQL"),
    (EXPORTER_POSTGRES, "Postgres"),
    (EXPORTER_ORACLE, "Oracle"),
    (EXPORTER_SQLITE, "SQLite"),
)

CAN_EDIT = "can_edit"
CAN_VIEW = "can_view"
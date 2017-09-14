dbpatterns.models.Attribute = Backbone.Model.extend({

    FOREIGN_KEY_SEPARATOR: "_",
    DEFAULT_TYPES: [
        {'field': 'is_', 'value': 'boolean', 'function': 'startsWith'},
        {'field': 'date', 'value': 'datetime', 'function': 'startsWith'},
        {'field': 'date', 'value': 'datetime', 'function': 'endsWith'},
        {'field': 'id', 'value': 'integer', 'function': 'endsWith'},
        {'field': '_at', 'value': 'datetime', 'function': 'endsWith'}
    ],

    defaults: {
        "order": 0
    },
    initialize: function () {
        this.detect_foreign_key();
        this.fill_defaults();
        this.on("fk_does_not_exist", this.invoke_foreign_key, this);
        this.on("change:name", this.detect_foreign_key, this);
    },
    save: function () {
        this.collection.trigger("persist");
    },
    detect_foreign_key: function () {
        var tokens = this.get("name").split(this.FOREIGN_KEY_SEPARATOR);
        if (tokens.length > 1 && this.get("is_foreign_key") === undefined) {
            var entity_name = tokens.slice(0, -1).join(this.FOREIGN_KEY_SEPARATOR);
            var attribute_name = tokens.slice(-1)[0];
            this.set({
                "is_foreign_key": true,
                "foreign_key_entity": entity_name,
                "foreign_key_attribute": attribute_name
            }).on("render", this.trigger.bind(this, "connect"));
        }
    },
    invoke_foreign_key: function () {
        this.set({
            "is_foreign_key": false,
            "foreign_key_entity": "",
            "foreign_key_attribute": ""
        });
    },
    fill_defaults: function () {
        if (!this.get("type")) {
            this.set("type", this.get_default_type(this.get("name")))
        }
    },
    get_default_type: function (name) {
        var value = _(name.toLowerCase());
        var detected_type = 'string';
        _.forEach(this.DEFAULT_TYPES, function(field) {
            if (value[field.function](field.field)) {
                detected_type = field.value;
                return;
            }
        });
        return detected_type;
    }
});

dbpatterns.collections.Attribute = Backbone.Collection.extend({
    model: dbpatterns.models.Attribute,
    comparator: function (attribute) {
        return attribute.get("order");
    }
});

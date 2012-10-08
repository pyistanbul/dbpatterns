dbpatterns.models.Attribute = Backbone.Model.extend({

    FOREIGN_KEY_SEPARATOR: "_",

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
        if (value.startsWith("is_")) return "boolean";
        if (value.startsWith("date") || value.endsWith("date")) return "datetime";
        if (value.endsWith("id")) return "integer";
        return "string"
    }
});

dbpatterns.collections.Attribute = Backbone.Collection.extend({
    model: dbpatterns.models.Attribute,
    comparator: function (attribute) {
        return attribute.get("order");
    }
});

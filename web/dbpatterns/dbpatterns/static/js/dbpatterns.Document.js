/*
* Document class
* */
dbpatterns.Document = $.Class.extend({

    options: {
        "document_container": "body",
        "new_entity_anchor": ".new-entity"
    },

    init: function (_options) {
        $.extend(this.options, _options);
        $(this.options.new_entity_anchor).click(this.new_entity.bind(this));
    },

    add_entity: function (entity) {
        $(this.options.document_container).append(entity.render().el)
    },

    new_entity: function () {
        var entity_name = window.prompt("Entity name");
        var en = new dbpatterns.Entity({
            "name": entity_name,
            "attributes": [],
            "position": {
                "left": "20%",
                "top": "30%"
            }
        });
        this.add_entity(en);
    }

});
dbpatterns.views.Document = Backbone.View.extend({

    el: "article#document",

    events: {
//        "click": "new_entity"
    },

    initialize: function () {
        this.model.bind("change:title", this.render_title.bind(this));
        this.options.entity_collection.bind("add", this.add_entity.bind(this));
        this.render_entities(this.options.entity_collection.models);
    },

    render_entities: function (entities) {
        _.each(entities, this.add_entity.bind(this))
    },

    add_entity: function (entity) {
        var entity_view = new dbpatterns.views.Entity({
            model: entity
        });
        this.$el.append(entity_view.render().el)
    },

    render_title: function () {
        this.$el.find("header h1").html(this.model.get("title"));
        return this;
    }

});
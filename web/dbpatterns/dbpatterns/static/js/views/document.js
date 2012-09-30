dbpatterns.views.Document = Backbone.View.extend({

    el: "article#document",

    events: {
        "click .new-entity": "new_entity",
        "click .edit-title": "edit_title"
    },

    initialize: function () {
        this.model.bind("change:title", this.render_title, this);
        this.model.entities.bind("reset", this.render_entities, this);
        this.model.entities.bind("add", this.add_entity, this);
    },

    render_entities: function (entities) {
        _.forEach(entities.models, this.add_entity, this)
    },

    add_entity: function (entity) {
        var entity_view = new dbpatterns.views.Entity({
            model: entity
        });
        this.$el.append(entity_view.render().el)
    },

    new_entity: function () {
        var entity_name = window.prompt("Entity name");

        if (!entity_name) {
            return;
        }

        var entity = new dbpatterns.models.Entity({
            name: entity_name,
            position: {
                left: "30%",
                top: "40%"
            }
        });
        this.model.entities.add(entity);
    },

    render_title: function () {
        this.$el.find("header h1").html(this.model.get("title"));
        return this;
    },

    edit_title: function () {

        var title = window.prompt("Title", this.model.get("title"));

        if (!title) {
            return false;
        }

        this.model.set("title", title);
        this.model.save();
        return this;
    }

});
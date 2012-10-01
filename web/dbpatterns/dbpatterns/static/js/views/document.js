dbpatterns.views.Document = Backbone.View.extend({

    DEFAULT_ENTITY_POSITION: {
        "top": 20,
        "left": 300
    },

    el: "article#document",

    events: {
        "click .new-entity": "new_entity",
        "click .edit-title": "edit_title",
        "click .save-document": "save_document"
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
        this.$el.find("#entities").append(entity_view.render().el);
        this.$el.find("#entities").height($(window).height() - $("header[role='banner']").height());
    },

    new_entity: function () {
        var entity_name = window.prompt("Entity name");

        if (!entity_name) {
            return;
        }

        var entity = new dbpatterns.models.Entity({
            name: entity_name,
            position: this.DEFAULT_ENTITY_POSITION
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
    },

    save_document: function () {
        this.model.save();
    }

});
dbpatterns.views.Entity = Backbone.View.extend({

    tagName: "div",
    className: "entity",
    template: $("#entity-template").html(),

    events: {
        "click .destroy": "destroy",
        "dblclick h3": "rename"
    },

    initialize: function () {
        this.model.on("change:name", this.render_name, this);
    },

    render: function () {
        this.$el.html(_.template(this.template, this.model.toJSON()));

        this.$el.css({
            "top": this.model.get("position").top,
            "left": this.model.get("position").left
        });

        this.$el.draggable({
            containment: "#entities",
            "handle": "h3",
            "stop": this.on_drag.bind(this)
        }).sortable({
            // TODO: implement!
        });

        this.$el.find(".attributes").html(new dbpatterns.views.Attributes({
            model: this.model.entity_attributes
        }).render().el);

        return this;
    },

    on_drag: function (event, ui) {
        console.log(arguments)
        this.model.set({
            "position": {
                "top": ui.position.top,
                "left": ui.position.left
            }
        });
        this.model.save();
    },

    destroy: function () {
        this.model.destroy();
        this.$el.fadeOut("fast", function () {
            $(this).remove();
        })
    },

    render_name: function () {
        this.$el.find("h3").html(this.model.get("name"));
    },

    rename: function () {
        var name = window.prompt("Entity name", this.model.get("name"));
        this.model.set({
            "name": name
        });
        this.model.save();
    }


});


dbpatterns.views.Entities = Backbone.View.extend({


    el: "article#document",

    events: {
        "click .new-entity": "new_entity"
    },

    DEFAULT_ENTITY_POSITION: {
        "top": 20,
        "left": 300
    },

    initialize: function () {
        this.model.bind("reset", this.render_entities, this);
        this.model.bind("add", this.add_entity, this);
    },

    render_entities: function (entities) {
        _.forEach(entities.models, this.add_entity, this);
        this.$el.find("#entities").height($(window).height() - $("header[role='banner']").height());
    },

    add_entity: function (entity) {
        var entity_view = new dbpatterns.views.Entity({
            model: entity
        });
        this.$el.find("#entities").append(entity_view.render().el);
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
        this.model.add(entity);
    }


});
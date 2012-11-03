dbpatterns.views.Entity = Backbone.View.extend({

    tagName: "div",
    className: "entity",
    template: $("#entity-template").html(),

    events: {
        "click .remove-entity": "destroy",
        "dblclick h3": "rename"
    },

    initialize: function () {
        this.model.on("change:name", this.render_name, this);
        this.model.on("destroy", this.detach, this);
    },

    render: function () {
        this.$el.html(_.template(this.template, this.model.toJSON()));

        this.$el.css({
            "top": this.model.get("position").top,
            "left": this.model.get("position").left
        });

        jsPlumb.draggable($(this.el), {
            "handle": "h3",
            "stop": this.on_drag.bind(this)
        });

        (new dbpatterns.views.ConnectorEndpoint({
            "el": this.$el
        })).render();

        this.$el.find(".attributes").html(new dbpatterns.views.Attributes({
            model: this.model.entity_attributes,
            app_view: this.options.app_view
        }).render().el);
        this.render_name();

        return this;
    },

    detach: function () {
        this.remove_reverse_relationships();
        this.remove();
        return this;
    },

    remove_reverse_relationships: function () {
        // checks reverse relationships for jsPlump
        _.each(jsPlumb.getConnections(), function (connection) {
            var source = connection.source,
                target = connection.target;
            if (target.is(this.$el)) {
                jsPlumb.removeAllEndpoints(target);
            }
        }.bind(this));
    },

    on_drag: function (event, ui) {
        this.model.set({
            "position": {
                "top": ui.position.top,
                "left": ui.position.left
            }
        });
        this.model.save();
    },

    destroy: function () {
        this.model.entity_attributes.trigger("detach");
        this.model.destroy();
    },

    render_name: function () {
        this.$el.find("h3").html(this.model.escape("name"));
        this.$el.attr("data-entity", this.model.escape("name"));
    },

    rename: function () {
        var name = window.prompt("Entity name", this.model.get("name"));
        this.model.set({
            "name": name
        });
        this.model.save();
    },

    focus: function () {
        this.$el.find(".new-attribute").focus();
        return this;
    }

});


dbpatterns.views.Entities = Backbone.View.extend({

    POSITION_TOP_INCREASE: 50,
    POSITION_LEFT_INCREASE: 50,

    el: "article#document",

    events: {
        "click .new-entity": "new_entity"
    },


    shortcuts: {
        "option+n": "new_entity"
    },

    initialize: function () {
        _.extend(this, new Backbone.Shortcuts);
        this.delegateShortcuts();
        this.model.bind("reset", this.render_entities, this);
        this.model.bind("add", this.add_entity, this);
    },

    render_entities: function (entities) {
        _.forEach(entities.models, this.add_entity, this);
        this.options.app_view.trigger("load");
    },

    add_entity: function (entity) {
        var entity_view = new dbpatterns.views.Entity({
            model: entity,
            app_view: this.options.app_view
        });
        this.$el.find("#entities").append(entity_view.render().el);
        entity_view.focus();
    },

    new_entity: function () {
        var entity_name = window.prompt("Entity name");

        if (!entity_name) {
            return;
        }

        var entity = new dbpatterns.models.Entity({
            name: entity_name,
            position: this.get_entity_position()
        });
        this.model.add(entity);
    },

    get_entity_position: function () {
        var previous = dbpatterns.views.Entities.prototype._previous_position;
        var position = {
            "top": previous.top + this.POSITION_TOP_INCREASE,
            "left": previous.left + this.POSITION_LEFT_INCREASE
        };
        dbpatterns.views.Entities.prototype._previous_position = position;
        return position;
    },

    _previous_position: {
        "top": 0,
        "left": 0
    }

});
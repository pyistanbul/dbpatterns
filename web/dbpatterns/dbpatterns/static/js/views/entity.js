dbpatterns.views.Entity = Backbone.View.extend({

    tagName: "div",
    className: "entity",
    template: $("#entity-template").html(),

    events: {
        "click .new-attribute": "new_attribute",
        "click .destroy": "destroy",
        "dblclick h3": "rename"
    },

    initialize: function () {
        this.model.entity_attributes.bind("add", this.add_attribute, this);
        this.model.on("change:name", this.render_name, this)
    },

    render_attributes: function (attributes) {
        _.forEach(attributes, this.add_attribute, this);
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
        });

        this.render_attributes(this.model.entity_attributes.models);

        return this;
    },

    add_attribute: function (attribute) {

        this.$el.find("ul").append(new dbpatterns.views.Attribute({
            model: attribute
        }).render().el);

    },

    new_attribute: function () {
        var attribute_name = window.prompt("Attribute name");
        var attribute = new dbpatterns.models.Attribute({
            "name": attribute_name,
            "type": "string"
        });
        this.model.entity_attributes.add(attribute);
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
        })
        this.model.save();
    }


});
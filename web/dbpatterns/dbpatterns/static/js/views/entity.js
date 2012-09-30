dbpatterns.views.Entity = Backbone.View.extend({

    tagName: "div",
    className: "entity",
    template: $("#entity-template").html(),

    events: {
        "click .new-attribute": "new_attribute"
    },

    initialize: function () {
        this.model.entity_attributes.bind("add", this.add_attribute, this);
    },

    render_attributes: function (attributes) {
        _.forEach(attributes, this.add_attribute, this);
    },

    render: function () {
        this.$el.html(_.template(this.template, this.model.toJSON()));

        this.$el.draggable();

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
    }




});
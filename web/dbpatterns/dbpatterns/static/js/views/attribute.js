dbpatterns.views.Attributes = Backbone.View.extend({

    template: $("#attribute-list-template").html(),

    events: {
        "click .new-attribute": "new_attribute"
    },

    initialize: function () {
        this.model.bind("add", this.add_attribute, this);
    },

    render_attributes: function (attributes) {
        _.forEach(attributes, this.add_attribute, this);
    },

    add_attribute: function (attribute) {

        this.$el.find("ul").append(new dbpatterns.views.Attribute({
            model: attribute
        }).render().el);

        console.log(this.$el)

    },

    render: function () {
        this.$el.html(_.template(this.template))
        this.render_attributes(this.model.models);
        return this;
    },

    new_attribute: function () {
        var attribute_name = window.prompt("Attribute name");
        var attribute = new dbpatterns.models.Attribute({
            "name": attribute_name,
            "type": "string"
        });
        this.model.add(attribute);
    }

});

dbpatterns.views.Attribute = Backbone.View.extend({

    tagName: "li",

    template: $("#attribute-template").html(),

    render: function () {
        this.$el.html(_.template(this.template, this.model.toJSON()));
        return this;
    }
});
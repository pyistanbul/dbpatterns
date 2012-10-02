dbpatterns.views.Attribute = Backbone.View.extend({

    tagName: "li",

    template: $("#attribute-template").html(),

    events: {
        "click a": "show_attribute_form"
    },

    show_attribute_form: function () {
        console.log(this.model)
    },

    render: function () {
        this.$el.html(_.template(this.template, this.model.toJSON()));
        return this;
    }
});

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
    },

    render: function () {
        this.$el.html(_.template(this.template));
        this.render_attributes(this.model.models);
        return this;
    },

    new_attribute: function () {
        var button = this.$el.find(".new-attribute");
        var view = new dbpatterns.views.EditInPlaceForm();
        button.before(view.render().el);
        view.success(function (name) {
            this.model.add(new dbpatterns.models.Attribute({
                "name": name
            }));
           button.focus();
        }.bind(this));
        view.focus();
    }

});

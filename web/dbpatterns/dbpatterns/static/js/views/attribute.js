dbpatterns.views.Attribute = Backbone.View.extend({

    tagName: "li",

    template: $("#attribute-template").html(),
    form_template: $("#attribute-form-template").html(),

    events: {
        "click a": "show_attribute_form",
        "dblclick a": "destroy"
    },

    types: ["string", "integer", "boolean", "currency", "date", "time", "datetime"],

    show_attribute_form: function () {
        var dialog = (new dbpatterns.views.FormDialog({
            "form": _.template(this.form_template, this),
            "title": "Attribute",
            "model": this.model
        })).success(function () {
            return true;
        }).render();
        return this;
    },

    render: function () {
        this.$el.html(_.template(this.template, this.model.toJSON()));
        return this;
    },

    destroy: function () {
        this.model.destroy();
        this.$el.remove();
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
        this.get_sortable_content().sortable({
            "axis": "y",
            "containment": this.get_sortable_content(),
            "opacity": 0.6
        });
        return this;
    },

    get_sortable_content: function () {
        return this.$el.find("ul");
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

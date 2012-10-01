dbpatterns.views.Attribute = Backbone.View.extend({

    tagName: "li",

    template: $("#attribute-template").html(),

    render: function () {
        this.$el.html(_.template(this.template, this.model.toJSON()));
        return this;
    }
});
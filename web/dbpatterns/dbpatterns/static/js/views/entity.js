dbpatterns.views.Entity = Backbone.View.extend({

    tagName: "div",
    className: "entity",
    template: $("#entity-template").html(),

    render: function () {
        this.$el.html(_.template(this.template, this.model.toJSON()));

        this.$el.draggable();

        return this;
    }


});
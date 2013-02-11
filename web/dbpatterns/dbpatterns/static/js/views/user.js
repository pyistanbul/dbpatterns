dbpatterns.views.AssigneesView = Backbone.View.extend({
    field: "#assignees",
    template: $("#assignees-template").html(),
    render: function () {
        $(this.el).html(_.template(this.template, {}));
        var replaced_field = $(this.field).hide(),
            user_input = $(this.el).find("#user");

        user_input.autocomplete({
            source: "/api/users/"
        });

        replaced_field.after(this.el)
    }
});

dbpatterns.views.AssigneeItemView = Backbone.View.extend({
    tagName: "li",
    template: $("#assignee-item-template").html(),
    render: function () {
        $(this.el).html(_.template(this.template, this.model.toJSON()));
        return this;
    }
});

dbpatterns.views.AssigneesView = Backbone.View.extend({
    field: "#assignees",
    template: $("#assignees-template").html(),

    initialize: function () {
        this.model.on("add", this.add_assignee, this);
    },

    add_assignee: function (assignee) {
        var users = $(this.el).find(".users");
        users.append((new dbpatterns.views.AssigneeItemView({
            model: assignee
        })).render().el)
    },

    render: function () {
        $(this.el).html(_.template(this.template, {}));
        var replaced_field = $(this.field).hide(),
            user_input = $(this.el).find("#user");

        _.forEach(this.model.models, function (assignee) {
            this.add_assignee(assignee);
        }, this);

        user_input.autocomplete({
            source: "/api/users/",
            select: function (event, ui) {
                var assignee = new dbpatterns.models.Assignee({
                    "id": ui.item.id,
                    "username": ui.item.label,
                    "avatar": ui.item.avatar
                });
                this.model.add(assignee);
                user_input.val("");
                return false;
            }.bind(this)
        });

        replaced_field.after(this.el)
    }
});

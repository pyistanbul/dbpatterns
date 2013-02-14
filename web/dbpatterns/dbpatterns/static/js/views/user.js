dbpatterns.views.AssigneeItemView = Backbone.View.extend({
    tagName: "li",
    template: $("#assignee-item-template").html(),
    events: {
        "click .remove": "destroy"
    },
    render: function () {
        $(this.el).html(_.template(this.template, this.model.toJSON()));
        this.$el
            .find(".permission")
            .val(this.model.get("permission"))
            .change(function (event) {
                this.model.set("permission", $(event.target).val())
            }.bind(this));
        return this;
    },
    destroy: function () {
        this.model.destroy();
    }
});

dbpatterns.views.AssigneesView = Backbone.View.extend({
    field: "#assignees",
    template: $("#assignees-template").html(),

    initialize: function () {
        this.model.on("add", this.add_assignee, this);
        this.model.on("remove", this.render_assignees, this);
    },

    add_assignee: function (assignee) {
        var users = $(this.el).find(".users");
        users.append((new dbpatterns.views.AssigneeItemView({
            model: assignee
        })).render().el)
    },

    render_assignees: function () {
        $(this.el).find(".users").empty();
        _.forEach(this.model.models, function (assignee) {
            this.add_assignee(assignee);
        }, this);
    },

    render: function () {
        $(this.el).html(_.template(this.template, {}));
        var replaced_field = $(this.field).hide(),
            user_input = $(this.el).find("#user");

        this.render_assignees();

        user_input.autocomplete({
            source: function(request, response) {
                var excludes = this.model.pluck("id").join(",");
                $.get("/api/users/", {
                    term: request.term,
                    excludes: excludes
                }, function(data) {
                    response(data);
                });
            }.bind(this),
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

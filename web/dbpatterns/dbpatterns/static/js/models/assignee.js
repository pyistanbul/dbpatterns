dbpatterns.models.Assignee = Backbone.Model.extend({
    defaults: {
        "permission": "can_edit"
    }
});

dbpatterns.collections.Assignees = Backbone.Collection.extend({
    model: dbpatterns.models.Assignee
});

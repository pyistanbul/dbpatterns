dbpatterns.models.Comment = Backbone.Model.extend({
    defaults: {
        has_delete_permission: false
    }
});

dbpatterns.collections.Comments = Backbone.Collection.extend({
    model: dbpatterns.models.Comment,
    initialize: function (options) {
        this.document = options.document;
    },
    url: function() {
        return this.document.get("comments_uri");
    }
});
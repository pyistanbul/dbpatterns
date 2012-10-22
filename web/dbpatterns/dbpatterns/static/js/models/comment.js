dbpatterns.models.Comment = Backbone.Model.extend({

    urlRoot: "/api/comments"


});

dbpatterns.collections.Comments = Backbone.Collection.extend({
    model: dbpatterns.models.Comment,
    initialize: function (options) {
        this.document = options.document;
    },
    url: function() {
        return this.document.get("resource_uri") + 'comments';
    }
});
dbpatterns.models.Attribute = Backbone.Model.extend({
    defaults: {
        "type": "string"
    },
    destroy: function () {
        this.collection.remove(this);
    },
    save: function () {
        this.collection.trigger("persist");
    }
});

dbpatterns.collections.Attribute = Backbone.Collection.extend({
    model: dbpatterns.models.Attribute
});

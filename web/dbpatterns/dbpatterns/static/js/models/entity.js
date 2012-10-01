dbpatterns.models.Entity = Backbone.Model.extend({

    defaults: {
        "attributes": []
    },

    initialize: function () {
        this.entity_attributes = new dbpatterns.collections.Attribute();
        this.entity_attributes.reset(this.get("attributes"));
        this.entity_attributes.on("add persist", this.persist, this);

    },

    persist: function () {
        this.set({
            "attributes": this.entity_attributes.toJSON()
        });

        this.collection && this.collection.trigger("persist");
    },

    save: function () {
        this.trigger("persist")
    },

    destroy: function () {
        this.collection.remove(this);

    }


});

dbpatterns.collections.Entity = Backbone.Collection.extend({
    model: dbpatterns.models.Entity
});

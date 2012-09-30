dbpatterns.models.Entity = Backbone.Model.extend({

    defaults: function () {
        return {
            "attributes": []
        }
    },

    initialize: function () {
        this.entity_attributes = new dbpatterns.collections.Entity();
        this.entity_attributes.reset(this.get("attributes"))
        this.entity_attributes.on("add", this.persist, this);
    },

    persist: function () {
        this.set({
            "attributes": this.entity_attributes.toJSON()
        })
    }
});

dbpatterns.collections.Entity = Backbone.Collection.extend({
    model: dbpatterns.models.Entity
});

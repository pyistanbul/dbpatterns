dbpatterns.models.Document = Backbone.Model.extend({

    urlRoot: "/api/documents",

    initialize: function (model, options) {
        this.entities = new dbpatterns.collections.Entity;
        this.socket = io.connect(options.socket_uri);
    },

    parse: function (result) {
        if (!result) { return result; }
        this.entities.reset(result.entities);
        this.entities.bind("add remove persist", this.persist.bind(this));
        return result;
    },

    persist: function () {
        this.set({"entities": this.entities.toJSON()});
    }

});
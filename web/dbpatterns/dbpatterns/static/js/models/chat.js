dbpatterns.models.Room = Backbone.Model.extend({
    initialize: function (model, options) {
        this.socket = options.socket;
        this.clients = new dbpatterns.collections.Clients(this.get("clients"));
        this.messages = new dbpatterns.collections.Messages();
    }
});

dbpatterns.models.Client = Backbone.Model.extend({
    idAttribute: "username"
});

dbpatterns.models.Message = Backbone.Model.extend({

});

dbpatterns.collections.Clients = Backbone.Collection.extend({
    model: dbpatterns.models.Client
});

dbpatterns.collections.Messages = Backbone.Collection.extend({
    model: dbpatterns.models.Message
});
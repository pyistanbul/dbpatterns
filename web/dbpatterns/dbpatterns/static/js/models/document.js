dbpatterns.models.Document = Backbone.Model.extend({

    urlRoot: "/api/documents",

    initialize: function (model, options) {
        this.socket = io.connect(options.socket_uri);
        this.entities = new dbpatterns.collections.Entity;
        this.on("change:assignees change:title change:is_public", this.push, this);
        this.socket.on("pull", this.pull.bind(this));
    },

    parse: function (result) {
        if (!result) { return result; }
        this.entities.reset(result.entities);
        this.entities.bind("add remove persist", this.persist.bind(this));
        return result;
    },

    persist: function () {
        this.set({"entities": this.entities.toJSON()});
        this.push();
    },

    channel: function () {
        // specifies the channel of user
        return this.get("id")
    },

    push: function () {
        console.log("push")
        // pushes the changes to the channel of user
        this.socket.emit("push", this.toJSON());
    },

    pull: function (data) {
        console.log("pull")
        // pulls the changes from the channel
        this.set(data);
        this.entities.reset(data.entities);
    }

});
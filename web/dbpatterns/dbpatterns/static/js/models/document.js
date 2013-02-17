dbpatterns.models.Document = Backbone.Model.extend({

    urlRoot: "/api/documents",

    initialize: function (model, options) {
        this.entities = new dbpatterns.collections.Entity;
        this.use_websocket = options.use_websocket;
        if (this.use_websocket) {
            this.socket = io.connect(options.socket_uri);
            this.socket.on("pull", this.pull.bind(this));
            this.on("change:assignees change:title change:is_public", this.push, this);
        } else {
            this.socket = {};
            _.extend(this.socket, Backbone.Events);
        }
    },

    parse: function (result) {
        if (!result) { return result; }
        this.entities.reset(result.entities);
        this.entities.bind("add remove persist", this.persist.bind(this));
        return result;
    },

    persist: function () {
        this.set({"entities": this.entities.toJSON()});
        if (this.use_websocket) {
            this.push();
        }
    },

    channel: function () {
        // specifies the channel of user
        return this.get("id")
    },

    push: function () {
        // pushes the changes to the channel of user
        this.socket.emit("push", this.toJSON());
    },

    pull: function (data) {
        // pulls the changes from the channel
        this.set(data);
        this.entities.reset(data.entities);
    }

});
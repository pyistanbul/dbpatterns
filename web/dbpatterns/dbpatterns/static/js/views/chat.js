dbpatterns.views.Room = Backbone.View.extend({

    el: $("#chat"),
    button: $("#chat-button"),

    initialize: function () {
        this.model.socket.on("message", this.pull_message.bind(this));
        this.model.socket.on("join", this.join.bind(this));
        this.model.socket.on("leave", this.leave.bind(this));
    },

    render: function () {

        this.$el.find("aside").html((new dbpatterns.views.Clients({
            model: this.model.clients
        })).render().el);

        this.$el.find("footer").html((new dbpatterns.views.MessageForm({
            model: this.model
        })).render().el);

        this.$el.find("section").html((new dbpatterns.views.Messages({
            model: this.model.messages
        })).render().el);

        this.render_client_count();

        return this;
    },

    is_active: function () {
        return this.$el.hasClass("active");
    },

    render_client_count: function () {
        var count = this.model.clients.length;
        this.button.find("#online-count").html(count);
        if (count > 1) {
            this.button.show();
        }
    },

    pull_message: function (data) {
        data.is_read = this.is_active();
        this.model.messages.add(new dbpatterns.models.Message(data));
    },

    join: function (username) {
        this.model.clients.add(new dbpatterns.models.Client({
            username: username
        }));
        this.render_client_count();
        dbpatterns.notifications.trigger("flash", username + " joined to the chat room");
    },

    leave: function (username) {
        var client = this.model.clients.get(username);
        this.model.clients.remove(client);
        dbpatterns.notifications.trigger("flash", username + " left from to the chat room");
        this.render_client_count();
    }

});

dbpatterns.views.MessageForm = Backbone.View.extend({
    tagName: "form",
    events: {
        "submit": "submit"
    },
    render: function () {
        this.input = $("<input>", {
            "type": "text",
            "placeholder": "Type text and press enter."
        });
        this.$el.html(this.input);
        return this;
    },
    submit: function () {
        this.model.socket.emit("message", this.input.val());
        this.input.val("");
        return false;
    }
});

dbpatterns.views.Client = Backbone.View.extend({
    tagName: "li",
    render: function () {
        this.$el.html(this.model.get("username"));
        return this;
    }
});

dbpatterns.views.Clients = Backbone.View.extend({
    tagName: "ul",
    initialize: function () {
        this.model.on("add remove", this.render, this);
    },
    render: function () {
        this.$el.empty();
        _.forEach(this.model.models, function (client) {
            this.$el.append(new dbpatterns.views.Client({
                model: client
            }).render().el);
        }, this);
        return this;
    }
});

dbpatterns.views.Message = Backbone.View.extend({
    tagName: "li",
    template: $("#message-template").html(),
    render: function () {
        this.$el.html(_.template(this.template, this.model.toJSON()));
        return this;
    }
});

dbpatterns.views.Messages = Backbone.View.extend({
    tagName: "ul",
    initialize: function () {
        this.model.on("add", this.add_message, this);
    },
    render: function () {
        _.forEach(this.model.models, this.add_message, this);
        return this;
    },
    add_message: function (message) {
        this.$el.append(new dbpatterns.views.Message({
            model: message
        }).render().el);
    }

});
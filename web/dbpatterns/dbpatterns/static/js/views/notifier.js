dbpatterns.views.Notification = Backbone.View.extend({

    DELAY: 1000,

    tagName: "div",
    className: "notification",
    render: function () {
        this.$el.html(this.options.text);
        this.$el.delay(this.DELAY).slideUp("fast");
        return this;
    }
});

dbpatterns.views.Notifier = Backbone.View.extend({
    el: "#notifications",
    initialize: function () {
        dbpatterns.notifications.on("flash", this.flash, this);
    },
    flash: function (text) {
        this.$el.append(new dbpatterns.views.Notification({
            text: text
        }).render().el);
    }
});
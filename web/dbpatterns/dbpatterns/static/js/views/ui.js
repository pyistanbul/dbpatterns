dbpatterns.views.EditInPlaceForm = Backbone.View.extend({
    tagName: "form",
    input: $("<input>"),
    events: {
        "submit": "submit"
    },
    attributes: {
        "action": "#"
    },
    render: function (initial) {
        this.input.val(initial || "");
        this.$el.append(this.input);
        return this;
    },
    focus: function () {
        this.input.focus();
    },
    submit: function (event) {
        this.submit_callback(this.input.val());
        this.$el.remove();
        event.preventDefault();
        return this;
    },
    success: function (callback) {
        this.submit_callback = callback;
        return this;
    }
});


dbpatterns.views.FormDialog = Backbone.View.extend({
    tagName: "div",
    container: "body",
    options: {
        "form": null,
        "model": null,
        "title": "Dialog",
        "submit_callback": function () {}
    },
    initialize: function (options) {
        $.extend(this.options, options);
        this.form = $(this.options.form);
        this.form.submit(this.submit.bind(this));
    },
    render: function () {
        this.$el.appendTo(this.container).append(this.form);
        this.$el.dialog({
            modal: true,
            title: this.options.title,
            buttons: {
                OK: this.submit.bind(this)
            }
        });
        this.load_data(this.model.toJSON());
        return this;
    },
    load_data: function (data) {
        _.forEach(data, function (value, key) {
            var input = this.form.find("#" + key);
            if (input.is(":checkbox")) {
                input.attr("checked", value);
            } else {
                input.val(value);
            }
        }.bind(this));
    },
    save_data: function () {
        this.model.set(this.form.form2json());
        this.model.save();
    },
    submit: function () {
        this.save_data();
        if (this.options.submit_callback()) {
            this.$el.dialog("destroy");
            this.form.remove();
        }
    },
    success: function (callback) {
        this.options.submit_callback = callback;
        return this;
    }

});
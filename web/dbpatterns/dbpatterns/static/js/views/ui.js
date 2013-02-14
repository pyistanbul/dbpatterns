dbpatterns.views.EditInPlaceForm = Backbone.View.extend({
    tagName: "form",
    input: $("<input>"),
    events: {
        "submit": "submit"
    },
    attributes: {
        "action": "#"
    },
    shortcuts: {
        'esc': 'destroy'
    },
    initialize: function () {
        _.extend(this, new Backbone.Shortcuts);
        this.delegateShortcuts();
        this.submit_callback = function () {};
        this.cancel_callback = function () {};
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
    cancel: function (callback) {
        this.cancel_callback = callback;
    },
    success: function (callback) {
        this.submit_callback = callback;
        return this;
    },
    destroy: function () {
        this.cancel_callback();
        this.$el.remove();
    }
});


dbpatterns.views.Dialog = Backbone.View.extend({
    tagName: "div",
    container: "body",
    className: "dialog",
    template: $("#dialog-template").html(),
    draggable: true,
    events: {
        "click .close": "destroy"
    },
    shortcuts: {
        'esc': 'destroy'
    },
    initialize: function () {
        _.extend(this, new Backbone.Shortcuts);
        this.delegateShortcuts();
    },
    render: function () {
        this.$el.html(_.template(this.template, {
            title: this.options.title || "Dialog"
        })).appendTo(this.container);
        if (this.draggable) {
            $(this.$el).draggable();
        }
    },
    destroy: function () {
        this.$el.remove();
    }
});

dbpatterns.views.FormDialog = dbpatterns.views.Dialog.extend({
    initialize: function () {
        dbpatterns.views.Dialog.prototype.initialize.apply(this);
        this.form = $(this.options.form);
        this.form.submit(this.submit.bind(this));
        this.options.submit_callback = function () {
            return true;
        }
    },
    events: {
        "click .close": "destroy"
    },
    render: function () {
        dbpatterns.views.Dialog.prototype.render.apply(this);
        this.$el.append(this.form);
        this.load_data(this.model.toJSON());
        this.$el.find("input").eq(0).focus();
        this.trigger("render");
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
            this.destroy();
            this.form.remove();
        }
        return false;
    },
    success: function (callback) {
        this.options.submit_callback = callback;
        return this;
    }

});


dbpatterns.views.ExportDialog = dbpatterns.views.Dialog.extend({
    template: $("#export-dialog-template").html(),
    className: "export-dialog",
    events: {
        "click .close": "destroy",
        "click .new-window": "new_window"
    },
    initialize: function () {
        dbpatterns.views.Dialog.prototype.initialize.apply(this);
    },
    render: function () {
        this.$el.html(_.template(this.template, {
            title: this.options.title,
            code: "Loading"
        })).appendTo(this.container);

        $.get(this.options.url, function (response) {
            this.$el.find("code").html(response);
            prettyPrint();
        }.bind(this))
    },
    new_window: function () {
        window.open(this.options.url);
    }
});
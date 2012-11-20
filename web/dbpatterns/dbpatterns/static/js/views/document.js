dbpatterns.views.Document = Backbone.View.extend({

    messages: {
        save: "The document was saved successfully",
        rename: "The document was renamed successfully."
    },

    el: "article#document",

    events: {
        "click .edit-title": "rename",
        "click .save-document": "save_document",
        "click .export": "export_document",
        "click .show": "show_document",
        "click #show-comments": "render_comments"
    },

    shortcuts: {
        "option+r": "rename",
        "option+s": "save_document"
    },

    initialize: function () {
        _.extend(this, new Backbone.Shortcuts);
        this.delegateShortcuts();

        // bindings
        this.model.bind("change:title", this.render_title, this);

        // sub views
        this.entities_view = new dbpatterns.views.Entities({
            model: this.model.entities,
            app_view: this
        });
        this.comments_view = null; // it's lazy.
    },

    render_title: function () {
        this.$el.find("header h1").html(this.model.escape("title"));
        window.document.title = this.model.get("title");
        return this;
    },

    rename: function () {

        var title = window.prompt("Title", this.model.get("title"));

        if (!title) {
            return false;
        }

        this.model.set("title", title);
        dbpatterns.notifications.trigger("flash", this.messages.rename);
        return this;
    },

    save_document: function (callback) {
        this.model.save().success(function () {
            dbpatterns.notifications.trigger("flash", this.messages.save);
            callback && callback();
        }.bind(this));
    },

    render_comments: function () {

        if (this.comments_view) {
            this.comments_view.show();
            return;
        }

        this.comments_view = (new dbpatterns.views.Comments({
            document: this.model
        })).render();

    },

    export_document: function () {
        var exporter_link = $(event.target);
        var dialog = (new dbpatterns.views.ExportDialog({
            title: exporter_link.html(),
            url: exporter_link.attr("href")
        }));
        if (this.options.edit) {
            this.save_document(function () {
                dialog.render();
            }.bind(this));
        } else {
            dialog.render();
        }
        return false;
    },

    show_document: function (event) {
        this.save_document(_.delay(function () {
            window.location = $(event.target).attr("href");
        }, 500));
        return false;
    }
});
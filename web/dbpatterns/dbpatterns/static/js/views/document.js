dbpatterns.views.Document = Backbone.View.extend({

    messages: {
        save: "The document was saved successfully",
        rename: "The document was renamed successfully."
    },

    el: "article#document",

    events: {
        "click .edit-title": "rename",
        "click .save-document": "save_document",
        "click .export": "export_document"
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
    },

    render_title: function () {
        this.$el.find("header h1").html(this.model.get("title"));
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

    export_document: function () {
        var exporter_link = $(event.target);
        this.save_document(function () {
            (new dbpatterns.views.ExportDialog({
                title: exporter_link.html(),
                url: exporter_link.attr("href")
            })).render();
        }.bind(this));
        return false;
    }

})
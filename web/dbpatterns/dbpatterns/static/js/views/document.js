dbpatterns.views.Document = Backbone.View.extend({

    messages: {
        save: "The document was saved successfully",
        rename: "The document was renamed successfully."
    },

    el: "article#document",

    events: {
        "click .edit-title": "rename",
        "click .edit-document": "show_settings_form",
        "click .save-document": "save_document",
        "click .export": "export_document",
        "click .show": "show_document",
        "click #show-comments": "render_comments"
    },

    shortcuts: {
        "option+r": "rename",
        "option+s": "save_document",
        "esc": "hide_comments"
    },

    settings_form_template: $("#document-edit-template").html(),

    initialize: function () {
        _.extend(this, new Backbone.Shortcuts);
        this.delegateShortcuts();

        // bindings
        this.model.on("change:title", this.render_title, this);
        this.model.socket.on("enter", this.enter_room.bind(this));

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

        return false;

    },

    hide_comments: function () {
        if (this.comments_view) {
            this.comments_view.hide();
        }
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
    },

    show_settings_form: function () {
        (new dbpatterns.views.DocumentEditDialog({
            "form": _.template(this.settings_form_template, this),
            "model": this.model,
            "title": "Document Settings"
        })).success(function () {
            this.save_document();
            return true;
        }.bind(this)).render();
    },

    enter_room: function (data) {
        if (this.options.edit) {
            new dbpatterns.views.Room({
                model: new dbpatterns.models.Room(data, {
                    socket: this.model.socket
                })
            }).render();
        }
    }
});

dbpatterns.views.DocumentEditDialog = dbpatterns.views.FormDialog.extend({
    tagName: "div",
    className: "settings",
    draggable: false,

    initialize: function () {
        dbpatterns.views.FormDialog.prototype.initialize.apply(this);
        this.on("render", this.show_assignees)
    },

    show_assignees: function () {

        this.assignees = new dbpatterns.collections.Assignees(this.model.get("assignees"));
        var assignees_view = new dbpatterns.views.AssigneesView({
            model: this.assignees
        });
        assignees_view.render();
    },

    load_data: function () {

        this.form.find("#title").val(this.model.get("title"));

        if (this.model.get("is_public")) {
            this.form.find("#is_public").attr("checked", "checked");
        } else {
            this.form.find("#is_private").attr("checked", "checked");
        }
    },

    save_data: function () {
        this.model.set({
            "title": this.form.find("#title").val(),
            "is_public": this.form.find("#is_public").is(":checked"),
            "assignees": this.assignees.toJSON()
        });
    }
});
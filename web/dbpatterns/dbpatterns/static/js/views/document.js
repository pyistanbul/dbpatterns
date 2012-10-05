dbpatterns.views.Document = Backbone.View.extend({

    el: "article#document",

    events: {
        "click .edit-title": "rename",
        "click .save-document": "save_document"
    },

    initialize: function () {
        this.model.bind("change:title", this.render_title, this);
        this.entities_view = new dbpatterns.views.Entities({
            model: this.model.entities,
            app_view: this
        })
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
        return this;
    },

    save_document: function () {
        this.model.save();
    }

});
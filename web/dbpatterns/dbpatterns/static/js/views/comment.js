dbpatterns.views.CommentForm = Backbone.View.extend({
    tagName: "form",
    template: $("#comment-form-template").html(),
    events: {
        "submit": "submit"
    },
    render: function () {
        this.$el.html(_.template(this.template, {}));
        return this;
    },
    submit: function () {

        var data = this.$el.form2json();

        if (!data.body) {
            return false;
        }

        var comment = new dbpatterns.models.Comment(data);
        this.model.create(comment, {
            wait: true
        });
        this.reset();
        return false;
    },
    reset: function () {
        this.$el[0].reset();
    }
});

dbpatterns.views.CommentItem = Backbone.View.extend({
    tagName: "li",
    template: $("#comment-item-template").html(),
    events: {
        "click .delete": "destroy"
    },
    render: function () {
        this.$el.html(_.template(this.template, this.model.toJSON()));
        return this;
    },
    destroy: function () {
        this.model.destroy();
        this.$el.slideUp(300, function () {
            this.$el.remove();
        }.bind(this));

    }
});

dbpatterns.views.CommentList = Backbone.View.extend({

    tagName: "ul",

    initialize: function () {
        this.model.on("reset", this.render, this);
        this.model.on("add", this.render_comment, this);
        this.model.fetch();
    },

    render: function () {
        _.forEach(this.model.models, function (model) {
            this.render_comment(model);
        }, this);
        return this;
    },

    render_comment: function (comment) {
        this.$el.append((new dbpatterns.views.CommentItem({
            model: comment
        }).render().el))

    }


});

dbpatterns.views.Comments = Backbone.View.extend({
    el: $("#comments"),

    events: {
        "click .close": "hide"
    },

    initialize: function () {
        this.model = new dbpatterns.collections.Comments({
            document: this.options.document
        });
    },

    render: function () {

        this.$el.append((new dbpatterns.views.CommentList({
            model: this.model
        })).el);

        this.$el.append((new dbpatterns.views.CommentForm({
            model: this.model
        }).render().el));

        this.model.on("reset", function (model) {
            if (!model.models.length) {
                this.$el.find(".no-comment").delay(300).slideDown(300);
            }
        }, this);

        this.model.on("add", function () {
            this.$el.find(".no-comment").hide();
        }, this);
        
        this.show();
        return this;
    },

    show: function () {
        this.$el.show();
    },

    hide: function () {
        this.$el.hide();
    }

});
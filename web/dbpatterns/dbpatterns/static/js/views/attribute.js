dbpatterns.views.AttributeFormDialog = dbpatterns.views.FormDialog.extend({
    events: function () {
        return $.extend({
            "click #is_foreign_key": "toggle_foreign_key"
        }, dbpatterns.views.FormDialog.prototype.events)
    },
    toggle_foreign_key: function () {
        this.$el.find(".foreign-key-details").toggle();
    },
    render: function () {
        dbpatterns.views.FormDialog.prototype.render.apply(this);
        if (this.model.get("is_foreign_key")) {
            this.toggle_foreign_key();
        }
        return this;
    }
});

dbpatterns.views.Attribute = Backbone.View.extend({

    tagName: "div",
    className: "attribute",

    template: $("#attribute-template").html(),
    form_template: $("#attribute-form-template").html(),

    events: {
        "click a.edit": "show_attribute_form",
        "click a.remove-attribute": "destroy"
    },

    initialize: function () {
        this.model.bind("change", this.render, this);
        this.model.bind("destroy", this.detach, this);
        this.model.bind("change connect", this.render_connection, this);
        this.model.collection.on("detach", this.detach, this);
    },

    show_attribute_form: function () {
        var dialog = (new dbpatterns.views.AttributeFormDialog({
            "form": _.template(this.form_template, this),
            "model": this.model,
            "title": "Attribute"
        })).success(function () {
            return true;
        }).render();

        return this;
    },

    render: function () {
        this.$el.html(_.template(this.template, this.model.toJSON()));
        this.$el.data("model", this.model);
        this.load_connection();
        return this;
    },

    load_connection: function () {
        this.options.app_view.on("load", this.render_connection, this);
    },

    render_connection: function () {

        var source = this.$el.parents(".entity");
        var target = $("[data-entity='" + this.model.get("foreign_key_entity") + "']");

        if (this.connection) {
            this.connection.destroy();
        }

        if (!this.model.get("is_foreign_key")) {
            return;
        }

        if (!source.length || !target.length) {
            this.model.trigger("fk_does_not_exist"); // foreign key does not exist.
            return;
        }

        this.connection = (new dbpatterns.views.Connection({
            model: this.model,
            el: source,
            target: target,
            label: function (model) {
                return model.escape("name") + " -> " + model.escape("foreign_key_attribute");
            }
        })).render();


    },

    detach: function () {
        if (this.connection) {
            this.connection.destroy();
        }

        this.$el.remove();
    },

    destroy: function () {
        this.model.destroy();
    }
});

dbpatterns.views.Attributes = Backbone.View.extend({

    template: $("#attribute-list-template").html(),

    events: {
        "click .new-attribute": "new_attribute"
    },

    initialize: function () {
        this.model.bind("add", this.add_attribute, this);
    },

    render_attributes: function (attributes) {
        _.forEach(attributes, this.add_attribute, this);
    },

    add_attribute: function (attribute) {

        if (!attribute.get("name")) {
            return
        }

        this.$el.find("section.attributes").append(new dbpatterns.views.Attribute({
            model: attribute,
            app_view: this.options.app_view
        }).render().el);
        attribute.trigger("render");
    },

    render: function () {
        this.$el.html(_.template(this.template));
        this.render_attributes(this.model.models);
        this.get_sortable_content().sortable({
            "axis": "y",
            "containment": this.get_sortable_content(),
            "opacity": 0.6,
            "placeholder": "attribute-place-holder",
            "update": function (event, sorted) {
                var target = $(event.target);
                target.find(".attribute").each(function (index, element) {
                    var item = $(element);
                    item.data("model").set({
                        "order": item.index()
                    });
                });
                this.model.sort();
                this.model.trigger("persist");
            }.bind(this)
        });
        return this;
    },

    get_sortable_content: function () {
        return this.$el.find("section");
    },

    new_attribute: function (event) {
        event.preventDefault();
	var button = this.$el.find(".new-attribute");
        var view = new dbpatterns.views.EditInPlaceForm();
        button.before(view.render().el);
        view.success(function (name) {
           button.focus();
           if (!name) return;
           this.model.add(new dbpatterns.models.Attribute({
                "name": name,
                "order": this.model.length
            }));
        }.bind(this));
        view.cancel(function () {
           button.focus();
        }.bind(this));
        view.focus();
    }

});

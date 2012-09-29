dbpatterns.Entity = $.Class.extend({

    options: {
        "entity_template": "entity_template",
        "attribute_template": "attribute_template",
        "new_attribute": ".new",
        "attributes_container": "ul"
    },

    entity: {
        "drag": true,
        "name": "entity",
        "attributes": []
    },

    el: null,

    init: function (_entity) {
        $.extend(this.entity, _entity);

    },

    render: function () {

        this.el = $(tmpl(this.options.entity_template, this));

        if (this.entity.drag) {
            this.make_draggable()
        }

        this.el.find(this.options.new_attribute).click(this.add_attribute.bind(this));

        return this;
    },

    add_attribute: function (event) {
        var attribute_name = window.prompt("Attribute name");
        if (!attribute_name) {
            return;
        }

        var attribute = {
            "name":  attribute_name,
            "type": "string"
        };
        this.entity.attributes.push(attribute);
        this.el.find(this.options.attributes_container).append(this.render_attribute(attribute));

    },

    render_attribute: function (attribute) {
        console.log(attribute)
        return tmpl(this.options.attribute_template, attribute);
    },

    make_draggable: function () {
        $(this.el).draggable();
    }


});
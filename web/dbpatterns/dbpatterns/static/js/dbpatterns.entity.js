dbpatterns.Entity = $.Class.extend({

    options: {
        "template": "entity_template"
    },

    entity: {
        "drag": true,
        "name": "entity",
        "position": {
            "left": 200,
            "top": 300
        },
        "attributes": []
    },

    el: null,

    init: function (_entity) {
        $.extend(this.entity, _entity);

    },

    render: function () {
        this.el = $(tmpl(this.entity.template, this));

        if (this.entity.drag) {
            this.make_draggable()

        }
        return this.el;
    },

    make_draggable: function () {
        $(this.el).draggable();
    }


});
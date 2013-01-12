dbpatterns.views.ConnectorEndpoint = Backbone.View.extend({
    initialize: function () {
        this.configure();
    },
    configure: function () {

    },
    render: function () {
        jsPlumb.makeSource(this.$el, {
            "anchor": [ "RightMiddle", "LeftMiddle" ],
            "connector": ["Flowchart"],
            "connectorStyle": { strokeStyle:"#dedede", lineWidth:6 },
            "paintStyle": { fillStyle:"#dedede" }
        });

        jsPlumb.makeTarget(this.$el, {
            "anchor": [ "RightMiddle", "LeftMiddle" ],
            "paintStyle": { fillStyle:"#dedede" }
        });
    }
});


dbpatterns.views.Connection = Backbone.View.extend({
    initialize: function () {
        this.model.bind("change", this.set_label, this);
    },
    render: function () {
        this.connection = jsPlumb.connect({
            source: this.el,
            target: this.options.target
        });
        return this;
    },
    set_label: function () {
        this.connection.setLabel(this.options.label(this.model));
    },
    destroy: function () {

       jsPlumb.detach(this.connection);
    }
});
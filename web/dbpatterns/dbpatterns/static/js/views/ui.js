dbpatterns.views.EditInPlaceForm = Backbone.View.extend({
    tagName: "form",
    input: $("<input>"),
    events: {
        "submit": "submit"
    },
    render: function (initial) {
        this.input.val(initial || "");
        this.$el.append(this.input);
        return this;
    },
    focus: function () {
        this.input.focus();
    },
    submit: function () {
        this.submit_callback(this.input.val());
        this.$el.remove();
    },
    success: function (callback) {
        this.submit_callback = callback;
    }
});
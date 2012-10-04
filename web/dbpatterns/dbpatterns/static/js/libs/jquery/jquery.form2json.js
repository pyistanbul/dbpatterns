/*
 * Serializes form data as object.
 * */
!function ($) {

    $.fn.form2json = function(_options) {
        var options = $.extend({
            "include": "select, input, textarea",
            "exclude": "input[type='button'], input[type='submit']"
        }, _options);

        var get_input_value = function (input) {
            if (input.is(":checkbox")) {
                return input.is(":checked");
            }
            else {
                return input.val();
            }
        };

        var result_object = {};
        this.find(options.include).not(options.exclude).each(function () {
            var input_name = $(this).attr("name");
            result_object[input_name] = get_input_value($(this));
        });

        return result_object;
    };

}(window.jQuery);
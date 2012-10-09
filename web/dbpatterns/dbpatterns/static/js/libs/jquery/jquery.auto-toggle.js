!(function ($) {
    $(function () {
        $("a[data-toggle]").click(function () {
            $($(this).attr("href")).toggle();
        });
    });
})(window.jQuery);
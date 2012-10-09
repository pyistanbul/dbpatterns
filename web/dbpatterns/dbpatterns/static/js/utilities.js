!(function ($) {

    // auto toggle manipulation
    $(function () {
        $("a[data-toggle]").click(function () {
            $($(this).attr("href")).toggle();
            return false;
        });
    });

})(window.jQuery);
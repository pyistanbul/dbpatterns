!(function ($) {

    // auto toggle manipulation
    $(function () {
        $("a[data-toggle]").click(function () {
            var target = $($(this).attr("href"));
            target.toggle().find("a").click(function (event) {
                target.hide();
            });
            return false;
        });
    });

})(window.jQuery);
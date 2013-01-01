!(function ($) {

    $(function () {
        // auto toggle manipulation
        $("a[data-toggle]").click(function () {
            var target = $($(this).attr("href"));
            target.toggle().find("a").click(function (event) {
                target.hide();
            });
            return false;
        });

        $("#user-notifications-button").click(function () {
            var notifications = $("#user-notifications"),
                notifications_section = notifications.find("section"),
                notifications_bubble = $(this).find("span"),
                notifications_url = $(this).attr("href");
            notifications.toggle();
            notifications_bubble.remove();
            notifications_section.load(notifications_url);
            $.ajax({"type": "PUT", "url": notifications_url});
            return false;
        });
    });

})(window.jQuery);
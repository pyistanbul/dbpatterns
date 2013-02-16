!(function ($) {

    $(function () {
        // auto toggle manipulation
        $("a[data-toggle]").click(function () {
            var button = $(this),
                target = $(button.attr("href"));
            button.toggleClass("active");
            target.toggle().find("a").click(function (event) {
                target.hide();
            });
            return false;
        });

        // notifications
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

        // tab implementation
        $(".tabs nav a").click(function () {
            var tab_link = $(this),
                link_container = tab_link.parent(),
                focused_tab = $(tab_link.attr("href"));
            focused_tab.siblings("section").hide();
            focused_tab.show();
            link_container.siblings().removeClass("active");
            link_container.addClass("active");
            return false;
        });

    });

})(window.jQuery);
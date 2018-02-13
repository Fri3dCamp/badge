window.notifications = {};

(function(notifications) {

  // define our own style
  $.notify.addStyle( "general", {
    html: 
      "<div>" +
        "<div class='clearfix'>" +
          "<div class='message' data-notify-html='message'/>" +
        "</div>" +
      "</div>"
  });

  // API call to report success
  notifications.report_success = function report_success(message) {
    $.notify({
      message: i18n.get(message),
    }, { 
      style: "general",
      autoHideDelay: 15000,
    });
  };

  // API call to report failure
  notifications.report_failure = function report_failure(message) {
    $.notify({
      message: i18n.get(message),
    }, {
      style: "error",
      autoHideDelay: 15000,
    });
  };

})(window.notifications);

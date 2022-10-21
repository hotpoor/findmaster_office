// Generated by CoffeeScript 1.12.7
(function() {
  var Hs, root;

  root = typeof exports !== "undefined" && exports !== null ? exports : this;

  root.Hs || (root.Hs = {});

  Hs = root.Hs;

  $(function() {
    console.log("msh hollow");
    $("body").on("click", ".login_scan_submit", function(evt) {
      return $.ajax({
        url: "/api/login_scan/submit",
        data: {
          app: FINDMASTER_APP,
          room_id: LOGIN_SCAN_ROOM_ID,
          user_id: LOGIN_SCAN_USER_ID,
          uuid: LOGIN_SCAN_UUID,
          uuid_now: uuid2(6, null)
        },
        dataType: 'json',
        type: 'POST',
        success: function(data) {
          console.log(data);
          if (data.info === "ok") {
            if (IS_WEIXIN) {
              return root.close_window();
            } else {
              window.opener = null;
              window.open('', '_self');
              return window.close();
            }
          }
        },
        error: function(data) {
          return console.log(data);
        }
      });
    });
    return $("body").on("click", ".login_scan_close", function(evt) {
      if (IS_WEIXIN) {
        return root.close_window();
      } else {
        window.opener = null;
        window.open('', '_self');
        return window.close();
      }
    });
  });

}).call(this);
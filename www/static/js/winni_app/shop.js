// Generated by CoffeeScript 1.12.7
(function() {
  var Hs, root;

  root = typeof exports !== "undefined" && exports !== null ? exports : this;

  root.Hs || (root.Hs = {});

  Hs = root.Hs;

  $(function() {
    var auto_login_stripe;
    console.log("winni app user");
    $("body").on("click", ".stripe_account_retrieve_btn", function(evt) {
      var _pay_type, _stripe_account;
      _pay_type = $(this).parents(".stripe_account_card").first().attr("data-pay-type");
      _stripe_account = $(this).parents(".stripe_account_card").first().attr("data-account-id");
      return $.ajax({
        url: "/api/store/app/stripe/retrieve",
        type: "POST",
        dataType: "json",
        data: {
          pay_type: _pay_type,
          stripe_account: _stripe_account,
          shop_id: SHOP_ID
        },
        success: function(data) {
          console.log(data);
          return alert(data.about);
        },
        error: function(data) {
          return console.log(data);
        }
      });
    });
    $("body").on("click", ".stripe_account_login_btn", function(evt) {
      var _pay_type, _stripe_account;
      _pay_type = $(this).parents(".stripe_account_card").first().attr("data-pay-type");
      _stripe_account = $(this).parents(".stripe_account_card").first().attr("data-account-id");
      $(this).parents(".stripe_account_card").first().find(".log").empty();
      return $.ajax({
        url: "/api/store/app/stripe/login_link",
        type: "POST",
        dataType: "json",
        data: {
          pay_type: _pay_type,
          stripe_account: _stripe_account,
          shop_id: SHOP_ID
        },
        success: function(data) {
          console.log(data);
          if (data.info === "ok") {
            return $(".stripe_account_card[data-account-id=" + _stripe_account + "][data-pay-type=" + _pay_type + "]").append("<a target=\"_blank\" href=\"" + data.result["url"] + "\">go login stripe</a>");
          }
        },
        error: function(data) {
          return console.log(data);
        }
      });
    });
    return auto_login_stripe = function(type) {
      if (type == null) {
        type = "test";
      }
      if (type === "test") {
        if (!STRIPE_ACCOUNT_ID_TEST_PAYOUTS_ENABLED) {
          return $.ajax({
            url: "/api/store/app/stripe/login_link",
            type: "POST",
            dataType: "json",
            data: {
              pay_type: type,
              stripe_account: STRIPE_ACCOUNT_ID_TEST,
              shop_id: SHOP_ID
            },
            success: function(data) {
              console.log(data);
              if (data.info === "ok") {
                return window.location.href = data.result["url"];
              }
            },
            error: function(data) {
              return console.log(data);
            }
          });
        }
      }
    };
  });

}).call(this);

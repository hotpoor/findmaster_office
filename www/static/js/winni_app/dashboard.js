// Generated by CoffeeScript 1.12.7
(function() {
  var Hs, root;

  root = typeof exports !== "undefined" && exports !== null ? exports : this;

  root.Hs || (root.Hs = {});

  Hs = root.Hs;

  $(function() {
    console.log("winni_app dashbaord");
    $("body").on("click", ".stripe_account_list_create_btn", function(evt) {
      var data_type;
      data_type = $(this).attr("data-type");
      return $.ajax({
        url: "/api/stripe/account/add",
        data: {
          pay_type: data_type
        },
        dataType: 'json',
        type: 'POST',
        success: function(data) {
          return console.log(data);
        },
        error: function(data) {
          return console.log(data);
        }
      });
    });
    $("body").on("click", ".stripe_account_list_load_btn", function(evt) {
      var data_type;
      data_type = $(this).attr("data-type");
      return $.ajax({
        url: "/api/stripe/account/list",
        data: {
          pay_type: data_type
        },
        dataType: 'json',
        type: 'GET',
        success: function(data) {
          var results, stripe_account_id, stripe_account_json, stripe_accounts;
          console.log(data);
          stripe_accounts = data.stripe_accounts;
          $(".stripe_account_list[data-type=" + data_type + "]").empty();
          results = [];
          for (stripe_account_id in stripe_accounts) {
            stripe_account_json = stripe_accounts[stripe_account_id];
            $(".stripe_account_list[data-type=" + data_type + "]").append("<div class=\"stripe_account_line\" data-stripe-account=\"" + stripe_account_id + "\">\n    <div>stripe_account_id: <span>" + stripe_account_id + "</span></div>\n    <div>\n        <button class=\"stripe_account_line_btn_retrieve\">同步店铺数据</button>\n        <button class=\"stripe_account_line_btn_account_link\">获取账户链接</button>\n    </div>\n    <div><textarea class=\"stripe_account_line_json\"></textarea></div>\n    <div class=\"store_card\">\n        <div class=\"store_card_display_name\">" + stripe_account_json["settings"]["dashboard"]["display_name"] + "</div>\n        <div class=\"store_card_display_email\">" + stripe_account_json["email"] + "</div>\n        <div class=\"store_card_display_icon\"></div>\n    </div>\n</div>");
            results.push($(".stripe_account_list[data-type=" + data_type + "]>.stripe_account_line[data-stripe-account=\"" + stripe_account_id + "\"]").find("textarea").val(JSON.stringify(stripe_account_json)));
          }
          return results;
        },
        error: function(data) {
          return console.log(data);
        }
      });
    });
    $("body").on("click", ".stripe_account_line_btn_retrieve", function(evt) {
      var data_type, stripe_account;
      data_type = $(this).parents(".stripe_account_list").first().attr("data-type");
      stripe_account = $(this).parents(".stripe_account_line").first().attr("data-stripe-account");
      return $.ajax({
        url: "/api/stripe/account/retrieve",
        data: {
          pay_type: data_type,
          stripe_account: stripe_account
        },
        dataType: 'json',
        type: 'POST',
        success: function(data) {
          return console.log(data);
        },
        error: function(data) {
          return console.log(data);
        }
      });
    });
    return $("body").on("click", ".stripe_account_line_btn_account_link", function(evt) {
      var data_type, stripe_account;
      data_type = $(this).parents(".stripe_account_list").first().attr("data-type");
      stripe_account = $(this).parents(".stripe_account_line").first().attr("data-stripe-account");
      return $.ajax({
        url: "/api/stripe/account/add_link",
        data: {
          pay_type: data_type,
          stripe_account: stripe_account
        },
        dataType: 'json',
        type: 'POST',
        success: function(data) {
          return console.log(data);
        },
        error: function(data) {
          return console.log(data);
        }
      });
    });
  });

}).call(this);
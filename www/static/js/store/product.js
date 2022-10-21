// Generated by CoffeeScript 1.12.7
(function() {
  var Hs, root;

  root = typeof exports !== "undefined" && exports !== null ? exports : this;

  root.Hs || (root.Hs = {});

  Hs = root.Hs;

  Hs.login_scan_uri_uuid = null;

  $(function() {
    var stores_info, xialiwei_find_good, xialiwei_goods_list, xialiwei_goods_list_load;
    console.log("msh product");
    xialiwei_find_good = function(chat_id, comment_id, store_id, add_num) {
      if (add_num == null) {
        add_num = 0;
      }
      return $.ajax({
        url: "/api/page/comment/load",
        type: "GET",
        dataType: "json",
        data: {
          chat_id: chat_id,
          comment_id: comment_id
        },
        success: function(data) {
          var _html, _html_price, _html_prices, _html_prices_html, _html_prices_new, _html_prices_new_list, colors, colors_html, comment, comment_json, e, i, j, k, l, last_comment_id, len, len1, len2, len3, len4, line_through_class_str, m, n, name, o, p, prices, prices_html, q, ref, ref1, ref2, sizes, sizes_html, store_score, uuid_now, v;
          console.log(data);
          if (data.info === "ok") {
            ref = data.comments;
            for (j = ref.length - 1; j >= 0; j += -1) {
              comment = ref[j];
              comment_json = null;
              try {
                comment_json = JSON.parse(comment[4]);
              } catch (error) {
                e = error;
                continue;
              }
              if (comment_json !== null) {
                if (comment_json["json_type"] === "good_info") {
                  _html_prices = comment_json["promotion-item"];
                  _html_prices_html = "";
                  _html_prices_new = "";
                  _html_prices_new_list = {};
                  ref1 = comment_json["promotion-item"];
                  for (l = 0, len = ref1.length; l < len; l++) {
                    _html_price = ref1[l];
                    name = _html_price["name"];
                    if (_html_price["sizes"] === void 0) {
                      sizes = [];
                    } else {
                      sizes = _html_price["sizes"];
                    }
                    sizes_html = "";
                    for (m = 0, len1 = sizes.length; m < len1; m++) {
                      i = sizes[m];
                      sizes_html = sizes_html + "\n<span>" + i + "</span>";
                    }
                    if (_html_price["colors"] === void 0) {
                      colors = [];
                    } else {
                      colors = _html_price["colors"];
                    }
                    colors_html = "";
                    for (n = 0, len2 = colors.length; n < len2; n++) {
                      i = colors[n];
                      colors_html = colors_html + "\n<span>" + i + "</span>";
                    }
                    if (_html_price["prices"] === void 0) {
                      prices = [];
                    } else {
                      prices = _html_price["prices"];
                    }
                    prices_html = "";
                    for (o = prices.length - 1; o >= 0; o += -1) {
                      i = prices[o];
                      prices_html = prices_html + "\n<div class=\"prices_btn\" data-price=" + i[1] + ">" + i[0] + " person: " + comment_json["currency-now"] + "$" + ((i[1] / 100.0).toFixed(2)) + "</div>";
                    }
                    _html_prices_new = _html_prices_new + "\n<div class=\"prices_btns_area\">\n    <div class=\"name\">PN:" + name + "</div>\n    <div class=\"sizes\">sizes:" + sizes_html + "</div>\n    <div class=\"colors\">colors:" + colors_html + "</div>\n    <div class=\"prices\">\n        " + prices_html + "\n    </div>\n</div>";
                    ref2 = _html_price["prices"];
                    for (p = 0, len3 = ref2.length; p < len3; p++) {
                      i = ref2[p];
                      if (_html_prices_new_list[i[0]] === void 0) {
                        _html_prices_new_list[i[0]] = {
                          "min": i[1],
                          "max": i[1]
                        };
                      } else {
                        if (_html_prices_new_list[i[0]]["min"] > i[1]) {
                          _html_prices_new_list[i[0]]["min"] = i[1];
                        }
                        if (_html_prices_new_list[i[0]]["max"] < i[1]) {
                          _html_prices_new_list[i[0]]["max"] = i[1];
                        }
                      }
                    }
                  }
                  console.log(_html_prices_new_list);
                  _html_prices = [];
                  for (k in _html_prices_new_list) {
                    v = _html_prices_new_list[k];
                    _html_prices.push([k, v]);
                  }
                  _html_prices.sort(function(a, b) {
                    return b[0] - a[0];
                  });
                  for (q = 0, len4 = _html_prices.length; q < len4; q++) {
                    _html_price = _html_prices[q];
                    line_through_class_str = "";
                    if (("" + _html_price[0]) === "1") {
                      line_through_class_str = "line_through";
                    }
                    _html_prices_html = _html_prices_html + "\n<div class=\"good_info_price " + line_through_class_str + "\" data-num=\"" + _html_price[0] + "\">\n    <span>" + comment_json["currency-now"] + "$</span>\n    <span>" + ((_html_price[1]["min"] / 100.0).toFixed(2)) + "</span>\n    <span>+</span>\n    <span class=\"hide\">" + ((_html_price[1]["max"] / 100.0).toFixed(2)) + "</span>\n</div>";
                  }
                  uuid_now = uuid2(6, null);
                  store_score = stores_info[store_id]["store_score"];
                  _html = "<div class=\"ground_good_item\" data-add-num=\"" + add_num + "\" data-product=\"" + chat_id + "\">\n    <div class=\"ground_good_item_info_top\">\n        <div class=\"ground_good_item_store_id\">0x" + store_id + "</div>\n        <div class=\"ground_good_item_store_score\">" + store_score + "</div>\n    </div>\n    <div class=\"ground_good_item_imgs\">\n        <img class=\"ground_good_item_img\" data-uuid=\"" + uuid_now + "\" src=\"" + comment_json["gallery-items"][0] + "\">\n        <script>\n            a_" + uuid_now + "_imgs_num = 0\n            a_" + uuid_now + "_imgs = " + (JSON.stringify(comment_json["gallery-items"])) + "\n            setInterval(function(){\n                a_" + uuid_now + "_imgs_num +=1\n                $(\".ground_good_item_img[data-uuid=" + uuid_now + "]\").attr(\"src\",a_" + uuid_now + "_imgs[a_" + uuid_now + "_imgs_num])\n                if (a_" + uuid_now + "_imgs_num > a_" + uuid_now + "_imgs.length -1){\n                    a_" + uuid_now + "_imgs_num = -1\n                }\n\n                },2000)\n        </script>\n    </div>\n    <div class=\"ground_good_item_info\">\n        <div class=\"good_info_name\">" + comment_json["product-name"] + "</div>\n        <div class=\"good_info_sell_num\">1000+</div>\n        " + _html_prices_html + "\n        <div class=\"good_info_relative\">\n            <div class=\"good_info_headimgurl\" data-store-id=\"" + store_id + "\">\n                <img class=\"good_info_headimgurl_img\" src=\"" + stores_info[store_id]["headimgurl"] + "\">\n            </div>\n            <div class=\"good_info_title\">" + comment_json["detail-box-title"] + "</div>\n        </div>\n    </div>\n</div>\n<div class=\"html_prices_new\">\n    " + _html_prices_new + "\n</div>";
                  document.title = comment_json["product-name"] + " | " + comment_json["detail-box-title"];
                  $(".ground_goods_area_main").append(_html);
                  return;
                }
              }
            }
            last_comment_id = data.last_comment_id;
            if (last_comment_id !== null) {
              return xialiwei_find_good(chat_id, last_comment_id);
            }
          } else if (data.info === "error") {

          }
        },
        error: function(data) {
          return console.log(data);
        }
      });
    };
    xialiwei_goods_list = [
      {
        "store": STORE_ID,
        "product": PRODUCT_ID
      }
    ];
    stores_info = {};
    xialiwei_goods_list_load = function() {
      var good_info, j, len, store_ids;
      store_ids = [];
      for (j = 0, len = xialiwei_goods_list.length; j < len; j++) {
        good_info = xialiwei_goods_list[j];
        store_ids.push(good_info["store"]);
      }
      return $.ajax({
        url: "/api/store/info",
        type: "POST",
        dataType: "json",
        data: {
          store_ids: JSON.stringify(store_ids)
        },
        success: function(data) {
          var a_good, a_store, good_info_add_num, l, len1, len2, m, ref, result, results;
          console.log(data);
          if (data.info === "ok") {
            ref = data.result;
            for (l = 0, len1 = ref.length; l < len1; l++) {
              result = ref[l];
              stores_info[result["store_id"]] = result;
            }
          }
          good_info_add_num = 0;
          results = [];
          for (m = 0, len2 = xialiwei_goods_list.length; m < len2; m++) {
            good_info = xialiwei_goods_list[m];
            a_store = good_info["store"];
            a_good = good_info["product"];
            xialiwei_find_good(a_good, null, a_store, good_info_add_num);
            results.push(good_info_add_num += 1);
          }
          return results;
        },
        error: function(data) {
          return console.log(data);
        }
      });
    };
    $(window).on("load", function() {
      return xialiwei_goods_list_load();
    });
    $("body").on("click", ".sizes>span", function(evt) {
      if ($(this).hasClass("current")) {
        return $(this).removeClass("current");
      } else {
        $(this).parents(".sizes").find("span").removeClass("current");
        return $(this).addClass("current");
      }
    });
    $("body").on("click", ".colors>span", function(evt) {
      if ($(this).hasClass("current")) {
        return $(this).removeClass("current");
      } else {
        $(this).parents(".colors").find("span").removeClass("current");
        return $(this).addClass("current");
      }
    });
    return $("body").on("click", ".prices_btn", function(evt) {
      var color, name, size;
      name = $(this).parents(".prices_btns_area").first().find(".name").text();
      size = $(this).parents(".prices_btns_area").first().find(".sizes").find(".current").text();
      color = $(this).parents(".prices_btns_area").first().find(".colors").find(".current").text();
      return $.ajax({
        url: "/api/stripe/pay_product",
        type: "POST",
        dataType: "json",
        data: {
          currency: "cad",
          name: name + " " + size + " " + color,
          unit_amount: $(this).attr("data-price"),
          quantity: 1,
          image: $(".ground_good_item_img").attr("src")
        },
        success: function(data) {
          var new_blank;
          console.log(data);
          if (data.info === "ok") {
            new_blank = window.open('_blank');
            if (new_blank === null) {
              return window.location.href = data.redirect_uri;
            } else {
              return new_blank.location = data.redirect_uri;
            }
          }
        },
        error: function(data) {
          return console.log(data);
        }
      });
    });
  });

}).call(this);
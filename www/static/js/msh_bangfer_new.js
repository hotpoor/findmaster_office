// Generated by CoffeeScript 1.12.7
(function() {
  var Hs, root;

  root = typeof exports !== "undefined" && exports !== null ? exports : this;

  root.Hs || (root.Hs = {});

  Hs = root.Hs;

  $(function() {
    console.log("msh bangfer new coffee");
    return $(window).on("load", function(evt) {
      var _w;
      _w = $(".sharetimeline_ischool_card").width();
      $(".sharetimeline_ischool_card").append("<div class=\"msh_menus\" style=\"\n    color: #bfbfbf;     font-size: 12px;\n    display:flex;       flex:3;\n    position:fixed;     bottom:0px;\n    width:" + _w + "px;      height:50px;\n    background:white;   box-shadow:0px -4px 4px -3px rgba(0,0,0,0.1);\n    \">\n    <div style=\"flex:1;text-align:center;cursor:pointer;\">\n        <a href=\"http://www.hotpoor.org/home/app/bangfer/028ee947c4ee4b3ea2927cccf8199976?v=msh&ischool_id=d35aee6e4e1f47ffbce49dba54b466a7\" target=\"_blank\">\n        <img style=\"margin-top:6px;width:20px;20px;\" src=\"http://msh-cdn0.xialiwei.com/41af9eed997d4871aff8b691196f48d1_44663bade6a9bd241f578c4e84a1712d?imageView2\">\n        <br><span style=\"color: #bfbfbf;\">讨论</span>\n        </a>\n    </div>\n    <div style=\"flex:1;text-align:center;cursor:pointer;\">\n        <a href=\"https://msh.xialiwei.com/home/page/7b4f5bc4b6694878b9f98a1f346ee647\" target=\"_blank\">\n        <img style=\"margin-top:6px;width:20px;20px;\" src=\"http://msh-cdn0.xialiwei.com/41af9eed997d4871aff8b691196f48d1_fea1af9d8826f03c77c374ae5dba8f70?imageView2\">\n        <br><span style=\"color: #bfbfbf;\">新品速递</span>\n        </a>\n    </div>\n    <div style=\"flex:1;text-align:center;cursor:pointer;\">\n        <a href=\"https://msh.xialiwei.com/home/page/1a158427afe543bda309c0c6ddce2cbf\" target=\"_blank\">\n        <img style=\"margin-top:6px;width:20px;20px;\" src=\"http://msh-cdn0.xialiwei.com/41af9eed997d4871aff8b691196f48d1_aed097ba3b821629d5a21c304420f9dd?imageView2\">\n        <br><span style=\"color: #bfbfbf;\">我的会员</span>\n        </a>\n    </div>\n</div>");
      return $.ajax({
        url: "/api/user/login/get",
        data: null,
        dataType: 'json',
        type: 'POST',
        success: function(data) {
          if (data.login != null) {
            return $.ajax({
              url: "https://www.moshanghua2020.net/api/msh/level/check",
              data: {
                t: (new Date()).getTime(),
                openid: data.login.split("_@@_")[1],
                app: "msh"
              },
              dataType: 'json',
              type: 'GET',
              success: function(data) {
                console.log(data);
                if (data.info === "ok") {
                  if (parseInt(data.msh_qrcodepackage_num) > 0) {
                    $(".sharetimeline_content_area").removeClass("hide");
                    return $(".sharetimeline_user_info").prepend("<div class=\"sharetimeline_user_name_level\"\n    style=\"\n        position: absolute;\n        right: 106px;\n        margin-top: 60px;\n        font-size: 14px;\n        color: #408a9f;\n        font-weight: bold;\n    \">Level " + data.msh_qrcodepackage_num + "</div>");
                  }
                } else {
                  return alert(data.about);
                }
              },
              error: function(data) {
                return console.log(data);
              }
            });
          }
        },
        error: function(data) {
          return console.log(data);
        }
      });
    });
  });

}).call(this);

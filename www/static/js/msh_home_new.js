// Generated by CoffeeScript 1.12.7
(function() {
  var Hs, root;

  root = typeof exports !== "undefined" && exports !== null ? exports : this;

  root.Hs || (root.Hs = {});

  Hs = root.Hs;

  Hs.action_current = "home";

  Hs.msh_color = "#42889e";

  $(function() {
    var img_flag, img_flag_max, img_num, img_width, load_msh_home_new_banner_imgs, load_msh_home_new_banner_imgs_animate;
    console.log("msh home new");
    $(".base_area").append("<div class=\"msh_area_width msh_area_normal\" style=\"background-color:#3c447b;\">\n    <div class=\"msh_area_banner_imgs_area\" style=\"position:relative;\">\n        <div class=\"msh_area_banner_imgs\">\n            <div class=\"msh_area_banner_img_area\">\n                <img class=\"msh_area_banner_img\">\n            </div>\n        </div>\n        <div style=\"\n            width: 100%;\n            height: 15px;\n            position: absolute;\n            bottom: 0px;\n            left: 0px;\n            background-color: #3c447b;\n            border-radius: 15px 15px 0px 0px;\n        \"></div>\n    </div>\n    <div class=\"msh_area_pages_area\" style=\"display:none;\">\n        <div class=\"msh_area_pages\">\n            <div style=\"width:100%;display:flex;flex-wrap:wrap;\">\n                <div style=\"width:50%;height:auto;position:relative;\">\n                    <img style=\"width:100%;\" src=\"http://msh-cdn0.qianshanghua.com/f644eba0484b45c784b712f562dcc095_b679c7789fb2f27e07e34487a9a10445?imageView2\">\n                </div>\n                <div style=\"width:50%;height:auto;position:relative;\">\n                    <img style=\"width:100%;\" src=\"http://msh-cdn0.qianshanghua.com/f644eba0484b45c784b712f562dcc095_fd7bb0d4853eb6d12be15f63368e0c2f?imageView2\">\n                </div>\n                <div style=\"width:50%;height:auto;position:relative;\">\n                    <img style=\"width:100%;\" src=\"http://msh-cdn0.qianshanghua.com/f644eba0484b45c784b712f562dcc095_1e400ad5e4dfa0030ebe1841160c2361?imageView2\">\n                </div>\n                <div style=\"width:50%;height:auto;position:relative;\">\n                    <img style=\"width:100%;\" src=\"http://msh-cdn0.qianshanghua.com/f644eba0484b45c784b712f562dcc095_2c8bc7c5e451879f3f634a2caf374991?imageView2\">\n                </div>\n            </div>\n            <div class=\"msh_area_page_btn\" style=\"display:none;\" data-action=\"ip_market\"><a href=\"/home/page/cdecaaad5c5049f3b6558f2c6587cb48\">IP故事</a></div>\n            <div class=\"msh_area_page_btn\" style=\"display:none;\" data-action=\"pinyan\"><a href=\"/home/msh/hollow\">树洞</a></div>\n            <div class=\"msh_area_page_btn\" style=\"display:none;\" data-action=\"gongyi\">公益</div>\n            <div class=\"msh_area_page_btn\" style=\"display:none;\" data-action=\"games\">游戏</div>\n        </div>\n    </div>\n    <div class=\"msh_area_pages_area_style_popmarkt\">\n        <div class=\"msh_area_pages_style_popmarkt\">\n            <div class=\"msh_area_page_style_popmarkt\" style=\"margin-top:-10px;\">\n                <div class=\"msh_area_page_style_popmarkt_title\">\n                    <div class=\"msh_area_page_style_popmarkt_title_main\">\n                        <p class=\"msh_area_page_style_popmarkt_title_main_base\">PUCO</p>\n                        <p class=\"msh_area_page_style_popmarkt_title_main_more\">SELECT</p>\n                    </div>\n                    <div class=\"msh_area_page_style_popmarkt_title_plus\">\n                        <p class=\"msh_area_page_style_popmarkt_title_plus_base\">Pick U Color</p>\n                        <p class=\"msh_area_page_style_popmarkt_title_plus_more\">An Interesting Story</p>\n                    </div>\n                </div>\n                <div style=\"width:100%;display:flex;flex-wrap:wrap;\">\n                    <div style=\"width:50%;height:auto;position:relative;\">\n                        <a href=\"#popmarket_line_IP故事\"><img style=\"width:100%;\" src=\"http://msh-cdn0.qianshanghua.com/f644eba0484b45c784b712f562dcc095_b679c7789fb2f27e07e34487a9a10445?imageView2\">\n                        </a>\n                    </div>\n                    <div style=\"width:50%;height:auto;position:relative;\">\n                        <a href=\"#popmarket_line_时光机\"><img style=\"width:100%;\" src=\"http://msh-cdn0.qianshanghua.com/f644eba0484b45c784b712f562dcc095_fd7bb0d4853eb6d12be15f63368e0c2f?imageView2\">\n                        </a>\n                    </div>\n                    <div style=\"width:50%;height:auto;position:relative;\">\n                        <a href=\"#popmarket_line_兑换商店\"><img style=\"width:100%;\" src=\"http://msh-cdn0.qianshanghua.com/f644eba0484b45c784b712f562dcc095_1e400ad5e4dfa0030ebe1841160c2361?imageView2\">\n                        </a>\n                    </div>\n                    <div style=\"width:50%;height:auto;position:relative;\">\n                        <img style=\"width:100%;\" src=\"http://msh-cdn0.qianshanghua.com/f644eba0484b45c784b712f562dcc095_2c8bc7c5e451879f3f634a2caf374991?imageView2\">\n                    </div>\n                </div>\n            </div>\n            <div class=\"msh_area_page_style_popmarkt\" id=\"popmarket_line_IP故事\">\n                <div class=\"msh_area_page_style_popmarkt_title\">\n                    <div class=\"msh_area_page_style_popmarkt_title_main\">\n                        <p class=\"msh_area_page_style_popmarkt_title_main_base\">IP故事</p>\n                        <p class=\"msh_area_page_style_popmarkt_title_main_more\">STORIES</p>     \n                    </div>\n                    <div class=\"msh_area_page_style_popmarkt_title_plus\">\n                        <p class=\"msh_area_page_style_popmarkt_title_plus_base\">Pick U Color</p>\n                        <p class=\"msh_area_page_style_popmarkt_title_plus_more\">An Interesting Story</p>\n                    </div>\n                </div>\n                <div class=\"msh_area_page_style_popmarkt_goods_area\">\n                    <div class=\"msh_area_page_style_popmarkt_goods\">\n                        <div class=\"msh_area_page_style_popmarkt_good\" style=\"margin:8px 2px;\">\n                            <img class=\"msh_area_page_style_popmarkt_good_img msh_area_page_style_popmarkt_good_img_pre\"\n                                data-src=\"http://msh-cdn0.qianshanghua.com/dbef06e02aca452e8509398efdac46ce_6b4800bbf17a9816927ae26005862cab?imageView2\"\n                                src=\"http://msh-cdn0.qianshanghua.com/f644eba0484b45c784b712f562dcc095_5ea08f6814c1e1f478ffb0f97bec8d73?imageView2\"\n                                style=\"width: 160px;height: auto;\">\n                        </div>\n                        <div class=\"msh_area_page_style_popmarkt_good\" style=\"margin:8px 2px;\">\n                            <img class=\"msh_area_page_style_popmarkt_good_img msh_area_page_style_popmarkt_good_img_pre\"\n                                data-src=\"http://msh-cdn0.qianshanghua.com/dbef06e02aca452e8509398efdac46ce_176d0346f56e34b00a4f24c81b76bba7?imageView2\"\n                                src=\"http://msh-cdn0.qianshanghua.com/f644eba0484b45c784b712f562dcc095_3fb2f67829174012d0f7f098dea07ed5?imageView2\"\n                                style=\"width: 160px;height: auto;\">\n                        </div>\n                        <div class=\"msh_area_page_style_popmarkt_good\" style=\"margin:8px 2px;\">\n                            <img class=\"msh_area_page_style_popmarkt_good_img msh_area_page_style_popmarkt_good_img_pre\"\n                                data-src=\"http://msh-cdn0.qianshanghua.com/dbef06e02aca452e8509398efdac46ce_e4cafbfff6d342462c05e531e4e617a7?imageView2\"\n                                src=\"http://msh-cdn0.qianshanghua.com/f644eba0484b45c784b712f562dcc095_e3d708239c0106b65be218b5287013bd?imageView2\"\n                                style=\"width: 160px;height: auto;\">\n                        </div>\n                        <div class=\"msh_area_page_style_popmarkt_good\" style=\"margin:8px 2px;\">\n                            <img class=\"msh_area_page_style_popmarkt_good_img msh_area_page_style_popmarkt_good_img_pre\"\n                                data-src=\"http://msh-cdn0.qianshanghua.com/dbef06e02aca452e8509398efdac46ce_5c947303c03919ba92667988f762fb82?imageView2\"\n                                src=\"http://msh-cdn0.qianshanghua.com/f644eba0484b45c784b712f562dcc095_bb75e44a3e77e9f36e9fa9d87c64f2a0?imageView2\"\n                                style=\"width: 160px;height: auto;\">\n                        </div>\n                    </div>\n                </div>\n            </div>\n            <div class=\"msh_area_page_style_popmarkt\" id=\"popmarket_line_时光机\">\n                <div class=\"msh_area_page_style_popmarkt_title\">\n                    <div class=\"msh_area_page_style_popmarkt_title_main\">\n                        <p class=\"msh_area_page_style_popmarkt_title_main_base\">时光机</p>\n                        <p class=\"msh_area_page_style_popmarkt_title_main_more\">Time Machine</p>     \n                    </div>\n                    <div class=\"msh_area_page_style_popmarkt_title_plus\">\n                        <p class=\"msh_area_page_style_popmarkt_title_plus_base\">Pick U Color</p>\n                        <p class=\"msh_area_page_style_popmarkt_title_plus_more\">An Interesting Story</p>\n                    </div>\n                </div>\n                <div class=\"msh_area_page_style_popmarkt_goods_area\">\n                    <div class=\"msh_area_page_style_popmarkt_goods\">\n                        <div class=\"msh_area_page_style_popmarkt_good\" style=\"margin:8px 2px;\">\n                            <a target=\"_blank\" href=\"/home/msh/hollow/a220ce8a87294ab087a2696803cf4f0d\">\n                            <img class=\"msh_area_page_style_popmarkt_good_img\"\n                                src=\"http://msh-cdn0.qianshanghua.com/f644eba0484b45c784b712f562dcc095_d91d816a632eacdb22379ca559447b58?imageView2\"\n                                style=\"width: 160px;height: auto;\">\n                            </a>\n                        </div>\n                        <div class=\"msh_area_page_style_popmarkt_good\" style=\"margin:8px 2px;\">\n                            <a target=\"_blank\" href=\"/home/msh/hollow/35c8b38ca3c0445995512a826169f50d\">\n                            <img class=\"msh_area_page_style_popmarkt_good_img\"\n                                src=\"http://msh-cdn0.qianshanghua.com/f644eba0484b45c784b712f562dcc095_473363e96100189419fc063552629f83?imageView2\"\n                                style=\"width: 160px;height: auto;\">\n                            </a>\n                        </div>\n                        <div class=\"msh_area_page_style_popmarkt_good\" style=\"margin:8px 2px;\">\n                            <a target=\"_blank\" href=\"/home/msh/hollow/27c19e2460c546e3823e5d1d9b8024e3\">\n                            <img class=\"msh_area_page_style_popmarkt_good_img\"\n                                src=\"http://msh-cdn0.qianshanghua.com/f644eba0484b45c784b712f562dcc095_e5dc158c34dc09274d3ef870ee57ca5d?imageView2\"\n                                style=\"width: 160px;height: auto;\">\n                            </a>\n                        </div>\n                        <div class=\"msh_area_page_style_popmarkt_good\" style=\"margin:8px 2px;\">\n                            <a target=\"_blank\" href=\"/home/msh/hollow/3adffb06a860481384961b32a410cfa4\">\n                            <img class=\"msh_area_page_style_popmarkt_good_img\"\n                                src=\"http://msh-cdn0.qianshanghua.com/f644eba0484b45c784b712f562dcc095_fffd2109ce71df709c246f75a45178ce?imageView2\"\n                                style=\"width: 160px;height: auto;\">\n                            </a>\n                        </div>\n                        <div class=\"msh_area_page_style_popmarkt_good\" style=\"margin:8px 2px;\">\n                            <a target=\"_blank\" href=\"/home/msh/hollow/0ee0edd7fd1d433d898235df5b7b3e60\">\n                            <img class=\"msh_area_page_style_popmarkt_good_img\"\n                                src=\"http://msh-cdn0.qianshanghua.com/f644eba0484b45c784b712f562dcc095_2c2d402985c3bd9ed890795bef3de61f?imageView2\"\n                                style=\"width: 160px;height: auto;\">\n                            </a>\n                        </div>\n                        <div class=\"msh_area_page_style_popmarkt_good\" style=\"margin:8px 2px;\">\n                            <a target=\"_blank\" href=\"/home/msh/hollow/59e89558c50244df81a3e5bf4946f187\">\n                            <img class=\"msh_area_page_style_popmarkt_good_img\"\n                                src=\"http://msh-cdn0.qianshanghua.com/f644eba0484b45c784b712f562dcc095_4d8238c1c4732ddff6067b3b92102679?imageView2\"\n                                style=\"width: 160px;height: auto;\">\n                            </a>\n                        </div>\n                    </div>\n                </div>\n            </div>\n            <div class=\"msh_area_page_style_popmarkt\" id=\"popmarket_line_兑换商店\">\n                <div class=\"msh_area_page_style_popmarkt_title\">\n                    <div class=\"msh_area_page_style_popmarkt_title_main\">\n                        <p class=\"msh_area_page_style_popmarkt_title_main_base\">兑换商店</p>\n                        <p class=\"msh_area_page_style_popmarkt_title_main_more\">Token Store</p>     \n                    </div>\n                    <div class=\"msh_area_page_style_popmarkt_title_plus\">\n                        <p class=\"msh_area_page_style_popmarkt_title_plus_base\">Pick U Color</p>\n                        <p class=\"msh_area_page_style_popmarkt_title_plus_more\">An Interesting Story</p>\n                    </div>\n                </div>\n                <div class=\"msh_area_page_style_popmarkt_goods_area\">\n                    <div class=\"msh_area_page_style_popmarkt_goods\">\n                        <div class=\"msh_area_page_style_popmarkt_good\" style=\"margin:8px 2px;\">\n                            <img class=\"msh_area_page_style_popmarkt_good_img\"\n                                src=\"http://msh-cdn0.qianshanghua.com/f644eba0484b45c784b712f562dcc095_66995aa738e364c3472f40fb51c5809b?imageView2\"\n                                style=\"width: 160px;height: auto;\">\n                        </div>\n                    </div>\n                </div>\n            </div>\n        </div>\n    </div>\n</div>\n<div class=\"msh_area_width msh_area_bottom_fixed\">\n    <div class=\"msh_area_bottom_btns\">\n        <div class=\"msh_area_bottom_btn btn_current\" align=\"center\" data-action=\"home\">\n            <div class=\"msh_area_bottom_btn_content\">\n                <div class=\"msh_icon msh_icon_home\"></div>\n                <div class=\"msh_icon_text\">首页</div>\n            </div>\n        </div>\n        <div class=\"msh_area_bottom_btn\"  align=\"center\" data-action=\"story\">\n            <div class=\"msh_area_bottom_btn_content\">\n                <div class=\"msh_icon msh_icon_story\"></div>\n                <div class=\"msh_icon_text\">品牌故事</div>\n            </div>\n        </div>\n        <div class=\"msh_area_bottom_btn\"  align=\"center\" data-action=\"giftclub\" style=\"display:none;\">\n            <div class=\"msh_area_bottom_btn_content\">\n                <div class=\"msh_icon msh_icon_giftclub\"></div>\n                <div class=\"msh_icon_text\">俱乐部</div>\n            </div>\n        </div>\n        <div class=\"msh_area_bottom_btn\"  align=\"center\" data-action=\"person\">\n            <div class=\"msh_area_bottom_btn_content\">\n                <div class=\"msh_icon msh_icon_person\"></div>\n                <div class=\"msh_icon_text\">我的会员</div>\n            </div>\n        </div>\n    </div>\n</div>");
    load_msh_home_new_banner_imgs_animate = null;
    img_num = null;
    img_flag = null;
    img_flag_max = null;
    img_width = null;
    load_msh_home_new_banner_imgs = function() {
      var i, img, len;
      clearInterval(load_msh_home_new_banner_imgs_animate);
      console.log("MSH_HOME_NEW_BANNER_IMGS", MSH_HOME_NEW_BANNER_IMGS);
      if (typeof MSH_HOME_NEW_BANNER_IMGS !== "undefined" && MSH_HOME_NEW_BANNER_IMGS !== null) {
        if (MSH_HOME_NEW_BANNER_IMGS.length > 0) {
          $(".msh_area_banner_imgs").empty();
          img_num = 0;
          img_flag = 0;
          img_flag_max = MSH_HOME_NEW_BANNER_IMGS.length;
          img_width = $(".msh_area_banner_imgs_area").width();
          for (i = 0, len = MSH_HOME_NEW_BANNER_IMGS.length; i < len; i++) {
            img = MSH_HOME_NEW_BANNER_IMGS[i];
            $(".msh_area_banner_imgs").append("<div class=\"msh_area_banner_img_area\" style=\"width:" + img_width + "px;left:" + (img_num * img_width) + "px;\">\n    <img class=\"msh_area_banner_img\" src=\"" + img + "\">\n</div>");
            img_num += 1;
          }
          return load_msh_home_new_banner_imgs_animate = setInterval(function() {
            img_flag += 1;
            if (img_flag === img_flag_max) {
              img_flag = 0;
            }
            console.log("img_flag", img_flag, img_flag_max, img_width, img_flag * img_width);
            return $(".msh_area_banner_imgs").animate({
              "scrollLeft": img_flag * img_width
            });
          }, 5000);
        }
      }
    };
    setTimeout(function() {
      return load_msh_home_new_banner_imgs();
    }, 1000);
    $(window).on("resize", function() {
      return load_msh_home_new_banner_imgs();
    });
    $("body").on("click", ".msh_area_bottom_btns>.msh_area_bottom_btn", function(evt) {
      var dom, dom_action;
      dom = $(this);
      dom_action = dom.attr("data-action");
      $(".msh_area_bottom_btns>.msh_area_bottom_btn").removeClass("btn_current");
      dom.addClass("btn_current");
      console.log("dom_action", dom_action);
      if (dom_action === "story") {
        if (IS_WEIXIN) {
          return window.location.href = "https://mp.weixin.qq.com/s/zm0syYdWWi-Iu2QDqfi5VQ";
        } else {
          return window.location.href = "/home/page/689f864598af4ed29f705101c82bcc00";
        }
      } else if (dom_action === "giftclub") {
        return window.location.href = "/home/page/40e7cb27fc604dca84c6ab84716bbed8";
      } else if (dom_action === "person") {
        return window.location.href = "/home/page/25df4bb293d046fc8b35358f9cc0c017";
      }
    });
    return $("body").on("click", ".msh_area_page_style_popmarkt_good_img_pre", function(evt) {
      var current, dom, i, len, pre_img, pre_img_doms, urls;
      pre_img_doms = $(".msh_area_page_style_popmarkt_good_img_pre");
      urls = [];
      for (i = 0, len = pre_img_doms.length; i < len; i++) {
        pre_img = pre_img_doms[i];
        urls.push($(pre_img).attr("data-src"));
      }
      dom = $(this);
      current = dom.attr("data-src");
      if (IS_WEIXIN) {
        return wx.previewImage({
          current: current,
          urls: urls
        });
      } else {
        return window.location.href = current;
      }
    });
  });

}).call(this);

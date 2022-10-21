root = exports ? this
# !!!! Hotpoor root object
root.Hs or= {}
Hs = root.Hs
Hs.action_current = "home"

Hs.msh_color = "#42889e"

$ ->
    console.log "msh home new"
    $(".base_area").append """
    <div class="msh_area_width msh_area_normal" style="background-color:#3c447b;">
        <div class="msh_area_banner_imgs_area" style="position:relative;">
            <div class="msh_area_banner_imgs">
                <div class="msh_area_banner_img_area">
                    <img class="msh_area_banner_img">
                </div>
            </div>
            <div style="
                width: 100%;
                height: 15px;
                position: absolute;
                bottom: 0px;
                left: 0px;
                background-color: #3c447b;
                border-radius: 15px 15px 0px 0px;
            "></div>
        </div>
        <div class="msh_area_pages_area" style="display:none;">
            <div class="msh_area_pages">
                <div style="width:100%;display:flex;flex-wrap:wrap;">
                    <div style="width:50%;height:auto;position:relative;">
                        <img style="width:100%;" src="http://msh-cdn0.qianshanghua.com/f644eba0484b45c784b712f562dcc095_42c8b7be0d5b7fbb3ec6a69cf17dd5c6?imageView2">
                        <span style="position: absolute;top: 15px;left: 15px;color: #823B43;font-size: 12px;">IP故事</span>
                    </div>
                    <div style="width:50%;height:auto;position:relative;">
                        <img style="width:100%;" src="http://msh-cdn0.qianshanghua.com/f644eba0484b45c784b712f562dcc095_2b69b220de4f499d30ccb76444c233c1?imageView2">
                        <span style="position: absolute;top: 15px;left: 15px;color: #823B43;font-size: 12px;">时光机</span>
                    </div>
                    <div style="width:50%;height:auto;position:relative;">
                        <img style="width:100%;" src="http://msh-cdn0.qianshanghua.com/f644eba0484b45c784b712f562dcc095_c13b03b90566899e53b8c9fdcbc9664e?imageView2">
                        <span style="position: absolute;top: 15px;left: 15px;color: #823B43;font-size: 12px;">积分商城</span>
                    </div>
                    <div style="width:50%;height:auto;position:relative;">
                        <img style="width:100%;" src="http://msh-cdn0.qianshanghua.com/f644eba0484b45c784b712f562dcc095_66995aa738e364c3472f40fb51c5809b?imageView2">
                    </div>
                </div>
                <div class="msh_area_page_btn" style="display:none;" data-action="ip_market"><a href="/home/page/cdecaaad5c5049f3b6558f2c6587cb48">IP故事</a></div>
                <div class="msh_area_page_btn" style="display:none;" data-action="pinyan"><a href="/home/msh/hollow">树洞</a></div>
                <div class="msh_area_page_btn" style="display:none;" data-action="gongyi">公益</div>
                <div class="msh_area_page_btn" style="display:none;" data-action="games">游戏</div>
            </div>
        </div>
        <div class="msh_area_pages_area_style_popmarkt">
            <div class="msh_area_pages_style_popmarkt">
                <div class="msh_area_page_style_popmarkt" style="margin-top:-10px;">
                    <div class="msh_area_page_style_popmarkt_title">
                        <div class="msh_area_page_style_popmarkt_title_main">
                            <p class="msh_area_page_style_popmarkt_title_main_base">PUCO</p>
                            <p class="msh_area_page_style_popmarkt_title_main_more">SELECT</p>
                        </div>
                        <div class="msh_area_page_style_popmarkt_title_plus">
                            <p class="msh_area_page_style_popmarkt_title_plus_base">Pick U Color</p>
                            <p class="msh_area_page_style_popmarkt_title_plus_more">An Interesting Story</p>
                        </div>
                    </div>
                    <div style="width:100%;display:flex;flex-wrap:wrap;">
                        <div style="width:50%;height:auto;position:relative;">
                            <a href="#popmarket_line_IP故事"><img style="width:100%;" src="http://msh-cdn0.qianshanghua.com/f644eba0484b45c784b712f562dcc095_42c8b7be0d5b7fbb3ec6a69cf17dd5c6?imageView2">
                            <span style="position: absolute;top: 15px;left: 15px;color: #823B43;font-size: 12px;">IP故事</span>
                            </a>
                        </div>
                        <div style="width:50%;height:auto;position:relative;">
                            <a href="#popmarket_line_时光机"><img style="width:100%;" src="http://msh-cdn0.qianshanghua.com/f644eba0484b45c784b712f562dcc095_2b69b220de4f499d30ccb76444c233c1?imageView2">
                            <span style="position: absolute;top: 15px;left: 15px;color: #823B43;font-size: 12px;">时光机</span>
                            </a>
                        </div>
                        <div style="width:50%;height:auto;position:relative;">
                            <a href="#popmarket_line_兑换商店"><img style="width:100%;" src="http://msh-cdn0.qianshanghua.com/f644eba0484b45c784b712f562dcc095_c13b03b90566899e53b8c9fdcbc9664e?imageView2">
                            <span style="position: absolute;top: 15px;left: 15px;color: #823B43;font-size: 12px;">积分商城</span>
                            </a>
                        </div>
                        <div style="width:50%;height:auto;position:relative;">
                            <img style="width:100%;" src="http://msh-cdn0.qianshanghua.com/f644eba0484b45c784b712f562dcc095_66995aa738e364c3472f40fb51c5809b?imageView2">
                        </div>
                    </div>
                </div>
                <div class="msh_area_page_style_popmarkt" id="popmarket_line_IP故事">
                    <div class="msh_area_page_style_popmarkt_title">
                        <div class="msh_area_page_style_popmarkt_title_main">
                            <p class="msh_area_page_style_popmarkt_title_main_base">IP故事</p>
                            <p class="msh_area_page_style_popmarkt_title_main_more">STORIES</p>     
                        </div>
                        <div class="msh_area_page_style_popmarkt_title_plus">
                            <p class="msh_area_page_style_popmarkt_title_plus_base">Pick U Color</p>
                            <p class="msh_area_page_style_popmarkt_title_plus_more">An Interesting Story</p>
                        </div>
                    </div>
                    <div class="msh_area_page_style_popmarkt_goods_area">
                        <div class="msh_area_page_style_popmarkt_goods">
                            <div class="msh_area_page_style_popmarkt_good">
                                <div class="msh_area_page_style_popmarkt_good_content">
                                    <div class="msh_area_page_style_popmarkt_good_img_area">
                                        <img class="msh_area_page_style_popmarkt_good_img" src="http://msh-cdn0.moshanghua2020.net/6af6e65f84464b9d9ff41caef80b4eff_1d1c048488f74a7b496a4c4037997079?imageView2">
                                    </div>
                                    <div class="msh_area_page_style_popmarkt_good_title">
                                        标题·Title
                                    </div>
                                    <div class="msh_area_page_style_popmarkt_good_info">
                                        <div class="msh_area_page_style_popmarkt_good_desc">
                                            描述·DESC
                                        </div>
                                        <div class="msh_area_page_style_popmarkt_good_price_info">
                                            ￥100<span>起</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="msh_area_page_style_popmarkt_good">
                                <div class="msh_area_page_style_popmarkt_good_content">
                                    <div class="msh_area_page_style_popmarkt_good_img_area">
                                        <img class="msh_area_page_style_popmarkt_good_img" src="http://msh-cdn0.moshanghua2020.net/6af6e65f84464b9d9ff41caef80b4eff_1d1c048488f74a7b496a4c4037997079?imageView2">
                                    </div>
                                    <div class="msh_area_page_style_popmarkt_good_title">
                                        标题·Title
                                    </div>
                                    <div class="msh_area_page_style_popmarkt_good_info">
                                        <div class="msh_area_page_style_popmarkt_good_price_info only">
                                            ￥100<span>起</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="msh_area_page_style_popmarkt_good">
                                <div class="msh_area_page_style_popmarkt_good_content">
                                    <div class="msh_area_page_style_popmarkt_good_img_area">
                                        <img class="msh_area_page_style_popmarkt_good_img" src="http://msh-cdn0.moshanghua2020.net/6af6e65f84464b9d9ff41caef80b4eff_1d1c048488f74a7b496a4c4037997079?imageView2">
                                    </div>
                                    <div class="msh_area_page_style_popmarkt_good_title">
                                        标题·Title
                                    </div>
                                    <div class="msh_area_page_style_popmarkt_good_info">
                                        <div class="msh_area_page_style_popmarkt_good_desc">
                                            描述·DESC
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="msh_area_page_style_popmarkt" id="popmarket_line_时光机">
                    <div class="msh_area_page_style_popmarkt_title">
                        <div class="msh_area_page_style_popmarkt_title_main">
                            <p class="msh_area_page_style_popmarkt_title_main_base">时光机</p>
                            <p class="msh_area_page_style_popmarkt_title_main_more">Time Machine</p>     
                        </div>
                        <div class="msh_area_page_style_popmarkt_title_plus">
                            <p class="msh_area_page_style_popmarkt_title_plus_base">Pick U Color</p>
                            <p class="msh_area_page_style_popmarkt_title_plus_more">An Interesting Story</p>
                        </div>
                    </div>
                    <div class="msh_area_page_style_popmarkt_goods_area">
                        <div class="msh_area_page_style_popmarkt_goods">
                            <div class="msh_area_page_style_popmarkt_good">
                                <div class="msh_area_page_style_popmarkt_good_content">
                                    <div class="msh_area_page_style_popmarkt_good_img_area">
                                        <img class="msh_area_page_style_popmarkt_good_img" src="http://msh-cdn0.moshanghua2020.net/6af6e65f84464b9d9ff41caef80b4eff_1d1c048488f74a7b496a4c4037997079?imageView2">
                                    </div>
                                    <div class="msh_area_page_style_popmarkt_good_title">
                                        标题·Title
                                    </div>
                                    <div class="msh_area_page_style_popmarkt_good_info">
                                        <div class="msh_area_page_style_popmarkt_good_desc">
                                            作者·Editor
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="msh_area_page_style_popmarkt_good">
                                <div class="msh_area_page_style_popmarkt_good_content">
                                    <div class="msh_area_page_style_popmarkt_good_img_area">
                                        <img class="msh_area_page_style_popmarkt_good_img" src="http://msh-cdn0.moshanghua2020.net/6af6e65f84464b9d9ff41caef80b4eff_1d1c048488f74a7b496a4c4037997079?imageView2">
                                    </div>
                                    <div class="msh_area_page_style_popmarkt_good_title">
                                        标题·Title
                                    </div>
                                    <div class="msh_area_page_style_popmarkt_good_info">
                                        <div class="msh_area_page_style_popmarkt_good_price_info only">
                                            ￥100<span>起 付费阅读</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="msh_area_page_style_popmarkt_good">
                                <div class="msh_area_page_style_popmarkt_good_content">
                                    <div class="msh_area_page_style_popmarkt_good_img_area">
                                        <img class="msh_area_page_style_popmarkt_good_img" src="http://msh-cdn0.moshanghua2020.net/6af6e65f84464b9d9ff41caef80b4eff_1d1c048488f74a7b496a4c4037997079?imageView2">
                                    </div>
                                    <div class="msh_area_page_style_popmarkt_good_title">
                                        标题·Title
                                    </div>
                                    <div class="msh_area_page_style_popmarkt_good_info">
                                        <div class="msh_area_page_style_popmarkt_good_desc">
                                            作者·Editor
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="msh_area_page_style_popmarkt" id="popmarket_line_兑换商店">
                    <div class="msh_area_page_style_popmarkt_title">
                        <div class="msh_area_page_style_popmarkt_title_main">
                            <p class="msh_area_page_style_popmarkt_title_main_base">兑换商店</p>
                            <p class="msh_area_page_style_popmarkt_title_main_more">Token Store</p>     
                        </div>
                        <div class="msh_area_page_style_popmarkt_title_plus">
                            <p class="msh_area_page_style_popmarkt_title_plus_base">Pick U Color</p>
                            <p class="msh_area_page_style_popmarkt_title_plus_more">An Interesting Story</p>
                        </div>
                    </div>
                    <div class="msh_area_page_style_popmarkt_goods_area">
                        <div class="msh_area_page_style_popmarkt_goods">
                            <div class="msh_area_page_style_popmarkt_good">
                                <div class="msh_area_page_style_popmarkt_good_content">
                                    <div class="msh_area_page_style_popmarkt_good_img_area">
                                        <img class="msh_area_page_style_popmarkt_good_img" src="http://msh-cdn0.moshanghua2020.net/6af6e65f84464b9d9ff41caef80b4eff_1d1c048488f74a7b496a4c4037997079?imageView2">
                                    </div>
                                    <div class="msh_area_page_style_popmarkt_good_title">
                                        标题·Title
                                    </div>
                                    <div class="msh_area_page_style_popmarkt_good_info">
                                        <div class="msh_area_page_style_popmarkt_good_desc">
                                            描述·DESC
                                        </div>
                                        <div class="msh_area_page_style_popmarkt_good_price_info">
                                            ￥100<span>起</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="msh_area_page_style_popmarkt_good">
                                <div class="msh_area_page_style_popmarkt_good_content">
                                    <div class="msh_area_page_style_popmarkt_good_img_area">
                                        <img class="msh_area_page_style_popmarkt_good_img" src="http://msh-cdn0.moshanghua2020.net/6af6e65f84464b9d9ff41caef80b4eff_1d1c048488f74a7b496a4c4037997079?imageView2">
                                    </div>
                                    <div class="msh_area_page_style_popmarkt_good_title">
                                        标题·Title
                                    </div>
                                    <div class="msh_area_page_style_popmarkt_good_info">
                                        <div class="msh_area_page_style_popmarkt_good_price_info only">
                                            ￥100<span>起</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="msh_area_page_style_popmarkt_good">
                                <div class="msh_area_page_style_popmarkt_good_content">
                                    <div class="msh_area_page_style_popmarkt_good_img_area">
                                        <img class="msh_area_page_style_popmarkt_good_img" src="http://msh-cdn0.moshanghua2020.net/6af6e65f84464b9d9ff41caef80b4eff_1d1c048488f74a7b496a4c4037997079?imageView2">
                                    </div>
                                    <div class="msh_area_page_style_popmarkt_good_title">
                                        标题·Title
                                    </div>
                                    <div class="msh_area_page_style_popmarkt_good_info">
                                        <div class="msh_area_page_style_popmarkt_good_desc">
                                            描述·DESC
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="msh_area_width msh_area_bottom_fixed">
        <div class="msh_area_bottom_btns">
            <div class="msh_area_bottom_btn btn_current" align="center" data-action="home">
                <div class="msh_area_bottom_btn_content">
                    <div class="msh_icon msh_icon_home"></div>
                    <div class="msh_icon_text">首页</div>
                </div>
            </div>
            <div class="msh_area_bottom_btn"  align="center" data-action="story">
                <div class="msh_area_bottom_btn_content">
                    <div class="msh_icon msh_icon_story"></div>
                    <div class="msh_icon_text">品牌故事</div>
                </div>
            </div>
            <div class="msh_area_bottom_btn"  align="center" data-action="giftclub">
                <div class="msh_area_bottom_btn_content">
                    <div class="msh_icon msh_icon_giftclub"></div>
                    <div class="msh_icon_text">俱乐部</div>
                </div>
            </div>
            <div class="msh_area_bottom_btn"  align="center" data-action="person">
                <div class="msh_area_bottom_btn_content">
                    <div class="msh_icon msh_icon_person"></div>
                    <div class="msh_icon_text">我的会员</div>
                </div>
            </div>
        </div>
    </div>
    """

    load_msh_home_new_banner_imgs_animate = null
    img_num = null
    img_flag = null
    img_flag_max = null
    img_width = null
    load_msh_home_new_banner_imgs = ()->
        clearInterval load_msh_home_new_banner_imgs_animate
        console.log "MSH_HOME_NEW_BANNER_IMGS",MSH_HOME_NEW_BANNER_IMGS
        if MSH_HOME_NEW_BANNER_IMGS?
            if MSH_HOME_NEW_BANNER_IMGS.length>0
                $(".msh_area_banner_imgs").empty()
                img_num = 0
                img_flag = 0
                img_flag_max = MSH_HOME_NEW_BANNER_IMGS.length
                img_width = $(".msh_area_banner_imgs_area").width()
                for img in MSH_HOME_NEW_BANNER_IMGS
                    $(".msh_area_banner_imgs").append """
                        <div class="msh_area_banner_img_area" style="width:#{img_width}px;left:#{img_num*img_width}px;">
                            <img class="msh_area_banner_img" src="#{img}">
                        </div>
                    """
                    img_num +=1
                load_msh_home_new_banner_imgs_animate = setInterval ()->
                    img_flag +=1
                    if img_flag == img_flag_max
                        img_flag = 0
                    console.log "img_flag",img_flag,img_flag_max,img_width,img_flag*img_width
                    $(".msh_area_banner_imgs").animate
                        "scrollLeft": img_flag*img_width
                ,5000
    setTimeout ()->
        load_msh_home_new_banner_imgs()
    ,1000
    
    $(window).on "resize",()->
        load_msh_home_new_banner_imgs()

    $("body").on "click",".msh_area_bottom_btns>.msh_area_bottom_btn", (evt)->
        dom = $(this)
        dom_action = dom.attr("data-action")
        $(".msh_area_bottom_btns>.msh_area_bottom_btn").removeClass("btn_current")
        dom.addClass("btn_current")
        console.log "dom_action", dom_action

        if dom_action in ["story"]
            if IS_WEIXIN
                window.location.href = "https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzkwNjI3NTUwMQ==&scene=124"
                # window.location.href = "https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzkyMzE0MjA5NA==&scene=124#wechat_redirect"
            else
                window.location.href = "/home/page/689f864598af4ed29f705101c82bcc00"
            # new_blank = window.open('_blank')
            # if new_blank == null
            #     if IS_WEIXIN
            #         window.location.href = "https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzkyMzE0MjA5NA==&scene=124#wechat_redirect"
            #     else
            #         window.location.href = "/home/page/689f864598af4ed29f705101c82bcc00"
            # else
            #     if IS_WEIXIN
            #         new_blank.location = "https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzkyMzE0MjA5NA==&scene=124#wechat_redirect"
            #     else
            #         new_blank.location = "/home/page/689f864598af4ed29f705101c82bcc00"
        else if dom_action in ["giftclub"]
            window.location.href = "/home/page/40e7cb27fc604dca84c6ab84716bbed8"
            # new_blank = window.open('_blank')
            # if new_blank == null
            #     window.location.href = "https://www.moshanghua2020.net/home/page/40e7cb27fc604dca84c6ab84716bbed8"
            # else
            #     new_blank.location = "https://www.moshanghua2020.net/home/page/40e7cb27fc604dca84c6ab84716bbed8"
        else if dom_action in ["person"]
            window.location.href = "/home/page/2c1b65a24d574e89aeb2b1275458470b"
            # new_blank = window.open('_blank')
            # if new_blank == null
            #     window.location.href = "https://www.moshanghua2020.net/home/page/2c1b65a24d574e89aeb2b1275458470b"
            # else
            #     new_blank.location = "https://www.moshanghua2020.net/home/page/2c1b65a24d574e89aeb2b1275458470b"



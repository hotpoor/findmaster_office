root = exports ? this
# !!!! Hotpoor root object
root.Hs or= {}
Hs = root.Hs
Hs.login_scan_uri_uuid = null
$ ->
    console.log "msh hollow"

    root.调用弹出警告创 = (内容=null)->
        弹出警告窗(内容)
    root.弹出警告窗 = (内容=null)->
        alert 内容
    root.check_is_subscribe = (app="#{FINDMASTER_APP}")->
        openid = null
        if IS_WEIXIN
            $(".dev_log").append JSON.stringify(WX_DATA)
            openid = WX_DATA["openid"]
        is_subscribe = 0
        $.ajax
            url:"/api/weixin/get_weixin_user_info"
            data:
                app: app
                openid: openid
            dataType: 'json'
            type: 'GET'
            success:(data)->
                is_need_login_scan = false
                
                if data.info == "ok"
                    console.log data.data.subscribe
                    if data.data.subscribe == undefined or data.data.subscribe == null
                        is_subscribe = 2
                    else
                        is_subscribe = data.data.subscribe
                if not is_subscribe
                    cover_html = ""
                    if IS_WEIXIN
                        cover_html = """
                        <div><img style="width:160px;" src="http://msh-cdn0.qianshanghua.com/2290fcea343a43b4a4983f0d22231c39_fecad6c952c6546a772abed50cd81e1f?imageView2/2/w/300"></div>
                        <div><div style="color:#ccc;">还没有关注公众号<br>记得扫码关注</div></div>
                        """
                    else
                        # 不在微信内
                        if USER_ID.indexOf("no_login:") > -1
                            cover_html = """
                                <div class="msh_qrcode_login_img_area">
                                    <img class="msh_qrcode_login_img">
                                    <div class="msh_qrcode_login_img_canvas_doms" style="display:none;"></div>
                                </div>
                                <div style="display:none;"><button>没有关注，扫码关注登录</button></div>
                                <div><div style="color:#ccc;">微信扫码登录</div></div>
                            """
                            is_need_login_scan = true
                        else
                            cover_html = """
                                <div><img style="width:160px;" src="http://msh-cdn0.qianshanghua.com/2290fcea343a43b4a4983f0d22231c39_fecad6c952c6546a772abed50cd81e1f?imageView2/2/w/300"></div>
                                <div><div style="color:#ccc;">还没有关注公众号<br>记得扫码关注</div></div>
                            """
                    if $(".msh_top_cover_card").length==0
                        hollow_confirm_is_subscribe "欢迎访问PUCO噗叩·时光机",cover_html
                        # $("body").append """
                        # <div class="msh_top_cover_card">
                        #     <div>
                        #         #{cover_html}
                        #         <div class="remove_msh_top_cover_card">关闭</div>
                        #     </div>
                        # </div>
                        # """
                if is_subscribe == 2
                    # if IS_WEIXIN
                        # {'errcode': 41001, 'errmsg': 'access_token missing rid: 613111c5-3b7ef917-508e522e'}
                    cover_html = """微信ACCESS_TOKEN需更新，5秒记得刷新页面！"""
                    console.log "微信ACCESS_TOKEN需更新，5秒后再次请求！"
                    setTimeout ()->
                            root.check_is_subscribe(FINDMASTER_APP)
                        ,5000
                        # if $(".msh_top_cover_card").length==0
                        #     hollow_confirm_is_subscribe "欢迎访问PUCO噗叩·时光机",cover_html
                        #     do ()->
                        #         setTimeout ()->
                        #                 window.location.href = window.location.href
                        #             , 3000
                        # cover_html = """微信ACCESS_TOKEN需更新，将3秒后自动刷新页面！"""
                        # if $(".msh_top_cover_card").length==0
                        #     hollow_confirm_is_subscribe "欢迎访问PUCO噗叩·时光机",cover_html
                        #     do ()->
                        #         setTimeout ()->
                        #                 window.location.href = window.location.href
                        #             , 3000
                if is_need_login_scan
                    Hs.login_scan_uri_uuid = uuid2(6,null)
                    login_scan_uri = "#{HOST_URL}/home/login_scan?room_id=MSH_USER&user_id=#{USER_ID}&uuid=#{Hs.login_scan_uri_uuid}&app=#{app}"
                    console.log login_scan_uri
                    $(".msh_qrcode_login_img_canvas_doms").empty()
                    $(".msh_qrcode_login_img_canvas_doms").qrcode login_scan_uri
                    $(".msh_qrcode_login_img").attr "src", $(".msh_qrcode_login_img_canvas_doms>canvas").first()[0].toDataURL()
                    root.join_more_room_message_send "JOINMOREROOMS",USER_ID,"MSH USER",["MSH_USER/#{USER_ID}/#{Hs.login_scan_uri_uuid}"]
            error:(data)->
                console.log data

    $("body").on "click",".remove_msh_top_cover_card",(evt)->
        $(".msh_top_cover_card").remove()
    load_msh_topics_nums_timer = null
    load_msh_topics_nums_list = []
    root.load_msh_topics_nums = (alist,timer)->
        clearTimeout load_msh_topics_nums_timer
        load_msh_topics_nums_timer = setTimeout ()->
            url = "/api/page/count_connect_num_list"
            $.ajax
                url:url
                data:
                    aim_ids: JSON.stringify alist
                dataType: 'json'
                type: 'GET'
                success:(data)->
                    console.log data
                    if data.info == "ok"
                        for k,v of data.result
                            if v.num == 0
                                $(".msh_topic_line[data-block=#{k}]").find(".onlinenum").attr("data-num0",v.num)
                            else
                                $(".msh_topic_line[data-block=#{k}]").find(".onlinenum").removeAttr("data-num0")
                error:(data)->
                    console.log data
            load_msh_topics_nums(load_msh_topics_nums_list,timer)
        ,timer

    root.load_msh_topics = ()->
        url = "/api/page/comment/load"
        $.ajax
            url:url
            data:
                chat_id: "514699f27bd142bd9ab6d4d1063fb314"
                comment_id: null
            dataType: 'json'
            type: 'GET'
            success:(data)->
                console.log data
                $(".msh_topic_list").empty()
                if data.info == "ok"
                    load_msh_topics_nums_list = []
                    for comment in data.comments
                        content_json = JSON.parse(comment[4])
                        headimgurl = content_json["headimgurl"]
                        title_list = content_json["title_list"]
                        block_id = content_json["msh_hollow_block_id"]
                        title_list_show = """"""
                        for title_list_item in title_list
                            title_list_show = """
                                #{title_list_show}
                                #{title_list_item}
                                <br>
                            """

                        $(".msh_topic_list").prepend """
                            <div class="msh_line msh_topic_line" data-block="#{block_id}">
                                <div class="msh_line_card w_82_h_auto" align="center">
                                    <div class="msh_c_img_area onlinenum">
                                        <img class="msh_c_img" src="#{headimgurl}">
                                    </div>
                                    <div class="msh_c_c_plus">
                                        <div class="msh_c_c_plus_icon"></div>
                                    </div>
                                    <div class="msh_c_title">#{title_list_show}</div>
                                </div>
                            </div>
                        """
                        load_msh_topics_nums_list.push block_id
                    $(".msh_topic_list").prepend """
                    <div class="msh_line msh_topic_line">
                        <a href="/" target="_blank">
                        <div class="msh_line_card w_82_h_auto" align="center" style="box-shadow: none;color: #333;">
                            <div class="msh_c_img_area onlinenum_0">
                                <img class="msh_c_img" src="/static/img/msh_icon/logo.png">
                            </div>
                            <div class="msh_c_c_plus">
                                <div class="msh_c_c_plus_icon"></div>
                            </div>
                            <div class="msh_c_title">BACK HOME<br>返回主页</div>
                        </div>
                        </a>
                    </div>
                    """
                    $(".msh_topic_list").prepend """
                    <div class="msh_line msh_topic_line">
                        <div class="msh_topic_list_left_fix"></div>
                    </div>
                    """
                    load_msh_topics_nums(load_msh_topics_nums_list,300000)
            error:(data)->
                console.log data
    $("body").on "click",".msh_topic_line",(evt)->
        dom = $(this)
        aim_id = dom.attr("data-block")
        if aim_id not in [undefined,null,""]
            window.location.href = "/home/msh/hollow/#{aim_id}"
        else
            window.location.href = "/"

    $("body").on "click",".msh_area_bottom_btn", (evt)->
        dom = $(this)
        dom_action = dom.attr("data-action")
        $(".msh_area_bottom_btn").removeClass("btn_current")
        dom.addClass("btn_current")
        console.log "dom_action", dom_action
        if dom_action in ["story"]
            if IS_WEIXIN
                window.location.href = "https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzkwNjI3NTUwMQ==&scene=124#wechat_redirect"
                # window.location.href = "https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzkyMzE0MjA5NA==&scene=124#wechat_redirect"
            else
                window.location.href = "/home/page/689f864598af4ed29f705101c82bcc00"
        else if dom_action in ["person"]
            window.location.href = "/home/page/25df4bb293d046fc8b35358f9cc0c017"
        else if dom_action in ["home"]
            window.location.href = "/home/page/f644eba0484b45c784b712f562dcc095"
            # PUCO慕斯唇泥海报页面
            # window.location.href = "/home/page/5857a32c7f214c6ca9c0c1a72a0f3bf5"
            # if IS_WEIXIN
            #     window.location.href = "https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzkwNjI3NTUwMQ==&scene=124#wechat_redirect"
            # else
    load_hollows = (hollow_ids)->
        for hollow_id in hollow_ids
            $(".msh_main_area").append """
            <div class="comments_area" data-block="#{hollow_id}">
                <div class="comments_submit_tools hide" style="border-bottom: 1px solid #f2f2f2;padding-bottom: 20px;margin-bottom: 30px;">
                    <div><textarea class="comment_content" placeholder="Add some comment..." style="resize:none;"></textarea></div>
                    <div class="comment_submit_add_imgs hide">
                        <div class="comment_submit_add_img_more">
                            <div class="comment_submit_add_img_more_img"></div>
                        </div>
                    </div>
                    <div style="display:flex;margin-top:5px;">
                        <div><button class="comment_submit_add_img"></button></div>
                        <div><button class="comment_submit">发送</button></div>
                    </div>
                </div>
                <div class="comments hollow_comments"></div>
            </div>
            """
            comment_load(hollow_id)
    $(window).on "load",(evt)->
        load_msh_topics()
        load_hollows(HOLLOWS)
    root.content_to_html = (content)->
        content_type_list = content.split("//")
        content_type = content_type_list[0]
        by_secret_user = null
        if content_type in ["HWEBIMG","HWEBLINK","HWEBIMGS","HWEBVIDEO","HWEBVIDEOS"]
            if content_type in ["HWEBIMG"]
                imgurl = content.replace("HWEBIMG//","")
                content = """<div class="content_img_area"><img class="content_img card_webimg_thumb" src="#{imgurl}"></div>"""
            else if content_type in ["HWEBIMGS"]
                try
                    imgurl_json = JSON.parse content.replace("HWEBIMGS//","")
                catch e
                    imgurl_json = {
                        "content":"【该消息不支持显示】",
                        "images":[],
                    }
                current_content_json = imgurl_json["content"].split("[BYSECRETUSER]")
                current_content_json_content = current_content_json[0]
                if current_content_json.length>1
                    try
                        by_secret_user = JSON.parse current_content_json[1]
                    catch e
                        by_secret_user = null
                current_imgs = imgurl_json["images"]
                current_imgs_mod = current_imgs.length
                base_width = $(".comments_area").width() - 90
                if current_imgs_mod in [0,1]
                    current_imgs_mod = 1
                    _w = "width:75%;"
                    _h = "height:auto;"
                else if current_imgs_mod in [2,4]
                    current_imgs_mod = 2
                    _w = parseInt base_width / (current_imgs_mod * 1.0) - 8
                    _h = _w
                    _w = "width:#{_w}px;"
                    _h = "height:#{_h}px;"
                else
                    current_imgs_mod = 3
                    _w = parseInt base_width / (current_imgs_mod * 1.0) - 4
                    _h = _w
                    _w = "width:#{_w}px;"
                    _h = "height:#{_h}px;"
                current_imgs_html = """"""
                for current_img in current_imgs
                    current_img_url = current_img.replace("HWEBIMG//","")
                    current_imgs_html = """#{current_imgs_html}<div class="content_img_cover" style="#{_w}#{_h}"><img class="content_img card_webimg_thumb" style="width:100%;height:100%;" src="#{current_img_url}"></div>"""
                
                content_list = current_content_json_content.split("\n")
                content = """"""
                content_first = true
                for content_list_item in content_list
                    # console.log "root.ReplaceTag(content_list_item)"
                    # console.log root.ReplaceTag(content_list_item)
                    content_list_item_now = content_list_item
                    content_list_item_now = root.ReplaceTag(content_list_item_now)
                    content_list_item_now = root.ReplaceUrl(content_list_item_now)
                    if content_first
                        content = """#{content_list_item_now}"""
                        content_first = false
                    else
                        content = """#{content}<br>#{content_list_item_now}"""
                content = """
                    <div class="content_img_area" data-num-#{current_imgs_mod}="#{current_imgs_mod}">#{current_imgs_html}</div>
                    <div class="content_img_text">#{content}</div>"""
            else if content_type in ["HWEBVIDEO"]
                videourl = content.replace("HWEBVIDEO//","")
                video_uuid = uuid2(6,null)
                content = """<div class="content_video_area">
                <video id="player_#{video_uuid}"
                    class="video-js vjs-default-skin"
                    poster = "#{videourl}?vframe/jpg/offset/0/"
                    controls
                    webkit-playsinline="true"
                    playsinline="true"
                    style="width:100%;max-height:260px;min-height:200px;"
                    >
                    <source src="#{videourl}" type="video/mp4">
                    <!-- .m3u8 application/x-mpegURL -->
                </video>
                <script type="text/javascript">
                    videojs('#player_#{video_uuid}');
                </script>
                <div><a href="#{videourl}" target="_blank" style="color:#999;font-size:12px;">原视频链接</a></div>
                </div>

                """
            else if content_type in ["HWEBLINK"]
                try
                    weblink_json = JSON.parse content.replace("HWEBLINK//","")
                catch e
                    weblink_json =
                        "content":"【该消息不支持显示】"
                        "thumb_url":[]
                        "title":""
                        "digest":""
                        "url":""
                _thumb_url = weblink_json["thumb_url"]
                _title = weblink_json["title"]
                if _title.replace(/\s/g, "") == ""
                    _title = "分享链接"
                _digest = weblink_json["digest"]
                error_img_url = "http://msh-cdn0.qianshanghua.com/bf3dfd1f3af941d08e8ab802f88c28aa_d74dec75535984ff249527f7546c9bc1?imageView2"
                _current_weblink_html = """
                    <a href="#{weblink_json["url"]}" target="_blank">
                        <div class="card_hwxweblink">
                            <div class="card_hwxweblink_thumb"><img src="#{_thumb_url}" onerror="this.src='#{error_img_url}'"></div>
                            <div class="card_hwxweblink_title">#{_title}</div>
                            <div class="card_hwxweblink_digest">#{_digest}</div>
                        </div>
                    </a>
                """
                current_content_json = weblink_json["content"].split("[BYSECRETUSER]")
                current_content_json_content = current_content_json[0]
                if current_content_json.length>1
                    try
                        by_secret_user = JSON.parse current_content_json[1]
                    catch e
                        by_secret_user = null
                content_list = current_content_json_content.split("\n")
                content = """"""
                content_first = true
                for content_list_item in content_list
                    # console.log "root.ReplaceTag(content_list_item)"
                    # console.log root.ReplaceTag(content_list_item)
                    content_list_item_now = content_list_item
                    content_list_item_now = root.ReplaceTag(content_list_item_now)
                    content_list_item_now = root.ReplaceUrl(content_list_item_now)
                    if content_first
                        content = """#{content_list_item_now}"""
                        content_first = false
                    else
                        content = """#{content}<br>#{content_list_item_now}"""
                content = """
                    <div class="content_weblink_area" >#{_current_weblink_html}</div>
                    <div class="content_weblink_text">#{content}</div>"""
        else
            current_content_json = content.split("[BYSECRETUSER]")
            current_content_json_content = current_content_json[0]
            if current_content_json.length>1
                try
                    by_secret_user = JSON.parse current_content_json[1]
                catch e
                    by_secret_user = null
            content_list = current_content_json_content.split("\n")
            content = """"""
            content_first = true
            for content_list_item in content_list
                # console.log "root.ReplaceTag(content_list_item)"
                # console.log root.ReplaceTag(content_list_item)
                content_list_item_now = content_list_item
                content_list_item_now = root.ReplaceTag(content_list_item_now)
                content_list_item_now = root.ReplaceUrl(content_list_item_now)
                if content_first
                    content = """#{content_list_item_now}"""
                    content_first = false
                else
                    content = """#{content}<br>#{content_list_item_now}"""
        return [content,by_secret_user]
    root.comment_add_one_base = (content_json)->
        user_name = content_json["nickname"]
        content = content_json["content"]
        date_html = formatDateAllEn(content_json["time"]*1000)
        user_headimgurl = content_json["headimgurl"]
        comment_id = content_json["comment_id"]
        sequence = content_json["sequence"]
        control_tools=""
        if IS_EDITOR or USER_ID == content_json["user_id"]
            control_tools = """
            <div class="comment_line">
                <div class="comment_del_action"></div>
                <button class="comment_control_tool_btn comment_del hide">DEL</button>
            </div>
            """
        [content,by_secret_user] = content_to_html content
        user_fake_html =""""""
        if by_secret_user!= null
            user_fake = if by_secret_user["fake"]!=undefined then by_secret_user["fake"] else "false"
            if user_fake == "false"
                fake_user_headimgurl = user_headimgurl
                fake_user_name = user_name
            else
                fake_user_headimgurl = "/static/img/msh_hollow/msh_mask.jpg"
                fake_user_name = "匿名"
            user_fake_html = """<img class="fake_img" src="#{fake_user_headimgurl}">"""
            user_headimgurl = by_secret_user["headimgurl"]
            user_name = by_secret_user["name"]
        html = """
            <div class="comment" data-comment-id="#{comment_id}_#{sequence}">
                <div class="comment_img"><img src="#{user_headimgurl}">#{user_fake_html}</div>
                #{control_tools}
                <div class="comment_line">
                    <p class="p_name"><span class="name">#{user_name}</span></p>
                    <p class="p_date"><span class="date">#{date_html}</span></p>
                </div>

                <div class="comment_line"><div class="content">#{content}</div></div>
                <div class="comment_line">
                    <div class="hollow_btn_tools">
                        <div class="hollow_btn_tool hollow_btn_share comment_share_btn">
                            <div class="hollow_btn_tool_icon hollow_btn_share_btn comment_share"></div>
                            <div class="hollow_btn_tool_num hollow_btn_share_num comment_share_num" data-value="0"></div>
                        </div>
                        <div class="hollow_btn_tool hollow_btn_like comment_like_btn">
                            <div class="hollow_btn_tool_icon hollow_btn_like_btn comment_like"></div>
                            <div class="hollow_btn_tool_num hollow_btn_like_num comment_like_num" data-value="0">点赞</div>
                        </div>
                        <div class="hollow_btn_tool hollow_btn_remark comment_remark_btn">
                            <div class="hollow_btn_tool_icon hollow_btn_remark_btn comment_remark"></div>
                            <div class="hollow_btn_tool_num hollow_btn_remark_num comment_remark_num" data-value="0">评论</div>
                        </div>
                    </div>
                </div>
                <div class="comment_line">
                    <div class="hollow_remark_tools">
                        <div class="hollow_remark_list"></div>
                        <div class="hollow_remark_controls hide">
                            <div class="remark_content_line"><textarea class="remark_content" placeholder="请输入评论"></textarea></div>
                            <div class="remark_submit_line"><button class="remark_submit">发送</button></div>
                        </div>
                    </div>
                </div>
            </div>
        """
        setTimeout ()->
                $(".comment[data-comment-id=#{comment_id}_#{sequence}]").addClass("comment_animate_show")
            ,100
        return html
    root.comment_add = (content_json, chat_id)->
        comment_html = comment_add_one_base(content_json)
        comment_top_line = $(".comments_area[data-block=#{chat_id}]>.comments").find(".comment_top_line")
        if comment_top_line.length < 1
            $(".comments_area[data-block=#{chat_id}]>.comments").prepend """
                #{comment_html}
            """
        else
            comment_top_line.after """
                 #{comment_html}
            """
    root.comment_load_one_base = (comment_list,comment_id,comment_type="")->
        if comment_list[6]==1
            return ""
        user_name = members[comment_list[1]]["name"]
        content = comment_list[4]
        content_plus = comment_list[5]
        if content_plus == undefined or content_plus == null
            content_plus =
                "likes": []
                "remarks": []
                "ref_list": []
        if content_plus["likes"] == undefined
            likes_num = 0
            likes_current = ""
        else
            if USER_ID in content_plus["likes"]
                likes_current = "like"
            likes_num = content_plus["likes"].length
        if content_plus["remarks"] == undefined
            content_plus["remarks"] = []
            remarks_num = 0
        else
            remarks_num = content_plus["remarks"].length
        if content_plus["ref_list"] == undefined
            content_plus["ref_list"] = []
            ref_num = 0
        else
            ref_num = content_plus["ref_list"].length
        if comment_list[3] in ["COMMENT"]
            content = content
        else if comment_list[3] in ["WEIXINPAYCALLBACKSUCCESS","ALIPAYPAYCALLBACKSUCCESS"]
            content = ("""<div class="content_table"><div>#{k}</div><div>#{v}</div></div>""" for k,v of content).join("\n\r")

        date_html = formatDateAllEn(comment_list[2]*1000)
        user_headimgurl = members[comment_list[1]]["headimgurl"]

        remark_list_html = """"""
        remarks = content_plus["remarks"]
        for remark_item in remarks
            _html = comment_load_one_remark remark_item
            remark_list_html = """#{remark_list_html}#{_html}"""

        control_tools=""
        if comment_list[3] not in ["WEIXINPAYCALLBACKSUCCESS","ALIPAYPAYCALLBACKSUCCESS"]
            if IS_EDITOR or USER_ID == comment_list[1]
                control_tools = """
                <div class="comment_line">
                    <div class="comment_del_action"></div>
                    <button class="comment_control_tool_btn comment_del hide">DEL</button>
                </div>
                """
        [content,by_secret_user] = content_to_html content        
        user_fake_html =""""""
        if by_secret_user!= null
            user_fake = if by_secret_user["fake"]!=undefined then by_secret_user["fake"] else "false"
            if user_fake == "false"
                fake_user_headimgurl = user_headimgurl
                fake_user_name = user_name
            else
                fake_user_headimgurl = "/static/img/msh_hollow/msh_mask.jpg"
                fake_user_name = "匿名"
            user_fake_html = """<img class="fake_img" src="#{fake_user_headimgurl}">"""
            user_headimgurl = by_secret_user["headimgurl"]
            user_name = by_secret_user["name"]
        html = """
            <div class="comment #{comment_type}" data-comment-id="#{comment_id}_#{comment_list[0]}">
                <div class="comment_img"><img src="#{user_headimgurl}">#{user_fake_html}</div>
                #{control_tools}
                <div class="comment_line">
                    <p class="p_name"><span class="name">#{user_name}</span></p>
                    <p class="p_date"><span class="date">#{date_html}</span></p>
                    <div></div>
                </div>
                <div class="comment_line"><div class="content">#{content}</div></div>
                <div class="comment_line">
                    <div class="hollow_btn_tools">
                        <div class="hollow_btn_tool hollow_btn_share comment_share_btn">
                            <div class="hollow_btn_tool_icon hollow_btn_share_btn comment_share"></div>
                            <div class="hollow_btn_tool_num hollow_btn_share_num comment_share_num" data-value="#{ref_num}">#{num_change(ref_num,"")}</div>
                        </div>
                        <div class="hollow_btn_tool hollow_btn_like comment_like_btn">
                            <div class="hollow_btn_tool_icon hollow_btn_like_btn comment_like #{likes_current}"></div>
                            <div class="hollow_btn_tool_num hollow_btn_like_num comment_like_num" data-value="#{likes_num}">#{num_change(likes_num,"点赞")}</div>
                        </div>
                        <div class="hollow_btn_tool hollow_btn_remark comment_remark_btn">
                            <div class="hollow_btn_tool_icon hollow_btn_remark_btn comment_remark"></div>
                            <div class="hollow_btn_tool_num hollow_btn_remark_num comment_remark_num" data-value="#{remarks_num}">#{num_change(remarks_num,"评论")}</div>
                        </div>
                    </div>
                </div>
                <div class="comment_line">
                    <div class="hollow_remark_tools">
                        <div class="hollow_remark_list">#{remark_list_html}</div>
                        <div class="hollow_remark_controls hide">
                            <div class="remark_content_line"><textarea class="remark_content" placeholder="请输入评论"></textarea></div>
                            <div class="remark_submit_line"><button class="remark_submit">发送</button></div>
                        </div>
                    </div>
                </div>
            </div>
        """
        setTimeout ()->
                $(".comment[data-comment-id=#{comment_id}_#{comment_list[0]}]").addClass("comment_animate_show")
            ,100
        return html
    root.hollow_confirm_confirm_action = null
    root.hollow_confirm_share = (show_html=false,title="微信分享预览",text="",data_comment_id=null,remark_id=null) ->
        link_title = $(".comment[data-comment-id=#{data_comment_id}]").find(".content").text()
        web_title = document.title
        name = $(".comment[data-comment-id=#{data_comment_id}]").find(".comment_line").find(".p_name").text()
        desc_title = "【#{web_title}】#{name}"
        desc = link_title
        imgs = $(".comment[data-comment-id=#{data_comment_id}]").find(".content").find("img")
        if imgs.length < 1
            img = $(".comment[data-comment-id=#{data_comment_id}]").find(".comment_img").find("img").first().attr("src")
        else
            img = imgs.first().attr("src")
        if desc == ""
            desc = "发布瞬间，与小伙伴们一起互动分享！"
        _block_id = BLOCK_ID
        _chat_id = $(".comment[data-comment-id=#{data_comment_id}]").parents(".comments_area").attr("data-block")
        data_comment_id_list = data_comment_id.split("_")
        _comment_id = data_comment_id_list[0]
        _comment_sequence = data_comment_id_list[1]
        redirect_uri = "https://www.qianshanghua.com/home/msh/hollow/#{BLOCK_ID}?chat_id=#{_chat_id}&comment_id=#{_comment_id}&comment_sequence=#{_comment_sequence}&ref_id=#{USER_ID}"
        shareDataTimeline =
            title: "【#{web_title}】#{link_title}" #分享标题
            link: redirect_uri  #分享链接，该链接域名或路径必须与当前页面对应的公众号JS安全域名一致
            imgUrl: img #分享图标
            success: ()->
                console.log "update shareDataTimeline success"
        shareDataAppMessage =
            title: desc_title #分享标题
            desc: "#{desc.replaceAll("\n","").replaceAll("  ","")}" #分享描述
            link: redirect_uri #分享链接，该链接域名或路径必须与当前页面对应的公众号JS安全域名一致
            imgUrl: img #分享图标
            success: ()->
                console.log "update shareDataAppMessage success"
        console.log shareDataAppMessage
        wx.ready ()->
            wx.updateAppMessageShareData(shareDataAppMessage)
            wx.updateTimelineShareData(shareDataTimeline)
            wx.onMenuShareAppMessage(shareDataAppMessage)
            wx.onMenuShareTimeline(shareDataTimeline)
        if show_html
            $("body").append """
            <div class="hollow_confirm_show_area">
                <div class="hollow_confirm_show_area_card">
                    <div class="hollow_confirm_show_area_card_title">
                        <p>#{title}</p>
                    </div>
                    <div class="hollow_confirm_show_area_card_desc">
                        <div>
                            <div style="font-size:14px;">预览·分享到朋友圈</div>
                            <div style="display: flex;justify-content: center;margin: 5px;">
                                <div style="display: flex;align-items: center;background: #f2f2f2;width:100%;max-width: 320px;">
                                    <div style="margin: 5px;height: 40px;"><img src="#{img}"
                                        style="width: 40px;height:40px;object-fit:cover;"></div>
                                    <div style="text-align: left;padding: 0px 5px;color: #333;width: -webkit-fill-available;max-height: 40px;overflow: hidden;max-width: 290px;font-size: 12px;line-height:20px;">
                                        <div style="">【#{web_title}】#{link_title}</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div align="center">
                            <div style="font-size:14px;margin-top: 15px;">预览·发送给朋友</div>
                                <div style="padding: 5px;border: 1px solid #e2e2e2;border-radius: 6px;margin: 5px;max-width:320px;">
                                    <div style="text-align: left;font-size: 16px;color: #333;">#{desc_title}</div>
                                    <div style="display: flex;">
                                        <div style="font-size: 12px;text-align: left;height: 50px;overflow: hidden;width: -webkit-fill-available;">#{desc}</div>
                                        <div style="width: 50px;height: 50px;"><img
                                            src="#{img}"
                                            style="object-fit: cover;width: 50px;height: 50px;">
                                        </div>
                                </div>
                            </div>
                        </div>
                        <div>
                            <div style="font-size:16px;margin-top: 15px;color: #4caf50;">微信网页版分享方法<br>请点击右上角<span style="color: black;margin: 5px;">...</span>进行分享</div>
                        </div>
                    </div>
                    <div class="hollow_confirm_show_area_card_confirm_tools">
                        <div class="hollow_confirm_cancel">我知道了</div>
                    </div>
                </div>
                <div class="hollow_confirm_share_area_arrow">
                    <img style="width:100%;height:auto;" src="/static/img/msh_icon/share_arrow.png">
                </div>
            </div>
            """
    root.hollow_confirm_is_subscribe = (title="欢迎访问PUCO噗叩·时光机",text="是否确认？",data_comment_id=null,remark_id=null) ->
        $("body").append """
        <div class="hollow_confirm_show_area">
            <div class="hollow_confirm_show_area_card">
                <div class="hollow_confirm_show_area_card_title">
                    <p>#{title}</p>
                </div>
                <div class="hollow_confirm_show_area_card_desc">
                    <p>#{text}</p>
                </div>
                <div class="hollow_confirm_show_area_card_confirm_tools">
                    <div class="hollow_confirm_cancel">我知道了</div>
                </div>
            </div>
        </div>
        """
    root.hollow_confirm_del = (dom_area,title="提示",text="是否确认？",data_comment_id=null,remark_id=null) ->
        $("body").append """
        <div class="hollow_confirm_show_area">
            <div class="hollow_confirm_show_area_card">
                <div class="hollow_confirm_show_area_card_title">
                    <p>#{title}</p>
                </div>
                <div class="hollow_confirm_show_area_card_desc">
                    <p>#{text}</p>
                </div>
                <div class="hollow_confirm_show_area_card_confirm_tools">
                    <div class="hollow_confirm_cancel">取消</div>
                    <div class="hollow_confirm_submit">确认</div>
                </div>
            </div>
        </div>
        """
        if data_comment_id != null
            if remark_id == null 
                root.hollow_confirm_confirm_action = ["DEL",dom_area,data_comment_id]
            else
                root.hollow_confirm_confirm_action = ["DELREMARK",dom_area,data_comment_id,remark_id]
    $("body").on "click",".comment_del_action",(evt)->
        dom = $(this)
        del_dom_area = dom.parents(".comment_line")
        data_comment_id = dom.parents(".comment").attr("data-comment-id")
        del_dom_area_del = del_dom_area.find(".comment_del")
        hollow_confirm_del del_dom_area,"提示","删除该树洞瞬间？",data_comment_id,
        console.log del_dom_area,"提示","是否删除树洞瞬间内容？",data_comment_id
    $("body").on "click",".remark_del_action",(evt)->
        dom = $(this)
        del_dom_area = dom.parents(".comment_line")
        data_comment_id = dom.parents(".comment").attr("data-comment-id")
        del_dom_area_del = del_dom_area.find(".comment_del")

        del_remark_dom_area = dom.parents(".remark_line")
        data_remark_id = del_remark_dom_area.attr("data-remark-id")

        hollow_confirm_del del_dom_area,"提示","删除该树洞瞬间的留言？",data_comment_id, data_remark_id
        console.log del_dom_area,"提示","是否删除该树洞瞬间的留言？",data_comment_id, data_remark_id
        evt.stopPropagation()
        evt.preventDefault()
    $("body").on "click",".hollow_confirm_submit",(evt)->
        if root.hollow_confirm_confirm_action!=null
            console.log root.hollow_confirm_confirm_action
            _action = root.hollow_confirm_confirm_action[0]
            _dom_area = root.hollow_confirm_confirm_action[1]
            _comment_id = root.hollow_confirm_confirm_action[2]
            if _action == "DEL"
                $(".comment[data-comment-id=#{_comment_id}]").animate
                    "height":0
                $(".comment[data-comment-id=#{_comment_id}]").addClass("comment_animate_hide")
                do (_dom_area,_comment_id)->
                    setTimeout ()->
                            _dom_area.parents(".comment").find(".comment_del").click()
                            # $(".comment[data-comment-id=#{_comment_id}]").find(".comment_del").click()
                        ,1000
            else if _action == "DELREMARK"
                _remark_id = root.hollow_confirm_confirm_action[3]
                do (_dom_area,_comment_id,_remark_id)->
                    _dom_area.parents(".comment").find(".remark_line[data-remark-id=#{_remark_id}]").find(".remark_line_del").click()
                    # $(".comment[data-comment-id=#{_comment_id}]").find(".remark_line[data-remark-id=#{_remark_id}]").find(".remark_line_del").click()

        root.hollow_confirm_confirm_action = null
        $(".hollow_confirm_show_area").remove()
    $("body").on "click",".hollow_confirm_cancel",(evt)->
        root.hollow_confirm_confirm_action = null
        $(".hollow_confirm_show_area").remove()

    $("body").on "click",".comment_remark_btn",(evt)->
        _this = $(this)
        dom = _this.find(".comment_remark")
        dom_comment = dom.parents(".comment")
        remark_controls = dom_comment.find(".hollow_remark_controls")
        remark_controls.removeClass("hide")
        dom_remark_content = remark_controls.find(".remark_content")
        $(".remark_content").removeClass("current")
        dom_remark_content.addClass("current")
        do (dom_remark_content)->
            setTimeout ()->
                    # dom[0].scrollIntoView()
                    $("html").animate
                            scrollTop: dom_remark_content.offset().top - 120
                        , 250, ()->
                            $(window).scrollTop dom_remark_content.offset().top - 120
                            dom_remark_content.focus()
                ,250
    $("body").on "click",".hollow_btn_share_btn",(evt)->
        dom = $(this)
        data_comment_id = dom.parents(".comment").attr("data-comment-id")
        hollow_confirm_share true, "微信分享预览", "", data_comment_id

    root.comment_load_one_ref_add = ()->
        if CHAT_ID in ["None"] or COMMENT_ID in ["None"] or COMMENT_SEQUENCE in ["None"] or REF_ID in ["None"]
            return
        hollow_confirm_share false, "微信分享预览", "", "#{COMMENT_ID}_#{COMMENT_SEQUENCE}"
        content = "ref add remark comment #{COMMENT_ID}_#{COMMENT_SEQUENCE}"
        $.ajax
            url:"/api/page/comment/ref_add"
            data:
                block_id:BLOCK_ID
                chat_id:CHAT_ID
                content:content
                comment_id:COMMENT_ID
                comment_sequence:COMMENT_SEQUENCE
                remark_id:REMARK_ID
                uuid:uuid2(6,null)
                ref_id:REF_ID
            dataType: 'json'
            type: 'POST'
            success:(data)->
                console.log data
                if data.info == "ok"
                    aim_dom = $(".comments_area[data-block=#{CHAT_ID}]>.comments").find(".comment[data-comment-id=#{COMMENT_ID}_#{COMMENT_SEQUENCE}]")
                    aim_btn = aim_dom.find(".comment_share")
                    aim_value_dom = aim_dom.find(".comment_share_num")
                    aim_value = parseInt data.ref_num
                    if aim_value <=0
                        aim_value_dom.attr("data-value","0")
                        aim_value_dom.text ""
                    else
                        aim_value_dom.attr("data-value",aim_value)
                        aim_value_dom.text num_change(aim_value)
            error: (data)->
                console.log data
    root.comment_load_one_from_share = ()->
        if CHAT_ID in ["None"] or COMMENT_ID in ["None"] or COMMENT_SEQUENCE in ["None"]
            return
        $.ajax
            url:"/api/page/comment/load_one"
            data:
                block_id:BLOCK_ID
                chat_id:CHAT_ID
                comment_id:COMMENT_ID
                comment_sequence:COMMENT_SEQUENCE
                remark_id:REMARK_ID
            dataType: 'json'
            type: 'GET'
            success:(data)->
                if data.info == "ok"
                    for k,v of data.members
                        members[k]=v
                    comment_top_line = $(".comments_area[data-block=#{CHAT_ID}]>.comments").find(".comment_top_line")
                    if comment_top_line.length < 1
                        $(".comments_area[data-block=#{CHAT_ID}]>.comments").prepend """
                        <div class="comment_top_line"></div>
                        """
                    if data.comments.length == 0
                        $(".comments_area[data-block=#{CHAT_ID}]>.comments").prepend """
                            <div class="comment_type_flag" data-comment-id="#{COMMENT_ID}_#{COMMENT_SEQUENCE}"><span class="span_comment_type_share">分享</span></div>
                            <div class="comment_type_flag" data-comment-id="#{COMMENT_ID}_#{COMMENT_SEQUENCE}"
                                style="border-bottom:1px solid #f2f2f2;text-align:center;"><img style="width:100%;max-width:300px;" src="/static/img/msh_hollow/msh_not_found.jpg"></div>
                        """
                    for comment in data.comments by -1
                        comment_html = comment_load_one_base(comment,data.comment_id,"comment_type_share")
                        $(".comments_area[data-block=#{CHAT_ID}]>.comments").prepend """
                            <div class="comment_type_flag" data-comment-id="#{COMMENT_ID}_#{COMMENT_SEQUENCE}"><span class="span_comment_type_share">分享</span></div>
                            #{comment_html}
                        """
                    comment_load_one_ref_add()
            error: (data)->
                console.log data
    $("body").on "click",".card_webimg_thumb",(evt)->
        urls = []
        doms = $(".card_webimg_thumb")
        dom = $(this)
        dom.addClass("current")
        current = dom.attr("src")
        if current.indexOf("msh-cdn0.qianshanghua.com")>=0
            current = current.split("?")[0]+"?imageView2"
        if current.indexOf("?")>=0
            current = current + "&a=current"
        for _dom in doms
            url = $(_dom).attr("src")
            if url.indexOf("msh-cdn0.qianshanghua.com")>=0
                url = url.split("?")[0]+"?imageView2"
            if $(_dom).hasClass("current")
                if url.indexOf("?")>=0
                    url = url + "&a=current"
                $(_dom).removeClass("current")
            urls.push url
        wx.previewImage
            current: current # 当前显示图片的http链接
            urls: urls # 需要预览的图片http链接列表
    root.hollow_confirm_show_add_comment_area = (title="发布瞬间",text="是否确认？",data_comment_id=null,remark_id=null) ->
        $("body").append """
        <div class="hollow_confirm_show_area">
            <div class="hollow_confirm_show_area_card">
                <div class="hollow_confirm_show_area_card_title">
                    <p>#{title}</p>
                </div>
                <div class="hollow_confirm_show_area_card_desc">
                    <p>#{text}</p>
                </div>
                <div class="hollow_confirm_show_area_card_confirm_tools">
                    <div class="hollow_confirm_cancel">我知道了</div>
                </div>
            </div>
        </div>
        """
    $("body").on "click",".show_add_comment_area",(evt)->
        $.ajax
            url:"/api/msh/level/check"
            data: null
            dataType: 'json'
            type: 'GET'
            success:(data)->
                if data.info == "ok"
                    if data.msh_qrcodepackage_num < 1
                        _html = """
                            <div>您还没有达到开通等级哟</div>
                        """
                        hollow_confirm_show_add_comment_area "发布瞬间",_html
                    else
                        $(".comments_submit_tools").removeClass("hide")
                        if $(".comments_submit_tools").length>0
                            $(".comments_submit_tools")[0].scrollIntoViewIfNeeded()
                            $(".comments_submit_tools").find(".comment_content").focus()
                else
                    _html = """
                        <div>尚未登录</div>
                    """
                    hollow_confirm_show_add_comment_area "发布瞬间",_html
            error:(data)->
                _html = """
                    <div>您还没有达到开通等级哟</div>
                """
                hollow_confirm_show_add_comment_area "发布瞬间",_html
    root.comment_submit =(dom)->
        chat_id = dom.parents(".comments_area").attr("data-block")
        content = dom.parents(".comments_area").find(".comment_content").val()
        comment_submit_add_img_one_list = $(".comment_submit_add_imgs").find(".comment_submit_add_img_one")
        if comment_submit_add_img_one_list.length > 0
            _imgs = []
            for _img in comment_submit_add_img_one_list
                _imgs.push $(_img).find(".comment_submit_add_img_one_img").attr("src")
            json_data =
                content: content
                images: _imgs
            json_data_str = JSON.stringify json_data
            content = "HWEBIMGS//#{json_data_str}"
        $.ajax
            url:"/api/page/comment/submit"
            data:
                block_id: BLOCK_ID
                chat_id: chat_id
                content: content
                uuid: uuid2(6,null)
            dataType: 'json'
            type: 'POST'
            success:(data)->
                console.log JSON.stringify(data)
                if data.info == "ok"
                    dom.parents(".comments_area").find(".comment_content").val("")
                    $(".comment_submit_add_imgs").addClass("hide")
                    $(".comment_submit_add_imgs").find(".comment_submit_add_img_one").remove()
                if data.info == "error"
                    alert data.about
            error:(data)->
                console.log data

    $("body").on "click",".del_one",(evt)->
        dom = $(this)
        dom_img_current = dom.parents(".comment_submit_add_img_one")
        dom_img_current.remove()        

    $(window).on "load",(evt)->
        comment_load_one_from_share()






root = exports ? this
# !!!! Hotpoor root object
root.Hs or= {}
Hs = root.Hs
Hs.DEVICE_USER = null
hotpoor_ws = null
hotpoor_timestamp = null
hotpoor_ws_device = null
WS_DEVICE =
    UNKNOWN  : 0
    READY    : 1
    OPEN     : 2
    POST     : 3
    BAD      : 4
root.formatDate = (now) ->
    now_date = new Date(now)
    audio_list_time_now = new Date()
    year = now_date.getFullYear()
    month = now_date.getMonth()+1
    date = now_date.getDate()
    hour = now_date.getHours()
    minute = now_date.getMinutes()
    if hour < 10
        hour = "0"+hour
    if minute < 10
        minute = "0"+minute

    if audio_list_time_now.getFullYear() == year && audio_list_time_now.getMonth()+1 == month && audio_list_time_now.getDate() == date
        return  hour+":"+minute
    if audio_list_time_now.getFullYear() == year
        # return  month+"月"+date+"日 "+hour+":"+minute
        return  "#{month}/#{date}/#{year}"
    # return  year+"年"+month+"月"+date+"日 "+hour+":"+minute
    return  "#{month}/#{date}/#{year}"
root.formatDateAll = (now) ->
    now_date = new Date(now)
    audio_list_time_now = new Date()
    year = now_date.getFullYear()
    month = now_date.getMonth()+1
    date = now_date.getDate()
    hour = now_date.getHours()
    minute = now_date.getMinutes()
    if hour < 10
        hour = "0"+hour
    if minute < 10
        minute = "0"+minute

    if audio_list_time_now.getFullYear() == year && audio_list_time_now.getMonth()+1 == month && audio_list_time_now.getDate() == date
        return  hour+":"+minute
    if audio_list_time_now.getFullYear() == year
        return  month+"月"+date+"日 "+hour+":"+minute
        # return  "#{month}/#{date}/#{year}"
    return  year+"年"+month+"月"+date+"日 "+hour+":"+minute
    # return  "#{month}/#{date}/#{year}"
root.formatDateAllEn = (now) ->
    now_date = new Date(now)
    audio_list_time_now = new Date()
    year = now_date.getFullYear()
    month = now_date.getMonth()+1
    date = now_date.getDate()
    hour = now_date.getHours()
    minute = now_date.getMinutes()
    if hour < 10
        hour = "0"+hour
    if minute < 10
        minute = "0"+minute

    if audio_list_time_now.getFullYear() == year && audio_list_time_now.getMonth()+1 == month && audio_list_time_now.getDate() == date
        return  hour+":"+minute
    if audio_list_time_now.getFullYear() == year
        return  date+"/"+month+" "+hour+":"+minute
        # return  "#{month}/#{date}/#{year}"
    return  date+"/"+month+"/"+year+" "+hour+":"+minute
    # return  "#{month}/#{date}/#{year}"
root.num_change = (num,zero="")->
    if num >= 1000000000000
        num_str = "AWSOME!!!"
    else if num >= 1000000000
        num_str = (num/1000000000.0).toFixed(1)
        num_str = "#{num_str}b"
    else if num >= 1000000
        num_str = (num/1000000.0).toFixed(1)
        num_str = "#{num_str}m"
    else if num >= 1000
        num_str = (num/1000.0).toFixed(1)
        num_str = "#{num_str}k"
    else if num == 0
        num_str = zero
    else
        num_str = num
        num_str = "#{num_str}"
    return num_str
root.str_is_JSON =(str)->
    if typeof str == 'string'
        try 
            obj = JSON.parse(str)
            if typeof obj == 'object' and obj
                return true
            else
                return false
        catch
            console.log("error：#{str}!!!")
            return false
    else
        console.log('It is not a string!')
        return false
root.ReplaceUrl = (text) ->
    a_text = text
    # re = /.*(?<![',",(])http[s]?:\/\/.*/gi
    re = /(http[s]?:\/\/([\w-]+.)+([:\d+])?(\/[\w-\.\/\?%&=]*)?)/gi
    s = a_text.replace re,(a)->
        a = a.split("<br>")[0]
        return '<a href="'+a+'" target=_blank>'+a+'</a>'
    return s
root.ReplaceTag = (text) ->
    a_text = text
    re = /<.*?>+/g
    s = a_text.replace re,(a)->
        a = a.replaceAll("</","[")
        a = a.replaceAll("<","[")
        a = a.replaceAll(">","]")
        return a
    return s
root.page_alert =(content)->
    alert content
$ ->
    console.log "page"

    if BLOCK_ID?
        hotpoor_ws_device = WS_DEVICE.UNKNOWN
        hotpoor_ws_device_open = false
        hotpoor_ws_timer = null

        heartCheck = (num=0)->
            message = JSON.stringify ["PING",num]
            console.log "hotpoor_ws_device",hotpoor_ws_device,hotpoor_ws
            if hotpoor_ws_device == WS_DEVICE.OPEN
                setTimeout ()->
                        hotpoor_ws.send message
                    ,10000
            else
                setTimeout ()->
                        heartCheck(num)
                    ,1000 
        restart_ws_connection = () ->
            console.log "restart_ws_connection"
            on_message = (params) ->
                # console.log params
                m_type = params[0]
                content_json = params[1]
                m_plus = ""
                m_aim = params[2]
                if m_type == "PONG"
                    num = content_json + 1
                    heartCheck(num)
                else if m_type in ["JOIN","LEAVE"]
                    join_info(content_json,m_aim)
                else if m_type == "COMMENT"
                    comment_add(content_json,m_aim)
                else if m_type == "COMMENTDEL"
                    comment_del(content_json,m_aim)
                else if m_type == "COMMENTLIKE"
                    comment_like(content_json,m_aim)
                else if m_type == "COMMENTREMARK"
                    comment_remark(content_json,m_aim)
                else if m_type == "COMMENTREMARKDEL"
                    comment_remark_del(content_json,m_aim)
                else if m_type == "COMMENTREFID"
                    comment_ref(content_json,m_aim)
                else if m_type == "WEIXINPAYCALLBACKSUCCESS"
                    weixin_pay_callback_add(content_json,m_aim)
                else if m_type == "ALIPAYPAYCALLBACKSUCCESS"
                    alipay_pay_callback_add(content_json,m_aim)
                else if m_type == "COMMENTPAGEUPDATEDOM"
                    page_dom(content_json)
                else if m_type == "COMMENTPAGEUPDATEDOMS"
                    page_doms(content_json)
                else if m_type == "COMMENTPAGEUPDATEDOMCONTENT"
                    page_dom_content(content_json)
                else if m_type == "COMMENTPAGEUPDATEDOMVIDEO"
                    page_dom_video(content_json)
                else if m_type == "COMMENTPAGEUPDATEDOMFILE"
                    page_dom_file(content_json)
                else if m_type == "COMMENTPAGEADDDOM"
                    page_dom_add(content_json)
                else if m_type == "COMMENTPAGEDELDOM"
                    page_dom_del(content_json)
                else if m_type == "COMMENTPAGEPERMISSION"
                    page_permission(content_json)
                else if m_type in ["COMMENTPAGEADDEDITOR","COMMENTPAGEDELEDITOR"]
                    page_editor_change(content_json)
                else if m_type in ["COMMENTPAGEADDHOLLOW","COMMENTPAGEDELHOLLOW"]
                    page_hollow_change(content_json)
                else if m_type == "COMMENTPAGEUPDATEDOMIFRAME"
                    page_dom_iframe(content_json)
                else if m_type == "COMMENTPAGEUPDATETITLE"
                    page_title(content_json)
                else if m_type == "COMMENTPAGEUPDATEDESC"
                    page_desc(content_json)
                else if m_type == "COMMENTPAGEGRIDGRAPH"
                    page_grid_graph(content_json)
                else if m_type == "COMMENTPAGEMAINAREA"
                    page_main_area(content_json)
                else if m_type == "COMMENTPAGECOPYDOM"
                    page_dom_copy(content_json)
                else if m_type == "COMMENTPAGECOPYDOMS"
                    page_doms_copy(content_json)
                else if m_type == "LOGINSCANSUBMIT"
                    login_scan_submit(content_json,m_aim)

                # Hs.video_list.push video_uri
                # console.log Hs.video_list

            if "WebSocket" of window and hotpoor_ws_device == WS_DEVICE.UNKNOWN
                hotpoor_ws.close() if hotpoor_ws?
                hotpoor_ws = new WebSocket WEBSOCKET_URL
                hotpoor_ws_device = WS_DEVICE.READY
                hotpoor_ws.onopen = () ->
                    heartCheck()
                    if hotpoor_ws_device != WS_DEVICE.POST
                        hotpoor_ws_device = WS_DEVICE.OPEN
                        hotpoor_ws_device_open = true
                        # load_chat_list() #开启hotpoor_ws成功，加载列表页
                        console.log "开启hotpoor_ws成功，加载列表页"
                        if root.check_is_subscribe?
                            root.check_is_subscribe()
                hotpoor_ws.onmessage = (evt) ->
                    if hotpoor_ws_device != WS_DEVICE.POST
                        params = JSON.parse(evt.data)
                        on_message(params)
                    console.log "ws 收到消息"
                hotpoor_ws.onclose = () ->
                    console.log "hotpoor_ws_device:#{hotpoor_ws_device}"
                    if hotpoor_ws_device != WS_DEVICE.POST
                        if hotpoor_ws_device == WS_DEVICE.OPEN or hotpoor_ws_device == WS_DEVICE.READY
                            hotpoor_ws_device = WS_DEVICE.UNKNOWN
                            console.log "wait"
                            clearTimeout hotpoor_ws_timer if hotpoor_ws_timer
                            hotpoor_ws_timer = setTimeout restart_ws_connection(), 500 if USER_ID
                        else
                            hotpoor_ws_device = WS_DEVICE.BAD
                hotpoor_ws.onerror = () ->
                    console.log "ws error"
                clearTimeout hotpoor_ws_timer if hotpoor_ws_timer
                hotpoor_ws_timer = setTimeout restart_ws_connection, 10000 if USER_ID
            else
                if hotpoor_ws_device_open
                    clearTimeout hotpoor_ws_timer if hotpoor_ws_timer
                    hotpoor_ws_timer = setTimeout restart_ws_connection, 10000 if USER_ID
                    return
        restart_ws_connection()
    root.login_scan_submit = (content_json,m_aim)->
        console.log content_json,m_aim
        login_scan_allow_now = "#{m_aim}/#{content_json['uuid']}"
        $.ajax
            url:"/api/login_scan/confirm"
            data:
                app: FINDMASTER_APP
                login_scan_allow:login_scan_allow_now
                user_id:content_json['user_id']
                redirect:window.location.href
            dataType: 'json'
            type: 'POST'
            success:(data)->
                console.log data
                if data.info == "ok"
                    if data.about == "redirect"
                        window.location.href = data.redirect
                else
                    page_alert data.about
            error:(data)->
                console.log data
    root.join_info = (content_json,chat_id)->
        num = content_json["num"]
        $(".room_connect_num>.span_num").text num_change(num)
    root.comment_add = (content_json, chat_id)->
        comment_html = comment_add_one_base(content_json)
        $(".comments_area[data-block=#{chat_id}]>.comments").prepend """
            #{comment_html}
        """
    root.comment_del = (content_json, chat_id)->
        if PAGE_TYPE == "msh_hollow"
            aim_dom = $(".comments_area[data-block=#{chat_id}]>.comments").find(".comment[data-comment-id=#{content_json['comment_id']}_#{content_json['sequence']}]")
            aim_dom.animate
                "height":0
            aim_dom.addClass("comment_animate_hide")
            aim_dom_flag = $(".comments_area[data-block=#{chat_id}]>.comments").find(".comment_type_flag[data-comment-id=#{content_json['comment_id']}_#{content_json['sequence']}]")
            aim_dom_flag.remove()
            do (aim_dom)->
                setTimeout ()->
                        aim_dom.remove()
                    ,1000
        else
            $(".comments_area[data-block=#{chat_id}]>.comments").find(".comment[data-comment-id=#{content_json['comment_id']}_#{content_json['sequence']}]").remove()
    root.comment_like = (content_json, chat_id)->
        if PAGE_TYPE == "msh_hollow"
            aim_dom = $(".comments_area[data-block=#{chat_id}]>.comments").find(".comment[data-comment-id=#{content_json['comment_id']}_#{content_json['sequence']}]")
            aim_btn = aim_dom.find(".comment_like")
            aim_value_dom = aim_dom.find(".comment_like_num")
            aim_value = parseInt content_json["likes_num"]
            aim_like = content_json["like"]
            if aim_value <=0
                aim_value_dom.attr("data-value","0")
                aim_value_dom.text "点赞"
            else
                aim_value_dom.attr("data-value",aim_value)
                aim_value_dom.text num_change(aim_value)
            if content_json["user_id"] == USER_ID
                if aim_like == "like"
                    aim_btn.addClass("like")
                else if aim_like == "dislike"
                    aim_btn.removeClass("like")
    root.comment_ref = (content_json, chat_id)->
        if PAGE_TYPE == "msh_hollow"
            aim_dom = $(".comments_area[data-block=#{chat_id}]>.comments").find(".comment[data-comment-id=#{content_json['comment_id']}_#{content_json['sequence']}]")
            aim_btn = aim_dom.find(".comment_share")
            aim_value_dom = aim_dom.find(".comment_share_num")
            aim_value = parseInt content_json["ref_num"]
            if aim_value <=0
                aim_value_dom.attr("data-value","0")
                aim_value_dom.text ""
            else
                aim_value_dom.attr("data-value",aim_value)
                aim_value_dom.text num_change(aim_value)

    root.secret_user_check = (content,headimg,nickname)->
        bysecretuser_fake = "false"
        bysecretuser = false
        bysecretuser_json = null
        if content?
            if content.indexOf("[BYSECRETUSER]")>=0
                bysecretuser_json = content.split("[BYSECRETUSER]")[1]
                content = content.split("[BYSECRETUSER]")[0]
                if str_is_JSON(bysecretuser_json)
                    bysecretuser = true
                    bysecretuser_json = JSON.parse(bysecretuser_json)
        if bysecretuser
            headimg = bysecretuser_json["headimgurl"]
            nickname = bysecretuser_json["name"]
            bysecretuser_fake = if bysecretuser_json["fake"]!=undefined then bysecretuser_json["fake"] else "false"
        else
            headimg = null
            nickname = null
        return [content,headimg,nickname,bysecretuser_fake]
    root.comment_add_one_remark = (content_json)->
        user_name = content_json["nickname"]
        content = content_json["content"]
        date_html = formatDateAllEn(content_json["time"]*1000)
        user_headimgurl = content_json["headimgurl"]
        comment_id = content_json["comment_id"]
        sequence = content_json["sequence"]
        user_id = content_json["user_id"]
        remark = content_json["remark"]

        remark_line_user_id = remark[0]
        remark_line_content = remark[1]
        remark_line_del_btn = ""
        if remark_line_user_id == USER_ID or IS_EDITOR
            remark_line_del_btn = """
                <span class="remark_del_action">Del</span>
                <span class="remark_line_del hide">Del</span>
            """
        remark_line_id = ""
        if remark.length > 3
            remark_line_id = remark[3]

        [remark_line_content,fake_headimg,fake_nickname,user_fake] = secret_user_check remark_line_content,user_headimgurl,user_name
        if user_fake == "true"
            nickname = "#{fake_nickname}[匿名]"
        else
            if fake_nickname == null
                nickname = "#{user_name}"
            else
                nickname = "#{fake_nickname}[#{user_name}]"
        remark_line_content_list = remark_line_content.split("//")
        remark_line_content_list_msgtype = remark_line_content_list[0]
        if remark_line_content_list_msgtype in ["HCALLUSER"]
            remark_line_content_list_call_user = remark_line_content_list[1]
            remark_line_content = remark_line_content_list[2]
            remark_line_content = ReplaceTag(remark_line_content)
            remark_line_content = ReplaceUrl(remark_line_content)
            remark_line_content_list_call_user_list = remark_line_content_list_call_user.split("_")
            remark_line_content_list_call_user = remark_line_content_list_call_user_list[0]
            if remark_line_content_list_call_user_list.length >=2
                nickname_call = remark_line_content_list_call_user_list[1]
            else
                nickname_call = members[remark_line_content_list_call_user].name
            if not nickname_call?
                nickname_call = ""
            html = """
                <div class="remark_line" data-user-id="#{remark_line_user_id}" data-remark-id="#{remark_line_id}"><span class="remark_line_nickname">#{nickname}</span>回复<span class="remark_line_nickname_call">#{nickname_call}</span><span>:</span><span class="remark_line_content">#{remark_line_content}</span>#{remark_line_del_btn}</div>
            """
            return html
        remark_line_content = ReplaceTag(remark_line_content)
        remark_line_content = ReplaceUrl(remark_line_content)
        html = """
            <div class="remark_line" data-user-id="#{remark_line_user_id}" data-remark-id="#{remark_line_id}"><span class="remark_line_nickname">#{nickname}</span><span>:</span><span class="remark_line_content">#{remark_line_content}</span>#{remark_line_del_btn}</div>
        """
        return html
    root.comment_load_one_remark = (remark)->
        remark = remark
        remark_line_user_id = remark[0]
        remark_line_content = remark[1]
        
        user_name = members[remark_line_user_id]["name"]
        user_headimgurl = members[remark_line_user_id]["headimgurl"]
        
        remark_line_del_btn = ""
        if remark_line_user_id == USER_ID or IS_EDITOR
            remark_line_del_btn = """
                <span class="remark_del_action">Del</span>
                <span class="remark_line_del hide">Del</span>
            """
        remark_line_id = ""
        if remark.length > 3
            remark_line_id = remark[3]

        [remark_line_content,fake_headimg,fake_nickname,user_fake] = secret_user_check remark_line_content,user_headimgurl,user_name
        if user_fake == "true"
            nickname = "#{fake_nickname}[匿名]"
        else
            if fake_nickname == null
                nickname = "#{user_name}"
            else
                nickname = "#{fake_nickname}[#{user_name}]"
        remark_line_content_list = remark_line_content.split("//")
        remark_line_content_list_msgtype = remark_line_content_list[0]
        if remark_line_content_list_msgtype in ["HCALLUSER"]
            remark_line_content_list_call_user = remark_line_content_list[1]
            remark_line_content = remark_line_content_list[2]
            remark_line_content = ReplaceTag(remark_line_content)
            remark_line_content = ReplaceUrl(remark_line_content)
            remark_line_content_list_call_user_list = remark_line_content_list_call_user.split("_")
            remark_line_content_list_call_user = remark_line_content_list_call_user_list[0]
            if remark_line_content_list_call_user_list.length >=2
                nickname_call = remark_line_content_list_call_user_list[1]
            else
                nickname_call = members[remark_line_content_list_call_user].name
            if not nickname_call?
                nickname_call = ""
            html = """
                <div class="remark_line" data-user-id="#{remark_line_user_id}" data-remark-id="#{remark_line_id}"><span class="remark_line_nickname">#{nickname}</span>回复<span class="remark_line_nickname_call">#{nickname_call}</span><span>:</span><span class="remark_line_content">#{remark_line_content}</span>#{remark_line_del_btn}</div>
            """
            return html
        remark_line_content = ReplaceTag(remark_line_content)
        remark_line_content = ReplaceUrl(remark_line_content)
        html = """
            <div class="remark_line" data-user-id="#{remark_line_user_id}" data-remark-id="#{remark_line_id}"><span class="remark_line_nickname">#{nickname}</span><span>:</span><span class="remark_line_content">#{remark_line_content}</span>#{remark_line_del_btn}</div>
        """
        return html
    root.comment_remark = (content_json, chat_id)->
        if PAGE_TYPE == "msh_hollow"
            aim_dom = $(".comments_area[data-block=#{chat_id}]>.comments").find(".comment[data-comment-id=#{content_json['comment_id']}_#{content_json['sequence']}]")
            aim_value_dom = aim_dom.find(".comment_remark_num")
            aim_value = parseInt content_json["remarks_num"]
            if aim_value <=0
                aim_value_dom.attr("data-value","0")
                aim_value_dom.text "评论"
            else
                aim_value_dom.attr("data-value",aim_value)
                aim_value_dom.text num_change(aim_value)
            aim_dom_remark_list = aim_dom.find(".hollow_remark_list")
            aim_dom_remark_list_one = comment_add_one_remark content_json
            aim_dom_remark_list.append """#{aim_dom_remark_list_one}"""
    root.comment_remark_del = (content_json,chat_id)->
        if PAGE_TYPE == "msh_hollow"
            aim_dom = $(".comments_area[data-block=#{chat_id}]>.comments").find(".comment[data-comment-id=#{content_json['comment_id']}_#{content_json['sequence']}]")
            aim_value_dom = aim_dom.find(".comment_remark_num")
            aim_value = parseInt content_json["remarks_num"]
            if aim_value <=0
                aim_value_dom.attr("data-value","0")
                aim_value_dom.text "评论"
            else
                aim_value_dom.attr("data-value",aim_value)
                aim_value_dom.text num_change(aim_value)
            aim_dom_remark_list = aim_dom.find(".hollow_remark_list")
            aim_dom_remark_id = content_json["remark_id"]
            aim_dom_remark_list_one = aim_dom_remark_list.find(".remark_line[data-remark-id=#{aim_dom_remark_id}]")
            aim_dom_remark_list_one.remove()
    root.weixin_pay_callback_add = (content_json, chat_id)->
        comment_html = weixin_pay_callback_add_one_base(content_json)
        $(".comments_area[data-block=#{chat_id}]>.comments").prepend """
            #{comment_html}
        """
    root.alipay_pay_callback_add = (content_json, chat_id)->
        comment_html = alipay_pay_callback_add_one_base(content_json)
        $(".comments_area[data-block=#{chat_id}]>.comments").prepend """
            #{comment_html}
        """
    root.page_dom_content_self = (content_json,key,key_item)->
        # console.log content_json[key]
        # console.log key
        # console.log key_item
        if typeof(content_json[key])=="string"
            # uuid2_now = JSON.parse(content_json[key])[key_item]
            try
                uuid2_now = JSON.parse(content_json[key])[key_item]
            catch d
                return false

        else
            uuid2_now = content_json[key][key_item]
        # console.log "uuid2_now:",uuid2_now
        if uuid2_now in root.uuid2s
            root.uuid2s.pop uuid2_now
            return true
        return false
    root.page_doms_copy = (content_jsons)->
        # console.log content_jsons["content"]
        page_doms_copy_items = []
        for content_json_content in content_jsons["content"]
            page_doms_copy_items.push content_json_content["dom_current"]
            do (content_json_content)->
                console.log "page_doms_copy"
                new_content_json = content_jsons
                new_content_json["content"]=content_json_content
                page_dom_copy(new_content_json)
        action_ids = "##{page_doms_copy_items.join(",#")}"
        $(".card_more_selected").removeClass("card_more_selected")
        $(action_ids).find(".card_more_select").click()
    root.page_dom_copy = (content_json)->
        page_dom_add content_json, true, (content_json)->
            do (content_json)->
                main_content = content_json["content"]
                if main_content["dom_type"] == "iframe"
                    page_dom_iframe content_json,true,(content_json)->
                        page_dom(content_json)
                else if main_content["dom_type"] == "text"
                    page_dom_content content_json,true,(content_json)->
                        page_dom(content_json)
                else if main_content["dom_type"] == "video"
                    page_dom_video content_json,true,(content_json)->
                        page_dom(content_json)
                else if main_content["dom_type"] == "file"
                    page_dom_file content_json,true,(content_json)->
                        page_dom(content_json)
                else
                    page_dom(content_json)
    root.page_doms = (content_json)->
        if page_dom_content_self(content_json["content"],"dom_content","uuid")
            console.log "self"
        main_content = content_json["content"]
        console.log main_content
        for update in main_content["updates"]
            $("##{update["dom_id"]}").animate
                "left":update["x"]
                "top":update["y"]
                "width":update["w"]
                "height":update["h"]
    root.page_dom = (content_json)->
        console.log "page_dom"
        console.log content_json
        main_content = content_json["content"]
        dom_id = main_content["dom_current"]
        dom_x = main_content["dom_position_x"]
        dom_y = main_content["dom_position_y"]
        dom_w = main_content["dom_position_w"]
        dom_h = main_content["dom_position_h"]
        dom_z = main_content["dom_position_z"]
        dom_s = main_content["dom_scroll"]
        dom_r = main_content["dom_scroll_relative"]
        dom = $("##{dom_id}")
        if $("##{dom_id}").hasClass "dom_video"
            $("#player_#{dom_id}").css
                "width":dom_w
                "height":dom_h
        else if $("##{dom_id}").hasClass "dom_iframe"
            $("##{dom_id}>.sections>.section>iframe").css
                "width":dom_w
                "height":dom_h
        if dom.hasClass("self-editing")
            return
        if dom_s == ""
            if $("##{dom_id}").hasClass("dom_scroll_auto")
                $("##{dom_id}").removeClass("dom_scroll_auto")
        else
            $("##{dom_id}").addClass(dom_s)
        $("##{dom_id}").css
            "width":dom_w
            "height":dom_h
        $("##{dom_id}").animate
                "left":dom_x
                "top":dom_y
                "zIndex":dom_z
            ,500
        if dom_r == ""
            if $("##{dom_id}").hasClass("dom_scroll_relative")
                $("##{dom_id}").removeClass("dom_scroll_relative")
                $("##{dom_id}").css
                    "padding": "0px"
        else
            $("##{dom_id}").addClass(dom_r)
            $("##{dom_id}").css
                "width": "-webkit-fill-available"
                "height": "fit-content"
                "padding": "10px 20px"
        $("##{dom_id}>.z_index_num").text dom_z
        
    root.page_dom_content = (content_json,copy=false,callback=null)->
        if page_dom_content_self(content_json["content"],"dom_content","uuid")
            console.log "self"
        else
            if copy
                b = content_json["content"]["dom_content"]
                b_html = b
                b["dom_id"]=content_json["content"]["dom_current"]
            else    
                b = JSON.parse(content_json["content"]["dom_content"])
                b_html = b["text"]

            a=$("##{b["dom_id"]}>.sections").html(b_html)
            # a=$("##{b["dom_id"]}>.sections>.section")[0]
            
            # if b["end_node"]==b["start_node"] and b["end"]>b["start"]
            #     # 增加
            #     if b["text"]!=""
            #         a.childNodes[b["start_node"]].insertData(b["start"],b["text"])
            # else if b["end_node"]==b["start_node"] and b["end"]<=b["start"]
            #     if b["text"]!=""
            #         # 删除
            #         a.childNodes[b["start_node"]].deleteData(b["end"],b["start"]-b["end"])
            # else if b["end_node"]==-1
            #     a.insertBefore(document.createElement("br"),null)
            # a.normalize()
        if copy
            callback(content_json)
    root.page_dom_file = (content_json,copy=false,callback=null)->
        main_content = content_json["content"]
        if copy
            b = content_json["content"]["dom_content"]
            b["dom_id"]=main_content["dom_current"]
            b["text"]=
                "src":b["src"]
                "type":b["type"]
                "poster":b["poster"]
                "name":b["name"]
                "size":b["size"]
        else
            b = JSON.parse(content_json["content"]["dom_content"])
        # b = JSON.parse(content_json["content"]["dom_content"])
        w = $("##{b["dom_id"]}").width()
        h = $("##{b["dom_id"]}").height()
        vt = uuid2(6,null)
        $(".nofilespan").remove()
        $("##{b['dom_id']}>.sections>.section").prepend """
            <button class="file_download" data-href="#{b["text"]["src"]}" data-name="#{b["text"]["name"]}">点击下载</button>
            <a target="_blank" href="#{b["text"]["src"]}?attname=#{b["text"]["name"]}" >
                <div>#{b["text"]["poster"]}</div>
                <div>#{b["text"]["type"]}</div>
                <div>#{b["text"]["name"]}</div>
                <div>#{b["text"]["size"]}</div>
            </a>

        """
        if PAGE_TYPE == "page_edit"
            $("##{b['dom_id']}>.sections>.section>div>.file_src").val(b["text"]["src"])
            $("##{b['dom_id']}>.sections>.section>div>.file_type").val(b["text"]["type"])
            $("##{b['dom_id']}>.sections>.section>div>.file_poster").val(b["text"]["poster"])
            $("##{b['dom_id']}>.sections>.section>div>.file_name").val(b["text"]["name"])
            $("##{b['dom_id']}>.sections>.section>div>.file_size").val(b["text"]["size"])
        if copy
            callback(content_json)
    root.page_dom_video = (content_json,copy=false,callback=null)->
        main_content = content_json["content"]
        if copy
            b = content_json["content"]["dom_content"]
            b["dom_id"]=main_content["dom_current"]
            b["text"]=
                "src":b["src"]
                "type":b["type"]
                "poster":b["poster"]
        else
            b = JSON.parse(content_json["content"]["dom_content"])
        # b = JSON.parse(content_json["content"]["dom_content"])
        w = $("##{b["dom_id"]}").width()
        h = $("##{b["dom_id"]}").height()
        $("#player_#{b["dom_id"]}").remove()
        vt = uuid2(6,null)
        $(".novideospan").remove()
        $("##{b['dom_id']}>.sections>.section").prepend """
            <video id="player_#{b["dom_id"]}" data-vt="#{vt}" width="#{w}" height="#{h}" class="video-js vjs-default-skin" poster="#{b["text"]["poster"]}"
                    controls
                    webkit-playsinline="true"
                    playsinline="true">
                <source src="#{b["text"]["src"]}" type="#{b["text"]["type"]}">
                <!-- .m3u8 application/x-mpegURL -->
            </video>
        """
        videojs("#player_#{b["dom_id"]}[data-vt=#{vt}]");

        if PAGE_TYPE == "page_edit"
            $("##{b['dom_id']}>.sections>.section>div>.video_src").val(b["text"]["src"])
            $("##{b['dom_id']}>.sections>.section>div>.video_type").val(b["text"]["type"])
            $("##{b['dom_id']}>.sections>.section>div>.video_poster").val(b["text"]["poster"])
        if copy
            callback(content_json)
    root.page_dom_iframe = (content_json,copy=false,callback=null)->
        main_content = content_json["content"]
        if copy
            console.log main_content
            console.log "========"
            b = main_content["dom_content"]
            iframe_html = b["html"]
            b["dom_id"]=main_content["dom_current"]
            console.log b["dom_id"]
        else
            b = JSON.parse(main_content["dom_content"])
            iframe_html = b["text"]["html"]
        console.log iframe_html
        # b = JSON.parse(content_json["content"]["dom_content"])
        w = $("##{b["dom_id"]}").width()
        h = $("##{b["dom_id"]}").height()

        if PAGE_TYPE == "page_edit"
            iframe_tools = $("##{b['dom_id']}>.sections>.section>.iframe_tool")
        $("##{b['dom_id']}>.sections>.section>iframe").remove()
        $("##{b['dom_id']}>.sections>.section").empty()
        $("##{b['dom_id']}>.sections>.section").prepend """
            #{iframe_html}
        """
        $("##{b['dom_id']}>.sections>.section>iframe").css
            "width":w
            "height":h

        if PAGE_TYPE == "page_edit"
            $("##{b['dom_id']}>.sections>.section").append iframe_tools
            console.log "===iframe_html 1==="
            console.log iframe_html
            console.log "===iframe_html 2==="
            console.log "##{b['dom_id']}>.sections>.section>div>.iframe_html"
            $("##{b['dom_id']}>.sections>.section>div>.iframe_html").val(iframe_html)
        if copy
            callback(content_json)
    root.page_main_area=(content_json)->
        main_content = content_json["content"]
        if page_dom_content_self(main_content,"dom_content","uuid")
            console.log "self"
            return
        if typeof(content_json["content"]["dom_content"]) == "string"
            b = JSON.parse(content_json["content"]["dom_content"])
        else
            b = content_json["content"]["dom_content"]
        # b = JSON.parse(content_json["content"]["dom_content"])
        _w = parseInt(b["text"]["w"])
        _h = parseInt(b["text"]["h"])

        if PAGE_TYPE in ["page_edit","page"]
            $(".main_area").css
                "width":"#{_w}px"
                "height":"#{_h}px"
    root.page_grid_graph=(content_json)->
        main_content = content_json["content"]
        if page_dom_content_self(main_content,"dom_content","uuid")
            console.log "self"
            return
        if typeof(content_json["content"]["dom_content"]) == "string"
            b = JSON.parse(content_json["content"]["dom_content"])
        else
            b = content_json["content"]["dom_content"]
        # b = JSON.parse(content_json["content"]["dom_content"])
        _w = parseInt(b["text"]["w"])*2
        _h = parseInt(b["text"]["h"])*2

        if PAGE_TYPE == "page_edit"
            $("body").css
                "backgroundSize":"#{_w}px #{_h}px"
    root.page_title=(content_json)->
        main_content = content_json["content"]
        if page_dom_content_self(main_content,"dom_content","uuid")
            console.log "self"
            return
        b = JSON.parse(content_json["content"]["dom_content"])
        title = b["title"]

        if PAGE_TYPE == "page_edit"
            $(".top_area_info_title").val(title)
            title_tag = "Page Edit"
        else
            title_tag = "Page"
        title_list = window.document.title.split(title_tag)
        title_list[0]="#{title} "
        window.document.title = title_list.join(title_tag)
    root.page_desc=(content_json)->
        main_content = content_json["content"]
        if page_dom_content_self(main_content,"dom_content","uuid")
            console.log "self"
            return
        b = JSON.parse(content_json["content"]["dom_content"])
        desc = b["desc"]

        if PAGE_TYPE == "page_edit"
            block_desc_content_old = desc
            $(".block_desc_content").val(desc)
    root.page_dom_add = (content_json,copy=false,callback=null)->
        main_content = content_json["content"]
        dom_current = main_content["dom_current"]
        dom_content = main_content["dom_content"]
        dom_x = main_content["dom_position_x"]
        dom_y = main_content["dom_position_y"]
        dom_w = main_content["dom_position_w"]
        dom_h = main_content["dom_position_h"]
        dom_z = main_content["dom_position_z"]
        dom_type = main_content["dom_type"]

        if PAGE_TYPE == "page_edit"
            if dom_type == "video"
                dom_content = """
                <div class="section" contenteditable="false">
                    <div>video_src:<input class="video_src"></div>
                    <div>video_type:<input class="video_type"></div>
                    <div>video_poster:<input class="video_poster"></div>
                    <div>
                        <button class="video_add">upload video</button>
                        <button class="video_save">save</button>
                    </div>
                </div>
                """
            else if dom_type == "file"
                dom_content = """
                <div class="section" contenteditable="false">
                    <div>file_src:<input class="file_src"></div>
                    <div>file_type:<input class="file_type"></div>
                    <div>file_poster:<input class="file_poster"></div>
                    <div>file_size:<input class="file_size"></div>
                    <div>file_name:<input class="file_name"></div>
                    <div>
                        <button class="file_add">upload file</button>
                        <button class="file_save">save</button>
                    </div>
                </div>
                """
            else if dom_type == "iframe"
                dom_content = """
                <div class="section" contenteditable="false">
                    <div class="iframe_tool"><textarea class="iframe_html" placeholder="/* html code */"></textarea></div>
                    <div class="iframe_tool"><button class="iframe_save">save</button></div>
                </div>
                """
            html_control = """
            <div class="card_move"></div>
            <div class="card_more_select"></div>
            <div class="card_copy"></div>
            <div class="card_del"></div>
            <div class="resize_btn"></div>
            <div class="card_z_index z_index_max"></div>
            <div class="card_z_index z_index_up"></div>
            <div class="card_z_index z_index_down"></div>
            <div class="card_z_index z_index_min"></div>
            <div class="card_z_index z_index_num">#{dom_z}</div>
            <div class="card_scroll_relative">
                <div class="card_scroll_relative_svg"></div>
            </div>
            <div class="card_scroll_auto">
                <div class="card_scroll_auto_svg"></div>
            </div>
            <div class="card_text_align text_align_left"></div>
            <div class="card_text_align text_align_center"></div>
            <div class="card_text_align text_align_right"></div>
            <div class="card_font_size font_size_big"></div>
            <div class="card_font_size font_size_small"></div>
            <div class="card_font_color">
                <div class="card_font_color_demo">
                </div>
            </div>
            """
            html = """
                <div    id="#{dom_current}" class="card dom dom_#{dom_type}" 
                            data-tree="#{dom_current}" 
                            style="
                            left: #{dom_x}px;
                            top: #{dom_y}px;
                            width: #{dom_w}px;
                            height: #{dom_h}px;
                            z-index: #{dom_z};
                            ">
                            <style></style>
                        <div class="sections" contenteditable="true">
                            #{dom_content}
                        </div>
                        #{html_control}
                </div>
            """
        else
            if dom_type == "video"
                dom_content = """
                    <div class="section" contenteditable="false"><span class="novideospan">视频未设置</span></div>
                """
            else if dom_type == "file"
                dom_content = """
                    <div class="section" contenteditable="false"><span class="novideospan">文件未设置</span></div>
                """
            else if dom_type == "iframe"
                dom_content = """
                    <div class="section" contenteditable="false">iframe暂未设置</div>
                """
            html_control = """
            <div class="card_move hide"></div>
            <div class="card_more_select hide"></div>
            <div class="card_copy hide"></div>
            <div class="card_del hide"></div>
            <div class="resize_btn hide"></div>
            """
            html = """
                <div    id="#{dom_current}" class="card dom dom_#{dom_type}" 
                            data-tree="#{dom_current}" 
                            style="
                            left: #{dom_x}px;
                            top: #{dom_y}px;
                            width: #{dom_w}px;
                            height: #{dom_h}px;
                            z-index: #{dom_z};
                            ">
                            <style></style>
                        <div class="sections">
                            #{dom_content}
                        </div>
                        #{html_control}
                </div>
            """
        $(".main_area").append html
        if copy
            callback(content_json)
    root.page_dom_del = (content_json)->
        main_content = content_json["content"]
        dom_current = main_content["dom_current"]
        $("##{dom_current}").remove()
    root.page_permission = (content_json)->
        main_content = content_json["content"]
        if main_content["action"] == "reload page"
            window.location.reload()
    root.page_editor_change = (content_json)->
        main_content = content_json["content"]
        if main_content["aim_user_id"] == USER_ID
            window.location.reload()
        else
            if main_content["action"] == "add editor"
                load_users(["editors"])
            else if main_content["action"] == "del editor"
                load_users(["editors"])
    root.page_hollow_change = (content_json)->
        main_content = content_json["content"]
        if main_content["action"] == "add hollow"
            load_keys(["hollows"])
        else if main_content["action"] == "del hollow"
            load_keys(["hollows"])
    root.load_keys = (groups)->
        for group in groups
            do (group)->
                $.ajax
                    url:"/api/page/#{group}"
                    data:
                        block_id: BLOCK_ID
                    dataType: 'json'
                    type: 'GET'
                    success:(data)->
                        console.log JSON.stringify(data)
                        $(".block_#{group}_list").text data[group]
                    error:(data)->
                        console.log data
    root.load_keys(["hollows"])
    root.load_users = (groups)->
        for group in groups
            do (group)->
                $.ajax
                    url:"/api/page/#{group}"
                    data:
                        block_id: BLOCK_ID
                    dataType: 'json'
                    type: 'GET'
                    success:(data)->
                        console.log JSON.stringify(data)
                        $(".block_#{group}_list").text data[group]
                    error:(data)->
                        console.log data
    root.load_users(["editors","readers","blackers","members"])

    device_uuid = uuid2(6,null)
    Hs.DEVICE_USER = "#{USER_ID}_#{device_uuid}"
    console.log Hs.DEVICE_USER

    root.members = {}
    root.alipay_pay_callback_add_one_base = (content_json)->
        user_name = content_json["nickname"]
        content = content_json["content"]
        content = ("""<div class="content_table"><div>#{k}</div><div>#{v}</div></div>""" for k,v of content).join("\n\r")
        date_html = formatDateAllEn(content_json["time"]*1000)
        user_headimgurl = content_json["headimgurl"]
        comment_id = content_json["comment_id"]
        sequence = content_json["sequence"]
        html = """
            <div class="comment" data-comment-id="#{comment_id}_#{sequence}">
                <div class="comment_img"><img src="#{user_headimgurl}"></div>
                <div class="comment_line"><span class="name">#{user_name}</span><span class="date">#{date_html}</span></div>
                <div class="comment_line"><p class="content">#{content}</p></div>
            </div>
        """
        return html
    root.weixin_pay_callback_add_one_base = (content_json)->
        user_name = content_json["nickname"]
        content = content_json["content"]
        content = ("""<div class="content_table"><div>#{k}</div><div>#{v}</div></div>""" for k,v of content).join("\n\r")
        date_html = formatDateAllEn(content_json["time"]*1000)
        user_headimgurl = content_json["headimgurl"]
        comment_id = content_json["comment_id"]
        sequence = content_json["sequence"]
        html = """
            <div class="comment" data-comment-id="#{comment_id}_#{sequence}">
                <div class="comment_img"><img src="#{user_headimgurl}"></div>
                <div class="comment_line"><span class="name">#{user_name}</span><span class="date">#{date_html}</span></div>
                <div class="comment_line"><p class="content">#{content}</p></div>
            </div>
        """
        return html
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
                <button class="comment_control_tool_btn comment_del">DEL</button>
            </div>
            """
        html = """
            <div class="comment" data-comment-id="#{comment_id}_#{sequence}">
                <div class="comment_img"><img src="#{user_headimgurl}"></div>
                <div class="comment_line"><span class="name">#{user_name}</span><span class="date">#{date_html}</span></div>
                <div class="comment_line"><p class="content">#{content}</p></div>
                #{control_tools}
            </div>
        """
        return html
    root.comment_load_one_base = (comment_list,comment_id)->
        if comment_list[6]==1
            return ""
        user_name = members[comment_list[1]]["name"]
        content = comment_list[4]
        if comment_list[3] in ["COMMENT"]
            content = content
        else if comment_list[3] in ["WEIXINPAYCALLBACKSUCCESS","ALIPAYPAYCALLBACKSUCCESS"]
            content = ("""<div class="content_table"><div>#{k}</div><div>#{v}</div></div>""" for k,v of content).join("\n\r")

        date_html = formatDateAllEn(comment_list[2]*1000)
        user_headimgurl = members[comment_list[1]]["headimgurl"]
        control_tools=""
        if comment_list[3] not in ["WEIXINPAYCALLBACKSUCCESS","ALIPAYPAYCALLBACKSUCCESS"]
            if IS_EDITOR or USER_ID == comment_list[1]
                control_tools = """
                <div class="comment_line">
                    <button class="comment_control_tool_btn comment_del">DEL</button>
                </div>
                """
        html = """
            <div class="comment" data-comment-id="#{comment_id}_#{comment_list[0]}">
                <div class="comment_img"><img src="#{user_headimgurl}"></div>
                <div class="comment_line"><span class="name">#{user_name}</span><span class="date">#{date_html}</span></div>
                <div class="comment_line"><p class="content">#{content}</p></div>
                #{control_tools}
            </div>
        """
        return html
    root.comment_load = (chat_id,comment_id=null)->
        $(".comments_area[data-block=#{chat_id}]>.comments>.comment_more_info").removeClass("comment_more_action")
        $(".comments_area[data-block=#{chat_id}]>.comments>.comment_more_info").text "—— LOADING ——"
        $.ajax
            url:"/api/page/comment/load"
            data:
                chat_id: chat_id
                comment_id: comment_id
            dataType: 'json'
            type: 'GET'
            success:(data)->
                if data.info == "ok"
                    for k,v of data.members
                        members[k]=v
                    for comment in data.comments by -1
                        comment_html = comment_load_one_base(comment,data.comment_id)
                        $(".comments_area[data-block=#{chat_id}]>.comments").append """
                            #{comment_html}
                        """
                    $(".comments_area[data-block=#{chat_id}]>.comments>.comment_more_info").remove()
                    if data.last_comment_id == null
                        if data.comments.length > 0
                            $(".comments_area[data-block=#{chat_id}]>.comments").append """
                                <div class="comment_more_info">—— END ——</div>
                            """
                        else
                            $(".comments_area[data-block=#{chat_id}]>.comments").append """
                                <div class="comment_more_info">—— WAIT YOUR COMMENTS ——</div>
                            """
                    if data.last_comment_id != null
                        $(".comments_area[data-block=#{chat_id}]>.comments").append """
                            <div class="comment_more_info comment_more_action" data-flag="#{data.last_comment_id}">—— MORE ——</div>
                        """
                        if data.comments.length < 10
                            comment_load(chat_id,data.last_comment_id)
                        
            error:(data)->
                console.log data

    $("body").on "click",".comment_more_action",(evt)->
        chat_id = $(this).parents(".comments_area").attr("data-block")
        last_comment_id = $(this).attr("data-flag")
        comment_load(chat_id,last_comment_id)

    root.comment_submit =(dom)->
        chat_id = dom.parents(".comments_area").attr("data-block")
        content = dom.parents(".comments_area").find(".comment_content").val()
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
                if data.info == "error"
                    page_alert data.about
            error:(data)->
                console.log data
    $("body").on "click",".comment_submit",(evt)->
        dom = $(this)
        root.comment_submit dom

    $("body").on "click",".comment_del",(evt)->
        dom = $(this)
        chat_id = dom.parents(".comments_area").attr("data-block")
        data_comment_id_list = dom.parents(".comment").attr("data-comment-id").split("_")
        comment_id = data_comment_id_list[0]
        comment_sequence = data_comment_id_list[1]
        content = "del comment #{comment_id}_#{comment_sequence}"
        $.ajax
            url:"/api/page/comment/del"
            data:
                block_id: BLOCK_ID
                chat_id: chat_id
                content: content
                comment_id:comment_id
                comment_sequence:comment_sequence
                like_content:"del"
                uuid: uuid2(6,null)
            dataType: 'json'
            type: 'POST'
            success:(data)->
                console.log JSON.stringify(data)
                if data.info == "error"
                    page_alert data.about
            error:(data)->
                console.log data

    $("body").on "click",".comment_like_btn",(evt)->
        _this = $(this)
        dom = _this.find(".comment_like")
        like_content = "like"
        if dom.hasClass("like")
            like_content = "dislike"
            dom.removeClass("like")
        else
            dom.addClass("like")
        like_dom_comment_id = dom.parents(".comment").attr("data-comment-id")
        like_doms = $(".comment[data-comment-id=#{like_dom_comment_id}]").find(".comment_like")
        if like_content in ["like"]
            like_doms.addClass("like")
        else if like_content in ["dislike"]
            like_doms.removeClass("like")
        chat_id = dom.parents(".comments_area").attr("data-block")
        data_comment_id_list = dom.parents(".comment").attr("data-comment-id").split("_")
        comment_id = data_comment_id_list[0]
        comment_sequence = data_comment_id_list[1]
        content = "like comment #{comment_id}_#{comment_sequence}"
        $.ajax
            url:"/api/page/comment/like"
            data:
                block_id: BLOCK_ID
                chat_id: chat_id
                content: content
                comment_id:comment_id
                comment_sequence:comment_sequence
                like_content:like_content
                uuid: uuid2(6,null)
            dataType: 'json'
            type: 'POST'
            success:(data)->
                console.log JSON.stringify(data)
                if data.info == "error"
                    page_alert data.about
            error:(data)->
                console.log data
    $("body").on "click",".remark_line_del",(evt)->
        _this = $(this)
        dom = _this.parents(".hollow_remark_list")
        remark_id = _this.parents(".remark_line").attr("data-remark-id")
        chat_id = dom.parents(".comments_area").attr("data-block")
        console.log "--------"
        console.log dom.parents(".comment")
        data_comment_id_list = dom.parents(".comment").attr("data-comment-id").split("_")
        comment_id = data_comment_id_list[0]
        comment_sequence = data_comment_id_list[1]
        content = "del remark comment #{comment_id}_#{comment_sequence}"
        $.ajax
            url:"/api/page/comment/remark_del"
            data:
                block_id: BLOCK_ID
                chat_id: chat_id
                content: content
                comment_id:comment_id
                comment_sequence:comment_sequence
                remark_id:remark_id
                uuid: uuid2(6,null)
            dataType: 'json'
            type: 'POST'
            success:(data)->
                console.log JSON.stringify(data)
                if data.info == "error"
                    page_alert data.about
            error:(data)->
                console.log data
        evt.stopPropagation()
        evt.preventDefault()
    $("body").on "click",".remark_submit",(evt)->
        _this = $(this)
        dom = _this.parents(".hollow_remark_controls")
        dom_remark_content = dom.find(".remark_content")
        remark_content = dom_remark_content.val()
        remark_content = ReplaceTag(remark_content)

        remark_call_user = dom_remark_content.attr("data-call-user")
        remark_call_user_name = dom_remark_content.attr("data-call-user-name")
        if remark_call_user in [undefined,null,""]
            remark_content = "#{remark_content}"
        else
            if remark_call_user_name in [undefined,null,""]
                remark_content = "HCALLUSER//#{remark_call_user}//#{remark_content}"
            else
                remark_content = "HCALLUSER//#{remark_call_user}_#{remark_call_user_name}//#{remark_content}"

        chat_id = dom.parents(".comments_area").attr("data-block")
        data_comment_id_list = dom.parents(".comment").attr("data-comment-id").split("_")
        comment_id = data_comment_id_list[0]
        comment_sequence = data_comment_id_list[1]
        content = "remark comment #{comment_id}_#{comment_sequence}"
        $.ajax
            url:"/api/page/comment/remark"
            data:
                block_id: BLOCK_ID
                chat_id: chat_id
                content: content
                comment_id:comment_id
                comment_sequence:comment_sequence
                remark_content:remark_content
                uuid: uuid2(6,null)
            dataType: 'json'
            type: 'POST'
            success:(data)->
                dom_remark_content.val("")
                console.log JSON.stringify(data)
                if data.info == "error"
                    page_alert data.about
            error:(data)->
                console.log data
    remark_line_select = "false"
    $("body").on "mousedown",".remark_line",(evt)->
        console.log "mousedown"
        remark_line_select = "false"
    $("body").on "mousemove",".remark_line",(evt)->
        console.log "mousemove"
        remark_line_select = "true"
    $("body").on "mouseup",".remark_line",(evt)->
        console.log "mouseup"
        if remark_line_select == "true"
            setTimeout ()->
                    remark_line_select = "false"
                ,1000

    $("body").on "click",".file_download",(evt)->
        dom = $(this)
        a = dom.attr("data-href")
        b = dom.attr("data-name")
        window.open(a.replace("http://","https://")+"?attname="+encodeURIComponent(b),"Download·下载")

    $("body").on "click",".remark_line",(evt)->
        if  remark_line_select == "false"
            console.log "click"
            _this = $(this)
            dom_user_id = _this.attr("data-user-id")
            dom = _this.parents(".hollow_remark_tools")
            dom_remark_content = dom.find(".remark_content")
            dom_user_nickname = _this.find(".remark_line_nickname").text()
            console.log dom_user_id,USER_ID
            console.log dom_remark_content
            console.log dom_user_nickname
            if dom_user_id != USER_ID
                dom_remark_content.attr("placeholder","回复#{dom_user_nickname}:")
                dom_remark_content.attr("data-call-user","#{dom_user_id}")
                dom_remark_content.attr("data-call-user-name","#{dom_user_nickname}")
                # dom_remark_content.val("")
                # dom_remark_content.focus()
            else
                dom_remark_content.attr("data-call-user","")
                dom_remark_content.attr("data-call-user-name","")
                dom_remark_content.attr("placeholder","请输入评论")
                # dom_remark_content.val("")
                # dom_remark_content.focus()
            dom_remark_controls = dom.find(".hollow_remark_controls")
            if dom_remark_controls.hasClass("hide")
                dom_remark_controls.removeClass("hide")
                $(".remark_content").removeClass("current")
                dom_remark_content.addClass("current")
                do (dom_remark_content)->
                    setTimeout ()->
                            # dom[0].scrollIntoView()
                            $("html").animate
                                    scrollTop: dom_remark_content.offset().top - 120
                                , "250", ()->
                                    $(window).scrollTop dom_remark_content.offset().top - 120
                                    dom_remark_content.focus()
                        ,250

    root.join_more_room_message_send = (a,b,c,d)->
        join_more_room_message = JSON.stringify [a,b,c,d]
        console.log join_more_room_message
        hotpoor_ws.send join_more_room_message


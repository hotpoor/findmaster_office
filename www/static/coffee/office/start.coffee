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
$ ->
    console.log "start"
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
                    alert data.about
            error:(data)->
                console.log data
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
                        hollow_confirm_is_subscribe "欢迎访问PUCO噗叩·Office",cover_html
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
    root.hollow_confirm_is_subscribe = (title="欢迎访问PUCO噗叩·时光机",text="是否确认？",data_comment_id=null,remark_id=null) ->
        $(".hollow_confirm_show_area").remove()
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
    root.join_more_room_message_send = (a,b,c,d)->
        join_more_room_message = JSON.stringify [a,b,c,d]
        console.log join_more_room_message
        hotpoor_ws.send join_more_room_message








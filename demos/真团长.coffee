<style>
#qq_map{
    width:100%;
    height:100%;
}
#qq_map_page{
    width:100%;
    position:fixed;
    min-height:120px;
    height:auto;
    background:white;
    border-radius:20px 20px 0px 0px;
    box-shadow:0px -2px 4px rgba(0,0,0,0.2);
    bottom:0px;
    z-index:2000;
}
.qq_map_page_line{
    width:100%;
    min-height:60px;
    height:auto;
}
.qq_map_page_line>div.qqmt_get_location{
    text-align: center;
    color: white;
    background: black;
    margin: 20px 30px 10px 30px;
    padding: 10px 20px;
    font-size: 20px;
    border-radius: 16px;
    box-shadow: 0px 4px 8px rgba(0,0,0,0.2);
    cursor:pointer;
}
.qq_map_page_line>div.qqmt_get_comments{
    text-align: center;
    color: white;
    background: black;
    margin: 10px 30px;
    padding: 10px 20px;
    font-size: 20px;
    border-radius: 16px;
    box-shadow: 0px 4px 8px rgba(0,0,0,0.2);
    cursor:pointer;
}
.qq_map_page_line>div{
    margin:10px 0px;
}
.qq_map_user{
    box-shadow: rgba(0, 0, 0, 0.3) 0px 2px 8px;
    height:30px;
    width:30px;
    background:#fff;
    border-radius:50%;
    position:absolute;
    top:0px;
    left:0px;
    border:2px solid white;
}
.qqmt_card_pointer[data-type="user"]{
    width:100%;
    height:100%;
    border-radius:50%;
    overflow:hidden;
}
.qqmt_card_pointer[data-type="user"]>img{
    width:100%;
    height:100%;
    object-fit:cover;
}
.content{
    word-break:break-all;
}
</style>

<script charset="utf-8" src="https://map.qq.com/api/gljs?v=1.exp&amp;libraries=service&amp;key=HWIBZ-2PQC6-T6DSS-EW5WV-I6JQQ-3XBD5"></script>
<script type="text/coffeescript">
root = exports ? this
# !!!! Hotpoor root object
root.Hs or= {}
Hs = root.Hs
Hs.qq_map_chat_id = "d903bdbdb23444e396bf17e2fd4bd050"
if window.location.href.indexOf("/page/edit/")>-1
    $(".base_area").show()
else
    $(".base_area").hide()
    $("body").css "height","100%"
$("body").append """
    <div id="qq_map"></div>
    <div id="qq_map_page">
        <div class="qq_map_page_line">
            <div class="qq_map_tool qqmt_get_location">更新获取当前定位</div>
        </div>
        <div class="qq_map_page_line">
            <div class="qq_map_tool qqmt_get_comments">展开留言板</div>
        </div>
        <div class="qq_map_page_line" style="display:none;">
            <div class="qq_map_tool qqmt_log"></div>
        </div>
        <div class="qq_map_page_line qqmt_comments_area" style="display:none;">
            <div class="comments_area" data-block="#{Hs.qq_map_chat_id}">
                <div class="comments" style="padding-bottom:72px;"></div>
                <div style="
display: flex;
padding: 10px 10px;
position: fixed;
bottom: 0px;
width: -webkit-fill-available;
background: white;
                ">
                    <textarea style="
flex: 1;
min-height: 30px;
height: 30px;
padding: 5px 10px;
border: 1px solid #ccc;
resize: none;
box-shadow:none;
                    " class="comment_content" placeholder="Add some comment..."></textarea>
                    <button style="
width: 60px;
height: 42px;
background: black;
color: white;
font-weight: bold;
font-size: 16px;
border: 0;
border-radius: 14px;
                    " class="comment_submit">发送</button>
                </div>
            </div>
        </div>
    </div>
"""

Hs.qq_map = null
Hs.qq_control = null

Hs.qq_map_zoom_center_lat_fix =
    "16":0.001


root.scroll_to_latest_comment = ()->
    $(".comment").get($(".comment").length-1).scrollIntoView()

$("body").on "click",".qqmt_get_comments",(evt)->
    $(this).parents(".qq_map_page_line").first().hide()
    $(".qqmt_comments_area").show()
    $("#qq_map").height "320px"
    $("#qq_map_page").css
        "height":$(window).height()-320+20
        "overflow-y": "auto"
    setTimeout ()->
            scroll_to_latest_comment()
        ,500

$("body").on "click",".qqmt_get_location",(evt)->
    if IS_WEIXIN
        #默认为wgs84的gps坐标，如果要返回直接给openLocation用的火星坐标，可传入'gcj02'
        setTimeout ()->
            wx.getLocation
                type: 'gcj02'
                success: (res)->
                    console.log res
                    latitude = res.latitude #纬度，浮点数，范围为90 ~ -90
                    longitude = res.longitude #经度，浮点数，范围为180 ~ -180。
                    speed = res.speed #速度，以米/每秒计
                    accuracy = res.accuracy #位置精度
                    latitude_fix = 0
                    if latitude>=0
                        latitude_fix = latitude - Hs.qq_map_zoom_center_lat_fix["16"]
                        console.log "latitude>=0",latitude_fix
                    else
                        latitude_fix = latitude + Hs.qq_map_zoom_center_lat_fix["16"]
                        console.log "latitude<0",latitude_fix
                    Hs.qq_map.setCenter([latitude_fix,longitude])
                    Hs.qq_map.setZoom(16)
                    $.ajax
                        url:"/api/user/get_user_info"
                        data:null
                        dataType: 'json'
                        type: 'GET'
                        success:(data)->
                            console.log data
                            if data.info == "ok"
                                _html = """
                                <div class="qqmt_card_pointer" data-type="user" data-id="#{USER_ID}">
                                    <img src="#{data.headimgurl}">
                                </div>
                                """
                                qq_map_add_marker_self(latitude,longitude,_html,USER_ID)
                                content_json =
                                    "map":"lbs_qq"
                                    "gps_type":"gcj02"
                                    "latitude":latitude
                                    "longitude":longitude
                                content = "HLBS//#{JSON.stringify(content_json)}"
                                $.ajax
                                    url:"/api/page/comment/submit"
                                    data:
                                        block_id: BLOCK_ID
                                        chat_id: Hs.qq_map_chat_id
                                        content: content
                                        uuid: uuid2(6,null)
                                    dataType: 'json'
                                    type: 'POST'
                                    success:(data)->
                                        console.log JSON.stringify(data)
                                        if data.info == "error"
                                            page_alert data.about
                                    error:(data)->
                                        console.log data
                        error:(data)->
                            console.log data
        ,1000
root.myInfoWindow = (options)->
    mydom = null
    TMap.DOMOverlay.call(this, options)
root.myInfoWindow.prototype = new TMap.DOMOverlay()
root.myInfoWindow.prototype.onInit = (options)->
    this.position = options.position;
    this.content = options.content;
root.myInfoWindow.prototype.createDOM =()->
    mydom = document.createElement("div")
    mydom.className = "qq_map_user"
    mydom.style.cssText = """"""
    mydom.innerHTML = this.content
    return mydom;
root.myInfoWindow.prototype.updateDOM = ()->
    if !this.map
        return
    pixel = this.map.projectToContainer(this.position)
    left = pixel.getX() - this.dom.clientWidth / 2 + 'px'
    top = pixel.getY() - this.dom.clientHeight/ 2 + 'px'
    this.dom.style.transform = """translate3d(#{left}, #{top}, 0px)"""
root.myInfoWindow.prototype.updateContent = (content)->
    mydom.innerHTML = content

root.qq_map_add_marker_user={}

root.qq_map_bounds_update = ()->
    bounds = new TMap.LatLngBounds()
    for k,v of qq_map_add_marker_user
        if bounds.isEmpty() or !bounds.contains(v["position"])
            bounds.extend(v["position"])
    Hs.qq_map.fitBounds bounds,{padding:50}
    # setTimeout ()->
    #         Hs.qq_map.setZoom (parseFloat(Hs.qq_map.getZoom())-0.25).toFixed(2)
    #     ,1000
root.qq_map_add_marker_user_latest = []
root.qq_map_bounds_update_latest = ()->
    console.log root.qq_map_add_marker_user_latest
    bounds = new TMap.LatLngBounds()
    for k in root.qq_map_add_marker_user_latest
        console.log k
        v = root.qq_map_add_marker_user[k]
        console.log v
        if bounds.isEmpty() or !bounds.contains(v["position"])
            bounds.extend(v["position"])
    Hs.qq_map.fitBounds bounds,{padding:50}
root.qq_map_add_marker_self = (lat,lng,_html,_user_id)->
    $(".qq_map_user>.qqmt_card_pointer[data-type=user][data-id=#{_user_id}]").parents(".qq_map_user").remove()
    position_now = new TMap.LatLng(lat, lng)
    myIW = new myInfoWindow
        map:Hs.qq_map
        position: position_now
        content:_html
    qq_map_add_marker_user[_user_id]=
        "position":position_now
        "lat":lat
        "lng":lng
        "html":_html
        "user_id":_user_id
    qq_map_bounds_update()
root.qq_map_add_marker_other = (lat,lng,_html,_user_id)->
    $(".qq_map_user>.qqmt_card_pointer[data-type=user][data-id=#{_user_id}]").parents(".qq_map_user").remove()
    position_now = new TMap.LatLng(lat, lng)
    myIW = new myInfoWindow
        map:Hs.qq_map
        position: position_now
        content:_html
    qq_map_add_marker_user[_user_id]=
        "position":position_now
        "lat":lat
        "lng":lng
        "html":_html
        "user_id":_user_id
    qq_map_bounds_update()
root.qq_map_add_marker_history = (lat,lng,_html,_user_id)->
    if $(".qq_map_user>.qqmt_card_pointer[data-type=user][data-id=#{_user_id}]").length >0
        return
    position_now = new TMap.LatLng(lat, lng)
    myIW = new myInfoWindow
        map:Hs.qq_map
        position: position_now
        content:_html
    qq_map_add_marker_user[_user_id]=
        "position":position_now
        "lat":lat
        "lng":lng
        "html":_html
        "user_id":_user_id
    qq_map_bounds_update()

qq_initMap =()->
    #定义地图中心点坐标
    center = new TMap.LatLng(36.50217920100954, 106.51069169463551)
    #定义map变量，调用 TMap.Map() 构造函数创建地图
    dom = $("#qq_map")[0]
    data =
        "center": center
        "zoom": 3
    Hs.qq_map = new TMap.Map dom,data
    # Hs.qq_control = Hs.qq_map.getControl(TMap.constants.DEFAULT_CONTROL_ID.ZOOM)
    # Hs.qq_control.setPosition(TMap.constants.CONTROL_POSITION.TOP_RIGHT)
    Hs.qq_map.removeControl(TMap.constants.DEFAULT_CONTROL_ID.SCALE)
    Hs.qq_map.removeControl(TMap.constants.DEFAULT_CONTROL_ID.LOGO)


    # Hs.qq_map.on "click", (evt)=>
    #     console.log(evt)
    #     $(".qqmt_log").prepend """
    #     <div>#{JSON.stringify(evt.latLng)}</div>
    #     """
root.some_one_join_map = (hlbs_json,_user_id,_user_name,_user_headimgurl)->
    _html = """
    <div class="qqmt_card_pointer" data-type="user" data-id="#{_user_id}">
        <img src="#{_user_headimgurl}">
    </div>
    """
    qq_map_add_marker_other hlbs_json["latitude"],hlbs_json["longitude"],_html,_user_id
root.some_one_join_map_history = (hlbs_json,_user_id,_user_name,_user_headimgurl)->
    _html = """
    <div class="qqmt_card_pointer" data-type="user" data-id="#{_user_id}">
        <img src="#{_user_headimgurl}">
    </div>
    """
    qq_map_add_marker_history hlbs_json["latitude"],hlbs_json["longitude"],_html,_user_id

Hs.qq_map_zIndex=0
$("body").on "click",".qqmt_card_pointer",(evt)->
    _user_id = $(this).attr("data-id")
    Hs.qq_map_zIndex +=1
    $(this).parents(".qq_map_user").first().css
        zIndex:Hs.qq_map_zIndex
    v = qq_map_add_marker_user[_user_id]
    Hs.qq_map.setCenter(v["position"])
    if Hs.qq_map.getZoom() < 15
        Hs.qq_map.setZoom(15)
$("body").on "touchend",".qqmt_card_pointer",(evt)->
    _user_id = $(this).attr("data-id")
    Hs.qq_map_zIndex +=1
    $(this).parents(".qq_map_user").first().css
        zIndex:Hs.qq_map_zIndex
    v = qq_map_add_marker_user[_user_id]
    Hs.qq_map.setCenter(v["position"])
    if Hs.qq_map.getZoom() < 15
        Hs.qq_map.setZoom(15)
$("body").on "click",".comment_img",(evt)->
    _user_id = $(this).attr("data-user")
    Hs.qq_map_zIndex +=1
    $(".qqmt_card_pointer[data-type=\"user\"][data-id=\"#{_user_id}\"]").parents(".qq_map_user").first().css
        zIndex:Hs.qq_map_zIndex
    v = root.qq_map_add_marker_user[_user_id]
    if _user_id == USER_ID
        Hs.qq_map.setCenter(v["position"])
        if Hs.qq_map.getZoom() < 15
            Hs.qq_map.setZoom(15)
    else
        root.qq_map_add_marker_user_latest=[USER_ID,_user_id]
        root.qq_map_bounds_update_latest()

$(window).on "load",()->
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
                <button class="comment_control_tool_btn comment_del hide">DEL</button>
            </div>
            """

        content_type_list = content.split("//")
        content_type = content_type_list[0]
        if content_type in ["HLBS"]
            hlbs_json = null
            try
                hlbs_json = JSON.parse content.replace("HLBS//","")
            catch e
                hlbs_json = null
            if hlbs_json == null
                return ""
            some_one_join_map hlbs_json,content_json["user_id"],user_name,user_headimgurl
            return ""
        else
            content = content.replaceAll("\n","<br>")
        html = """
            <div class="comment" data-comment-id="#{comment_id}_#{sequence}">
                <div class="comment_img" data-user="#{content_json["user_id"]}"><img src="#{user_headimgurl}"></div>
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
        user_headimgurl = members[comment_list[1]]["headimgurl"]
        content = comment_list[4]
        if comment_list[3] in ["COMMENT"]
            content = content
        else if comment_list[3] in ["WEIXINPAYCALLBACKSUCCESS","ALIPAYPAYCALLBACKSUCCESS"]
            content = ("""<div class="content_table"><div>#{k}</div><div>#{v}</div></div>""" for k,v of content).join("\n\r")
        content_type_list = content.split("//")
        content_type = content_type_list[0]
        if content_type in ["HLBS"]
            hlbs_json = null
            try
                hlbs_json = JSON.parse content.replace("HLBS//","")
            catch e
                hlbs_json = null
            if hlbs_json == null
                return ""
            some_one_join_map_history hlbs_json,comment_list[1],user_name,user_headimgurl
            return ""
        else
            content = content.replaceAll("\n","<br>")

        date_html = formatDateAllEn(comment_list[2]*1000)
        control_tools=""
        if comment_list[3] not in ["WEIXINPAYCALLBACKSUCCESS","ALIPAYPAYCALLBACKSUCCESS"]
            if IS_EDITOR or USER_ID == comment_list[1]
                control_tools = """
                <div class="comment_line">
                    <button class="comment_control_tool_btn comment_del hide">DEL</button>
                </div>
                """
        html = """
            <div class="comment" data-comment-id="#{comment_id}_#{comment_list[0]}">
                <div class="comment_img" data-user="#{comment_list[1]}"><img src="#{user_headimgurl}"></div>
                <div class="comment_line"><span class="name">#{user_name}</span><span class="date">#{date_html}</span></div>
                <div class="comment_line"><p class="content">#{content}</p></div>
                #{control_tools}
            </div>
        """
        return html

    root.comment_add = (content_json, chat_id)->
        comment_html = comment_add_one_base(content_json)
        $(".comments_area[data-block=#{chat_id}]>.comments").append """
            #{comment_html}
        """
        setTimeout ()->
                scroll_to_latest_comment()
            ,500
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
                        $(".comments_area[data-block=#{chat_id}]>.comments").prepend """
                            #{comment_html}
                        """
                    $(".comments_area[data-block=#{chat_id}]>.comments>.comment_more_info").remove()
                    if data.last_comment_id == null
                        if data.comments.length > 0
                            $(".comments_area[data-block=#{chat_id}]>.comments").prepend """
                                <div class="comment_more_info">—— 群聊初始化成功 ——</div>
                            """
                        else
                            $(".comments_area[data-block=#{chat_id}]>.comments").prepend """
                                <div class="comment_more_info">—— WAIT YOUR COMMENTS ——</div>
                            """
                    if data.last_comment_id != null
                        # $(".comments_area[data-block=#{chat_id}]>.comments").prepend """
                        #     <div class="comment_more_info comment_more_action" data-flag="#{data.last_comment_id}">—— MORE ——</div>
                        # """
                        # if data.comments.length < 10
                        #     comment_load(chat_id,data.last_comment_id)
                        comment_load(chat_id,data.last_comment_id)
            error:(data)->
                console.log data
    root.comment_load(Hs.qq_map_chat_id)
    qq_initMap()
    setTimeout ()->
        $(".qqmt_get_location").click()
    ,1000

</script>
<script src="/static/js/coffeescript.js"></script>
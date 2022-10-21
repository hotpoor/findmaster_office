root = exports ? this
# !!!! Hotpoor root object
root.Hs or= {}
Hs = root.Hs
Hs.login_scan_uri_uuid = null
$ ->
    console.log "msh ground"
    $("body").on "click",".msh_area_bottom_btn", (evt)->
        dom = $(this)
        dom_action = dom.attr("data-action")
        $(".msh_area_bottom_btn").removeClass("btn_current")
        dom.addClass("btn_current")
        console.log "dom_action", dom_action
        if dom_action in ["order"]
            window.location.href = "/home/store/order"
        else if dom_action in ["person"]
            window.location.href = "/home/store/user/#{USER_ID}"
        else if dom_action in ["hollow"]
            window.location.href = "/home/store/hollow"
        else if dom_action in ["home"]
            window.location.href = "/home/store/ground"
    
    root.hollow_confirm_confirm_action = null
    $("body").on "click",".hollow_confirm_submit",(evt)->
        if root.hollow_confirm_confirm_action!=null
            console.log root.hollow_confirm_confirm_action
            _action = root.hollow_confirm_confirm_action[0]
            _dom_area = root.hollow_confirm_confirm_action[1]
            _comment_id = root.hollow_confirm_confirm_action[2]
            if _action == "DEL"
                console.log _action
            else if _action == "DELREMARK"
                console.log _action
            else if _action == "GOTOLOGIN"
                window.location.href = "/login?redirect_uri="+encodeURIComponent(window.location.href)
        root.hollow_confirm_confirm_action = null
        $(".hollow_confirm_show_area").remove()
    $("body").on "click",".hollow_confirm_cancel",(evt)->
        root.hollow_confirm_confirm_action = null
        $(".hollow_confirm_show_area").remove()

    root.hollow_confirm_login = (title="Notice",text="Do you confirm?",data_comment_id=null,remark_id=null) ->
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
                    <div class="hollow_confirm_cancel">Cancel</div>
                    <div class="hollow_confirm_submit">Confirm</div>
                </div>
            </div>
        </div>
        """
        root.hollow_confirm_confirm_action = ["GOTOLOGIN",null,null]

    root.hollow_confirm_is_subscribe = (title="Notice",text="Do you confirm?",data_comment_id=null,remark_id=null) ->
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
                    <div class="hollow_confirm_cancel">I see.</div>
                </div>
            </div>
        </div>
        """
    if USER_ID.indexOf("no_login")>-1
        hollow_confirm_login("Notice","No login, will you go with a account?")

    root.load_stores_list_json = {}
    root.load_stores_list = (owner_id)->
        $.ajax
            url:"/api/store/list"
            data:
                user_id:owner_id
            dataType: 'json'
            type: 'GET'
            success:(data)->
                console.log "========="
                console.log data
                if data.info == "ok"
                    for item in data.result
                        load_stores_list_json[item["store_id"]]=item
                        $(".store_user_info_store_list").append """
<div class="store_line_card">
    <div class="store_line store_span" data-store-id="#{item["store_id"]}">STORE ID: #{item["store_id"]}</div>
    <div class="store_line">
        <img class="store_headimgurl" src="#{item["headimgurl"]}">
        <div class="store_title">#{item["title"]}</div>
        <div class="store_desc">#{item["desc"]}</div>
    </div>
</div>

                        """
            error:(data)->
                console.log data
    $(window).on "load",()->
        load_stores_list(BLOCK_ID)



















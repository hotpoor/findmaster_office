root = exports ? this
# !!!! Hotpoor root object
root.Hs or= {}
Hs = root.Hs

$ ->
    console.log "winni app user"
    get_chat = (chat_id,comment_id=null,type)->
        if comment_id == null
            $(".me_results").append """
            <div class="comments" data-block="#{chat_id}">
                <div class="comment_log">Loading</div>
            </div>
            """
        $.ajax
            url:"/api/page/comment/load"
            type:"GET"
            dataType:"json"
            data:
                chat_id: chat_id
                comment_id: comment_id
            success:(data)->
                console.log data
                if data.info =="error"
                    console.log data.info
                    if data.about == "no chat's comment"
                        console.log data.about,"No more"
                        $(".comment_log").text "No More"
                else if data.info ="ok"
                    for comment in data.comments by -1
                        comment_id_sequence = "#{data.comment_id}_#{comment[0]}"
                        comment_json = null
                        try
                            comment_json = JSON.parse(comment[4])
                        catch e
                            comment_json = null
                        if comment_json!=null
                            $(".comments[data-block=#{chat_id}]").append """
                                <div class="comment" data-id="#{comment_id_sequence}">
                                    <a target="_blank" href="/home/store/app/shop/#{comment_json["block_id"]}">
                                        <div class="one_shop_card" data-id="#{comment_json["block_id"]}">
                                            <div class="one_shop_card_headimgurl">
                                                <img src="#{comment_json["headimgurl"]}">
                                            </div>
                                            <div class="one_shop_card_entity">#{comment_json["block_id"]}</div>
                                            <div class="one_shop_card_title">#{comment_json["title"]}</div>
                                            <div class="one_shop_card_desc">#{comment_json["desc"]}</div>
                                            <div class="one_shop_card_address">#{comment_json["address"]}</div>
                                        </div>
                                    </a>
                                </div>
                            """
                    if data.last_comment_id == null
                        $(".comment_log").remove()
                        $(".comments[data-block=#{chat_id}]").append """
                            <div class="comment_log">No More</div>
                        """
                    else
                        $(".comment_log").remove()
                        $(".comments[data-block=#{chat_id}]").append """
                            <div class="comment_load_more" data-type="#{type}" data-last-comment-id="#{data.last_comment_id}">Click Load More</div>
                        """
            error:(data)->
                console.log data
    current_create_shop_info =
        "title":""
        "desc":""
        "headimgurl":""
        "address":""
    create_shop = ()->
        current_create_shop_info =
            "title":""
            "desc":""
            "headimgurl":""
            "address":""
        $("body").append """
        <div class="cover_create">
            <div class="cover_create_base">
                <div class="cover_create_card">
                    <div class="cover_create_card_line">
                        <div>Shop Name</div>
                        <div><input class="cover_create_card_store_title"></div>
                    </div>
                    <div class="cover_create_card_line">
                        <div>Shop Description</div>
                        <div><textarea class="cover_create_card_store_desc"></textarea></div>
                    </div>
                    <div class="cover_create_card_line">
                        <div>Shop Address</div>
                        <div><textarea class="cover_create_card_store_address"></textarea></div>
                    </div>
                    <div class="cover_create_card_line">
                        <div>Shop Profile</div>
                        <div>
                            <div class="cover_create_card_store_headimgurl">
                                <img src="https://www.winni.app/static/img/winni_app/shops.png">
                            </div>
                            <button
                                class="img_add_upload_target_now"
                                data-target-class="cover_create_card_store_headimgurl"
                                data-target-rule="replace"
                            >select img</button>
                        </div>
                    </div>
                    <div class="cover_create_card_line">
                        <button class="create_shop_action">Create</button>
                    </div>

                </div>
            </div>
        </div>
        """
    current_create_shop_info_action = ()->
        current_create_shop_info =
            "title":$(".cover_create_card_store_title").val()
            "desc":$(".cover_create_card_store_desc").val()
            "headimgurl":$(".cover_create_card_store_headimgurl").find("img").first().attr("src")
            "address":$(".cover_create_card_store_address").val()
        $.ajax
            url:"/api/store/app/shop/create"
            dataType:"json"
            type:"POST"
            data:current_create_shop_info
            success:(data)->
                console.log data
                if data.info == "ok"
                    _block_id = data.block_id
                    current_create_shop_info["block_id"]=_block_id
                    current_create_shop_info["block_type"]="shop"
                    user_comment_submit_one USER_ID,SHOPS_ENTITY,JSON.stringify(current_create_shop_info),()->
                        user_comment_submit_one "5d85f0ecc99c47b78bc87f382ef4ad18","a91eccee5a0b411388cee48a3afd7b67",JSON.stringify(current_create_shop_info),()->
                            alert "create success"
                            window.location.href = "/home/store/app/shop/#{_block_id}"
            error:(data)->
                console.log data
    user_comment_submit_one = (block_id,chat_id,content,callback=null)->
        $.ajax
            url:"/api/page/comment/submit"
            dataType:"json"
            type:"POST"
            data:
                block_id:block_id
                chat_id:chat_id
                content:content
                uuid:uuid2(6,null)
            success:(data)->
                console.log data
                if callback != null
                    callback()
            error:(data)->
                console.log data

    $("body").on "click",".comment_load_more",(evt)->
        load_type = $(this).attr("data-type")
        chat_id = $(this).parents(".comments").first().attr("data-block")
        last_comment_id = $(this).attr("data-last-comment-id") 
        get_chat(chat_id,last_comment_id,load_type)

    $("body").on "click",".get_shops",(evt)->
        $(".me_results").empty()
        chat_id = $(this).attr("data-block")
        get_chat(chat_id,null,"shops")
    $("body").on "click",".create_shop",(evt)->
        create_shop()
    $("body").on "click",".create_shop_action",(evt)->
        current_create_shop_info_action()
    $(window).on "load",(evt)->
        $(".me_results").empty()
        chat_id = SHOPS_ENTITY
        get_chat(SHOPS_ENTITY,null,"shops")

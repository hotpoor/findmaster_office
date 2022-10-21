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
                                    #{comment[4]}
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
    $("body").on "click",".comment_load_more",(evt)->
        load_type = $(this).attr("data-type")
        chat_id = $(this).parents(".comments").first().attr("data-block")
        last_comment_id = $(this).attr("data-last-comment-id") 
        get_chat(chat_id,last_comment_id,load_type)

    $("body").on "click",".get_orders",(evt)->
        $(".me_results").empty()
        chat_id = $(this).attr("data-block")
        get_chat(chat_id,null,"orders")
    $("body").on "click",".get_collections",(evt)->
        $(".me_results").empty()
        chat_id = $(this).attr("data-block")
        get_chat(chat_id,null,"collections")
    $("body").on "click",".get_likes",(evt)->
        $(".me_results").empty()
        chat_id = $(this).attr("data-block")
        get_chat(chat_id,null,"likes")

root = exports ? this
# !!!! Hotpoor root object
root.Hs or= {}
Hs = root.Hs

$ ->
    console.log "alipay coffee"
    $("body").on "click",".alipay",(e)->
        user_id = USER_ID
        aim_id = USER_ID
        block_id = $(this).attr("data-block-id")
        chat_id = $(this).attr("data-chat-id")
        price = $(this).attr("data-price")
        title = $(this).attr("data-title")
        alipay_app = $(this).attr("data-app")
        $.ajax
            url:"/api/pay/alipay/unified_plus"
            data:
                price:price
                user_id:aim_id
                block_id:block_id
                chat_id:chat_id
                app:alipay_app
                title:title
            dataType: 'json'
            type: 'POST'
            success: (data) ->
                console.log data
                if data.info=="ok"
                    new_blank = window.open('_blank')
                    if new_blank == null
                        window.location.href = data.redirect_url
                    else
                        new_blank.location = data.redirect_url
                else
                    alert data.about
            error: (data)->
                console.log data
                console.log "alipay_unifiedorder error"
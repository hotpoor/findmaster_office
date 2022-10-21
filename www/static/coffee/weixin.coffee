root = exports ? this
# !!!! Hotpoor root object
root.Hs or= {}
Hs = root.Hs
wx.config
    debug: false
    # debug: true
    appId: WX_APPID
    timestamp: WX_TIMESTAMP
    nonceStr: WX_NONCESTR
    signature: WX_SIGNATURE
    jsApiList: [
        'checkJsApi',
        'onMenuShareTimeline',
        'onMenuShareAppMessage',
        'updateTimelineShareData',
        'updateAppMessageShareData',
        'onMenuShareQQ',
        'onMenuShareWeibo',
        'hideMenuItems',
        'showMenuItems',
        'hideAllNonBaseMenuItem',
        'showAllNonBaseMenuItem',
        'translateVoice',
        'startRecord',
        'stopRecord',
        'onVoiceRecordEnd',
        'playVoice',
        'pauseVoice',
        'stopVoice',
        'uploadVoice',
        'downloadVoice',
        'chooseImage',
        'previewImage',
        'uploadImage',
        'downloadImage',
        'getNetworkType',
        'openLocation',
        'getLocation',
        'hideOptionMenu',
        'showOptionMenu',
        'closeWindow',
        'scanQRCode',
        'chooseWXPay',
        'openProductSpecificView',
        'addCard',
        'chooseCard',
        'openCard'
      ]
$ ->
    wx.ready ()->
        console.log "wx ready"
    console.log "weixin.coffee"
    weixin_pay_action = (user_id,aim_id,block_id,chat_id,price)->
        console.log "weixin_pay_action"
    $("body").on "click",".weixin_pay",(e)->
        if IS_WEIXIN
            user_id = USER_ID
            aim_id = USER_ID
            block_id = $(this).attr("data-block-id")
            chat_id = $(this).attr("data-chat-id")
            price = $(this).attr("data-price")
            title = $(this).attr("data-title")
            $.ajax
                url:"/api/pay/weixin/unified"
                data:
                    price:price
                    user_id:aim_id
                    block_id:block_id
                    chat_id:chat_id
                    app:WX_APP
                    title:title
                dataType: 'json'
                type: 'POST'
                success: (data) ->
                    console.log data
                    if data.info=="ok"
                        wxPayData =
                            timestamp: data["timestamp"],
                            nonceStr: data["nonce"],
                            signType: 'MD5',
                            package: 'prepay_id='+data["prepay_id"],
                            paySign: data["paysign"],
                            success: (res)->
                                console.log "pay success"
                                console.log res
                                alert "pay success"
                            complete: (res)->
                                console.log res
                        wx.chooseWXPay wxPayData
                    else
                        alert data.about
                error: (data)->
                    console.log data
                    console.log "wx_pay_unifiedorder error"
    root.close_window = ()->
        wx.closeWindow();

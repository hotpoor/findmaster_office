root = exports ? this
# !!!! Hotpoor root object
root.Hs or= {}
Hs = root.Hs

$ ->
    console.log "winni app user"

    $("body").on "click",".stripe_account_retrieve_btn",(evt)->
        _pay_type = $(this).parents(".stripe_account_card").first().attr("data-pay-type")
        _stripe_account = $(this).parents(".stripe_account_card").first().attr("data-account-id")
        $.ajax
            url:"/api/store/app/stripe/retrieve"
            type:"POST"
            dataType:"json"
            data:
                pay_type: _pay_type
                stripe_account: _stripe_account
                shop_id: SHOP_ID
            success:(data)->
                console.log data
                alert data.about
            error:(data)->
                console.log data
    $("body").on "click",".stripe_account_login_btn",(evt)->
        _pay_type = $(this).parents(".stripe_account_card").first().attr("data-pay-type")
        _stripe_account = $(this).parents(".stripe_account_card").first().attr("data-account-id")
        $(this).parents(".stripe_account_card").first().find(".log").empty()
        $.ajax
            url:"/api/store/app/stripe/login_link"
            type:"POST"
            dataType:"json"
            data:
                pay_type: _pay_type
                stripe_account: _stripe_account
                shop_id: SHOP_ID
            success:(data)->
                console.log data
                if data.info == "ok"
                    $(".stripe_account_card[data-account-id=#{_stripe_account}][data-pay-type=#{_pay_type}]").append """
                    <a target="_blank" href="#{data.result["url"]}">go login stripe</a>
                    """
            error:(data)->
                console.log data
    auto_login_stripe=(type="test")->
        if type=="test"
            if not STRIPE_ACCOUNT_ID_TEST_PAYOUTS_ENABLED
                $.ajax
                    url:"/api/store/app/stripe/login_link"
                    type:"POST"
                    dataType:"json"
                    data:
                        pay_type: type
                        stripe_account: STRIPE_ACCOUNT_ID_TEST
                        shop_id: SHOP_ID
                    success:(data)->
                        console.log data
                        if data.info =="ok"
                            window.location.href = data.result["url"]
                    error:(data)->
                        console.log data

    # $(window).on "load",()->
    #     if IS_EDITORS
    #         auto_login_stripe()

root = exports ? this
# !!!! Hotpoor root object
root.Hs or= {}
Hs = root.Hs

$ ->
    console.log "winni_app dashbaord"

    $("body").on "click",".stripe_account_list_create_btn",(evt)->
        data_type = $(this).attr("data-type")
        $.ajax
            url:"/api/stripe/account/add"
            data:
                pay_type:data_type
            dataType: 'json'
            type: 'POST'
            success: (data) ->
                console.log data
            error:(data)->
                console.log data
    $("body").on "click",".stripe_account_list_load_btn",(evt)->
        data_type = $(this).attr("data-type")
        $.ajax
            url:"/api/stripe/account/list"
            data:
                pay_type:data_type
            dataType: 'json'
            type: 'GET'
            success: (data) ->
                console.log data
                stripe_accounts = data.stripe_accounts
                $(".stripe_account_list[data-type=#{data_type}]").empty()
                for stripe_account_id,stripe_account_json of stripe_accounts
                    $(".stripe_account_list[data-type=#{data_type}]").append """
                    <div class="stripe_account_line" data-stripe-account="#{stripe_account_id}">
                        <div>stripe_account_id: <span>#{stripe_account_id}</span></div>
                        <div>
                            <button class="stripe_account_line_btn_retrieve">同步店铺数据</button>
                            <button class="stripe_account_line_btn_account_link">获取账户链接</button>
                        </div>
                        <div><textarea class="stripe_account_line_json"></textarea></div>
                        <div class="store_card">
                            <div class="store_card_display_name">#{stripe_account_json["settings"]["dashboard"]["display_name"]}</div>
                            <div class="store_card_display_email">#{stripe_account_json["email"]}</div>
                            <div class="store_card_display_icon"></div>
                        </div>
                    </div>
                    """
                    $(".stripe_account_list[data-type=#{data_type}]>.stripe_account_line[data-stripe-account=\"#{stripe_account_id}\"]").find("textarea").val(JSON.stringify(stripe_account_json))

            error:(data)->
                console.log data
    $("body").on "click",".stripe_account_line_btn_retrieve",(evt)->
        data_type = $(this).parents(".stripe_account_list").first().attr("data-type")
        stripe_account = $(this).parents(".stripe_account_line").first().attr("data-stripe-account")
        $.ajax
            url:"/api/stripe/account/retrieve"
            data:
                pay_type:data_type
                stripe_account:stripe_account
            dataType: 'json'
            type: 'POST'
            success: (data) ->
                console.log data
            error:(data)->
                console.log data
    $("body").on "click",".stripe_account_line_btn_account_link",(evt)->
        data_type = $(this).parents(".stripe_account_list").first().attr("data-type")
        stripe_account = $(this).parents(".stripe_account_line").first().attr("data-stripe-account")
        $.ajax
            url:"/api/stripe/account/add_link"
            data:
                pay_type:data_type
                stripe_account:stripe_account
            dataType: 'json'
            type: 'POST'
            success: (data) ->
                console.log data
            error:(data)->
                console.log data

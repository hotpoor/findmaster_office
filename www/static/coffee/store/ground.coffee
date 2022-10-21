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

    xialiwei_find_good = (chat_id,comment_id,store_id,add_num=0)->
        $.ajax
            url:"/api/page/comment/load"
            type:"GET"
            dataType:"json"
            data:
                chat_id:chat_id
                comment_id:comment_id
            success:(data)->
                console.log data
                if data.info == "ok"
                    for comment in data.comments by -1
                        comment_json = null
                        try
                            comment_json = JSON.parse(comment[4])
                        catch e
                            continue
                        if comment_json != null
                            if comment_json["json_type"]=="good_info"
                                _html_prices = comment_json["promotion-item"]
                                _html_prices.push [1,comment_json["price-now"]]
                                _html_prices.sort (a,b)->
                                    return b[0]-a[0]
                                _html_price_first = true
                                _html_prices_html = """"""
                                for _html_price in _html_prices
                                    line_through_class_str = ""
                                    if _html_price[0]==1
                                        line_through_class_str = "line_through"
                                    _html_prices_html = """
                                    #{_html_prices_html}
                                    <div class="good_info_price #{line_through_class_str}" data-num="#{_html_price[0]}">
                                        <span>#{comment_json["currency-now"]}$</span>
                                        <span>#{(_html_price[1]/100.0).toFixed(2)}</span>
                                    </div>
                                    """
                                uuid_now = uuid2(6,null)
                                _html = """
<div class="ground_good_item" data-add-num="#{add_num}" data-store="#{store_id}" data-product="#{chat_id}">
    <div class="ground_good_item_info_top">
        <div class="ground_good_item_store_id">0x#{store_id}</div>
        <div class="ground_good_item_store_score">#{stores_info[store_id]["store_score"]}</div>
    </div>
    <div class="ground_good_item_imgs">
        <img class="ground_good_item_img" data-uuid="#{uuid_now}" src="#{comment_json["gallery-items"][0]}">
        <script>
            a_#{uuid_now}_imgs_num = 0
            a_#{uuid_now}_imgs = #{JSON.stringify(comment_json["gallery-items"])}
            setInterval(function(){
                a_#{uuid_now}_imgs_num +=1
                $(".ground_good_item_img[data-uuid=#{uuid_now}]").attr("src",a_#{uuid_now}_imgs[a_#{uuid_now}_imgs_num])
                if (a_#{uuid_now}_imgs_num > a_#{uuid_now}_imgs.length -1){
                    a_#{uuid_now}_imgs_num = -1
                }

                },2000)
        </script>
    </div>
    <div class="ground_good_item_info">
        <div class="good_info_name">#{comment_json["product-name"]}</div>
        <div class="good_info_sell_num">1000+</div>
        #{_html_prices_html}
        <div class="good_info_relative">
            <div class="good_info_headimgurl" data-store-id="#{store_id}">
                <img class="good_info_headimgurl_img" src="#{stores_info[store_id]["headimgurl"]}">
            </div>
            <div class="good_info_title">#{comment_json["detail-box-title"]}</div>
        </div>
    </div>
</div>
                                """
                                if add_num%2==0
                                    $(".ground_goods_area_left").append _html
                                else
                                    $(".ground_goods_area_right").append _html
                                return
                    last_comment_id = data.last_comment_id
                    if last_comment_id != null
                        xialiwei_find_good chat_id,last_comment_id
                        
                else if data.info == "error"
                    return
            error:(data)->
                console.log data

    xialiwei_goods_list = []
    stores_info = {}
    xialiwei_goods_list_load = ()->
        store_ids = []
        for good_info in xialiwei_goods_list
            store_ids.push good_info["store"]
        $.ajax
            url:"/api/store/info"
            type:"POST"
            dataType:"json"
            data:
                store_ids: JSON.stringify(store_ids)
            success:(data)->
                console.log data
                if data.info == "ok"
                    for result in data.result
                        stores_info[result["store_id"]]=result
                good_info_add_num = 0
                for good_info in xialiwei_goods_list
                    a_user_id = good_info["owner"]
                    a_store = good_info["store"]
                    a_good = good_info["product"]
                    xialiwei_find_good a_good,null,a_store,good_info_add_num
                    good_info_add_num +=1
            error:(data)->
                console.log data
        

        
    xialiwei_find_goods = (chat_id,comment_id)->
        $.ajax
            url:"/api/page/comment/load"
            type:"GET"
            dataType:"json"
            data:
                chat_id:chat_id
                comment_id:comment_id
            success:(data)->
                console.log data
                if data.info == "ok"
                    for comment in data.comments
                        comment_json = null
                        try
                            comment_json = JSON.parse(comment[4])
                        catch e
                            continue
                        if comment_json != null
                            xialiwei_goods_list.push comment_json
                    last_comment_id = data.last_comment_id
                    if last_comment_id == null
                        xialiwei_goods_list_load()
                    else
                        xialiwei_find_goods chat_id,last_comment_id
                        
                else if data.info == "error"
                    return
            error:(data)->
                console.log data

    xialiwei_find_goods "123e9e1c79a94786a961bd004a4ec71f",null


    $("body").on "click",".ground_good_item",(evt)->
        product_id = $(this).attr("data-product")
        store_id = $(this).attr("data-store")
        new_blank = window.open('_blank')
        if new_blank == null
            window.location.href = "/home/store/product/#{store_id}/#{product_id}"
        else
            new_blank.location = "/home/store/product/#{store_id}/#{product_id}"


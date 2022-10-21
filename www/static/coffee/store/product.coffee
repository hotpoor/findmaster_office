root = exports ? this
# !!!! Hotpoor root object
root.Hs or= {}
Hs = root.Hs
Hs.login_scan_uri_uuid = null
$ ->
    console.log "msh product"

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
                                _html_prices_html = """"""
                                # _html_prices.push [1,comment_json["price-now"]]
                                # _html_prices.sort (a,b)->
                                #     return b[0]-a[0]
                                # _html_price_first = true
                                
                                # for _html_price in _html_prices
                                #     line_through_class_str = "line_through"
                                #     if _html_price_first
                                #         line_through_class_str = ""
                                #         _html_price_first = false
                                #     _html_prices_html = """
                                #     #{_html_prices_html}
                                #     <div class="good_info_price #{line_through_class_str}" data-num="#{_html_price[0]}">
                                #         <span>#{comment_json["currency-now"]}$</span>
                                #         <span>#{(_html_price[1]/100.0).toFixed(2)}</span>
                                #     </div>
                                #     """
                                _html_prices_new = """"""
                                _html_prices_new_list = {}
                                for _html_price in comment_json["promotion-item"]
                                    name = _html_price["name"]

                                    if _html_price["sizes"]==undefined
                                        sizes=[]
                                    else
                                        sizes = _html_price["sizes"]
                                    sizes_html = ""
                                    for i in sizes
                                        sizes_html = """
                                        #{sizes_html}
                                        <span>#{i}</span>
                                        """
                                    if _html_price["colors"]==undefined
                                        colors=[]
                                    else
                                        colors = _html_price["colors"]
                                    colors_html = ""
                                    for i in colors
                                        colors_html = """
                                        #{colors_html}
                                        <span>#{i}</span>
                                        """
                                    if _html_price["prices"]==undefined
                                        prices=[]
                                    else
                                        prices = _html_price["prices"]
                                    prices_html = ""
                                    for i in prices by -1
                                        prices_html = """
                                        #{prices_html}
                                        <div class="prices_btn" data-price=#{i[1]}>#{i[0]} person: #{comment_json["currency-now"]}$#{(i[1]/100.0).toFixed(2)}</div>
                                        """
                                    _html_prices_new = """
#{_html_prices_new}
<div class="prices_btns_area">
    <div class="name">PN:#{name}</div>
    <div class="sizes">sizes:#{sizes_html}</div>
    <div class="colors">colors:#{colors_html}</div>
    <div class="prices">
        #{prices_html}
    </div>
</div>
                                    """

                                    for i in _html_price["prices"]
                                        if _html_prices_new_list[i[0]]==undefined
                                             _html_prices_new_list[i[0]]=
                                                "min":i[1]
                                                "max":i[1]
                                        else
                                            if _html_prices_new_list[i[0]]["min"] > i[1]
                                                _html_prices_new_list[i[0]]["min"]=i[1]
                                            if _html_prices_new_list[i[0]]["max"] < i[1]
                                                _html_prices_new_list[i[0]]["max"]=i[1]
                                console.log _html_prices_new_list
                                _html_prices = []
                                for k,v of _html_prices_new_list
                                    _html_prices.push [k,v]
                                _html_prices.sort (a,b)->
                                    return b[0]-a[0]

                                for _html_price in _html_prices
                                    line_through_class_str = ""
                                    if "#{_html_price[0]}"=="1"
                                        line_through_class_str = "line_through"
                                        
                                    _html_prices_html = """
                                    #{_html_prices_html}
                                    <div class="good_info_price #{line_through_class_str}" data-num="#{_html_price[0]}">
                                        <span>#{comment_json["currency-now"]}$</span>
                                        <span>#{(_html_price[1]["min"]/100.0).toFixed(2)}</span>
                                        <span>+</span>
                                        <span class="hide">#{(_html_price[1]["max"]/100.0).toFixed(2)}</span>
                                    </div>
                                    """
                                uuid_now = uuid2(6,null)
                                store_score = stores_info[store_id]["store_score"]
                                _html = """
<div class="ground_good_item" data-add-num="#{add_num}" data-product="#{chat_id}">
    <div class="ground_good_item_info_top">
        <div class="ground_good_item_store_id">0x#{store_id}</div>
        <div class="ground_good_item_store_score">#{store_score}</div>
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
<div class="html_prices_new">
    #{_html_prices_new}
</div>
                                """
                                document.title = "#{comment_json["product-name"]} | #{comment_json["detail-box-title"]}"
                                $(".ground_goods_area_main").append _html
                                return
                    last_comment_id = data.last_comment_id
                    if last_comment_id != null
                        xialiwei_find_good chat_id,last_comment_id
                        
                else if data.info == "error"
                    return
            error:(data)->
                console.log data

    xialiwei_goods_list = [
        {
            "store":STORE_ID,
            "product":PRODUCT_ID,
        }
    ]
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
                    # a_user_id = good_info["owner"]
                    a_store = good_info["store"]
                    a_good = good_info["product"]
                    xialiwei_find_good a_good,null,a_store,good_info_add_num
                    good_info_add_num +=1
            error:(data)->
                console.log data
    $(window).on "load",()->
        xialiwei_goods_list_load()

    $("body").on "click",".sizes>span",(evt)->
        if $(this).hasClass("current")
            $(this).removeClass("current")
        else
            $(this).parents(".sizes").find("span").removeClass("current")
            $(this).addClass("current")
    $("body").on "click",".colors>span",(evt)->
        if $(this).hasClass("current")
            $(this).removeClass("current")
        else
            $(this).parents(".colors").find("span").removeClass("current")
            $(this).addClass("current")
    $("body").on "click",".prices_btn",(evt)->
        name = $(this).parents(".prices_btns_area").first().find(".name").text()
        size = $(this).parents(".prices_btns_area").first().find(".sizes").find(".current").text()
        color = $(this).parents(".prices_btns_area").first().find(".colors").find(".current").text()
        $.ajax
            url:"/api/stripe/pay_product"
            type:"POST"
            dataType:"json"
            data:
                currency:"cad"
                name:"#{name} #{size} #{color}"
                unit_amount:$(this).attr("data-price")
                quantity:1
                image:$(".ground_good_item_img").attr("src")
            success:(data)->
                console.log data
                if data.info == "ok"
                    new_blank = window.open('_blank')
                    if new_blank == null
                        window.location.href = data.redirect_uri
                    else
                        new_blank.location = data.redirect_uri
            error:(data)->
                console.log data



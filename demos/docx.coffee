root = exports ? this
abc=0
root.abc_list = []
for k,v of doc_dd_0
    is_nan = not isNaN(parseInt(k))
    if is_nan
        for _k,_v of v["value"]
            ais_nan = not isNaN(parseInt(_k))
            if ais_nan
                if _v["key"] in ["w:p","w:tbl","w:sectPr"]
                    p = ""
                    p_add = false
                    for _kk,_vv of _v["value"]
                        if typeof(_vv) in ["object"]
                            if _vv["key"] in ["w:r"]
                                for _kkk,_vvv of _vv["value"]
                                    if _vvv["key"] in ["w:t"] and typeof(_vvv["value"])=="string"
                                        console.log _vvv["value"]
                                        p = """#{p}#{_vvv["value"]}"""
                                        p_add = true
                    if p_add
                        ajax_data =
                              block_id: BLOCK_ID
                              dom_owner: ""
                              dom_type: "text"
                              dom_position_x: parseInt($(".main_area").width()/4)
                              dom_position_y: 100
                              time_now: abc
                        
                        abc_list_json =
                            "abc":abc
                            "p":p
                        abc=abc+1
                        $.ajax
                            url:"/api/page/add_dom"
                            data:ajax_data
                            dataType: 'json'
                            type: 'POST'
                            async: false
                            success:(data)->
                                console.log JSON.stringify(data)
                                if data.info == "ok"
                                    # $("##{data.dom_sequence}").find(".section").html """
                                    # <div>#{p}</div>
                                    # """
                                    abc_list_json["dom_id"]=data.dom_sequence
                                    abc_list.push abc_list_json
                                    # card.find(".card_scroll_relative")[0].click()
                                    # card.find(".text_align_left")[0].click()
                                    # root.page_edit_current(card,true)
root.load_abc_list = ()->
    i = 0
    a = setInterval ()->
        if i == abc_list.length
            clearInterval(a)
        card = $("##{abc_list[i]["dom_id"]}")
        card.find(".section").html """
            <div>#{abc_list[i]["p"]}</div>
        """
        card.find(".card_scroll_relative")[0].click()
        card.find(".text_align_left")[0].click()
        i=i+1
    ,1000

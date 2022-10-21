root = exports ? this
# !!!! Hotpoor root object
root.Hs or= {}
Hs = root.Hs
Hs.current_block_infos_json = {}
$ ->
    console.log "start"

    # a=[0,1,2,3,4,5,6,7,8,9,10,11]
    # def a_change(list_now,aim_num):
    #     result = []
    #     if len(a)%aim_num==0:
    #         result_num = int(len(a)/aim_num)
    #     else:
    #         result_num = int(len(a)/aim_num)+1
    #     for i in range(0,result_num):
    #         result.append(list_now[i*aim_num:(i+1)*aim_num])
    #     return result
    # result_now = a_change(a,4)
    # print(result_now)


    load_block_infos = (block_ids,query_num=10,current_block_infos_json={})->
        action_list = []
        mod_num = block_ids.length%query_num
        divide_num = block_ids.length/query_num
        if mod_num == 0
            result_num = parseInt(divide_num)
        else
            result_num = parseInt(divide_num)+1
        for i in [0..result_num-1]
            action_list.push block_ids.slice(i*query_num,(i+1)*query_num)
        for action_ids in action_list
            console.log action_ids
            $.ajax
                url:"/api/office/block_infos"
                data:
                    block_ids:JSON.stringify(action_ids)
                dataType: 'json'
                type: 'GET'
                success:(data)->
                    console.log data
                    for k,v of data.result_json
                        current_block_infos_json[k]=v
                        title = if v["title"]=="" then "Title" else v["title"]
                        desc = if v["desc"]=="" then "desc" else v["desc"]
                        subtype = v["subtype"]
                        if subtype in ["office_folder"]
                            $(".office_item[data-id=#{k}]>.office_item_info>.office_item_title").text(title)
                            $(".office_item[data-id=#{k}]>.office_item_info>.office_item_desc").text(desc)
                        else if subtype in ["page"]
                            $(".office_item[data-id=#{k}]>a>.office_item_info>.office_item_title").text(title)
                            $(".office_item[data-id=#{k}]>a>.office_item_info>.office_item_desc").text(desc)
                error:(data)->
                    console.log data

    load_dict_with_list = (list_now,html="""""",num=0)->
        for i in list_now
            if typeof(i) == 'object'
                i_keys = Object.keys(i)
                _html_items = """"""
                _html_items = load_dict_with_list(i[i_keys[0]],_html_items,num+1)
                html_item = """
                    <div class="office_item folder" data-num="#{num}" data-id="#{i_keys[0]}">
                        <div class="office_item_id">block_id: #{i_keys[0]}</div>
                        <div class="office_item_info">
                            <img class="office_item_logo close" src="/static/img/office/icon/folder.png">
                            <img class="office_item_logo open hide" src="/static/img/office/icon/folder_open.png">
                            <div class="office_item_title">TITLE</div>
                            <div class="office_item_desc">desc</div>
                            <div class="office_item_edit" data-now="edit">编辑</div>
                        </div>
                        <div class="office_items hide">#{_html_items}</div>
                    </div>
                """
            else
                html_item = """
                    <div class="office_item file" data-num="#{num}" data-id="#{i}">
                        <div class="office_item_id">block_id: #{i}</div>
                        <a href="/home/page/edit/#{i}">
                        <div class="office_item_info">
                            <img class="office_item_logo" src="/static/img/office/icon/page.png">
                            <div class="office_item_title">TITLE</div>
                            <div class="office_item_desc">desc</div>
                            <div class="office_item_edit" data-now="edit">编辑</div>
                        </div>
                        </a>
                    </div>
                """                
            html = """
                #{html}
                #{html_item}
            """
        return html
    load_dashboard_map = (dashboard_map=[])->
        _html = """"""
        _html = load_dict_with_list dashboard_map,_html
        $(".office_dashboard").append _html
        
    load_office_dashboard = ()->
        $(".office_dashboard").empty()
        $.ajax
            url:"/api/office/list"
            data:null
            dataType: 'json'
            type: 'GET'
            success:(data)->
                console.log data
                if data.info == "ok"
                    block_ids = data.block_ids
                    load_dashboard_map data.dashboard_map
                    load_block_infos block_ids, 20, Hs.current_block_infos_json
                    
            error:(data)->
                console.log data
    $(window).on "load",(evt)->
        load_office_dashboard()
    $("body").on "click",".office_item.folder>.office_item_info",(evt)->
        dom = $(this)
        if dom.find(".office_item_edit").first().attr("data-now") in ["done"]
            return false
        if dom.parents(".office_item.folder").first().find(".office_items").first().hasClass("hide")
            dom.parents(".office_item.folder").first().find(".office_items").first().removeClass("hide")
            dom.find(".office_item_logo.close").addClass("hide")
            dom.find(".office_item_logo.open").removeClass("hide")
            dom_id = dom.parents(".office_item.folder").first().attr("data-id")
            dom.append """
            <div class="office_add_area">
                <div class="office_add_btn_action"></div>
                <div class="office_add_btns hide" data-aim-folder-id="#{dom_id}">
                    <div class="office_add_btn no_border_top" data-type="folder">新建文件夹</div>
                    <div class="office_add_btn" data-type="excel">新建表格</div>
                    <div class="office_add_btn" data-type="doc">新建文稿</div>
                    <div class="office_add_btn" data-type="page">新建主页</div>
                </div>
            </div>
            """
        else
            dom.parents(".office_item.folder").first().find(".office_items").first().addClass("hide")
            dom.find(".office_item_logo.close").removeClass("hide")
            dom.find(".office_item_logo.open").addClass("hide")
            dom.find(".office_add_area").first().remove()

    $("body").on "click",".office_add_btn_action",(evt)->
        dom = $(this)
        if dom.parents(".office_add_area").first().find(".office_add_btns").first().hasClass("hide")
            $(".office_add_btns").addClass("hide")
            dom.parents(".office_add_area").first().find(".office_add_btns").first().removeClass("hide")
        else
            dom.parents(".office_add_area").first().find(".office_add_btns").first().addClass("hide")
        evt.stopPropagation()
        evt.preventDefault()
        return false

    $("body").on "click",".office_add_btn",(evt)->
        dom = $(this)
        dom_type = dom.attr("data-type")
        aim_folder_id = dom.parents(".office_add_btns").first().attr("data-aim-folder-id")
        if aim_folder_id == ""
            aim_folder_id = null
        if dom_type in ["folder","page"]
            $.ajax
                url:"/api/office/add_#{dom_type}"
                data:
                    title: null
                    desc: null
                    aim_folder_id: aim_folder_id
                dataType: 'json'
                type: 'POST'
                success:(data)->
                    console.log data
                    if data.info == "ok"
                        if dom_type in ["folder"]
                            folder_id = data.folder_id
                            if aim_folder_id == null
                                _html = """"""
                                _html = load_dict_with_list [{"#{folder_id}":[]}],_html,0
                                $(".office_dashboard").prepend _html
                            else
                                num = parseInt($(".office_item[data-id=#{aim_folder_id}]").attr("data-num"))+1
                                _html = """"""
                                _html = load_dict_with_list [{"#{folder_id}":[]}],_html,num
                                $(".office_item[data-id=#{aim_folder_id}]>.office_items").prepend _html
                            load_block_infos ["#{folder_id}"], 20, Hs.current_block_infos_json
                        else if dom_type in ["page"]
                            block_id = data.block_id
                            if aim_folder_id == null
                                _html = """"""
                                _html = load_dict_with_list ["#{block_id}"],_html,0
                                $(".office_dashboard").prepend _html
                            else
                                num = parseInt($(".office_item[data-id=#{aim_folder_id}]").attr("data-num"))+1
                                _html = """"""
                                _html = load_dict_with_list ["#{block_id}"],_html,num
                                $(".office_item[data-id=#{aim_folder_id}]>.office_items").prepend _html
                            load_block_infos ["#{block_id}"], 20, Hs.current_block_infos_json
                error:(data)->
                    console.log data
        evt.stopPropagation()
        evt.preventDefault()
        return false
    $("body").on "click",".office_item_edit",(evt)->
        dom = $(this)
        if dom.attr("data-now") in ["edit"]
            dom.text("完成")
            dom.attr("data-now","done")
            dom.parents(".office_item_info").first().find(".office_item_title,.office_item_desc").attr("contenteditable","true")
            dom.parents(".office_item_info").first().find(".office_item_title,.office_item_desc").css("cursor","text")
            if dom.parents(".office_item_info").first().parents("a").first().length > 0
                href_old = dom.parents(".office_item_info").first().parents("a").first().attr("href")
                dom.parents(".office_item_info").first().parents("a").first().attr("href","##{href_old}")
        else if dom.attr("data-now") in ["done"]
            dom.text("编辑")
            dom.attr("data-now","edit")
            dom.parents(".office_item_info").first().find(".office_item_title,.office_item_desc").attr("contenteditable","false")
            dom.parents(".office_item_info").first().find(".office_item_title,.office_item_desc").css("cursor","pointer")
            if dom.parents(".office_item_info").first().parents("a").first().length > 0
                href_old = dom.parents(".office_item_info").first().parents("a").first().attr("href")
                href_old.replace("#","")
                dom.parents(".office_item_info").first().parents("a").first().attr("href","#{href_old}")
        evt.stopPropagation()
        evt.preventDefault()
        return false
    update_dom_when_key_up_timer = null
    $("body").on "keydown",".office_item_title,.office_item_desc",(evt)->
        clearTimeout update_dom_when_key_up_timer
    $("body").on "keyup",".office_item_title,.office_item_desc",(evt)->
        dom = $(this)
        if dom.parents(".office_item_info").first().find(".office_item_edit").first().attr("data-now") in ["done"]
            clearTimeout update_dom_when_key_up_timer
            update_dom_when_key_up_timer = setTimeout ()->
                console.log("update_dom_when_key_up_timer")
                block_id = dom.parents(".office_item").first().attr("data-id")
                if dom.hasClass("office_item_title")
                    key = "title"
                else if dom.hasClass("office_item_desc")
                    key = "desc"
                else
                    return
                value = dom.text()
                $.ajax
                    url:"/api/office/update_info"
                    data:
                        key:key
                        value:value
                        block_id: block_id
                    dataType: 'json'
                    type: 'POST'
                    success:(data)->
                        console.log data
                    error:(data)->
                        console.log data
            ,1000


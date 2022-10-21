<style>
.wjd_data{
    
}
.wjd_data_col{
    display:flex;
}
.wjd_data_row{
    margin:5px;
}
tr>th,tr>td{
    border-left:1px solid #999;
    border-top:1px solid #999;
    min-width:40px;
}
table{
    border-right:1px solid #999;
    border-bottom:1px solid #999;   
}
th.text_120,td.text_120{
    min-width:120px;
}
.wjd_data_update,.wjd_data_create,.add_tr_td{
    margin:5px;
    padding:4px 8px;
}

button.wjd_data_btn {
    width: -webkit-fill-available;
    height: 44px;
    margin: 10px;
    font-size: 18px;
    border: 0;
    background-color: #3c447b;
    color: white;
    font-weight: bold;
    border-radius: 8px;
}
.wjd_plan_line {
    margin: 10px;
    background-color: #f2f2f2;
    color: #333;
    padding: 10px;
    border-radius: 4px;
}
.wjd_plan_line_title {
    font-size: 20px;
    color: #333;
}
.wjd_plan_line_creater {
    font-size: 16px;
    color: #666;
}
.wjd_plan_line_createtime {
    font-size: 16px;
    color: #999;
}
.wjd_plan_comment_log{
    text-align: center;
    font-size: 14px;
    color: #ccc;
}
.wjd_plan_comment_load_more{
    text-align: center;
    background: #f2f2f2;
    margin: 10px;
    padding: 15px;
    font-size: 16px;
    border-radius: 4px;
    color: #999;
    cursor:pointer;
}
.wjd_plan_line_tool_edit,.wjd_plan_line_tool_look{
    color:#999;
    font-size:16px;
    text-align:center;
    cursor:pointer;
}
.wjd_plan_line_tools{
    display: flex;
    border-top: 1px solid #ccc;
    margin-top: 10px;
    padding-top: 10px;
}
.wjd_plan_line_tools>div{
    flex:1;
}
</style>
<script type="text/coffeescript">

root = exports ? this
# !!!! Hotpoor root object
root.Hs or= {}
Hs = root.Hs

Hs.wjd_data_chat_id = "943880a71bad4c2db8be3818cb8d1f59"
Hs.wjd_data_current_commend_id = null
if window.location.href.indexOf("/home/page/edit")>-1
    $(".base_area").show()
else
    $(".base_area").hide()
    $("body").css "height","100%"

$(window).on "load",(evt)->
    $("body").append """
    <div class="wjd_plan_edit_list_area">
        <div class="wjd_tools">
            <div class="wjd_tool">
                <div><button class="wjd_data_btn wjd_data_plan_new">新建计划</button></div>
                <div class="wjd_plan_list">
                    <div class="wjd_plan_comment_log">正在加载中</div>
                </div>
            </div>
        </div>
    </div>
    <div class="wjd_plan_edit_area" style="display:none;">
        <div class="wjd_tools">
            <div class="wjd_tool">
                <div><button class="wjd_data_btn wjd_data_clean_and_back">放弃编辑 返回计划列表</button></div>
                <div>公司：<input class="wjd_company_input"></div>
                <div>年份：<input class="wjd_year_input"></div>
                <div>月度：<input class="wjd_month_input"></div>
                <div><button class="wjd_data_update">更新当前数据</button><button class="wjd_data_create">使用当前编辑创建新计划</button></div>
            </div>
        </div>
        <div class="wjd_data wjd_data_col">
            <div class="wjd_data_row wjd_data_items">
                <table class="wjd_data_item" data-table="采煤工作面测点" border="0" cellspacing="0" cellpadding="0">
                    <tr class="tr_th">
                        <th>点号</th>
                        <th class="text_120">采煤工作面测点</th>
                        <th>次数</th>
                        <th>操作</th>
                    </tr>
                </table>
                <div><button class="add_tr_td">加一行</button></div>
            </div>
            <div class="wjd_data_row wjd_data_items">
                <table class="wjd_data_item" data-table="掘进工作面测点" border="0" cellspacing="0" cellpadding="0">
                    <tr class="tr_th">
                        <th>点号</th>
                        <th class="text_120">掘进工作面测点</th>
                        <th>次数</th>
                        <th>操作</th>
                    </tr>
                </table>
                <div><button class="add_tr_td">加一行</button></div>
            </div>
            <div class="wjd_data_row wjd_data_items">
                <table class="wjd_data_item" data-table="硐室测点" border="0" cellspacing="0" cellpadding="0">
                    <tr class="tr_th">
                        <th>点号</th>
                        <th class="text_120">硐室测点</th>
                        <th>次数</th>
                        <th>操作</th>
                    </tr>
                </table>
                <div><button class="add_tr_td">加一行</button></div>
            </div>
            <div class="wjd_data_row wjd_data_items">
                <table class="wjd_data_item" data-table="其他测点" border="0" cellspacing="0" cellpadding="0">
                    <tr class="tr_th">
                        <th>点号</th>
                        <th class="text_120">其他测点</th>
                        <th>次数</th>
                        <th>操作</th>
                    </tr>
                </table>
                <div><button class="add_tr_td">加一行</button></div>
            </div>
        </div>
    </div>
    """
    $(".wjd_plan_list").empty()
    wjd_plan_list_load Hs.wjd_data_chat_id,null
$("body").on "click",".add_tr_td",(evt)->
    dom = $(this)
    dom_table = dom.parents(".wjd_data_items").first().find("table.wjd_data_item")
    dom_table.append """
    <tr class="tr_td">
        <td contenteditable="true"></td>
        <td contenteditable="true" class="text_120"></td>
        <td contenteditable="true"></td>
        <td><button class="del_tr_td">删除</button></td>
    </tr>
    """
$("body").on "click",".del_tr_td",(evt)->
    dom = $(this)
    dom_tr_td = dom.parents("tr.tr_td")
    dom_tr_td.remove()

$("body").on "paste",".tr_td>td",(evt)->
    evt.preventDefault()
    _text=(evt.originalEvent or evt).clipboardData.getData('text/plain')
    window.document.execCommand "insertText", false, _text

wjd_data = {}

$("body").on "click",".wjd_data_clean_and_back",(evt)->
    wjd_data = {}
    $(".wjd_company_input").val("")
    $(".wjd_year_input").val("")
    $(".wjd_month_input").val("")
    $(".wjd_plan_edit_area").hide()
    $(".wjd_plan_edit_list_area").show()
    Hs.wjd_data_current_commend_id = null
$("body").on "click",".wjd_data_plan_new",(evt)->
    wjd_data = {}
    $(".wjd_company_input").val("请输入公司名称")
    $(".wjd_year_input").val((new Date()).getFullYear())
    $(".wjd_month_input").val((new Date()).getMonth()+2)
    $(".wjd_plan_edit_area").show()
    $(".wjd_plan_edit_list_area").hide()
    Hs.wjd_data_current_commend_id = null

root.wjd_data_create = ()->
    wjd_data = {}
    _wjd_company = $(".wjd_company_input").val()
    _wjd_year = parseInt($(".wjd_year_input").val())
    _wjd_year = "#{_wjd_year}"
    $(".wjd_year_input").val(_wjd_year)

    _wjd_month= parseInt($(".wjd_month_input").val())
    _wjd_month = "#{_wjd_month}"
    $(".wjd_month_input").val(_wjd_month)

    if _wjd_company in [""] or _wjd_year in [""] or _wjd_month in [""]
        alert "公司、年份、月度值有空"
        return
    _title = "#{_wjd_company}_@@_#{_wjd_year}_@@_#{_wjd_month}"
    wjd_data =
        "title":_title
        "wjd_company":_wjd_company
        "wjd_year":_wjd_year
        "wjd_month":_wjd_month
        "wjd_items":[]
    wjd_items = []
    for table in $("table.wjd_data_item")
        wjd_item_json = {}
        wjd_item_json["table"]=$(table).attr("data-table")
        wjd_item_json_table_tds = []
        for _tr in $(table).find(".tr_td")
            _tds = $(_tr).find("td")
            _tds_data = [$(_tds[0]).text(),$(_tds[1]).text(),$(_tds[2]).text()]

            wjd_item_json_table_tds.push _tds_data
        wjd_item_json["tds_data"]=wjd_item_json_table_tds
        wjd_items.push wjd_item_json
    wjd_data["wjd_items"]=wjd_items
    console.log wjd_data
    wjd_data_load_check wjd_data,Hs.wjd_data_chat_id,null,(is_has)->
        if is_has == true
            alert "已存在该公司月度计划"
            wjd_data = {}
            return
        wjd_data_create_submit()
root.wjd_data_update = ()->
    if Hs.wjd_data_current_commend_id == null
        alert "当前数据无法更新\n可使用当前数据创建新计划"
        return
    $(".wjd_company_input").val(wjd_data["wjd_company"])
    $(".wjd_year_input").val(wjd_data["wjd_year"])
    $(".wjd_month_input").val(wjd_data["wjd_month"])
    wjd_items = []
    for table in $("table.wjd_data_item")
        wjd_item_json = {}
        wjd_item_json["table"]=$(table).attr("data-table")
        wjd_item_json_table_tds = []
        for _tr in $(table).find(".tr_td")
            _tds = $(_tr).find("td")
            _tds_data = [$(_tds[0]).text(),$(_tds[1]).text(),$(_tds[2]).text()]

            wjd_item_json_table_tds.push _tds_data
        wjd_item_json["tds_data"]=wjd_item_json_table_tds
        wjd_items.push wjd_item_json
    wjd_data["wjd_items"]=wjd_items
    console.log wjd_data
    wjd_data_comment_submit wjd_data["page_id"],wjd_data["comment_entity"],JSON.stringify(wjd_data),(data0)->
        $.ajax
            url:"/api/page/comment/remark"
            dataType:"json"
            type:"POST"
            data:
                block_id:BLOCK_ID
                chat_id: Hs.wjd_data_chat_id
                content: "remark comment #{Hs.wjd_data_current_commend_id}"
                comment_id: Hs.wjd_data_current_commend_id.split("_")[0]
                comment_sequence: Hs.wjd_data_current_commend_id.split("_")[1]
                remark_content: JSON.stringify(wjd_data)
                uuid: uuid2(6,null)
            success:(data)->
                console.log data
                if data.info == "ok"
                    alert "更新计划成功"
                    $(".wjd_plan_list").empty()
                    wjd_plan_list_load Hs.wjd_data_chat_id

            error:(data)->
                console.log data

$("body").on "click",".wjd_data_create",(evt)->
    wjd_data_create()

$("body").on "click",".wjd_data_update",(evt)->
    wjd_data_update()
root.wjd_data_load_check = (base_json,chat_id,comment_id=null,callback=null)->
    console.log "wjd_data_load_chat"
    $.ajax
        url:"/api/page/comment/load"
        dataType:"json"
        type:"GET"
        data:
            chat_id:chat_id
            comment_id:comment_id
        success:(data)->
            console.log data
            if data.info == "error"
                if data.about == "no chat's comment"
                    if callback!=null
                        callback(false)
                        return
            else if data.info == "ok"
                for comment in data.comments
                    comment_json = null
                    try
                        comment_json = JSON.parse(comment[4])
                    catch e
                        comment_json = null
                    if comment_json!=null
                        if base_json["title"] == comment_json["title"]
                            callback(true)
                            return
                if data.last_comment_id == null
                    callback(false)
                    return
                else
                    _comment_id = data.last_comment_id
                    wjd_data_load_check base_json,chat_id,_comment_id,(is_has)->
                        if is_has == true
                            alert "已存在该公司月度计划"
                            return
                        wjd_data_create_submit()
        error:(data)->
            console.log data
root.wjd_data_create_submit=(base_json)->
    alert "正在创建计划"
    console.log "wjd_data_create_submit"
    $.ajax
        url:"/api/page/add"
        dataType:"json"
        type:"POST"
        data:
            title:wjd_data["title"]
            desc:"月度瓦检点设置计划 #{wjd_data["title"]}"
        success:(data)->
            console.log data
            if data.info == "ok"
                page_id = data.block_id
                wjd_data["page_id"]=page_id
                $.ajax
                    url:"/api/page/add_comment"
                    dataType:"json"
                    type:"POST"
                    data:
                        block_id:page_id
                    success:(data)->
                        console.log data
                        if data.info == "ok"
                            comment_entity = data.comment_entity
                            wjd_data["comment_entity"]=comment_entity
                            wjd_data_comment_submit page_id,comment_entity,JSON.stringify(wjd_data),(data0)->
                                wjd_data_comment_submit BLOCK_ID,Hs.wjd_data_chat_id,JSON.stringify(wjd_data),(data1)->
                                    alert "创建计划成功"
                                    $(".wjd_plan_list").empty()
                                    wjd_plan_list_load Hs.wjd_data_chat_id
                                    Hs.wjd_data_current_commend_id = "#{data1.comment_id}_#{data1.sequence}"
                    error:(data)->
                        console.log data
        error:(data)->
            console.log data
root.wjd_data_comment_submit = (block_id,chat_id,content,callback=null)->
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
            if data.info == "ok"
                if callback!=null
                    callback(data)
        error:(data)->
            console.log data

wjd_plan_list_load_json = {}
wjd_plan_list_load_json_member = {}
root.wjd_plan_list_load = (chat_id,comment_id=null)->
    $(".wjd_plan_comment_log").remove()
    $(".wjd_plan_comment_load_more").remove()
    $(".wjd_plan_list").append """
        <div class="wjd_plan_comment_log">正在加载</div>
    """
    $.ajax
        url:"/api/page/comment/load"
        dataType:"json"
        type:"GET"
        data:
            chat_id:chat_id
            comment_id:comment_id
        success:(data)->
            if data.info == "error"
                if data.about == "no chat's comment"
                    $(".wjd_plan_comment_log").text "尚未创建计划"
                    return
            else if data.info == "ok"
                _comment_id = data.comment_id
                for k,v of data.members
                    wjd_plan_list_load_json_member[k]=v
                for comment in data.comments by -1
                    _comment_sequence = comment[0]
                    _user_id = comment[1]
                    _createtime = comment[2]
                    _createtime_str = formatDateAll(_createtime*1000)
                    comment_json = null
                    
                    try
                        comment_json = JSON.parse(comment[4])
                    catch e
                        comment_json = null
                    if comment_json == null
                        continue

                    remarks = comment[5]["remarks"]
                    for remark_item in remarks
                        remark_item_json = null
                        try
                            remark_item_json = JSON.parse(remark_item[1])
                        catch e
                            remark_item_json = null
                        if remark_item_json!=null
                            comment_json = remark_item_json

                    wjd_plan_list_load_json["#{_comment_id}_#{_comment_sequence}"]=
                        "comment_id":_comment_id
                        "data":comment
                        "json":comment_json
                    $(".wjd_plan_list").append """
                    <div class="wjd_plan_line" data-comment-id="#{_comment_id}_#{_comment_sequence}">
                        <div class="wjd_plan_line_title">计划：#{comment_json["wjd_company"]}-#{comment_json["wjd_year"]}-#{comment_json["wjd_month"]}</div>
                        <div class="wjd_plan_line_creater">创建人：#{wjd_plan_list_load_json_member[_user_id]["name"]}</div>
                        <div class="wjd_plan_line_createtime">创建时间：#{_createtime_str}</div>
                        <div class="wjd_plan_line_tools" style="display:flex;">
                            <div style="flex:1;">
                                <div class="wjd_plan_line_tool_edit">编辑</div>
                            </div>
                            <div style="flex:1;">
                                <div class="wjd_plan_line_tool_look">查看</div>
                            </div>
                        </div>
                    </div>
                    """
                $(".wjd_plan_comment_log").remove()
                if data.last_comment_id == null
                    $(".wjd_plan_list").append """
                        <div class="wjd_plan_comment_log">暂无更多计划</div>
                    """
                else
                    $(".wjd_plan_list").append """
                        <div class="wjd_plan_comment_load_more" data-chat-id="#{chat_id}" data-last-comment-id="#{data.last_comment_id}">暂无更多计划</div>
                    """
        error:(data)->
            console.log data
$("body").on "click",".wjd_plan_comment_load_more",(evt)->
    _chat_id = $(this).attr("data-chat-id")
    _comment_id = $(this).attr("data-last-comment-id")
    wjd_plan_list_load _chat_id,_comment_id
$("body").on "click",".wjd_plan_line_tool_edit",(evt)->
    data_comment_id = $(this).parents(".wjd_plan_line").first().attr("data-comment-id")
    wjd_data_load_one data_comment_id,true
$("body").on "click",".wjd_plan_line_tool_look",(evt)->
    data_comment_id = $(this).parents(".wjd_plan_line").first().attr("data-comment-id")
    wjd_data_load_one data_comment_id,false
root.wjd_data_load_one =(_data_comment_id,_edit=false)->
    Hs.wjd_data_current_commend_id = _data_comment_id
    if _edit
        $(".wjd_data_update,.wjd_data_create,.add_tr_td").show()
    else
        $(".wjd_data_update,.wjd_data_create,.add_tr_td").hide()
    $(".wjd_plan_edit_list_area").hide()
    $(".wjd_plan_edit_area").show()
    $(".tr_td").remove()
    console.log wjd_plan_list_load_json[_data_comment_id]
    wjd_data = wjd_plan_list_load_json[_data_comment_id]["json"]
    
    $(".wjd_company_input").val(wjd_data["wjd_company"])
    $(".wjd_year_input").val(wjd_data["wjd_year"])
    $(".wjd_month_input").val(wjd_data["wjd_month"])
    for wjd_item in wjd_data["wjd_items"]
        table = wjd_item["table"]
        tds_data = wjd_item["tds_data"]
        for td_data in tds_data
            if _edit
                $("table.wjd_data_item[data-table=\"#{table}\"]").append """
        <tr class="tr_td">
            <td contenteditable="true">#{td_data[0]}</td>
            <td contenteditable="true" class="text_120">#{td_data[1]}</td>
            <td contenteditable="true">#{td_data[2]}</td>
            <td><button class="del_tr_td">删除</button></td>
        </tr>
                """
            else
                $("table.wjd_data_item[data-table=\"#{table}\"]").append """
        <tr class="tr_td">
            <td contenteditable="false">#{td_data[0]}</td>
            <td contenteditable="false" class="text_120">#{td_data[1]}</td>
            <td contenteditable="false">#{td_data[2]}</td>
            <td></td>
        </tr>
                """


</script>
<script src="/static/js/coffeescript.js"></script>
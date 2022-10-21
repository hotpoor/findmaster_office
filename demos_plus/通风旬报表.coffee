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
    padding:5px;
}
table{
    width:100%;
    border-collapse: collapse;
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
.wjd_plan_line_tool_submit,.wjd_plan_line_tool_view{
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
.wjd_data_submit_area>div {
    margin: 5px;
    border-bottom: 1px solid #ccc;
    padding: 5px;
}
.wjd_data_span {
    color: #999;
    font-size: 14px;
}
.wjd_date_class_type,.wjd_date_class_type_value,.wjd_data_pointer_times {
    margin: 5px 10px;
    padding: 5px 10px;
    border-bottom: 4px solid white;
}
.wjd_date_class_type.is_current,.wjd_date_class_type_value.is_current,.wjd_data_pointer_times.is_current {
    border-bottom: 4px solid #3c447b;
}
.wjd_data_submit_data_k_v{
    display:flex;
}
.wjd_data_submit_data_k_v>div {
    flex: 1;
    padding: 5px;
    margin: 5px;
    font-size: 18px;
}

span.wjd_data_submit_data_k_about{
    color:#999;
    font-size:14px;
}
input.wjd_data_submit_data_v {
    padding: 5px;
    line-height: 16px;
    font-size: 16px;
}
.wjd_plan_edit_area{
    padding-bottom:30px;
}
.wjd_data_submit_data_btn_save{
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
select,input{
    font-size:18px;
    padding:5px;
    margin:5px;
}
.wjd_data_submit_data_btn_save_log{
    text-align: center;
    font-size: 18px;
    margin: 5px;
    color: red;
}
.has_data_date_str{
    margin: 5px;
    border-bottom: 1px solid #ccc;
    padding: 5px;
}
.has_data_date_list_tools>button{
    margin:5px;
}
.wjd_data_submit_data_v_calc{
    padding:5px 10px;
}

.need_to_print_type_back{
    cursor:pointer;
    color:#f2f2f2;
    margin:10px 0px;
}
.need_to_print_type_back:hover{
    color:black;
}

</style>
<script type="text/coffeescript">

root = exports ? this
# !!!! Hotpoor root object
root.Hs or= {}
Hs = root.Hs

root.formatDateMMDD = (now) ->
    now_date = new Date(now)
    audio_list_time_now = new Date()
    year = now_date.getFullYear()
    month = now_date.getMonth()+1
    date = now_date.getDate()
    hour = now_date.getHours()
    minute = now_date.getMinutes()
    return  month+"月"+date+"日"


Hs.wjd_data_chat_id = "bc124285c19d418a8d71d1a01ad8503c"
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
                <div class="wjd_plan_list">
                    <div class="wjd_plan_comment_log">正在加载中</div>
                </div>
            </div>
        </div>
    </div>
    <div class="wjd_plan_edit_area" style="display:none;">
        <div class="wjd_tools">
            <div class="wjd_tool">
                <div><button class="wjd_data_btn wjd_data_clean_and_back">返回月度计划列表</button></div>
            </div>
        </div>
        <div class="wjd_data_submit_area" style="display:none;">
            <div style="
                text-align: center;
                color: #999;
                font-size: 20px;
            ">旬报填写</div>
            <div>存储计划ID: <span class="wjd_page_id_submit"></span></div>
            <div>存储区块ID: <span class="wjd_comment_entity_submit"></span></div>
            <div>公司: <span class="wjd_compay_submit"></span></div>
            <div>年份: <span class="wjd_year_submit"></span></div>
            <div>月份: <span class="wjd_month_submit"></span></div>
            <div>日期选择: <select class="wjd_date_submit"></select></div>
            <div>当期旬报: <span class="wjd_date_fix_title">请选择日期，将匹配旬报</span></div>
            <div>报表存储区块: <span class="wjd_date_comment_entity_submit">获取中</span></div>
            <div style="display:none;">
                <div class="wjd_data_span">班次选择</div>
                <div style="display: flex;">
                    <div class="wjd_date_class_type is_current" data-num="0">不记录班次</div>
                    <div class="wjd_date_class_type" data-num="3">三班八小时制</div>
                    <div class="wjd_date_class_type" data-num="4">四班六小时制</div>
                </div>
                <div style="display: flex;">
                    <div class="wjd_date_class_type_value is_current" data-name="不记录班次">不记录班次</div>
                    <div class="wjd_date_class_type_value" data-name="早班">早班</div>
                    <div class="wjd_date_class_type_value" data-name="中班">中班</div>
                    <div class="wjd_date_class_type_value" data-name="晚班">晚班</div>
                    <div class="wjd_date_class_type_value" data-name="夜班">夜班</div>
                </div>
            </div>
            <div>
                <div class="wjd_data_span">测点选择</div>
                <div>
                    测点: <select class="wjd_data_pointer"></select>
                </div>
                <div class="wjd_data_span hide">次数选择</div>
                <div style="display: none;" class="wjd_data_pointer_times_area">
                    <div class="wjd_data_pointer_times is_current" data-times="1">第1次</div>
                </div>
            </div>
            <div>
                <div class="wjd_data_span">测点时间</div>
                <div>
                    <div>日期: <input class="wjd_data_time_date" type="date"></div>
                    <div>时间: 
                    <select class="wjd_data_time_date_hour"></select> :
                    <select class="wjd_data_time_date_minute"></select></div>
                </div>
            </div>
            <div>
                <div class="wjd_data_span">测风员</div>
                <div>用户ID: <span class="wjd_data_submit_user_id">#{USER_ID}</span></div>
                <div>邮箱: <span class="wjd_data_submit_user_email"></span></div>
                <div>姓名: <input class="wjd_data_submit_name"></div>
            </div>
            <div>
                <div class="wjd_data_span">检测项目</div>
                <div class="wjd_data_submit_data_k_v">
                    <div class="wjd_data_submit_data_k" data-key="断面m2">
                        断面
                        <span class="wjd_data_submit_data_k_about">m<sup>2</sup></span>
                    </div>
                    <div>
                        <input class="wjd_data_submit_data_v" type="tel"  data-key="断面m2">
                    </div>
                </div>
                <div class="wjd_data_submit_data_k_v">
                    <div class="wjd_data_submit_data_k" data-key="风速系数a">
                        风速系数
                        <span class="wjd_data_submit_data_k_about">a</span>
                    </div>
                    <div>
                        <input class="wjd_data_submit_data_v" type="tel"  data-key="风速系数a">
                    </div>
                </div>
                <div class="wjd_data_submit_data_k_v">
                    <div class="wjd_data_submit_data_k" data-key="风速系数b">
                        风速系数
                        <span class="wjd_data_submit_data_k_about">b</span>
                    </div>
                    <div>
                        <input class="wjd_data_submit_data_v" type="tel"  data-key="风速系数b">
                    </div>
                </div>
                <div class="wjd_data_submit_data_k_v">
                    <div class="wjd_data_submit_data_k" data-key="测量表风速">
                        测量表风速
                        <span class="wjd_data_submit_data_k_about">单位: 格</span>
                    </div>
                    <div>
                        第1次<input class="wjd_data_submit_data_v" type="tel"  data-key="测量表风速1"><br>
                        第2次<input class="wjd_data_submit_data_v" type="tel"  data-key="测量表风速2"><br>
                        第3次<input class="wjd_data_submit_data_v" type="tel"  data-key="测量表风速3"><br>
                        <button class="wjd_data_submit_data_v_calc">计算实际风速和风量</button>
                    </div>
                </div>
                <div class="wjd_data_submit_data_k_v">
                    <div class="wjd_data_submit_data_k" data-key="实际风速m/s">
                        实际风速
                        <span class="wjd_data_submit_data_k_about">m/s</span>
                    </div>
                    <div>
                        <input class="wjd_data_submit_data_v" type="tel"  data-key="实际风速m/s" disabled placeholder="填写上方参数后计算">
                    </div>
                </div>
                <div class="wjd_data_submit_data_k_v">
                    <div class="wjd_data_submit_data_k" data-key="实际风量m3/min">
                        实际风量
                        <span class="wjd_data_submit_data_k_about">m<sup>3</sup>/min</span>
                        <br>
                        <span class="wjd_data_submit_data_k_about">计划需风量: </span><span class="wjd_data_submit_data_k_about jihuaxufengliang">--</span>
                    </div>
                    <div>
                        <input class="wjd_data_submit_data_v" type="tel"  data-key="实际风量m3/min" disabled placeholder="填写上方参数后计算">
                    </div>
                </div>
                <div class="wjd_data_submit_data_k_v">
                    <div class="wjd_data_submit_data_k" data-key="瓦斯含量（%）CH4">
                        瓦斯含量（%）
                        <span class="wjd_data_submit_data_k_about">CH<sub>4</sub></span>
                    </div>
                    <div>
                        <input class="wjd_data_submit_data_v" type="tel" data-key="瓦斯含量（%）CH4" placeholder="选填">
                    </div>
                </div>
                <div class="wjd_data_submit_data_k_v">
                    <div class="wjd_data_submit_data_k" data-key="瓦斯含量（%）CO2">
                        瓦斯含量（%）
                        <span class="wjd_data_submit_data_k_about">CO<sup>2</sup></span>
                    </div>
                    <div>
                        <input class="wjd_data_submit_data_v" type="tel" data-key="瓦斯含量（%）CO2" placeholder="选填">
                    </div>
                </div>
                <div class="wjd_data_submit_data_k_v">
                    <div class="wjd_data_submit_data_k" data-key="温度°C">
                        温度
                        <span class="wjd_data_submit_data_k_about">单位: °C</span>
                    </div>
                    <div>
                        <input class="wjd_data_submit_data_v" type="tel" data-key="温度°C">
                    </div>
                </div>
            </div>
            <div>
                <div class="wjd_data_submit_data_btn_save_log" style="display:none;"></div>
                <button class="wjd_data_submit_data_btn_save">保存提交</button>
            </div>
        </div>
        <div class="wjd_data_view_area" style="display:none;">
            <div class="has_data_date_list_info">
                <div style="
                    text-align: center;
                    color: #999;
                    font-size: 20px;
                ">数据查看</div>
                <div class="has_data_date_list_info_line">
                    <div class="has_data_date_str">存储计划ID: <span class="has_data_date_page_id"></span></div>
                    <div class="has_data_date_str">存储区块ID: <span class="has_data_date_comment_entity"></span></div>
                    <div class="has_data_date_str">公司: <span class="has_data_date_company"></span></div>
                    <div class="has_data_date_str">年份: <span class="has_data_date_year"></span></div>
                    <div class="has_data_date_str">月份: <span class="has_data_date_month"></span></div>
                    <div class="has_data_date_str">日期: <select class="has_data_date_select"></select></div>
                    <div class="has_data_date_str">当期旬报: <span class="has_data_date_fix_title">请选择日期，将匹配旬报</span></div>
                    <div class="has_data_date_str">旬报存储区块: <span class="has_data_date_daily_comment_entity"></span></div>
                </div>
            </div>
            <div class="has_data_date_list_tools">
                <button class="sort_time_point_num_up">按点号顺序-旬报表</button>
                <button class="sort_time_submit_down">按最新提交时间</button>
                <button class="sort_time_point_ctv hide" data-ctv="早班">早班报表</button>
                <button class="sort_time_point_ctv hide" data-ctv="中班">中班报表</button>
                <button class="sort_time_point_ctv hide" data-ctv="晚班">晚班报表</button>
                <button class="sort_time_point_ctv hide" data-ctv="夜班">夜班报表</button>
                <button class="sort_time_submit_up">按提交时间顺序</button>
                <button class="sort_time_pointer">按记录时间顺序</button>
            </div>
            <div class="has_data_date_list_tools">
                <div>当前加载数据-人员筛选</div>
                <div class="has_data_date_list_tools person_select">
                </div>
            </div>
            <div class="has_data_date_list_tools">
                <button class="need_to_print_type">点击打印</button>
            </div>
            <div class="has_data_date_list">
            </div>
            <div class="has_data_date_list_sign" style="margin:10px 0px;">
                <div style="display:flex;">
                    <div style="flex:1;text-align:left;">总工程师：</div>
                    <div style="flex:1;text-align:left;">通风科长：</div>
                    <div style="flex:1;text-align:left;">通防技术：</div>
                    <div style="flex:1;text-align:left;">填报人：</div>
                </div>
                <div>
                    <div class="need_to_print_type_back">显示全部</div>
                </div>
            </div>
        </div>
    </div>
    """
    a=localStorage.getItem("风速系数a")
    b=localStorage.getItem("风速系数b")
    $(".wjd_data_submit_data_v[data-key=\"风速系数a\"]").val(a)
    $(".wjd_data_submit_data_v[data-key=\"风速系数b\"]").val(b)


    $(".wjd_plan_list").empty()
    wjd_plan_list_load Hs.wjd_data_chat_id,null

$("body").on "click",".need_to_print_type",(evt)->
    $(".wjd_tools").hide()
    $(".wjd_data_view_area>.has_data_date_list_info").hide()
    $(".wjd_data_view_area>.has_data_date_list_tools").hide()
    document.execCommand("print")

$("body").on "click",".need_to_print_type_back",(evt)->
    $(".wjd_tools").show()
    $(".wjd_data_view_area>.has_data_date_list_info").show()
    $(".wjd_data_view_area>.has_data_date_list_tools").show()
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
                                <div class="wjd_plan_line_tool_submit">旬报填写</div>
                            </div>
                            <div style="flex:1;">
                                <div class="wjd_plan_line_tool_view">数据查看</div>
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

$("body").on "click",".wjd_data_clean_and_back",(evt)->
    $(".wjd_plan_edit_area").hide()
    $(".wjd_data_view_area").hide()
    $(".wjd_data_submit_area").hide()
    $(".wjd_plan_edit_list_area").show()
current_plan_json = null
$("body").on "click",".wjd_plan_line_tool_submit",(evt)->
    $(".wjd_plan_edit_list_area").hide()
    $(".wjd_data_view_area").hide()
    $(".wjd_data_submit_area").show()
    $(".wjd_plan_edit_area").show()

    $(".wjd_data_time_date_hour").empty()
    for i in [0..23]
        $(".wjd_data_time_date_hour").append """
        <option value="#{i}">#{i}时</option>
        """
    $(".wjd_data_time_date_minute").empty()
    for i in [0..59]
        $(".wjd_data_time_date_minute").append """
        <option value="#{i}">#{i}分</option>
        """
    _data_comment_id = $(this).parents(".wjd_plan_line").first().attr("data-comment-id")
    console.log wjd_plan_list_load_json[_data_comment_id]
    current_plan_json =
        "data_comment_id":_data_comment_id

    $(".wjd_page_id_submit").text wjd_plan_list_load_json[_data_comment_id]["json"]["page_id"]
    $(".wjd_comment_entity_submit").text wjd_plan_list_load_json[_data_comment_id]["json"]["comment_entity"]
    $(".wjd_compay_submit").text wjd_plan_list_load_json[_data_comment_id]["json"]["wjd_company"]
    $(".wjd_year_submit").text wjd_plan_list_load_json[_data_comment_id]["json"]["wjd_year"]
    $(".wjd_month_submit").text wjd_plan_list_load_json[_data_comment_id]["json"]["wjd_month"]
    _page_id = wjd_plan_list_load_json[_data_comment_id]["json"]["page_id"]
    _comment_entity = wjd_plan_list_load_json[_data_comment_id]["json"]["comment_entity"]
    _wjd_company = wjd_plan_list_load_json[_data_comment_id]["json"]["wjd_company"]
    _wjd_year =wjd_plan_list_load_json[_data_comment_id]["json"]["wjd_year"]
    _wjd_month = wjd_plan_list_load_json[_data_comment_id]["json"]["wjd_month"]
    _time_now = new Date()
    _time_year = "#{_time_now.getFullYear()}"
    _time_month = "#{_time_now.getMonth()+1}"
    if _time_month.length ==1
        _time_month = "0#{_time_month}"
    _time_date = "#{_time_now.getDate()}"
    if _time_date.length ==1
        _time_date = "0#{_time_date}"
    _time_now_str="#{_time_year}-#{_time_month}-#{_time_date}"
    $(".wjd_data_time_date").val(_time_now_str)
    $(".wjd_data_time_date_hour").val(_time_now.getHours())
    $(".wjd_data_time_date_minute").val(_time_now.getMinutes())
    $(".wjd_date_submit").empty()
    _date_all = null
    _wjd_month_str = "#{_wjd_month}"
    _wjd_year_str = "#{_wjd_year}"
    if _wjd_month_str.length == 1
        _wjd_month_str = "0#{_wjd_month_str}"
    if _wjd_month_str in ["01","03","05","07","08","10","12"]
        _date_all = 31
    else if _wjd_month_str in ["02"]
        if _wjd_year_str%400 == 0
            _date_all = 29
        else if _wjd_year_str%4 == 0 and _wjd_year_str%100!=0
            _date_all = 29
        else
            _date_all = 28
    else
        _date_all = 30
    $(".wjd_date_submit").append """
        <option value="">选择日期</option>
    """
    for i in [1.._date_all]
        $(".wjd_date_submit").append """
        <option value="#{i}">#{i}</option>
        """
    
    $(".wjd_date_comment_entity_submit").text "请确定旬报选择"
    $(".wjd_date_comment_entity_submit").removeAttr "data-daily-chat"
    if "#{_wjd_year}" == "#{_time_year}"
        if "#{_wjd_month}" == "#{_time_now.getMonth()+1}"
            $(".wjd_date_submit").val("#{_time_now.getDate()}")
            _daily_title_span = _time_now.getDate()
            if _daily_title_span<=10
                _daily_title_span = "上旬"
            else if _daily_title_span<=20
                _daily_title_span = "中旬"
            else
                _daily_title_span = "下旬"
            $(".wjd_date_fix_title").text _daily_title_span
            _daily_title = "#{_wjd_company}_@@_#{_wjd_year}_@@_#{_wjd_month}_@@_#{_daily_title_span}"
            _daily_json =
                "daily_title": _daily_title
                "daily_comment_entity":null
                "daily_base_info":
                    "page_id":_page_id
                    "comment_entity":_comment_entity
                    "data_comment_id":_data_comment_id
            wjd_data_date_load_check _daily_json,_comment_entity,null,(is_has,daily_comment_entity)->
                if is_has == true
                    $(".wjd_date_comment_entity_submit").text daily_comment_entity
                    $(".wjd_date_comment_entity_submit").attr "data-daily-chat",daily_comment_entity
                    alert "已加载旬报存储区块"
                    return
                else
                    wjd_data_date_create_daily_comment_entity(_daily_json,_daily_json["daily_base_info"]["page_id"])

    # $(".wjd_date_class_type").removeClass("is_current")
    # $(".wjd_date_class_type_value").removeClass("is_current")
    # $(".wjd_date_class_type_value").show()
    # $(".wjd_data_pointer_times").removeClass("is_current")
    # $(".wjd_data_pointer_times").show()
    $(".wjd_data_pointer").empty()
    $(".wjd_data_pointer").append """
        <option value="">请选择检查点</option>
    """
    for _wjd_item in wjd_plan_list_load_json[_data_comment_id]["json"]["wjd_items"]
        _wjd_item_table = _wjd_item["table"]
        _s_index = 0
        _q_index = 0
        if _wjd_item_table in ["采煤工作面"]
            _s_index = 7
            _q_index = 6
        else if _wjd_item_table in ["掘进工作面"]
            _s_index = 4
            _q_index = 9
        else if _wjd_item_table in ["硐室","其他独立供风点"]
            _s_index = 3
            _q_index = 2
        for _wjd_item_pointer in _wjd_item["tds_data"]
            _wjd_item_pointer_value = "#{_wjd_item_table}_@@_#{_wjd_item_pointer[0]}_@@_#{_wjd_item_pointer[1]}_@@_#{_wjd_item_pointer[_s_index]}_@@_#{_wjd_item_pointer[_q_index]}"
            $(".wjd_data_pointer").append """
            <option value="#{_wjd_item_pointer_value}">编号:#{_wjd_item_pointer[0]}|#{_wjd_item_pointer[1]}</option>
            """
    $.ajax
        url:"/api/user/get_user_info"
        dataType:"json"
        type:"GET"
        data:null
        success:(data)->
            console.log data
            if data.info == "ok"
                $(".wjd_data_submit_user_email").text data.email
                $(".wjd_data_submit_name").val data.name
        error:(data)->
            console.log data
    $(".wjd_data_submit_data_v").val("")
    a=localStorage.getItem("风速系数a")
    b=localStorage.getItem("风速系数b")
    $(".wjd_data_submit_data_v[data-key=\"风速系数a\"]").val(a)
    $(".wjd_data_submit_data_v[data-key=\"风速系数b\"]").val(b)
    $(".wjd_data_submit_data_btn_save_log").hide()
    $(".wjd_data_submit_data_btn_save").show()

$("body").on "change",".wjd_data_pointer",(evt)->
    _wjd_data_pointer_value = $(".wjd_data_pointer").val()
    if _wjd_data_pointer_value in [""]
        $(".wjd_data_pointer_times").removeClass("is_current")
        return
    $(".wjd_data_pointer_times_area").empty()
    $(".wjd_data_pointer_times_area").append """
        <div class="wjd_data_pointer_times is_current" data-times="1">第1次</div>
    """
    _wjd_data_pointer_value_num = parseInt(_wjd_data_pointer_value.split("_@@_")[3])
    _wjd_data_pointer_value_num_q = parseInt(_wjd_data_pointer_value.split("_@@_")[4])
    if isNaN(_wjd_data_pointer_value_num_q)
        $(".jihuaxufengliang").text "未设置"
    else
        $(".jihuaxufengliang").text _wjd_data_pointer_value_num_q
    if isNaN(_wjd_data_pointer_value_num)
        $(".wjd_data_submit_data_v[data-key=\"断面m2\"]").val("")
    else
        $(".wjd_data_submit_data_v[data-key=\"断面m2\"]").val(_wjd_data_pointer_value_num)
    # if _wjd_data_pointer_value_num in [NaN]
    #     $(".wjd_data_pointer_times_area").append """
    #         <div class="wjd_data_pointer_times" data-times="1">第1次</div>
    #     """
    # else
    #     for i in [1.._wjd_data_pointer_value_num]
    #         $(".wjd_data_pointer_times_area").append """
    #             <div class="wjd_data_pointer_times" data-times="#{i}">第#{i}次</div>
    #         """

$("body").on "change",".wjd_date_submit",(evt)->
    _data_comment_id = current_plan_json["data_comment_id"]
    $(".wjd_data_pointer_times_area").empty()
    $(".wjd_data_pointer_times_area").append """
        <div class="wjd_data_pointer_times is_current" data-times="1">第1次</div>
    """
    
    _wjd_date = $(".wjd_date_submit").val()
    if _wjd_date == ""
        $(".wjd_date_comment_entity_submit").text "请确定旬报选择"
        $(".wjd_date_comment_entity_submit").removeAttr "data-daily-chat"
        return
    _wjd_date = parseInt(_wjd_date)
    # _wjd_date = "#{_wjd_date}"

    _page_id = wjd_plan_list_load_json[_data_comment_id]["json"]["page_id"]
    _comment_entity = wjd_plan_list_load_json[_data_comment_id]["json"]["comment_entity"]
    _wjd_company = wjd_plan_list_load_json[_data_comment_id]["json"]["wjd_company"]
    _wjd_year = wjd_plan_list_load_json[_data_comment_id]["json"]["wjd_year"]
    _wjd_month = wjd_plan_list_load_json[_data_comment_id]["json"]["wjd_month"]

    _daily_title_span = _wjd_date
    if _daily_title_span<=10
        _daily_title_span = "上旬"
    else if _daily_title_span<=20
        _daily_title_span = "中旬"
    else
        _daily_title_span = "下旬"
    if _daily_title_span in ["下旬"]
        $(".wjd_data_submit_data_v[data-key=\"瓦斯含量（%）CH4\"]").attr("placeholder","必填")
        $(".wjd_data_submit_data_v[data-key=\"瓦斯含量（%）CO2\"]").attr("placeholder","必填")
    else
        $(".wjd_data_submit_data_v[data-key=\"瓦斯含量（%）CH4\"]").attr("placeholder","选填")
        $(".wjd_data_submit_data_v[data-key=\"瓦斯含量（%）CO2\"]").attr("placeholder","选填")

    $(".wjd_date_fix_title").text _daily_title_span
    _daily_title = "#{_wjd_company}_@@_#{_wjd_year}_@@_#{_wjd_month}_@@_#{_daily_title_span}"
    _daily_json =
        "daily_title": _daily_title
        "daily_comment_entity":null
        "daily_base_info":
            "page_id":_page_id
            "comment_entity":_comment_entity
            "data_comment_id":_data_comment_id
    wjd_data_date_load_check _daily_json,_comment_entity,null,(is_has,daily_comment_entity)->
        if is_has == true
            $(".wjd_date_comment_entity_submit").text daily_comment_entity
            $(".wjd_date_comment_entity_submit").attr "data-daily-chat",daily_comment_entity
            alert "已加载旬报存储区块"
            return
        else
            wjd_data_date_create_daily_comment_entity(_daily_json,_daily_json["daily_base_info"]["page_id"])

root.wjd_data_date_load_check = (daily_json,chat_id,comment_id=null,callback=null)->
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
                        callback(false,null)
                        return
            else if data.info == "ok"
                for comment in data.comments
                    comment_json = null
                    try
                        comment_json = JSON.parse(comment[4])
                    catch e
                        comment_json = null
                    if comment_json!=null
                        if daily_json["daily_title"] == comment_json["daily_title"]
                            callback(true,comment_json["daily_comment_entity"])
                            return
                if data.last_comment_id == null
                    callback(false,null)
                    return
                else
                    _comment_id = data.last_comment_id
                    wjd_data_date_load_check daily_json,chat_id,_comment_id,(is_has,daily_comment_entity)->
                        if is_has == true
                            $(".wjd_date_comment_entity_submit").text daily_comment_entity
                            $(".wjd_date_comment_entity_submit").attr "data-daily-chat",daily_comment_entity
                            alert "已加载旬报存储区块"
                            return
                        else
                            wjd_data_date_create_daily_comment_entity(daily_json,daily_json["daily_base_info"]["page_id"])
        error:(data)->
            console.log data

root.wjd_data_date_create_daily_comment_entity = (daily_json,page_id)->
    $.ajax
        url:"/api/page/add_comment_force"
        dataType:"json"
        type:"POST"
        data:
            block_id:page_id
        success:(data)->
            console.log data
            if data.info == "ok"
                daily_comment_entity = data.comment_entity
                $(".wjd_date_comment_entity_submit").text daily_comment_entity
                $(".wjd_date_comment_entity_submit").attr "data-daily-chat",daily_comment_entity
                daily_json["daily_comment_entity"]=daily_comment_entity
                wjd_data_date_comment_submit page_id,daily_json["daily_base_info"]["comment_entity"],JSON.stringify(daily_json),(data)->
                    alert "已加载旬报存储区块"
        error:(data)->
            console.log data

root.wjd_data_date_comment_submit = (block_id,chat_id,content,callback=null)->
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

$("body").on "click",".wjd_date_class_type",(evt)->
    $(".wjd_date_class_type").removeClass("is_current")
    $(this).addClass("is_current")
    _data_num = $(this).attr("data-num")
    if _data_num == "3"
        $(".wjd_date_class_type_value[data-name=\"晚班\"]").hide()
    else if _data_num == "4"
        $(".wjd_date_class_type_value[data-name=\"晚班\"]").show()

$("body").on "click",".wjd_date_class_type_value",(evt)->
    $(".wjd_date_class_type_value").removeClass("is_current")
    $(this).addClass("is_current")
$("body").on "click",".wjd_data_pointer_times",(evt)->
    $(".wjd_data_pointer_times").removeClass("is_current")
    $(this).addClass("is_current")

$("body").on "click",".wjd_plan_line_tool_view",(evt)->
    $(".wjd_plan_edit_list_area").hide()
    $(".wjd_data_submit_area").hide()
    $(".wjd_data_view_area").show()
    $(".wjd_plan_edit_area").show()

    $(".has_data_date_list").empty()
    $(".has_data_date_daily_comment_entity").text "请确定旬报选择"
    $(".has_data_date_daily_comment_entity").removeAttr "data-daily-chat"

    _data_comment_id = $(this).parents(".wjd_plan_line").first().attr("data-comment-id")
    console.log wjd_plan_list_load_json[_data_comment_id]
    current_plan_json =
        "data_comment_id":_data_comment_id

    $(".has_data_date_page_id").text wjd_plan_list_load_json[_data_comment_id]["json"]["page_id"]
    $(".has_data_date_comment_entity").text wjd_plan_list_load_json[_data_comment_id]["json"]["comment_entity"]
    $(".has_data_date_company").text wjd_plan_list_load_json[_data_comment_id]["json"]["wjd_company"]
    $(".has_data_date_year").text wjd_plan_list_load_json[_data_comment_id]["json"]["wjd_year"]
    $(".has_data_date_month").text wjd_plan_list_load_json[_data_comment_id]["json"]["wjd_month"]
    
    $(".has_data_date_select").empty()
    $(".has_data_date_select").append """
        <option value="">请确定旬报选择</option>
    """
    _date_all = null
    _wjd_month_str = "#{wjd_plan_list_load_json[_data_comment_id]["json"]["wjd_month"]}"
    _wjd_year_str = "#{wjd_plan_list_load_json[_data_comment_id]["json"]["wjd_year"]}"
    if _wjd_month_str.length == 1
        _wjd_month_str = "0#{_wjd_month_str}"
    if _wjd_month_str in ["01","03","05","07","08","10","12"]
        _date_all = 31
    else if _wjd_month_str in ["02"]
        if _wjd_year_str%400 == 0
            _date_all = 29
        else if _wjd_year_str%4 == 0 and _wjd_year_str%100!=0
            _date_all = 29
        else
            _date_all = 28
    else
        _date_all = 30
    for i in [1.._date_all]
        $(".has_data_date_select").append """
            <option value="#{i}">#{i}</option>
        """
root.wjd_data_date_load_view_all_table_json = []

$("body").on "click",".sort_time_submit_up",(evt)->
    wjd_data_date_load_view_all_table_json_load("sort_time_submit_up")
$("body").on "click",".sort_time_submit_down",(evt)->
    wjd_data_date_load_view_all_table_json_load("sort_time_submit_down")
$("body").on "click",".sort_time_pointer",(evt)->
    wjd_data_date_load_view_all_table_json_load("sort_time_pointer")
$("body").on "click",".sort_time_point_num",(evt)->
    wjd_data_date_load_view_all_table_json_load("sort_time_point_num")
$("body").on "click",".sort_time_point_num_up",(evt)->
    wjd_data_date_load_view_all_table_json_load("sort_time_point_num_up")
$("body").on "click",".sort_time_point_ctv",(evt)->
    ctv = $(this).attr("data-ctv")
    wjd_data_date_load_view_all_table_json_load("sort_time_point_ctv",ctv)

root.wjd_data_date_load_view_all_table_json_load = (sort_type="sort_time_point_num_up",ctv=null)->
    $(".has_data_date_list").empty()
    _data_now = wjd_data_date_load_view_all_table_json.concat()
    
    if sort_type in ["sort_time_submit_up"]
        _data_now.reverse()
    else if sort_type in ["sort_time_pointer"]
        _a = (a,b)->
            return a[4]["wjd_data_time_date_timer"]-b[4]["wjd_data_time_date_timer"]
        _data_now.sort(_a)
    else if sort_type in ["sort_time_point_num"]
        _a = (a,b)->
            a_num = 0
            b_num = 0
            try
                a_num = parseInt(a[4]["wjd_data_pointer"].split("_@@_")[1])
            catch e
                a_num = 0
            try
                b_num = parseInt(b[4]["wjd_data_pointer"].split("_@@_")[1])
            catch e
                b_num = 0
            return a_num - b_num
        _b = (a,b)->
            return a[4]["wjd_data_time_date_timer"]-b[4]["wjd_data_time_date_timer"]

        _data_now.sort(_b).sort(_a)
    else if sort_type in ["sort_time_point_ctv"]
        _a = (a,b)->
            a_num = 0
            b_num = 0
            try
                a_num = parseInt(a[4]["wjd_data_pointer"].split("_@@_")[1])
            catch e
                a_num = 0
            try
                b_num = parseInt(b[4]["wjd_data_pointer"].split("_@@_")[1])
            catch e
                b_num = 0
            return a_num - b_num
        _b = (a,b)->
            return a[4]["wjd_data_time_date_timer"]-b[4]["wjd_data_time_date_timer"]
        _c = (a,b)->
            return a[4]["wjd_data_pointer_times"]-b[4]["wjd_data_pointer_times"]
        _data_now.sort(_b).sort(_c).sort(_a)
    else if sort_type in ["sort_time_point_num_up"]
        _a = (a,b)->
            a_num = 0
            b_num = 0
            try
                a_num = parseInt(a[4]["wjd_data_pointer"].split("_@@_")[1])
            catch e
                a_num = 0
            try
                b_num = parseInt(b[4]["wjd_data_pointer"].split("_@@_")[1])
            catch e
                b_num = 0
            return a_num - b_num
        _b = (a,b)->
            return a[4]["wjd_data_time_date_timer"]-b[4]["wjd_data_time_date_timer"]

        _data_now.sort(_b).sort(_a)


    _names_list = []
    if sort_type in ["sort_time_point_num"]
        items = []
        items_info =
            "class_type_max":0
            "times_max":0
        _data_comment_id = current_plan_json["data_comment_id"]
        for _wjd_item in wjd_plan_list_load_json[_data_comment_id]["json"]["wjd_items"]
            _wjd_item_table = _wjd_item["table"]
            for _wjd_item_pointer in _wjd_item["tds_data"]
                if parseInt(_wjd_item_pointer[2]) not in [NaN]
                    if parseInt(_wjd_item_pointer[2])>items_info["times_max"]
                        items_info["times_max"] = parseInt(_wjd_item_pointer[2])
        _item =
            "早班":{}
            "中班":{}
            "晚班":{}
            "夜班":{}
            "max_num":0
            "item_flag":null
        _items_flag = null
        for item in _data_now
            _t = formatDateAll(item[4]["wjd_data_time_date_timer"]*1000)
            _t_s = formatDateAll(item[2]*1000)
            _data = {}
            for _d in item[4]["collect_data"]
                _data[_d[0]]=_d[1]
            _p = item[4]["wjd_data_pointer"].split("_@@_")
            _name = item[4]["user_name"]
            if _name not in _names_list
                _names_list.push _name
            _c = item[4]["class_type"]
            if parseInt(_c) not in [NaN]
                if parseInt(_c)>items_info["class_type_max"]
                    items_info["class_type_max"]=parseInt(_c)
            _ct = item[4]["class_type_value"]
            _pt = item[4]["wjd_data_pointer_times"]
            _pt_need = _p[3]
            _item_flag = item[4]["wjd_data_pointer"]
            if _items_flag == null
                _items_flag = _item_flag
                _item["item_flag"]=_item_flag
            else
                if _items_flag != _item_flag
                    items.push _item
                    _items_flag = _item_flag
                    _item =
                        "早班":{}
                        "中班":{}
                        "晚班":{}
                        "夜班":{}
                        "max_num":0
                        "item_flag":_item_flag
            if _item[_ct][_pt] in [undefined,null,""]
                _item[_ct][_pt] = []
            _item[_ct][_pt].push item
            if _item[_ct][_pt].length > _item["max_num"]
                _item["max_num"] = _item[_ct][_pt].length
        items.push _item

        _first_line_tr_th = ""
        _second_line_tr_th = ""
        _third_line_tr_th = ""
        if items_info["class_type_max"]==4
            _times = items_info["times_max"]
            _first_line_tr = """
                <th rowspan="3">点号</th>
                <th rowspan="3">点名</th>
                <th colspan="#{_times*10}">早班</th>
                <th colspan="#{_times*10}">中班</th>
                <th colspan="#{_times*10}">晚班</th>
                <th colspan="#{_times*10}">夜班</th>
            """
            for i in [1..4]
                for j in [1.._times]
                    _second_line_tr_th = """
                    #{_second_line_tr_th}
                    <th colspan="10">第#{j}次</th>
                    """
                    _third_line_tr_th = """
                    #{_third_line_tr_th}
                    <th>时分</th>
                    <th>班次</th>
                    <th>采集次数</th>
                    <th>所需次数</th>
                    <th>CH4%</th>
                    <th>CO2%</th>
                    <th>COppm</th>
                    <th>温度°C</th>
                    <th>提交时间</th>
                    <th>瓦检工</th>
                    """
        else
            _times = items_info["times_max"]
            _first_line_tr = """
                <th rowspan="3">点号</th>
                <th rowspan="3">点名</th>
                <th colspan="#{_times*10}">早班</th>
                <th colspan="#{_times*10}">中班</th>
                <th colspan="#{_times*10}">夜班</th>
            """
            for i in [1..3]
                for j in [1.._times]
                    _second_line_tr_th = """
                    #{_second_line_tr_th}
                    <th colspan="10">第#{j}次</th>
                    """
                    _third_line_tr_th = """
                    #{_third_line_tr_th}
                    <th>时分</th>
                    <th>班次</th>
                    <th>采集次数</th>
                    <th>所需次数</th>
                    <th>CH4%</th>
                    <th>CO2%</th>
                    <th>COppm</th>
                    <th>温度°C</th>
                    <th>提交时间</th>
                    <th>瓦检工</th>
                    """
        $(".has_data_date_list").append """
        <table class="test_table">
            <tr>
                #{_first_line_tr}
            </tr>
            <tr>
                #{_second_line_tr_th}
            </tr>
            <tr>
                #{_third_line_tr_th}
            </tr>
        </table>
        """

        for _items in items
            for i in [0.._items["max_num"]-1]
                _td_p = _items["item_flag"].split("_@@_")
                _td_html = """
                <td>#{_td_p[1]}</td>
                <td>#{_td_p[2]}</td>
                """
                _i_list = []
                if items_info["class_type_max"]==4
                    _i_list = ["早班","中班","晚班","夜班"]
                else
                    _i_list = ["早班","中班","夜班"]

                for _i in _i_list
                    for j in [1..items_info["times_max"]]
                        if _items[_i][j] in [undefined,null,""]
                            _items[_i][j]=[]
                        
                        if _items[_i][j][i] in [undefined,null,""]
                            _td_html = """
                            #{_td_html}
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            """
                        else
                            item = _items[_i][j][i]
                            _t = formatDateMMDD(item[4]["wjd_data_time_date_timer"]*1000)
                            _t_s = formatDateAll(item[2]*1000)
                            _data = {}
                            for _d in item[4]["collect_data"]
                                _data[_d[0]]=_d[1]
                            _p = item[4]["wjd_data_pointer"].split("_@@_")
                            _name = item[4]["user_name"]
                            if _name not in _names_list
                                _names_list.push _name
                            _ct = item[4]["class_type_value"]
                            _pt = item[4]["wjd_data_pointer_times"]
                            _pt_need = _p[3]
                            _td_html = """
                            #{_td_html}
                            <td>#{_t}</td>
                            <td>#{_ct}</td>
                            <td>#{_pt}</td>
                            <td>#{_pt_need}</td>
                            <td>#{_data["CH4%"]}</td>
                            <td>#{_data["CO2%"]}</td>
                            <td>#{_data["COppm"]}</td>
                            <td>#{_data["温度°C"]}</td>
                            <td>#{_t_s}</td>
                            <td class="person_select_item" data-name="#{_name}">#{_name}</td>
                            """
                $(".test_table").append """
                <tr>#{_td_html}</tr>
                """
    else if sort_type in ["sort_time_point_ctv"]
        $(".has_data_date_list").append """
            <table class="test_table">
                <tr>
                    <th>点号</th>
                    <th>点名</th>
                    <th>时分</th>
                    <th>班次</th>
                    <th>采集次数</th>
                    <th>所需次数</th>
                    <th>CH4%</th>
                    <th>CO2%</th>
                    <th>COppm</th>
                    <th>温度°C</th>
                    <th>提交时间</th>
                    <th>瓦检工</th>
                </tr>
            </table>
            """
        for item in _data_now
            _t = formatDateMMDD(item[4]["wjd_data_time_date_timer"]*1000)
            _t_s = formatDateAll(item[2]*1000)
            _data = {}
            for _d in item[4]["collect_data"]
                _data[_d[0]]=_d[1]
            _p = item[4]["wjd_data_pointer"].split("_@@_")
            _name = item[4]["user_name"]
            if _name not in _names_list
                _names_list.push _name
            _ct = item[4]["class_type_value"]
            _pt = item[4]["wjd_data_pointer_times"]
            _pt_need = _p[3]
            if _ct not in [ctv]
                continue
            $(".test_table").append """
                <tr>
                    <td>#{_p[1]}</td>
                    <td>#{_p[2]}</td>
                    <td>#{_t}</td>
                    <td>#{_ct}</td>
                    <td>#{_pt}</td>
                    <td>#{_pt_need}</td>
                    <td>#{_data["CH4%"]}</td>
                    <td>#{_data["CO2%"]}</td>
                    <td>#{_data["COppm"]}</td>
                    <td>#{_data["温度°C"]}</td>
                    <td>#{_t_s}</td>
                    <td class="person_select_item" data-name="#{_name}">#{_name}</td>
                </tr>
            """
    else
        _company = $(".has_data_date_company").text()
        _y = $(".has_data_date_year").text()
        _m = $(".has_data_date_month").text()
        _d_str = $(".has_data_date_fix_title").text()
        _d_str_now = "未选择日期加载对应旬报"
        _d_str_start = ""
        if _d_str in ["上旬"]
            _d_str_now = "#{_y}年#{_m}月1-10日"
            _d_str_start = "1"
        else if _d_str in ["中旬"]
            _d_str_now = "#{_y}年#{_m}月11-20日"
            _d_str_start = "11"
        else if _d_str in ["下旬"]
            _fix=$(".has_data_date_select>option").length-1
            _d_str_now = "#{_y}年#{_m}月21-#{_fix}日"
            _d_str_start = "21"


        $(".has_data_date_list").append """
            <table class="test_table">
                <tr>
                    <th colspan="11">通风旬报表</th>
                </tr>
                <tr>
                    <th colspan="8" style="text-align:left;">单位: #{_company}</th>
                    <th colspan="3" style="text-align:left;">测定日期: #{_y}年#{_m}月<span class="xunbaoriqi">#{_d_str_start}</span>日</th>
                </tr>
                <tr>
                    <th rowspan="2">序号</th>
                    <th rowspan="2">测风地点</th>
                    <th rowspan="2">时分</th>
                    <th>断面</th>
                    <th>实际风速</th>
                    <th>实际风量</th>
                    <th colspan="2">瓦斯含量（%）</th>
                    <th rowspan="2">温度°C</th>
                    <th rowspan="2">提交时间</th>
                    <th rowspan="2">测风员</th>
                </tr>
                <tr>
                    <th>m<sup>2</sup></th>
                    <th>m/s</th>
                    <th>m<sup>3</sup>/min</th>
                    <th>CH<sub>4</sub></th>
                    <th>CO<sub>2</sub></th>
                </tr>
            </table>
            """
        for item in _data_now
            _t = formatDateMMDD(item[4]["wjd_data_time_date_timer"]*1000)
            _t_d = (new Date(item[4]["wjd_data_time_date_timer"]*1000)).getDate()
            if parseInt(_t_d) > parseInt(_d_str_start)
                _d_str_start = _t_d
                $(".xunbaoriqi").text _d_str_start
            _t_s = formatDateAll(item[2]*1000)
            _data = {}
            for _d in item[4]["collect_data"]
                _data[_d[0]]=_d[1]
            _p = item[4]["wjd_data_pointer"].split("_@@_")
            _name = item[4]["user_name"]
            if _name not in _names_list
                _names_list.push _name
            _ct = item[4]["class_type_value"]
            _pt = item[4]["wjd_data_pointer_times"]
            _pt_need = _p[3]
            $(".test_table").append """
                <tr>
                    <td>#{_p[1]}</td>
                    <td>#{_p[2]}</td>
                    <td>#{_t}</td>
                    <td>#{_data["断面m2"]}</td>
                    <td>#{_data["实际风速m/s"]}</td>
                    <td>#{_data["实际风量m3/min"]}</td>
                    <td>#{_data["瓦斯含量（%）CH4"]}</td>
                    <td>#{_data["瓦斯含量（%）CO2"]}</td>
                    <td>#{_data["温度°C"]}</td>
                    <td>#{_t_s}</td>
                    <td class="person_select_item" data-name="#{_name}">#{_name}</td>
                </tr>
            """
    $(".person_select").empty()
    for _name_item in _names_list
        $(".person_select").append """
        <button class="person_select_btn" data-name="#{_name_item}">#{_name_item}</button>
        """
$("body").on "click",".person_select_btn",(evt)->
    _name_now = $(this).attr("data-name")
    $(".person_select_item").parents("tr").hide()
    $(".person_select_item[data-name=\"#{_name_now}\"]").parents("tr").show()

root.wjd_data_date_load_view_all_table = (all_json,chat_id,comment_id=null)->
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
                    all_json = []
                    root.wjd_data_date_load_view_all_table_json = all_json
                    wjd_data_date_load_view_all_table_json_load()
                    return
            else if data.info == "ok"
                for comment in data.comments by -1
                    comment_json = null
                    try
                        comment_json = JSON.parse(comment[4])
                    catch e
                        comment_json = null
                    if comment_json!=null
                        if chat_id == comment_json["daily_comment_entity"]
                            all_json.push ["#{data.comment_id}_#{comment[0]}",comment[1],comment[2],comment[3],comment_json,comment[5],comment[6]]
                if data.last_comment_id == null
                    root.wjd_data_date_load_view_all_table_json = all_json
                    wjd_data_date_load_view_all_table_json_load()
                    return
                else
                    _comment_id = data.last_comment_id
                    wjd_data_date_load_view_all_table all_json,chat_id,_comment_id
        error:(data)->
            console.log data
$("body").on "change",".has_data_date_select",(evt)->
    _data_comment_id = current_plan_json["data_comment_id"]
    _wjd_date = $(".has_data_date_select").val()
    if _wjd_date == ""
        $(".has_data_date_daily_comment_entity").text "请确定旬报选择"
        $(".has_data_date_daily_comment_entity").removeAttr "data-daily-chat"
        return
    _wjd_date = parseInt(_wjd_date)
    # _wjd_date = "#{_wjd_date}"
    _page_id = wjd_plan_list_load_json[_data_comment_id]["json"]["page_id"]
    _comment_entity = wjd_plan_list_load_json[_data_comment_id]["json"]["comment_entity"]
    _wjd_company = wjd_plan_list_load_json[_data_comment_id]["json"]["wjd_company"]
    _wjd_year = wjd_plan_list_load_json[_data_comment_id]["json"]["wjd_year"]
    _wjd_month = wjd_plan_list_load_json[_data_comment_id]["json"]["wjd_month"]

    _daily_title_span = _wjd_date
    if _daily_title_span<=10
        _daily_title_span = "上旬"
    else if _daily_title_span<=20
        _daily_title_span = "中旬"
    else
        _daily_title_span = "下旬"
    $(".has_data_date_fix_title").text _daily_title_span
    _daily_title = "#{_wjd_company}_@@_#{_wjd_year}_@@_#{_wjd_month}_@@_#{_daily_title_span}"
    _daily_json =
        "daily_title": _daily_title
        "daily_comment_entity":null
        "daily_base_info":
            "page_id":_page_id
            "comment_entity":_comment_entity
            "data_comment_id":_data_comment_id
    wjd_data_date_load_view _daily_json,_comment_entity,null,(is_has,daily_comment_entity)->
        if is_has == true
            $(".has_data_date_daily_comment_entity").text daily_comment_entity
            $(".has_data_date_daily_comment_entity").attr "data-daily-chat",daily_comment_entity
            alert "已加载旬报存储区块"
            all_json = []
            wjd_data_date_load_view_all_table all_json,daily_comment_entity,null
            return
        else
            wjd_data_date_create_daily_comment_entity_view(_daily_json,_daily_json["daily_base_info"]["page_id"])

root.wjd_data_date_create_daily_comment_entity_view = (daily_json,page_id)->
    $.ajax
        url:"/api/page/add_comment_force"
        dataType:"json"
        type:"POST"
        data:
            block_id:page_id
        success:(data)->
            console.log data
            if data.info == "ok"
                daily_comment_entity = data.comment_entity
                $(".has_data_date_daily_comment_entity").text daily_comment_entity
                $(".has_data_date_daily_comment_entity").attr "data-daily-chat",daily_comment_entity
                daily_json["daily_comment_entity"]=daily_comment_entity
                wjd_data_date_comment_submit page_id,daily_json["daily_base_info"]["comment_entity"],JSON.stringify(daily_json),(data)->
                    alert "已加载旬报存储区块"
                    all_json = []
                    wjd_data_date_load_view_all_table all_json,daily_comment_entity,null
        error:(data)->
            console.log data

root.wjd_data_date_load_view = (daily_json,chat_id,comment_id=null,callback=null)->
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
                        callback(false,null)
                        return
            else if data.info == "ok"
                for comment in data.comments
                    comment_json = null
                    try
                        comment_json = JSON.parse(comment[4])
                    catch e
                        comment_json = null
                    if comment_json!=null
                        if daily_json["daily_title"] == comment_json["daily_title"]
                            callback(true,comment_json["daily_comment_entity"])
                            return
                if data.last_comment_id == null
                    callback(false,null)
                    return
                else
                    _comment_id = data.last_comment_id
                    wjd_data_date_load_view daily_json,chat_id,_comment_id,(is_has,daily_comment_entity)->
                        if is_has == true
                            $(".has_data_date_daily_comment_entity").text daily_comment_entity
                            $(".has_data_date_daily_comment_entity").attr "data-daily-chat",daily_comment_entity
                            alert "已加载旬报存储区块"
                            all_json = []
                            wjd_data_date_load_view_all_table all_json,daily_comment_entity,null
                            return
                        else
                            wjd_data_date_create_daily_comment_entity_view(daily_json,daily_json["daily_base_info"]["page_id"])
        error:(data)->
            console.log data




root.wjd_data_daily_submit_check_data = ()->
    _data_comment_id = current_plan_json["data_comment_id"]
    if _data_comment_id in ["",undefined,null]
        wjd_data_daily_submit_check_data_error "计划记录为空值"
        return
    _page_id = wjd_plan_list_load_json[_data_comment_id]["json"]["page_id"]
    if _page_id in ["",undefined,null]
        wjd_data_daily_submit_check_data_error "存储计划缺失"
        return
    _comment_entity = $(".wjd_comment_entity_submit").text()
    if _comment_entity in ["",undefined,null]
        wjd_data_daily_submit_check_data_error "存储区块缺失"
        return
    _daily_comment_entity = $(".wjd_date_comment_entity_submit").attr("data-daily-chat")
    if _daily_comment_entity in ["",undefined,null]
        wjd_data_daily_submit_check_data_error "旬报存储区块缺失"
        return
    _class_type = $(".wjd_date_class_type.is_current").attr("data-num")
    if _class_type in ["",undefined,null]
        wjd_data_daily_submit_check_data_error "班次类型未选择"
        return
    _class_type_value = $(".wjd_date_class_type_value.is_current").attr("data-name")
    if _class_type_value in ["",undefined,null]
        wjd_data_daily_submit_check_data_error "班次信息未选择"
        return
    _wjd_data_pointer = $(".wjd_data_pointer").val()
    if _wjd_data_pointer in ["",undefined,null]
        wjd_data_daily_submit_check_data_error "站点未选择"
        return
    _wjd_data_pointer_times = $(".wjd_data_pointer_times.is_current").attr("data-times")
    if _wjd_data_pointer_times in ["",undefined,null]
        wjd_data_daily_submit_check_data_error "站点对应次数未选择"
        return
    _wjd_data_time_date_timer = new Date($(".wjd_data_time_date").val())
    _wjd_data_time_date_timer.setHours($(".wjd_data_time_date_hour").val())
    _wjd_data_time_date_timer.setMinutes($(".wjd_data_time_date_minute").val())
    _wjd_data_time_date_timer = _wjd_data_time_date_timer.getTime()
    _user_id = USER_ID
    _user_name = $(".wjd_data_submit_name").val()
    if _user_name in ["",undefined,null]
        wjd_data_daily_submit_check_data_error "测风员姓名未填写"
        return
    _collect_data = []
    _collect_data_json = {}
    for item in $(".wjd_data_submit_data_v")
        _key = $(item).attr("data-key")
        _value = $(item).val()
        _collect_data.push [_key,_value]
        _collect_data_json[_key]=_value

        if _key not in ["瓦斯含量（%）CH4","瓦斯含量（%）CO2"]
            if _value in ["",undefined,null]
                wjd_data_daily_submit_check_data_error "#{_key}值未填写"
                return
        if $(".wjd_date_fix_title").text in ["下旬"]
            if _value in ["",undefined,null]
                wjd_data_daily_submit_check_data_error "#{_key}值未填写"
                return
    _comment_submit_data = 
        "page_id":_page_id
        "data_comment_id":_data_comment_id
        "comment_entity":_comment_entity
        "daily_comment_entity":_daily_comment_entity
        "class_type":_class_type
        "class_type_value":_class_type_value
        "wjd_data_pointer":_wjd_data_pointer
        "wjd_data_pointer_times":_wjd_data_pointer_times
        "wjd_data_time_date_timer":_wjd_data_time_date_timer/1000.0
        "user_name":_user_name
        "collect_data":_collect_data

    wjd_data_date_comment_submit _page_id,_daily_comment_entity,JSON.stringify(_comment_submit_data),(data)->
        if data.info == "ok"
            alert "提交成功"
            $(".wjd_data_submit_data_btn_save_log").text "提交成功"
            $(".wjd_data_submit_data_btn_save_log").show()
            $(".wjd_data_submit_data_btn_save").show()
            $(".wjd_data_pointer").val("")
            $(".wjd_data_submit_data_v").val("")
            a=localStorage.getItem("风速系数a")
            b=localStorage.getItem("风速系数b")
            $(".wjd_data_submit_data_v[data-key=\"风速系数a\"]").val(a)
            $(".wjd_data_submit_data_v[data-key=\"风速系数b\"]").val(b)

root.wjd_data_daily_submit_check_data_error=(alert_content)->
    alert alert_content
    $(".wjd_data_submit_data_btn_save_log").text alert_content
    $(".wjd_data_submit_data_btn_save").show()
    
$("body").on "click",".wjd_data_submit_data_btn_save",(evt)->
    $(".wjd_data_submit_data_btn_save_log").text "正在校验内容"
    $(".wjd_data_submit_data_btn_save_log").show()
    $(".wjd_data_submit_data_btn_save").hide()
    wjd_data_daily_submit_check_data()

$("body").on "click",".wjd_data_submit_data_v_calc",(evt)->
    e_vb = parseFloat($(".wjd_data_submit_data_v[data-key=\"测量表风速1\"]").val())+parseFloat($(".wjd_data_submit_data_v[data-key=\"测量表风速2\"]").val())+parseFloat($(".wjd_data_submit_data_v[data-key=\"测量表风速3\"]").val())
    a_vb = e_vb/3.0
    a = parseFloat($(".wjd_data_submit_data_v[data-key=\"风速系数a\"]").val())
    b = parseFloat($(".wjd_data_submit_data_v[data-key=\"风速系数b\"]").val())
    localStorage.setItem("风速系数a", a)
    localStorage.setItem("风速系数b", b)

    vn=(a*a_vb+b)/60.0
    s = parseFloat($(".wjd_data_submit_data_v[data-key=\"断面m2\"]").val())
    _fix_value = 0.4
    if $(".wjd_data_pointer").val().split("_@@_")[0] in ["硐室"]
        _fix_value = 0
    q=vn*(s-_fix_value)*60
    vn = parseFloat(vn).toFixed(2)
    q = parseFloat(q).toFixed(2)
    $(".wjd_data_submit_data_v[data-key=\"实际风速m/s\"]").val(vn)
    $(".wjd_data_submit_data_v[data-key=\"实际风量m3/min\"]").val(q)

</script>
<script src="/static/js/coffeescript.js"></script>
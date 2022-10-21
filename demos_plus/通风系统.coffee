<style>
.office_main_link{
    margin:10px;
    padding:20px 30px;
    font-size:20px;
    border-radius:8px;
    border:1px solid #999;
    color:#666;
    text-align:left;
}
</style>
<script type="text/coffeescript">
if window.location.href.indexOf("/home/page/edit")>-1
    $(".base_area").show()
else
    $(".base_area").hide()
    $("body").css "height","100%"

$(window).on "load",(evt)->
    if IS_EDITOR
        _setting_html = """
        <a href="/home/page/e97b9f49416f4190b3e1fb46d67dd118"><div class="office_main_link">📚月度需要风量计划</div></a>
        """
    else
        _setting_html = ""
    $("body").append """
    <div class="office_main_links">
        #{_setting_html}
        <a href="/home/page/e13bf3711987406b9fc2ff23337165d2"><div class="office_main_link">📝通风旬报表（填写）</div></a>
        <a href="/home/page/08aaa23f9cd64a1688d255200fdc6f46"><div class="office_main_link">🔍月度风量情况表</div></a>
    </div>
        """

</script>
<script src="/static/js/coffeescript.js"></script>
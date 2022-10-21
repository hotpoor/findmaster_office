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
        <a href="/home/page/fd035d6f297a4a30bd5384964c906dd3"><div class="office_main_link">📚瓦检点设置计划</div></a>
        """
    else
        _setting_html = ""
    $("body").append """
    <div class="office_main_links">
        #{_setting_html}
        <a href="/home/page/ae00db1d035c4827906103c604cd4f17"><div class="office_main_link">📝瓦斯班报表（填写）</div></a>
        <a href="/home/page/9a8b93d12ba448918dc5a7ba5358a985"><div class="office_main_link">🔍瓦斯日报表</div></a>
        <a href="/home/page/5ef0bd0aa06f4b50b276fddd2325a958"><div class="office_main_link">【文档】瓦斯检查制度（制度）</div></a>
        <a href="/home/page/32826fa9a41b4dec9e3aca47f7cfa20d"><div class="office_main_link">【文档】瓦斯鉴定报告要求（报告）</div></a>
        <a href="/home/page/6ac2a45237a94968921af8992b3eba60"><div class="office_main_link">【文档】瓦斯排放安全技术措施（提纲）</div></a>
        <a href="/home/page/dfab01bee77940b48556dc12acf666cf"><div class="office_main_link">【文档】矿井采掘工作面防治瓦斯安全技术措施</div></a>
        <a href="/home/page/7d0b1375a7894c719c3a8d9ba3689696"><div class="office_main_link">【文档】矿井停工停产期间安全技术措施（通防提纲）</div></a>
        <a href="/home/page/f5211fa2172a4fefa6f0325c769bc9fe"><div class="office_main_link">【文档】煤矿瓦斯治理技术方案及安全技术措施（提纲）</div></a>
        <a href="/home/page/daabc336960a49c0b2d6c1f56cb3de0d"><div class="office_main_link">【文档】瓦斯检查工交接班制度（提纲）</div></a>
    </div>
        """

</script>
<script src="/static/js/coffeescript.js"></script>
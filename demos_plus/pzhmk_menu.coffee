<style>
.btns_col{
    display:flex;
}
.btns_col_flex{
    flex:1;
}
.btn_sys{
    text-align:center;
    margin:10px;
    padding:15px;
    box-shadow:0px 2px 4px rgba(0,0,0,0.3);
    background-color:white;
    color:#666;
    border-radius:4px;
    font-size:14px;
    
}
</style>

<div class="btns_col">
    <div class="btns_col_flex">
        <a href="">
            <div class="btn_sys">通风系统</div>
        </a>
    </div>
    <div class="btns_col_flex">
        <a href="">
            <div class="btn_sys">监控系统</div>
        </a>
    </div>
    <div class="btns_col_flex">
        <a target="_blank" href="/home/page/e0b4d9f04ac34d5dab8fbdbf8d18e644">
            <div class="btn_sys">瓦斯管理</div>
        </a>
    </div>
</div>
<div class="btns_col">
    <div class="btns_col_flex">
        <a href="">
            <div class="btn_sys">粉尘系统</div>
        </a>
    </div>
    <div class="btns_col_flex">
        <a href="">
            <div class="btn_sys">防灭火系统</div>
        </a>
    </div>
    <div class="btns_col_flex">
        <a target="_blank" href="/home/pages">
            <div class="btn_sys">我的文件</div>
        </a>
    </div>
</div>
<script>
$(window).on("load",function(evt){
    if (USER_ID.indexOf("no_login")>-1){
        window.location.href = "/login?redirect_uri="+encodeURIComponent(window.location.href)
    }
})
</script>
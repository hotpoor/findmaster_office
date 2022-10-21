root = exports ? this
# !!!! Hotpoor root object
root.Hs or= {}
Hs = root.Hs

$ ->
    console.log "msh bangfer new coffee"
    $(window).on "load",(evt)->
        _w = $(".sharetimeline_ischool_card").width()
        $(".sharetimeline_ischool_card").append """
        <div class="msh_menus" style="
            color: #bfbfbf;     font-size: 12px;
            display:flex;       flex:3;
            position:fixed;     bottom:0px;
            width:#{_w}px;      height:50px;
            background:white;   box-shadow:0px -4px 4px -3px rgba(0,0,0,0.1);
            ">
            <div style="flex:1;text-align:center;cursor:pointer;">
                <a href="http://www.hotpoor.org/home/app/bangfer/028ee947c4ee4b3ea2927cccf8199976?v=msh&ischool_id=d35aee6e4e1f47ffbce49dba54b466a7" target="_blank">
                <img style="margin-top:6px;width:20px;20px;" src="http://msh-cdn0.xialiwei.com/41af9eed997d4871aff8b691196f48d1_44663bade6a9bd241f578c4e84a1712d?imageView2">
                <br><span style="color: #bfbfbf;">讨论</span>
                </a>
            </div>
            <div style="flex:1;text-align:center;cursor:pointer;">
                <a href="https://msh.xialiwei.com/home/page/7b4f5bc4b6694878b9f98a1f346ee647" target="_blank">
                <img style="margin-top:6px;width:20px;20px;" src="http://msh-cdn0.xialiwei.com/41af9eed997d4871aff8b691196f48d1_fea1af9d8826f03c77c374ae5dba8f70?imageView2">
                <br><span style="color: #bfbfbf;">新品速递</span>
                </a>
            </div>
            <div style="flex:1;text-align:center;cursor:pointer;">
                <a href="https://msh.xialiwei.com/home/page/1a158427afe543bda309c0c6ddce2cbf" target="_blank">
                <img style="margin-top:6px;width:20px;20px;" src="http://msh-cdn0.xialiwei.com/41af9eed997d4871aff8b691196f48d1_aed097ba3b821629d5a21c304420f9dd?imageView2">
                <br><span style="color: #bfbfbf;">我的会员</span>
                </a>
            </div>
        </div>
        """
        $.ajax
            url:"/api/user/login/get"
            data:null
            dataType: 'json'
            type: 'POST'
            success: (data) ->
                if data.login?
                    $.ajax
                        url:"https://www.moshanghua2020.net/api/msh/level/check"
                        data:
                            t:(new Date()).getTime()
                            openid:data.login.split("_@@_")[1]
                            app:"msh"
                        dataType: 'json'
                        type: 'GET'
                        success: (data) ->
                            console.log data
                            if data.info == "ok"
                                if parseInt(data.msh_qrcodepackage_num) > 0
                                    $(".sharetimeline_content_area").removeClass("hide")
                                    $(".sharetimeline_user_info").prepend """
                                    <div class="sharetimeline_user_name_level"
                                        style="
                                            position: absolute;
                                            right: 106px;
                                            margin-top: 60px;
                                            font-size: 14px;
                                            color: #408a9f;
                                            font-weight: bold;
                                        ">Level #{data.msh_qrcodepackage_num}</div>
                                    """
                            else
                                alert data.about   
                        error: (data) ->
                            console.log data
            error: (data) ->
                console.log data











root = exports ? this
# !!!! Hotpoor root object
root.Hs or= {}
Hs = root.Hs

$ ->
    console.log "dev qrcode"


    create_action = (time,times)->
        if time >= times
            return
        title = $(".title").val()
        subtype = $(".subtype").val()
        aim_id = $(".aim_id").val()
        num_each = parseInt($(".num_each").val())
        num_all = parseInt($(".num_all").val())
        $.ajax
            url:"/api/msh/create_block"
            data:
                title:title
                subtype:subtype
                aim_id:aim_id
                amount:num_all
            dataType: 'json'
            type: "POST"
            success:(data)->
                console.log data
                if data.info == "ok"
                    next_block_id = data.entity_id
                    $.ajax
                        url:"/api/msh/create_qrcode"
                        data:
                            block_id:next_block_id
                            num:num_each
                        dataType: 'json'
                        type: "POST"
                        success:(data)->
                            console.log data
                            if data.info == "ok"
                                create_action(time+1,times)
                        error:(data)->
                            console.log data
            error:(data)->
                console.log data

    $("body").on "click",".create_action",(evt)->
        title = $(".title").val()
        subtype = $(".subtype").val()
        aim_id = $(".aim_id").val()
        num_all = parseInt($(".num_all").val())
        num_each = parseInt($(".num_each").val())
        $(".times").val parseInt(num_all/num_each)
        times = $(".times").val()
        create_action(0,times)

    check_list_action = (check_list)->
        for item_id in check_list
            $.ajax
                url:"/api/data/json"
                data:
                    block_id:item_id
                dataType: 'json'
                type: "GET"
                success:(data)->
                    console.log data
                    if data.info == "ok"
                        if $(".qrcode_output_line[data-name=#{data.block.title}]").length == 0
                            $(".qrcode_output_list").append """
                                <table class="qrcode_output_line" data-name="#{data.block.title}"></table>
                            """
                        for a in data.block.qrcodes
                            $(".qrcode_output_line[data-name=#{data.block.title}]").append """
                                <tr><td><div>https://www.qianshanghua.com/api/msh/qrcode/#{data.block_id}/#{a}</div></td></tr>
                            """

                error:(data)->
                    console.log data

    $("body").on "click",".check_action",(evt)->
        check_aim_id = $(".check_aim_id").val()
        check_list = []
        $.ajax
            url:"/api/data/json"
            data:
                block_id:check_aim_id
            dataType: 'json'
            type: "GET"
            success:(data)->
                console.log data
                if data.info == "ok"
                    check_list = data.block.qrcodepackages
                    check_list_action(check_list)
            error:(data)->
                console.log data













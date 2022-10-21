root = exports ? this
# !!!! Hotpoor root object
root.Hs or= {}
Hs = root.Hs

$ ->
    console.log "dev dashboard"

    $("body").on "click",".submit",(evt)->
        dom = $(this)
        dom_tool = dom.parents(".tool")
        url = dom_tool.find("div>.url").val()
        type = dom_tool.find("div>.type").val()
        console.log url,type
        type = type.toLocaleUpperCase()
        data_json = dom_tool.find("div>.json").val()
        data_json = JSON.parse(data_json)
        $.ajax
            url:url
            data:data_json
            dataType: 'json'
            type: type
            success:(data)->
                console.log JSON.stringify(data)
                dom_tool.find(".request").append """
                    <div class="card_mini">#{JSON.stringify(data)}</div>
                """
            error:(data)->
                console.log data


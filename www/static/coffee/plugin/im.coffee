root = exports ? this
# !!!! Hotpoor root object
root.Hs or= {}
Hs = root.Hs

$ ->
    console.log "this is plugin im coffee"
    plugin_im_touch_id = null
    plugin_im_is_expanded = false
    plugin_im_is_expanding = false
    plugin_im_client_x = null
    plugin_im_client_y = null
    plugin_im_is_started = false
    plugin_im_is_moved = false
    plugin_im_start_x = null
    plugin_im_start_y = null
    plugin_im_max_offset = 0
    plugin_im_time = null
    plugin_im_r = 30
    plugin_im_w = window.innerWidth
    plugin_im_h = window.innerHeight
    plugin_im_min_x = plugin_im_r - 5
    plugin_im_max_x = plugin_im_w - plugin_im_min_x
    plugin_im_min_y = plugin_im_r + 5
    plugin_im_max_y = plugin_im_h - plugin_im_min_y
    
    plugin_im_x = plugin_im_max_x
    plugin_im_y = plugin_im_min_y + 80

    plugin_im_base_max_offset = 30 #触摸偏移的最大值 px
    plugin_im_base_max_period = 150 #触摸时间的最大值 ms
    plugin_im_base_z_index = 2147483647

    plugin_im_latest_room_ids = ["logo","logo1","logo2","logo3"]
    plugin_im_target_room_id = null
    plugin_im_max_rooms = 4

    plugin_im_html = """
        <div class="plugin_im_heads hide">
            <div class="plugin_im_head plugin_im_logo" data-im-room-id="logo"></div>
            <div class="plugin_im_head plugin_im_logo" data-im-room-id="logo1"></div>
            <div class="plugin_im_head plugin_im_logo" data-im-room-id="logo2"></div>
            <div class="plugin_im_head plugin_im_logo" data-im-room-id="logo3"></div>
        </div>
        
    """
    $("body").append plugin_im_html
    root.load_plugin_im_chats = ()->
        $.ajax
            url:"/api/plugin/im/chats"
            data:
                app: FINDMASTER_APP
            dataType: 'json'
            type: 'POST'
            success:(data)->
                console.log data
            error:(data)->
                console.log data
    $("body").on "click",".plugin_im_heads>.plugin_im_head",(e)->
        if e.timeStamp - plugin_im_time < plugin_im_base_max_period
            return
        console.log "plugin_im_heads plugin_im_head click plugin_im_is_expanded",plugin_im_is_expanded
        if plugin_im_is_expanded
            old_room_id = plugin_im_target_room_id
            plugin_im_target_room_id = $(this).attr("data-im-room-id")
            if old_room_id == plugin_im_target_room_id
                onHeadsClickWhenExpanded()

    root.plugin_im_run =()->
        $(".plugin_im_heads").removeClass("hide")
        onHeadsMoveEnd()
    $(window).on "load",(e)->
        plugin_im_run()

    root.moveHeads = (_x, _y)->
        els = []
        num = 0
        for i in plugin_im_latest_room_ids
            el = $(".plugin_im_heads").children("[data-im-room-id=#{i}]")[0]
            el.style.zIndex = plugin_im_base_z_index - num
            num +=1
            els.push el
            console.log "moveHeads plugin_im_latest_room_ids",el
        _callLater els, (el, index)->
            setTransform el, _x + 4 * index, _y
        plugin_im_x = _x
        plugin_im_y = _y
    root.moveHeadsTogether =(_x, _y)->
        els = []
        num = 0
        for i in plugin_im_latest_room_ids
            el = $(".plugin_im_heads").children("[data-im-room-id=#{i}]")[0]
            el.style.zIndex = plugin_im_base_z_index - num
            els.push el
            num +=1
            setTransform el, _x + 4 * i, _y
        plugin_im_x = _x
        plugin_im_y = _y

    root.onHeadsMoveEnd = ()->
        els = []
        num = 0
        for i in plugin_im_latest_room_ids
            el = $(".plugin_im_heads").children("[data-im-room-id=#{i}]")[0]
            el.style.zIndex = plugin_im_base_z_index - num
            els.push el
            num +=1
        _callLater els,(el,index)->
            console.log "onHeadsMoveEnd plugin_im_latest_room_ids",el
            $(el).addClass("transition")
            setTransform el, collapsedX(index), collapsedY(index)
        plugin_im_x = plugin_im_max_x

    root.setTransform = (el, x, y)->
        value = 'translate3d(' + x + 'px,' + y + 'px,0)'
        el.style.transform = value
        el.style.webkitTransform = value
    root.collapsedX =(i)->
        return plugin_im_max_x + 4 * i
    root.collapsedY =(i)->
        return plugin_im_y

    root.expandedX =(i)->
        return plugin_im_w - plugin_im_r * (2 * i + 1) - 5 * (i + 1)

    root.expandedY =(i)->
        return plugin_im_r + 10

    root._requestFrame = (n, callback)->
        if n > 0
            requestAnimationFrame ()->
                _requestFrame n-1, callback
        else if n == 0
            callback()
    root._callLater = (els, callback)->
        len = els.length
        if len
            _call = (i)->
                callback els[i], i
                i += 1
                if i < len
                    _requestFrame 3, ()->
                        _call i
            _call 0
    root.onHeadsClickWhenCollapsed = ()->
        for el in $(".plugin_im_heads").children()
            $(el).addClass("transition")
        if not plugin_im_is_expanded
            plugin_im_is_expanded = true
            plugin_im_target_room_id = plugin_im_latest_room_ids[0]
            $(".plugin_im_heads").addClass("expanded")
            setHeadsStyleExpanded()
    root.onHeadsClickWhenExpanded = ()->
        for el in $(".plugin_im_heads").children()
            $(el).addClass("transition")
        if plugin_im_is_expanded
            plugin_im_is_expanded = false
            plugin_im_target_room_id = plugin_im_latest_room_ids[0]
            $(".plugin_im_heads").removeClass("expanded")
            setHeadsStyleCollapsed()

    root.setHeadsStyleCollapsed =()->
        console.log "收起"
        num = 0
        for i in plugin_im_latest_room_ids
            el = $(".plugin_im_heads").children("[data-im-room-id=#{i}]")[0]
            el.style.zIndex = plugin_im_base_z_index - num
            setTransform el, collapsedX(num),collapsedY(num)
            num +=1

    root.setHeadsStyleExpanded =()->
        console.log "展开"
        num = 0
        for i in plugin_im_latest_room_ids
            el = $(".plugin_im_heads").children("[data-im-room-id=#{i}]")[0]
            el.style.zIndex = plugin_im_base_z_index - num
            setTransform el, expandedX(num),expandedY(num)
            num +=1
    $(window).on "resize",(e)->
        old_h = plugin_im_h
        plugin_im_w = window.innerWidth
        plugin_im_h = window.innerHeight
        plugin_im_max_x = plugin_im_w - plugin_im_min_x
        plugin_im_max_y = plugin_im_h - plugin_im_min_y
        plugin_im_x = plugin_im_max_x
        plugin_im_y = plugin_im_y / old_h * plugin_im_h
        if plugin_im_is_expanded
            setHeadsStyleExpanded()
        else
            setHeadsStyleCollapsed()

    if window.navigator.userAgent.indexOf("Mobile")>-1
        console.log "Mobile"
        $(".plugin_im_heads").on "touchstart",(e)->
            console.log "plugin_im_heads touchstart"
            if not plugin_im_is_expanded
                console.log "plugin_im_heads touchstart plugin_im_is_expanded",plugin_im_is_expanded
                e.stopPropagation()
                e.preventDefault()
                plugin_im_is_started = true
                plugin_im_is_moved = false
                plugin_im_max_offset = 0
                plugin_im_time = e.timeStamp
                touch = e.originalEvent.targetTouches[0]
                plugin_im_touch_id = touch.identifier
                plugin_im_client_x = touch.clientX
                plugin_im_client_y = touch.clientY
                plugin_im_start_x = plugin_im_client_x
                plugin_im_start_y = plugin_im_client_y
                els = $(".plugin_im_heads").children()
                for el in els
                    $(el).removeClass("transition")
        $(window).on "touchmove",(e)->
            if not plugin_im_is_expanded
                console.log "plugin_im_heads window touchmove plugin_im_is_expanded",plugin_im_is_expanded
                if plugin_im_is_started
                    # e.preventDefault()
                    plugin_im_is_moved = true
                    touch = e.originalEvent.targetTouches[0]
                    if touch.identifier == plugin_im_touch_id
                        x = touch.clientX
                        y = touch.clientY
                        if Math.abs(x - plugin_im_start_x) > plugin_im_max_offset
                            plugin_im_max_offset = Math.abs(x - plugin_im_start_x)
                        if Math.abs(y - plugin_im_start_y) > plugin_im_max_offset
                            plugin_im_max_offset = Math.abs(y - plugin_im_start_y)
                        dx = x - plugin_im_client_x
                        dy = y - plugin_im_client_y
                        plugin_im_client_x = x
                        plugin_im_client_y = y
                        _x = plugin_im_x + dx
                        _y = plugin_im_y + dy
                        console.log "_x,_y",_x,_y
                        if _y < plugin_im_min_y
                            _y = plugin_im_min_y
                            onHeadsMoveEnd()
                            isStarted = false
                        else if _y > plugin_im_max_y
                            _y = plugin_im_max_y
                            onHeadsMoveEnd()
                            isStarted = false
                        else
                            if plugin_im_max_offset > plugin_im_base_max_offset
                                moveHeads _x, _y
                            else
                                moveHeadsTogether _x, _y
        $(window).on "touchend",(e)->
            if not plugin_im_is_expanded
                if plugin_im_is_started
                    plugin_im_is_started = false
                    plugin_im_is_moved = true

                    if e.timeStamp - plugin_im_time < plugin_im_base_max_period and plugin_im_max_offset < plugin_im_base_max_offset
                        plugin_im_is_moved = false
                    console.log "plugin_im_heads window touchend plugin_im_is_expanded plugin_im_is_moved",plugin_im_is_expanded,plugin_im_is_moved
                    if not plugin_im_is_moved
                        onHeadsClickWhenCollapsed()
                    else
                        onHeadsMoveEnd()
    else
        console.log "Desktop pc"
        $(".plugin_im_heads").on "mousedown",(e)->
            console.log "plugin_im_heads touchstart"
            if not plugin_im_is_expanded
                console.log "plugin_im_heads mousedown plugin_im_is_expanded",plugin_im_is_expanded
                e.stopPropagation()
                e.preventDefault()
                plugin_im_is_started = true
                plugin_im_is_moved = false
                plugin_im_max_offset = 0
                plugin_im_time = e.timeStamp
                # touch = e.originalEvent.targetTouches[0]
                touch = e
                # plugin_im_touch_id = touch.identifier
                plugin_im_client_x = touch.clientX
                plugin_im_client_y = touch.clientY
                plugin_im_start_x = plugin_im_client_x
                plugin_im_start_y = plugin_im_client_y
                els = $(".plugin_im_heads").children()
                for el in els
                    $(el).removeClass("transition")
        $(window).on "mousemove",(e)->
            if not plugin_im_is_expanded
                console.log "plugin_im_heads window mousemove plugin_im_is_expanded",plugin_im_is_expanded
                if plugin_im_is_started
                    # e.preventDefault()
                    plugin_im_is_moved = true
                    # touch = e.originalEvent.targetTouches[0]
                    touch = e
                    # if touch.identifier == plugin_im_touch_id
                    if true
                        x = touch.clientX
                        y = touch.clientY
                        if Math.abs(x - plugin_im_start_x) > plugin_im_max_offset
                            plugin_im_max_offset = Math.abs(x - plugin_im_start_x)
                        if Math.abs(y - plugin_im_start_y) > plugin_im_max_offset
                            plugin_im_max_offset = Math.abs(y - plugin_im_start_y)
                        dx = x - plugin_im_client_x
                        dy = y - plugin_im_client_y
                        plugin_im_client_x = x
                        plugin_im_client_y = y
                        _x = plugin_im_x + dx
                        _y = plugin_im_y + dy
                        console.log "_x,_y",_x,_y
                        if _y < plugin_im_min_y
                            _y = plugin_im_min_y
                            onHeadsMoveEnd()
                            isStarted = false
                        else if _y > plugin_im_max_y
                            _y = plugin_im_max_y
                            onHeadsMoveEnd()
                            isStarted = false
                        else
                            if plugin_im_max_offset > plugin_im_base_max_offset
                                moveHeads _x, _y
                            else
                                moveHeadsTogether _x, _y
        $(window).on "mouseup",(e)->
            if not plugin_im_is_expanded
                if plugin_im_is_started
                    plugin_im_is_started = false
                    plugin_im_is_moved = true

                    if e.timeStamp - plugin_im_time < plugin_im_base_max_period and plugin_im_max_offset < plugin_im_base_max_offset
                        plugin_im_is_moved = false
                    console.log "plugin_im_heads window mouseup plugin_im_is_expanded plugin_im_is_moved",plugin_im_is_expanded,plugin_im_is_moved
                    if not plugin_im_is_moved
                        onHeadsClickWhenCollapsed()
                    else
                        onHeadsMoveEnd()



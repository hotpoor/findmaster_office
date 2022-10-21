root = exports ? this
# !!!! Hotpoor root object
root.Hs or= {}
Hs = root.Hs

$ ->
    console.log "msh hollow"

    $("body").on "click",".login_scan_submit",(evt)->
        $.ajax
            url:"/api/login_scan/submit"
            data:
                app: FINDMASTER_APP
                room_id:LOGIN_SCAN_ROOM_ID
                user_id:LOGIN_SCAN_USER_ID
                uuid:LOGIN_SCAN_UUID
                uuid_now:uuid2(6,null)
            dataType: 'json'
            type: 'POST'
            success:(data)->
                console.log data
                if data.info == "ok"
                    if IS_WEIXIN
                        root.close_window()
                    else
                        window.opener = null
                        window.open('','_self')
                        window.close()

            error:(data)->
                console.log data


    $("body").on "click",".login_scan_close",(evt)->
        if IS_WEIXIN
            root.close_window()
        else
            window.opener = null
            window.open('','_self')
            window.close()
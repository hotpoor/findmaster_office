root = exports ? this
root.Hs or= {}
Hs = root.Hs
$ ->
    root.page_edit_qrcode_img_load = (url=null)->
        $(".block_qrcode_area_div_canvas").empty()
        $(".block_qrcode_area_div_canvas").qrcode url
        $(".block_qrcode_area_div>img").attr "src", $(".block_qrcode_area_div_canvas>canvas").first()[0].toDataURL()

    $(window).on "load",(evt)->
        root.page_edit_qrcode_img_load window.location.href
    $("body").on "click",".qrcode_select_btn",(evt)->
        $(".qrcode_select_btn").removeClass("qrcode_select_btn_current")
        dom = $(this)
        dom.addClass("qrcode_select_btn_current")
        if dom.hasClass("edit_qrcode")
            _url = window.location.href
            console.log "edit_qrcode",_url
            root.page_edit_qrcode_img_load _url
        else if dom.hasClass("page_qrcode")
            _url = window.location.href.replace("/home/page/edit","/home/page")
            console.log "page_qrcode",_url
            root.page_edit_qrcode_img_load _url
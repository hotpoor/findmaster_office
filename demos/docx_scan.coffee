
for i in $(".dom_scroll_relative")
    do (i)->
        setTimeout ()->
            $(i).find(".text_align_left")[0].click()
        ,1000
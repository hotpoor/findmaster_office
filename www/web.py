#!/bin/env python
#!/bin/env python
#coding=utf-8
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/vendor/')
#os.chdir(os.path.dirname(os.path.abspath(__file__)))
import ssl
import time

import tornado.options
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template
import tornado.auth
import tornado.locale
from tornado import gen
from tornado.escape import json_encode, json_decode

from setting import settings
from setting import conn

from controller import auth
from controller import findmaster
from controller import findmaster_permission
from controller import findmaster_file
from controller import findmaster_tool
from controller import findmaster_fork
from controller import findmaster_comment
from controller import findmaster_agora
from controller import findmaster_msh
from controller import findmaster_msh_hollow
from controller import findmaster_auth
from controller import findmaster_dev

from controller import findmaster_hollow
from controller import findmaster_user

from controller import findmaster_office

from controller import findmaster_store
from controller import findmaster_stripe
from controller import findmaster_search

from controller import data
from controller import weixin
from controller import weixin_customservice
# from controller import findmaster_pay


from controller import findmaster_winni_app

tornado.httpclient.AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")

application = tornado.web.Application([
    (r"/home/main",findmaster.MainHomeHandler),
    (r"/home/welcome",findmaster.WelcomeHomeHandler),

    # (r"/login",findmaster.LoginHandler),
    # (r"/register",findmaster.RegisterHandler),

    (r"/home/pages",findmaster.PagesHomeHandler),
    # (r"/home/page/fix/(.*)",findmaster.PageFixHomeHandler),
    (r"/home/page/edit/(.*)",findmaster.PageEditHomeHandler),
    (r"/home/page/(.*)",findmaster.PageHomeHandler),

    (r"/api/pages/list",findmaster.PagesListAPIHandler),

    (r"/api/page/add_free_pdf",findmaster.PageAddFreePdfAPIHandler),
    (r"/api/page/add_free_docx",findmaster.PageAddFreeDocxAPIHandler),
    (r"/api/page/add_free",findmaster.PageAddFreeAPIHandler),
    (r"/api/page/add_dom",findmaster.PageAddDomAPIHandler),
    (r"/api/page/add",findmaster.PageAddAPIHandler),
    (r"/api/page/copy_doms",findmaster.PageCopyDomsAPIHandler),
    (r"/api/page/copy_dom",findmaster.PageCopyDomAPIHandler),
    (r"/api/page/del_dom",findmaster.PageDelDomAPIHandler),
    (r"/api/page/update_title",findmaster.PageUpdateTitleAPIHandler),
    (r"/api/page/update_desc",findmaster.PageUpdateDescAPIHandler),
    (r"/api/page/update_headimgurl",findmaster.PageUpdateHeadimgurlAPIHandler),
    (r"/api/page/update_grid_graph",findmaster.PageUpdateGridGraphAPIHandler),
    (r"/api/page/update_main_area",findmaster.PageUpdateMainAreaAPIHandler),
    (r"/api/page/update_doms",findmaster.PageUpdateDomsAPIHandler),
    (r"/api/page/update_dom_video",findmaster.PageUpdateDomVideoAPIHandler),
    (r"/api/page/update_dom_file",findmaster.PageUpdateDomFileAPIHandler),
    (r"/api/page/update_dom_content",findmaster.PageUpdateDomContentAPIHandler),
    (r"/api/page/update_dom_iframe",findmaster.PageUpdateDomIframeAPIHandler),
    (r"/api/page/update_dom",findmaster.PageUpdateDomAPIHandler),

    # public publish private
    (r"/api/page/set_permission",   findmaster_permission.PageSetPermissionAPIHandler),
    (r"/api/page/editors",          findmaster_permission.PageEditorsAPIHandler),
    (r"/api/page/readers",          findmaster_permission.PageReadersAPIHandler),
    (r"/api/page/members",          findmaster_permission.PageMembersAPIHandler),
    (r"/api/page/blackers",         findmaster_permission.PageBlackersAPIHandler),
    (r"/api/page/rules",            findmaster_permission.PageRulesAPIHandler),
    (r"/api/page/add_editor",       findmaster_permission.PageAddEditorAPIHandler),
    (r"/api/page/del_editor",       findmaster_permission.PageDelEditorAPIHandler),
    (r"/api/page/add_reader",       findmaster_permission.PageAddReaderAPIHandler),
    (r"/api/page/del_reader",       findmaster_permission.PageDelReaderAPIHandler),
    (r"/api/page/add_blacker",      findmaster_permission.PageAddBlackerAPIHandler),
    (r"/api/page/del_blacker",      findmaster_permission.PageDelBlackerAPIHandler),

    (r"/api/page/hollows",          findmaster_hollow.PageHollowsAPIHandler),
    (r"/api/page/add_hollow",      findmaster_hollow.PageAddHollowAPIHandler),
    (r"/api/page/del_hollow",      findmaster_hollow.PageDelHollowAPIHandler),

    (r"/api/image/check",   findmaster_file.ImageCheckAPIHandler),
    (r"/api/image/change",  findmaster_file.ImageChangeAPIHandler),
    (r"/api/image/add",     findmaster_file.ImageAddAPIHandler),
    (r"/api/image/del",     findmaster_file.ImageDelAPIHandler),

    (r"/api/video/check",   findmaster_file.VideoCheckAPIHandler),
    (r"/api/video/change",  findmaster_file.VideoChangeAPIHandler),
    (r"/api/video/add",     findmaster_file.VideoAddAPIHandler),
    (r"/api/video/del",     findmaster_file.VideoDelAPIHandler),

    (r"/api/file/check",   findmaster_file.FileCheckAPIHandler),
    (r"/api/file/change",  findmaster_file.FileChangeAPIHandler),
    (r"/api/file/add",     findmaster_file.FileAddAPIHandler),
    (r"/api/file/del",     findmaster_file.FileDelAPIHandler),

    (r"/api/page/count_connect_num",findmaster_tool.CountConnectNumAPIHandler),
    (r"/api/page/count_connect_num_list",findmaster_tool.CountConnectNumListAPIHandler),
    (r"/api/page/fork",findmaster_fork.ForkPageAPIHandler),
    (r"/api/page/add_to_top",findmaster_tool.AddToTopPageAPIHandler),
    (r"/api/page/remove_from_top",findmaster_tool.RemoveFromTopPageAPIHandler),
    (r"/api/page/remove_to_trash",findmaster_tool.RemoveToTrashAPIHandler),

    (r"/api/page/add_comment_force",findmaster_comment.AddCommentForceAPIHandler),
    (r"/api/page/add_comment",findmaster_comment.AddCommentAPIHandler),
    (r"/api/page/get_comment",findmaster_comment.GetCommentAPIHandler),
    (r"/api/page/comment/submit",findmaster_comment.CommentSubmitAPIHandler),
    (r"/api/page/comment/load",findmaster_comment.CommentLoadAPIHandler),
    (r"/api/page/comment/load_one",findmaster_comment.CommentLoadOneAPIHandler),

    (r"/api/page/comment/remark",       findmaster_comment.RemarkAPIHandler),
    (r"/api/page/comment/remark_del",   findmaster_comment.RemarkDelAPIHandler),
    (r"/api/page/comment/like",         findmaster_comment.LikeAPIHandler),
    (r"/api/page/comment/ref",          findmaster_comment.RefAPIHandler),
    (r"/api/page/comment/ref_add",      findmaster_comment.RefAddAPIHandler),
    (r"/api/page/comment/del",          findmaster_comment.DelAPIHandler),

    

    (r"/api/page/agora/get_token",findmaster_agora.GetTokenAPIHandler),
    (r"/api/page/agora/get_customer_token",findmaster_agora.GetCustomerTokenAPIHandler),


    (r"/api/user/get_user_plus_info",findmaster_user.GetUserPlusInfoAPIHandler),
    (r"/api/user/update_user_plus_info",findmaster_user.UpdateUserPlusInfoAPIHandler),

    (r"/api/user/get_user_info",findmaster_user.GetUserInfoAPIHandler),
    (r"/api/user/get_user_token_count",findmaster_user.GetUserTokenCountAPIHandler),
    (r"/api/user/check_daily",findmaster_user.CheckDailyAPIHandler),

    (r"/api/weixin/show_access_token",weixin.ShowAccessTokenAPIHandler),
    (r"/api/weixin/get_weixin_user_info",weixin.GetWeixinUserInfoAPIHandler),

    (r"/api/weixin/server",weixin.ServerWeixinAPIHandler),
    (r"/api/weixin/show_batchget_material",weixin.ShowBatchgetMaterialAPIHandler),

    (r"/api/weixin/customservice/kfsession/create",weixin_customservice.KfsessionCreateAPIHandler),
    (r"/api/weixin/customservice/kfsession/close",weixin_customservice.KfsessionCloseAPIHandler),
    (r"/api/weixin/customservice/msgrecord/getmsglist",weixin_customservice.MsgrecordGetmsgListAPIHandler),

    #阡上花
    (r"/home/start",findmaster_office.StartHandler),
    (r"/home/office",findmaster_office.HomeHandler),
    (r"/api/office/add_folder",findmaster_office.OfficeAddFolderAPIHandler),
    (r"/api/office/add_page",findmaster_office.OfficeAddPageAPIHandler),
    (r"/api/office/list",findmaster_office.OfficeListAPIHandler),
    (r"/api/office/block_infos",findmaster_office.BlockInfosAPIHandler),
    (r"/api/office/update_info",findmaster_office.UpdateInfoAPIHandler),

    #陌生花
    (r"/home/dev/dashboard",findmaster_dev.DashboardHandler),
    (r"/home/dev/qrcode",findmaster_dev.QrcodeHandler),
    (r"/api/msh/create_block",findmaster_msh.CreateBlockAPIHandler),
    (r"/api/msh/set_block_redirect",findmaster_msh.SetBlockRedirectAPIHandler),
    (r"/api/msh/create_qrcode",findmaster_msh.CreateQrcodeAPIHandler),
    (r"/api/msh/qrcode/check",findmaster_msh.QrcodeCheckAPIHandler),
    (r"/api/msh/qrcode/(.*)/(.*)",findmaster_msh.QrcodeAPIHandler),

    (r"/api/msh/level/check",findmaster_msh.CheckLevelAPIHandler),

    (r"/home/msh/hollow/(.*)",findmaster_msh_hollow.HomeEntityHandler),
    (r"/home/msh/hollow",findmaster_msh_hollow.HomeHandler),
    (r"/api/msh/hollow/list",findmaster_msh_hollow.ListAPIHandler),
    (r"/api/msh/hollow/search",findmaster_msh_hollow.SearchAPIHandler),
    (r"/api/msh/hollow/follow",findmaster_msh_hollow.FollowAPIHandler),
    (r"/api/msh/hollow/topic_list",findmaster_msh_hollow.TopicListAPIHandler),
    (r"/api/msh/hollow/topic_update",findmaster_msh_hollow.TopicRemoveAPIHandler),

    (r"/api/login_scan/submit",findmaster_auth.SubmitLoginScanAPIHandler),
    (r"/api/login_scan/confirm",findmaster_auth.ConfirmLoginScanAPIHandler),
    (r"/home/login_scan",findmaster_auth.LoginScanHandler),

    (r"/api/tool/connect_list",findmaster_tool.ListConnectAPIHandler),
    (r"/api/tool/wechat/login_silence",findmaster_tool.LoginSilenceWechatAPIHandler),

    (r"/home/store/user/(.*)",      findmaster_store.UserEntityHandler),
    (r"/home/store/shop/(.*)",      findmaster_store.ShopEntityHandler),
    (r"/home/store/product/(.*)/(.*)",   findmaster_store.ProductEntityHandler),
    (r"/home/store/order/(.*)",     findmaster_store.OrderEntityHandler),
    (r"/home/store/hollow/(.*)",    findmaster_store.HollowEntityHandler),

    (r"/home/store/ground",         findmaster_store.GroundHandler),
    (r"/home/store/search",         findmaster_store.SearchHandler),
    (r"/home/store/hollow",         findmaster_store.HollowHandler),

    (r"/home/store/app/user",           findmaster_winni_app.UserAppStoreHomeHandler),
    (r"/home/store/app/seller",         findmaster_winni_app.SellerAppStoreHomeHandler),
    (r"/api/store/app/shop/create",     findmaster_winni_app.CreateShopAppStoreAPIHandler),
    (r"/home/store/app/shop/(.*)",      findmaster_winni_app.ShopAppStoreHomeHandler),

    (r"/api/store/app/stripe/login_link",   findmaster_winni_app.LoginLinkStripeAppStoreAPIHandler),
    (r"/api/store/app/stripe/retrieve",     findmaster_winni_app.RetrieveStripeShopAppStoreAPIHandler),

    # (r"/home/store/app/product/(.*)",   findmaster_winni_app.ProductAppStoreHomeHandler),
    # (r"/home/store/app/order/(.*)",    findmaster_winni_app.OrderAppStoreHomeHandler),


    (r"/home/store/dashboard", findmaster_winni_app.DashboardStoreHomeHandler),#WORK
    (r"/api/store/info",        findmaster_store.InfoStoreAPIHandler),
    (r"/api/store/list",        findmaster_store.ListStoreAPIHandler),
    (r"/api/store/add",         findmaster_store.AddStoreAPIHandler),
    (r"/api/store/change",      findmaster_store.ChangeStoreAPIHandler),
    (r"/api/store/open",        findmaster_store.OpenStoreAPIHandler),
    (r"/api/store/close",       findmaster_store.CloseStoreAPIHandler),

    (r"/api/stripe/account/list",findmaster_stripe.AccountListAPIHandler),#WORK
    (r"/api/stripe/account/retrieve",findmaster_stripe.AccountRetrieveAPIHandler),#WORK
    (r"/api/stripe/account/add_link",findmaster_stripe.AccountAddLinkAPIHandler),#WORK
    (r"/api/stripe/account/add",findmaster_stripe.AccountAddAPIHandler),#WORK

    (r"/api/stripe/account/update",findmaster_stripe.AccountUpdateAPIHandler),

    (r"/api/stripe/create_account_link",findmaster_stripe.CreateAccountLinkAPIHandler),
    (r"/api/stripe/create_account",findmaster_stripe.CreateAccountAPIHandler),
    (r"/api/stripe/retrieve_account",findmaster_stripe.RetrieveAccountAPIHandler),
    (r"/api/stripe/create_login_link",findmaster_stripe.CreateLoginLinkAPIHandler),

    (r"/api/stripe/pay_create",findmaster_stripe.PayCreateAPIHandler),
    (r"/api/stripe/pay_product",findmaster_stripe.PayProductAPIHandler),
    (r"/api/stripe/hold_product",findmaster_stripe.HoldProductAPIHandler),
    (r"/api/stripe/hold_product_capture",findmaster_stripe.HoldProductCaptureAPIHandler),
    (r"/api/stripe/hold_product_cancel",findmaster_stripe.HoldProductCancelAPIHandler),

    (r"/api/stripe/pay_one_check",findmaster_stripe.PayOneCheckAPIHandler),
    (r"/api/stripe/pay_one_success",findmaster_stripe.PayOneSuccessAPIHandler),

    (r"/api/stripe/webhook",findmaster_stripe.WebhookAPIHandler),
    (r"/api/stripe/latest_webhook",findmaster_stripe.LatestWebhookAPIHandler),
    (r"/api/stripe/pay_success",findmaster_stripe.PaySuccessAPIHandler),
    (r"/api/stripe/pay_cancel",findmaster_stripe.PayCancelAPIHandler),


    #支付API
    # (r"/api/pay/weixin/unified" ,findmaster_pay.UnifiedWeixinAPIHandler),
    # (r"/api/pay/weixin/callback/(.*)",findmaster_pay.CallbackWeixinAPIHandler),

    # (r"/api/pay/alipay/unified_plus" ,findmaster_pay.UnifiedPlusAlipayAPIHandler),
    # (r"/api/pay/alipay/notify/(.*)/(.*)",findmaster_pay.NotifyAlipayAPIHandler),

    # (r"/start",auth.StartHomeHandler),

    (r"/api/search/add_free_page", findmaster_search.SearchAddFreePageAPIHandler),
    (r"/api/search/add_free", findmaster_search.SearchAddFreeAPIHandler),
    (r"/api/search/add", findmaster_search.SearchAddAPIHandler),
    (r"/api/search/list_more", findmaster_search.SearchListMoreAPIHandler),
    (r"/api/search/list_force", findmaster_search.SearchListForceAPIHandler),
    (r"/api/search/list", findmaster_search.SearchListAPIHandler),
    

    (r"/api/data/ws",data.DataWebSocket),

    (r"/api/data/json",findmaster_tool.JsonDataAPIHandler),

    (r"/api/register",auth.RegisterAPIHandler),
    (r"/api/login",auth.LoginAPIHandler),
    (r"/api/logout",auth.LogoutAPIHandler),
    (r"/logout",auth.LogoutHandler),
    (r"/api/get_vcode",auth.GetVcodeAPIHandler),
    (r"/api/reset_password",auth.ResetPasswordAPIHandler),
    (r"/api/get_login",auth.GetLoginAPIHandler),


    # (r"/(.*)", findmaster.MainHandler),
    (r"/(.*)", findmaster.UriMappingHandler),
    ],**settings)

if __name__ == "__main__":
    tornado.options.define("port", default=8100, help="Run server on a specific port", type=int)
    tornado.options.parse_command_line()

    i18n_path = os.path.join(os.path.dirname(__file__), "locales")
    # tornado.locale.load_gettext_translations(i18n_path, 'en_US')
    tornado.locale.load_translations(i18n_path)
    tornado.locale.set_default_locale('zh_CN')

    application_server = tornado.httpserver.HTTPServer(application, xheaders=True)
    application_server.listen(tornado.options.options.port)
    application_server.start()
    tornado.ioloop.IOLoop.instance().start()

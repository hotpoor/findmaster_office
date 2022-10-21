#!/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import os.path

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/vendor/')

import re
import uuid
import time
import random
import string
import hashlib
import urllib
import urllib.parse
import copy
from functools import partial
import logging
import datetime

import markdown
import tornado
import tornado.web
import tornado.escape
import tornado.websocket
import tornado.httpclient
import tornado.gen
from tornado.escape import json_encode, json_decode

import nomagic
import nomagic.auth
import nomagic.block
from nomagic.cache import get_user, get_users, update_user, get_doc, get_docs, update_doc, get_aim, get_aims, update_aim, get_entity, get_entities, update_entity
from nomagic.cache import BIG_CACHE
from setting import settings
from setting import conn

# from user_agents import parse as uaparse #早年KJ用来判断设备使用

from .base import WebRequest
from .base import WebSocket
import pymail
from .weixin import WeixinJSSDKSign
from .weixin import weixin_JS_SDK_check
from .weixin import weixin_access_token_for_apps

from .data import DataWebSocket

class LoginScanHandler(WebRequest):
    @tornado.gen.coroutine
    def get(self):
        login_scan_room_id = self.get_argument("room_id",None)
        login_scan_user_id = self.get_argument("user_id",None)
        login_scan_uuid = self.get_argument("uuid",None)
        entity_id = settings.get("msh_login_scan",None)
        block_id = entity_id
        MPWeixinAPP = self.get_argument('app',settings["MPWeixinAppDefault"])
        is_weixin = False
        if "Mobile" in self.request.headers.get("User-Agent", "") and "MicroMessenger" in self.request.headers.get("User-Agent", ""):
            is_weixin = True
        if is_weixin:
            code = self.get_argument("code",None)

            if not code or code == "":
                redirect_uri = "%s://%s%s" % (self.request.protocol,self.request.host,self.request.uri)
                # print(self.request)
                # print("redirect_uri:",redirect_uri)
                args = {
                    'appid'            : settings["MPWeixinInfo"][MPWeixinAPP]["MPWeixinAppID"],
                    'redirect_uri'     : redirect_uri,
                    'response_type'    : 'code',
                    'scope'            : 'snsapi_userinfo',
                    'state'            : MPWeixinAPP
                }
                url = 'https://open.weixin.qq.com/connect/oauth2/authorize?' + urllib.parse.urlencode(sorted(args.items())) + '#wechat_redirect'
                self.redirect(url)
                return
            else:
                http_client = tornado.httpclient.AsyncHTTPClient()
                url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid='+settings["MPWeixinInfo"][MPWeixinAPP]["MPWeixinAppID"]+'&secret='+settings["MPWeixinInfo"][MPWeixinAPP]["MPWeixinAppSecret"]+'&code='+code+'&grant_type=authorization_code'
                response = yield http_client.fetch(url)
                data = json_decode(response.body)
                if data.get('errcode','') == 40029 or data.get('errcode','') == 40163:
                    uri = self.request.uri
                    uri = uri.replace("&code=%s"%code,"")
                    uri = uri.replace("code=%s"%code,"")
                    redirect_uri = "%s://%s%s" % (self.request.protocol,self.request.host,uri)
                    self.redirect(redirect_uri)
                    return
                self.access_token = data.get('access_token')
                self.openid = data.get('openid')
                args = {
                    'access_token': self.access_token,
                    'openid'      : self.openid,
                    'lang'        : 'zh_CN'
                }
                url = 'https://api.weixin.qq.com/sns/userinfo?' + urllib.parse.urlencode(sorted(args.items()))
                response = yield http_client.fetch(url)
                data = json_decode(response.body)
                user_weixin_data_new = data

                weixinID = settings["MPWeixinInfo"][MPWeixinAPP]["MPWeixinID"]
                appID = settings["MPWeixinInfo"][MPWeixinAPP]["MPWeixinAppID"]
                appSecret = settings["MPWeixinInfo"][MPWeixinAPP]["MPWeixinAppSecret"]
                shopNumber = settings["MPWeixinInfo"][MPWeixinAPP]["ShopNumber"]
                shopNumberKey = settings["MPWeixinInfo"][MPWeixinAPP]["ShopNumberKey"]

                yield weixin_JS_SDK_check(weixinID, appID, appSecret)
                data = weixin_access_token_for_apps[weixinID]
                if not data:
                    self.finish({
                            "info":"error",
                            "about":"no accessToken data",
                        })
                    return
                sign = WeixinJSSDKSign(settings["MPWeixinInfo"][MPWeixinAPP]["ticket"], settings["MPWeixinInfo"][MPWeixinAPP]["accessTokenTimer"], self.request.full_url())
                wx_ret = sign.sign()
                wx_timestamp = wx_ret['timestamp']
                wx_noncestr  = wx_ret['nonceStr']
                wx_signature = wx_ret['signature']

        if not self.current_user:
            self.user_id = "no_login:%s"%str(time.time())
            print("scan no login",self.user_id)
        else:
            self.user_id = self.current_user["id"]
            print("scan login",self.user_id)

        if is_weixin:
            if self.current_user:
                user = get_aim(self.user_id)
                user_update = False
                user_weixin_openids = user.get("weixin_openids",{})
                user_weixin_openids_now = user_weixin_openids.get(MPWeixinAPP,[])
                if len(user_weixin_openids_now)>0:
                    if user_weixin_openids_now[0] != self.openid:
                        user_weixin_openids_now.remove(self.openid)
                        user_weixin_openids_now.insert(0,self.openid)
                        user_update = True
                else:
                    user_weixin_openids_now.insert(0,self.openid)
                    user_update = True
                user_weixin_openids[MPWeixinAPP]=user_weixin_openids_now
                user["weixin_openids"]=user_weixin_openids
                user_weixin_data = user.get("weixin_data",{})
                user_weixin_data_now = user_weixin_data.get(MPWeixinAPP,{})
                if user_weixin_data_now != user_weixin_data_new:
                    user_weixin_data_now = user_weixin_data_new
                    user_update = True
                user_weixin_data[MPWeixinAPP] = user_weixin_data_now
                user["weixin_data"]=user_weixin_data
                if user.get("name","")=="":
                    user["name"]=user_weixin_data[MPWeixinAPP]["nickname"]
                if user.get("headimgurl","")=="":
                    user["headimgurl"]=user_weixin_data[MPWeixinAPP]["headimgurl"]
                if user_update:
                    user["updatetime"]=int(time.time())
                    print("update user_id:",self.user_id)
                    update_aim(self.user_id,user)
            else:
                open_id = user_weixin_data_new["openid"]
                login = "weixin:%s_@@_%s"%(weixinID,open_id)
                result = conn.query("SELECT * FROM index_login WHERE login=%s",login)
                if not result:
                    password_str = "".join(random.choice(string.ascii_letters+string.digits) for x in range(8))
                    user = {
                        "password":password_str,
                        "name":user_weixin_data_new["nickname"],
                        "headimgurl":user_weixin_data_new["headimgurl"],
                        "weixin_data":{
                            MPWeixinAPP: user_weixin_data_new,
                        },
                    }
                    [new_id, user] = nomagic.auth.create_user(user)
                    user_id = new_id
                    conn.execute("INSERT INTO index_login (login, entity_id,app) VALUES(%s, %s, %s)", login, new_id,"")
                else:
                    user_id = result[0].get("entity_id",None)

                self.set_secure_cookie("user", tornado.escape.json_encode({"id": user_id, "v":1}),expires=time.time()+63072000,domain=settings.get("cookie_domain"))

        self.time_now = int(time.time())
        self.version = settings["version"]
        self.block_id = block_id
        if not block_id:
            self.render("../template/404.html")
            return
        block = get_aim(block_id)
        if not block:
            self.render("../template/404.html")
            return

        self.permission_btns = {
            "private":"Private·私有",
            "publish":"Publish·公开发表",
            "public":"Public·自由编辑"
        }
        self.permission = block.get("permission","private")
        self.permission = "publish"
        self.editors = block.get("editors",[block.get("owner",None)])
        self.readers = block.get("readers",[])
        self.blackers = block.get("blackers",[])
        if self.user_id in self.blackers:
            self.render("../template/404.html")
            return
        if self.permission in ["private"]:
            if self.user_id not in self.editors and self.user_id not in self.readers:
                self.render("../template/404.html")
                return

        self.doms = block.get("doms",[])
        websocket_protocol = "ws" if self.request.protocol == "http" else "wss"
        aim_host = self.request.host
        self.websocket_url = "%s://%s/api/data/ws?aim_id=%s" % (websocket_protocol, aim_host, block_id)

        self.title = block.get("title","")
        self.desc = block.get("desc","")
        self.fork_allow = block.get("fork_allow",True)
        self.fork_from = block.get("fork_from","")
        self.fork_entity = block.get("fork_entity",None)
        self.grid_graph = block.get("grid_graph",{})
        self.main_area = block.get("main_area",{})
        self.is_weixin = is_weixin
        self.host_url = "%s://%s"%(self.request.protocol,aim_host)
        self.findmaster_app = MPWeixinAPP
        if is_weixin:
            self.wx_app = self.findmaster_app
            self.wx_data = json_encode(user_weixin_data_new)
            self.wx_appid = appID
            self.wx_timestamp = wx_timestamp
            self.wx_noncestr  = wx_noncestr
            self.wx_signature = wx_signature
        self.login_scan_room_id = login_scan_room_id
        self.login_scan_user_id = login_scan_user_id
        self.login_scan_uuid = login_scan_uuid
        self.render("../template/msh_login_scan.html")
class SubmitLoginScanAPIHandler(WebRequest):
    def post(self):
        aim_room_id = self.get_argument("room_id",None)
        aim_user_id = self.get_argument("user_id",None)
        aim_uuid = self.get_argument("uuid",None)
        uuid = self.get_argument("uuid_now",None)
        aim_id = "%s/%s/%s"%(aim_room_id,aim_user_id,aim_uuid)

        if not self.current_user:
            self.finish({"info":"error","about":"not login"})
            return
        user_id = self.current_user["id"]
        user = get_aim(user_id)
        login_scan_allow = user.get("login_scan_allow",None)
        login_scan_allow_now = "%s/%s"%(aim_id,uuid)
        user_update = False
        if login_scan_allow != login_scan_allow_now:
            user["login_scan_allow"] = login_scan_allow_now
            user["updatetime"]=int(time.time())
            user_update = True
        user_name = user.get("name","")
        user_headimgurl = user.get("headimgurl","/static/img/headimgurl.png")
        msgtype = "LOGINSCANSUBMIT"
        time_now = int(time.time())
        chat_id = aim_id
        block_id = aim_id

        if user_update:
            update_aim(user_id,user)

        self.finish({"info": "ok","comment_id":"","sequence":"","time":time_now,"msgtype":msgtype})
        msg = [msgtype, {
            "content":"login scan submit",
            "nickname": user_name,
            "headimgurl": user_headimgurl,
            "time": time_now,
            "user_id": user_id,
            "sequence": "",
            "comment_id": "",
            "uuid":uuid,
        }, chat_id]
        if not block_id:
            DataWebSocket.send_to_all(json_encode(msg))
        else:
            DataWebSocket.send_to_target_room(json_encode(msg),block_id)
class ConfirmLoginScanAPIHandler(WebRequest):
    def post(self):
        login_scan_allow_now = self.get_argument("login_scan_allow",None)
        aim_user_id = self.get_argument("user_id",None)
        redirect = self.get_argument("redirect",None)
        if not login_scan_allow_now or not aim_user_id:
            self.finish({"info":"error","about":"no login_scan_allow or no user_id"})
            return
        aim_user = get_aim(aim_user_id)
        login_scan_allow = aim_user.get("login_scan_allow",None)
        if login_scan_allow_now != login_scan_allow:
            self.finish({"info":"error","about":"error login_scan_allow, qrcode is timeout"})
            return
        if not redirect:
            redirect = "/"
        user_id = aim_user_id
        self.set_secure_cookie("user", tornado.escape.json_encode({"id": user_id, "v":1}),expires=time.time()+63072000,domain=settings.get("cookie_domain"))
        self.finish({"info":"ok","about":"redirect","redirect":redirect})





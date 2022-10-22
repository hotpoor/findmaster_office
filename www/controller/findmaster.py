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

class UriMappingHandler(WebRequest):
    @tornado.gen.coroutine
    def get(self, app):
        if app in settings["MPWeixinJSMP"]:
            self.render("../static/weixin_js_map/%s"%app)
            return
        link_list = self.request.uri.split("?")
        uri_mapping = settings["uri_mapping"]
        block_id = uri_mapping.get(link_list[0],None)
        if "Mobile" in self.request.headers.get("User-Agent", "") and link_list[0]=="/":
            block_id = uri_mapping.get("/mobile",None)
        MPWeixinAPP = self.get_argument('app',settings["MPWeixinAppDefault"])
        is_weixin = False
        if "Mobile" in self.request.headers.get("User-Agent", "") and "MicroMessenger" in self.request.headers.get("User-Agent", ""):
            is_weixin = True
            is_weixin = False
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
        else:
            self.user_id = self.current_user["id"]

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
                if user.get("name","")=="" or user.get("name","") != user_weixin_data[MPWeixinAPP]["nickname"]:
                    user["name"]=user_weixin_data[MPWeixinAPP]["nickname"]
                    user_update = True
                if user.get("headimgurl","")=="" or user.get("headimgurl","")!=user_weixin_data[MPWeixinAPP]["headimgurl"]:
                    user["headimgurl"]=user_weixin_data[MPWeixinAPP]["headimgurl"]
                    user_update = True
                if user_update:
                    user["name"]=user_weixin_data[MPWeixinAPP]["nickname"]
                    user["headimgurl"]=user_weixin_data[MPWeixinAPP]["headimgurl"]
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
        self.findmaster_app = MPWeixinAPP
        if is_weixin:
            self.wx_app = self.findmaster_app
            self.wx_data = json_encode(user_weixin_data_new)
            self.wx_appid = appID
            self.wx_timestamp = wx_timestamp
            self.wx_noncestr  = wx_noncestr
            self.wx_signature = wx_signature
        self.render("../template/page.html")
class MainHandler(WebRequest):
    @tornado.gen.coroutine
    def get(self, app):
        is_weixin = False
        if "Mobile" in self.request.headers.get("User-Agent", "") and "MicroMessenger" in self.request.headers.get("User-Agent", ""):
            is_weixin = True
            is_weixin = False
        # self.time_now = int(time.time())
        # self.version = settings["version"]
        # self._ = self.locale.translate
        # self.render("../template/index.html")
        block_id = "0b5ee08ed0ed498593306193601680e7"
        if not self.current_user:
            self.user_id = "no_login:%s"%str(time.time())
        else:
            self.user_id = self.current_user["id"]
        self.time_now = int(time.time())
        self.version = settings["version"]
        self.block_id = block_id
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
        
        self.findmaster_app = settings["MPWeixinAppDefault"]
        self.title = block.get("title","")
        self.desc = block.get("desc","")
        self.fork_allow = block.get("fork_allow",True)
        self.fork_from = block.get("fork_from","")
        self.fork_entity = block.get("fork_entity",None)
        self.grid_graph = block.get("grid_graph",{})
        self.main_area = block.get("main_area",{})
        self.is_weixin = is_weixin
        self.render("../template/page.html")

class LoginHandler(WebRequest):
    @tornado.gen.coroutine
    def get(self):
        self.time_now = int(time.time())
        self.version = settings["version"]
        self._ = self.locale.translate
        self.render("../template/login.html")
class RegisterHandler(WebRequest):
    @tornado.gen.coroutine
    def get(self):
        block_id = "9b30f584a1cf4005996ec4d5e4170cbc"
        if not self.current_user:
            self.user_id = "no_login:%s"%str(time.time())
        else:
            self.user_id = self.current_user["id"]
        self.time_now = int(time.time())
        self.version = settings["version"]
        self.block_id = block_id
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

        self.findmaster_app = settings["MPWeixinAppDefault"]
        self.title = block.get("title","")
        self.desc = block.get("desc","")
        self.fork_allow = block.get("fork_allow",True)
        self.fork_from = block.get("fork_from","")
        self.fork_entity = block.get("fork_entity",None)
        self.grid_graph = block.get("grid_graph",{})
        self.main_area = block.get("main_area",{})
        self.render("../template/page.html")
class MainHomeHandler(WebRequest):
    def get(self):
        self.timer = int(time.time())
        print(self.request)
        self.render("../template/main.html")
class WelcomeHomeHandler(WebRequest):
    def get(self):
        self.timer = int(time.time())
        self.render("../template/welcome.html")
class PagesHomeHandler(WebRequest):
    def get(self):
        self.time_now = int(time.time())
        self.version = settings["version"]
        if not self.current_user:
            self.finish({"info":"error","about":"no login"})
            return
        user_id = self.current_user["id"]
        user = get_aim(user_id)
        self.pages = user.get("pages",[])
        self.render("../template/pages.html")
class PagesListAPIHandler(WebRequest):
    def get(self):
        if not self.current_user:
            self.finish({"info":"error","about":"no login"})
            return
        user_id = self.current_user["id"]
        user = get_aim(user_id)

        pages_ids = user.get("pages",[])
        pages = get_aims(pages_ids)
        result = []
        for page in pages:
            result_item = {
                "block_id":page[0],
                "title":page[1].get("title","new page"),
                "desc":page[1].get("desc","this is a new page"),
                "fork_allow":page[1].get("fork_allow",True),
                "fork_from":page[1].get("fork_from",None),
            }
            result.append(result_item)
        pages_top_ids = user.get("pages_top",[])
        
        self.finish({"info":"ok","result":result,"pages_top_ids":pages_top_ids})

class PageAddAPIHandler(WebRequest):
    def post(self):
        if not self.current_user:
            self.finish({"info":"error","about":"no login"})
            return
        user_id = self.current_user["id"]
        title = self.get_argument("title","new page")
        desc = self.get_argument("desc","this is a new page")
        user = get_aim(user_id)
        pages = user.get("pages",[])
        block = {
            "owner":user_id,
            "subtype":"page",
            "title":title,
            "desc":desc,
            "doms":[],
            "history":[],
            "updatetime":int(time.time())
        }
        [block_id,block]=nomagic.block.create_block(block)
        pages.insert(0,block_id)
        user["pages"]=pages
        update_aim(user_id,user)
        self.finish({"info":"ok","about":"create new page success","block_id":block_id})
class PageAddFreePdfAPIHandler(WebRequest):
    def post(self):
        token = self.get_argument("token","")
        if token not in ["xialiwei_follows_god"]:
            self.finish({"info":"error","about":"no login"})
            return
        user_id = self.get_argument("user_id","")
        title = self.get_argument("title","new page")
        desc = self.get_argument("desc","this is a new page")
        free_doc_xml1 = self.get_argument("xml1","{}")
        free_doc_xml1_json = json_decode(free_doc_xml1)
        free_doc_xml2 = self.get_argument("xml2","{}")
        free_doc_xml2_json = json_decode(free_doc_xml2)

        pre_p_list = self.get_argument("pre_p_list","[]")
        pre_p_list_json = json_decode(pre_p_list)

        doms = []
        for pre_p_item in pre_p_list_json:
            dom_sequence = "".join(random.choice(string.ascii_lowercase+string.digits) for _ in range(6))
            dom_sequence_same = False
            while True:
                for dom_item in doms:
                    if dom_item[0] == dom_sequence:
                        dom_sequence_same = True
                        break
                if dom_sequence_same:
                    dom_sequence = "".join(random.choice(string.ascii_lowercase+string.digits) for _ in range(6))
                    dom_sequence_same = False
                else:
                    break
            dom_position = {
                "x":10,
                "y":10,
                "w":100,
                "h":40,
                "z":0,
                "s":"",
                "r":"dom_scroll_relative"
            }
            dom_type="text"
            dom_css = ""
            # dom_content = """<div class="section" style="text-align: left;"><div>%s</div></div>"""%(pre_p_item)
            pre_p_item_list = pre_p_item.split("\n")
            pre_p_item_html = "<br>".join(pre_p_item_list)
            dom_content = """<div class="section" style="text-align: left;"><div>%s</div></div>"""%(pre_p_item_html)
            dom_children = []
            updatetime = int(time.time())
            dom = [dom_sequence,dom_type,dom_position,dom_content,dom_css,dom_children,updatetime]
            doms.append(dom)

        user = get_aim(user_id)
        pages = user.get("pages",[])
        block = {
            "owner":user_id,
            "subtype":"page",
            "title":title,
            "desc":desc,
            "doms":doms,
            "history":[],
            "updatetime":int(time.time()),
            "subtype_plus":"pdf",
            "subtype_plus_info":{
                # "xml1":free_doc_xml1_json,
                # "xml2":free_doc_xml2_json,
                "pre_p_list":pre_p_list_json,
            },
            "permission": "publish",
        }
        [block_id,block]=nomagic.block.create_block(block)
        pages.insert(0,block_id)
        user["pages"]=pages
        update_aim(user_id,user)
        self.finish({"info":"ok","about":"create new page success","block_id":block_id})
class PageAddFreeDocxAPIHandler(WebRequest):
    def post(self):
        token = self.get_argument("token","")
        if token not in ["xialiwei_follows_god"]:
            self.finish({"info":"error","about":"no login"})
            return
        user_id = self.get_argument("user_id","")
        title = self.get_argument("title","new page")
        desc = self.get_argument("desc","this is a new page")
        free_doc_xml1 = self.get_argument("xml1","{}")
        free_doc_xml1_json = json_decode(free_doc_xml1)
        free_doc_xml2 = self.get_argument("xml2","{}")
        free_doc_xml2_json = json_decode(free_doc_xml2)

        pre_p_list = self.get_argument("pre_p_list","[]")
        pre_p_list_json = json_decode(pre_p_list)

        doms = []
        for pre_p_item in pre_p_list_json:
            dom_sequence = "".join(random.choice(string.ascii_lowercase+string.digits) for _ in range(6))
            dom_sequence_same = False
            while True:
                for dom_item in doms:
                    if dom_item[0] == dom_sequence:
                        dom_sequence_same = True
                        break
                if dom_sequence_same:
                    dom_sequence = "".join(random.choice(string.ascii_lowercase+string.digits) for _ in range(6))
                    dom_sequence_same = False
                else:
                    break
            dom_position = {
                "x":10,
                "y":10,
                "w":100,
                "h":40,
                "z":0,
                "s":"",
                "r":"dom_scroll_relative"
            }
            dom_type="text"
            dom_css = ""
            pre_p_item_list = pre_p_item.split("\n")
            pre_p_item_html = "<br>".join(pre_p_item_list)
            dom_content = """<div class="section" style="text-align: left;"><div>%s</div></div>"""%(pre_p_item_html)
            dom_children = []
            updatetime = int(time.time())
            dom = [dom_sequence,dom_type,dom_position,dom_content,dom_css,dom_children,updatetime]
            doms.append(dom)

        user = get_aim(user_id)
        pages = user.get("pages",[])
        block = {
            "owner":user_id,
            "subtype":"page",
            "title":title,
            "desc":desc,
            "doms":doms,
            "history":[],
            "updatetime":int(time.time()),
            "subtype_plus":"docx",
            "subtype_plus_info":{
                # "xml1":free_doc_xml1_json,
                # "xml2":free_doc_xml2_json,
                "pre_p_list":pre_p_list_json,
            },
            "permission": "publish",
        }
        [block_id,block]=nomagic.block.create_block(block)
        pages.insert(0,block_id)
        user["pages"]=pages
        update_aim(user_id,user)
        self.finish({"info":"ok","about":"create new page success","block_id":block_id})

class PageAddFreeAPIHandler(WebRequest):
    def post(self):
        token = self.get_argument("token","")
        if token not in ["xialiwei_follows_god"]:
            self.finish({"info":"error","about":"no login"})
            return
        user_id = self.get_argument("user_id","")
        title = self.get_argument("title","new page")
        desc = self.get_argument("desc","this is a new page")
        user = get_aim(user_id)
        pages = user.get("pages",[])
        block = {
            "owner":user_id,
            "subtype":"page",
            "title":title,
            "desc":desc,
            "doms":[],
            "history":[],
            "updatetime":int(time.time()),
            "permission": "publish",
        }
        [block_id,block]=nomagic.block.create_block(block)
        pages.insert(0,block_id)
        user["pages"]=pages
        update_aim(user_id,user)
        self.finish({"info":"ok","about":"create new page success","block_id":block_id})
class PageHomeHandler(WebRequest):
    @tornado.gen.coroutine
    def get(self,block_id):
        # self.set_header("Access-Control-Allow-Origin", self.request.headers.get("Origin","*"))
        # self.set_header("Access-Control-Allow-Credentials", "true")
        if not self.current_user:
            self.user_id = "no_login:%s"%str(time.time())
        else:
            self.user_id = self.current_user["id"]
        self.time_now = int(time.time())
        self.version = settings["version"]
        self.block_id = block_id
        block = get_aim(block_id)
        if not block:
            self.render("../template/404.html")
            return

        MPWeixinAPP = self.get_argument('app',settings["MPWeixinAppDefault"])
        is_weixin = False
        if "Mobile" in self.request.headers.get("User-Agent", "") and "MicroMessenger" in self.request.headers.get("User-Agent", ""):
            is_weixin = True
            is_weixin = False
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
                if user.get("name","")=="" or user.get("name","") != user_weixin_data[MPWeixinAPP]["nickname"]:
                    user["name"]=user_weixin_data[MPWeixinAPP]["nickname"]
                    user_update = True
                if user.get("headimgurl","")=="" or user.get("headimgurl","")!=user_weixin_data[MPWeixinAPP]["headimgurl"]:
                    user["headimgurl"]=user_weixin_data[MPWeixinAPP]["headimgurl"]
                    user_update = True
                if user_update:
                    user["name"]=user_weixin_data[MPWeixinAPP]["nickname"]
                    user["headimgurl"]=user_weixin_data[MPWeixinAPP]["headimgurl"]
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

        self.permission_btns = {
            "private":"Private·私有",
            "publish":"Publish·公开发表",
            "public":"Public·自由编辑"
        }
        self.permission = block.get("permission","private")
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
        self.findmaster_app = MPWeixinAPP
        if is_weixin:
            self.wx_app = self.findmaster_app
            self.wx_data = json_encode(user_weixin_data_new)
            self.wx_appid = appID
            self.wx_timestamp = wx_timestamp
            self.wx_noncestr  = wx_noncestr
            self.wx_signature = wx_signature
        self.render("../template/page.html")
class PageEditHomeHandler(WebRequest):
    @tornado.gen.coroutine
    def get(self,block_id):
        # self.set_header("Access-Control-Allow-Origin", self.request.headers.get("Origin","*"))
        # self.set_header("Access-Control-Allow-Credentials", "true")
        if not self.current_user:
            self.user_id = "no_login:%s"%str(time.time())
        else:
            self.user_id = self.current_user["id"]
        self.time_now = int(time.time())
        self.version = settings["version"]
        self.block_id = block_id
        block = get_aim(block_id)
        if not block:
            self.render("../template/404.html")
            return

        MPWeixinAPP = self.get_argument('app',settings["MPWeixinAppDefault"])
        is_weixin = False
        if "Mobile" in self.request.headers.get("User-Agent", "") and "MicroMessenger" in self.request.headers.get("User-Agent", ""):
            is_weixin = True
            is_weixin = False
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
                if user.get("name","")=="" or user.get("name","") != user_weixin_data[MPWeixinAPP]["nickname"]:
                    user["name"]=user_weixin_data[MPWeixinAPP]["nickname"]
                    user_update = True
                if user.get("headimgurl","")=="" or user.get("headimgurl","")!=user_weixin_data[MPWeixinAPP]["headimgurl"]:
                    user["headimgurl"]=user_weixin_data[MPWeixinAPP]["headimgurl"]
                    user_update = True
                if user_update:
                    user["name"]=user_weixin_data[MPWeixinAPP]["nickname"]
                    user["headimgurl"]=user_weixin_data[MPWeixinAPP]["headimgurl"]
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



        self.doms = block.get("doms",[])
        websocket_protocol = "ws" if self.request.protocol == "http" else "wss"
        aim_host = self.request.host
        self.websocket_url = "%s://%s/api/data/ws?aim_id=%s" % (websocket_protocol, aim_host, block_id)

        self.permission_btns = {
            "private":"Private·私有",
            "publish":"Publish·公开发表",
            "public":"Public·自由编辑"
        }
        self.permission = block.get("permission","private")
        self.editors = block.get("editors",[block.get("owner",None)])
        self.readers = block.get("readers",[])
        self.blackers = block.get("blackers",[])
        self.members = block.get("members",[])
        self.stars = block.get("stars",[])

        if self.user_id in self.blackers:
            self.render("../template/404.html")
            return

        if self.permission not in ["public"]:
            if self.user_id not in self.editors:
                self.redirect("/home/page/%s"%block_id)
                return
        self.title = block.get("title","")
        self.desc = block.get("desc","")
        self.fork_allow = block.get("fork_allow",True)
        self.fork_from = block.get("fork_from","")
        self.fork_entity = block.get("fork_entity",None)
        self.grid_graph = block.get("grid_graph",{})
        self.main_area = block.get("main_area",{})
        self.is_weixin = is_weixin
        self.findmaster_app = MPWeixinAPP
        if is_weixin:
            self.wx_app = self.findmaster_app
            self.wx_appid = appID
            self.wx_timestamp = wx_timestamp
            self.wx_noncestr  = wx_noncestr
            self.wx_signature = wx_signature
        self.comment_entities = block.get("comment_entities",[])
        self.render("../template/page_edit.html")
class PageFixHomeHandler(WebRequest):
    def get(self,block_id):
        # self.set_header("Access-Control-Allow-Origin", self.request.headers.get("Origin","*"))
        # self.set_header("Access-Control-Allow-Credentials", "true")
        if not self.current_user:
            self.user_id = "no_login:%s"%str(time.time())
        else:
            self.user_id = self.current_user["id"]
        self.time_now = int(time.time())
        self.version = settings["version"]
        self.block_id = block_id
        block = get_aim(block_id)
        if not block:
            self.render("../template/404.html")
            return
        self.doms = block.get("doms",[])
        websocket_protocol = "ws" if self.request.protocol == "http" else "wss"
        aim_host = self.request.host
        self.websocket_url = "%s://%s/api/data/ws?aim_id=%s" % (websocket_protocol, aim_host, block_id)

        self.permission = block.get("permission","private")
        self.editors = block.get("editors",[block.get("owner",None)])
        self.readers = block.get("readers",[])
        self.blackers = block.get("blackers",[])
        self.members = block.get("members",[])

        if self.user_id in self.blackers:
            self.render("../template/404.html")
            return

        if self.permission not in ["public"]:
            if self.user_id not in self.editors:
                self.redirect("/home/page/%s"%block_id)
                return
        self.render("../template/page_fix.html")
class PageCopyDomAPIHandler(WebRequest):
    def post(self):
        if not self.current_user:
            self.finish({"info":"error","about":"no login"})
            return
        user_id = self.current_user["id"]
        block_id = self.get_argument("block_id",None)
        aim_id = self.get_argument("aim_id",None)
        aim_dom_id = self.get_argument("aim_dom_id",None)
        dom_owner = self.get_argument("dom_owner",None)
        dom_type = self.get_argument("dom_type","text")
        dom_position_x = int(float(self.get_argument("dom_position_x","0")))
        dom_position_y = int(float(self.get_argument("dom_position_y","0")))
        # if dom_type not in ["text","img","video","canvas","input","button","textarea"]:
        if dom_type not in ["domcopy"]:
            self.finish({"info":"error","about":"not allow dom type"})
            return
        block = get_aim(block_id)
        aim = get_aim(aim_id)
        #判断是否为编辑者
        if user_id not in block.get("editors",[block.get("owner",None)]):
        # if block.get("owner",None) != user_id:
            self.finish({"info":"error","about":"no in editors"})
            return
        doms = block.get("doms",[])
        dom_sequence = "".join(random.choice(string.ascii_lowercase+string.digits) for _ in range(6))
        dom_sequence_same = False
        while True:
            for dom_item in doms:
                if dom_item[0] == dom_sequence:
                    dom_sequence_same = True
                    break
            if dom_sequence_same:
                dom_sequence = "".join(random.choice(string.ascii_lowercase+string.digits) for _ in range(6))
                dom_sequence_same = False
            else:
                break
        copy_dom = None
        for aim_dom in aim.get("doms",[]):
            if aim_dom[0]==aim_dom_id:
                copy_dom = copy.deepcopy(aim_dom)
        if not copy_dom:
            self.finish({"info":"error","about":"copy dom is removed or none"})
            return
        updatetime = int(time.time())
        copy_dom[0]=dom_sequence
        # copy_dom[2]["x"]=dom_position_x
        # copy_dom[2]["y"]=dom_position_y
        copy_dom[6]=updatetime
        # dom = [dom_sequence,dom_type,dom_position,dom_content,dom_css,dom_children,updatetime]
        dom = copy_dom
        doms.append(dom)
        block["doms"] = doms
        block["updatetime"] = updatetime
        update_aim(block_id,block)
        self.finish({"info":"ok","dom_sequence":dom_sequence})
        [dom_sequence,dom_type,dom_position,dom_content,dom_css,dom_children,updatetime] = dom
        content_data = {
            "dom_current":dom_sequence,
            "dom_content":dom_content,
            "dom_position_x":dom_position["x"],
            "dom_position_y":dom_position["y"],
            "dom_position_w":dom_position["w"],
            "dom_position_h":dom_position["h"],
            "dom_position_z":dom_position["z"],
            "dom_scroll":dom_position.get("s",""),
            "dom_type":dom_type,
        }
        msgtype = "COMMENTPAGECOPYDOM"
        msg = [msgtype, {
            "content": content_data,
            "nickname": "",
            "headimgurl": "/static/img/oflogo.png",
            "tel": "",
            "time": updatetime,
            "user_id": user_id,
            "sequence": "",
            "comment_id": ""
        }, block_id]
        DataWebSocket.send_to_all(json_encode(msg))
class PageCopyDomsAPIHandler(WebRequest):
    def post(self):
        if not self.current_user:
            self.finish({"info":"error","about":"no login"})
            return
        user_id = self.current_user["id"]
        block_id = self.get_argument("block_id",None)
        # aim_id = self.get_argument("aim_id",None)
        # aim_dom_id = self.get_argument("aim_dom_id",None)
        current_copy = self.get_argument("current_copy","[]")
        dom_owner = self.get_argument("dom_owner",None)
        dom_type = self.get_argument("dom_type","text")
        dom_position_x = int(float(self.get_argument("dom_position_x","0")))
        dom_position_y = int(float(self.get_argument("dom_position_y","0")))
        # if dom_type not in ["text","img","video","canvas","input","button","textarea"]:
        if dom_type not in ["domcopy"]:
            self.finish({"info":"error","about":"not allow dom type"})
            return
        block = get_aim(block_id)
        #判断是否为编辑者
        if user_id not in block.get("editors",[block.get("owner",None)]):
        # if block.get("owner",None) != user_id:
            self.finish({"info":"error","about":"no in editors"})
            return
        aim_ids = []
        aim_dom_ids = []
        current_copy_items = json_decode(current_copy)
        for current_copy_item in current_copy_items:
            current_copy_item_list = current_copy_item.split("COPYDOM//")
            [a_aim_id,a_aim_dom_id]=current_copy_item_list[1].split(",")
            aim_ids.append(a_aim_id)
            aim_dom_ids.append([a_aim_id,a_aim_dom_id])
        aim_ids = list(set(aim_ids))
        aims = get_aims(aim_ids)
        aims_json = {}
        for aim in aims:
            aims_json[aim[0]]=aim[1]
        dom_sequences=[]
        doms = block.get("doms",[])
        content_datas = []
        for [aim_id,aim_dom_id] in aim_dom_ids:
            aim = aims_json[aim_id]
            dom_sequence = "".join(random.choice(string.ascii_lowercase+string.digits) for _ in range(6))
            dom_sequence_same = False
            while True:
                for dom_item in doms:
                    if dom_item[0] == dom_sequence:
                        dom_sequence_same = True
                        break
                if dom_sequence_same:
                    dom_sequence = "".join(random.choice(string.ascii_lowercase+string.digits) for _ in range(6))
                    dom_sequence_same = False
                else:
                    break
            copy_dom = None
            for aim_dom in aim.get("doms",[]):
                if aim_dom[0]==aim_dom_id:
                    copy_dom = copy.deepcopy(aim_dom)
            if not copy_dom:
                self.finish({"info":"error","about":"copy dom is removed or none"})
                return
            updatetime = int(time.time())
            copy_dom[0]=dom_sequence
            # copy_dom[2]["x"]=dom_position_x
            # copy_dom[2]["y"]=dom_position_y
            copy_dom[6]=updatetime
            # dom = [dom_sequence,dom_type,dom_position,dom_content,dom_css,dom_children,updatetime]
            dom = copy_dom
            doms.append(dom)
            dom_sequences.append(dom_sequence)
            [dom_sequence,dom_type,dom_position,dom_content,dom_css,dom_children,updatetime] = dom
            content_data = {
                "dom_current":dom_sequence,
                "dom_content":dom_content,
                "dom_position_x":dom_position["x"],
                "dom_position_y":dom_position["y"],
                "dom_position_w":dom_position["w"],
                "dom_position_h":dom_position["h"],
                "dom_position_z":dom_position["z"],
                "dom_scroll":dom_position.get("s",""),
                "dom_type":dom_type,
            }
            content_datas.append(content_data)
        block["doms"] = doms
        block["updatetime"] = updatetime
        update_aim(block_id,block)
        self.finish({"info":"ok","dom_sequences":dom_sequences})
        msgtype = "COMMENTPAGECOPYDOMS"
        msg = [msgtype, {
            "content": content_datas,
            "nickname": "",
            "headimgurl": "/static/img/oflogo.png",
            "tel": "",
            "time": updatetime,
            "user_id": user_id,
            "sequence": "",
            "comment_id": ""
        }, block_id]
        DataWebSocket.send_to_all(json_encode(msg))

class PageAddDomAPIHandler(WebRequest):
    def post(self):
        if not self.current_user:
            self.finish({"info":"error","about":"no login"})
            return
        user_id = self.current_user["id"]
        block_id = self.get_argument("block_id",None)
        dom_owner = self.get_argument("dom_owner",None)
        dom_type = self.get_argument("dom_type","text")
        dom_position_x = int(float(self.get_argument("dom_position_x","0")))
        dom_position_y = int(float(self.get_argument("dom_position_y","0")))
        dom_scroll = self.get_argument("dom_scroll","")
        # if dom_type not in ["text","img","video","canvas","input","button","textarea"]:
        if dom_type not in ["text","img","video","iframe","file"]:
            self.finish({"info":"error","about":"not allow dom type"})
            return
        block = get_aim(block_id)
        #判断是否为编辑者
        if user_id not in block.get("editors",[block.get("owner",None)]):
        # if block.get("owner",None) != user_id:
            self.finish({"info":"error","about":"no in editors"})
            return
        doms = block.get("doms",[])
        dom_sequence = "".join(random.choice(string.ascii_lowercase+string.digits) for _ in range(6))
        dom_sequence_same = False
        while True:
            for dom_item in doms:
                if dom_item[0] == dom_sequence:
                    dom_sequence_same = True
                    break
            if dom_sequence_same:
                dom_sequence = "".join(random.choice(string.ascii_lowercase+string.digits) for _ in range(6))
                dom_sequence_same = False
            else:
                break
        dom_position = {
            "x":dom_position_x,
            "y":dom_position_y,
            "w":100,
            "h":40,
            "z":0,
            "s":dom_scroll,
            "r":"",
        }
        dom_css = ""
        dom_content = ""
        dom_children = []
        updatetime = int(time.time())
        dom = [dom_sequence,dom_type,dom_position,dom_content,dom_css,dom_children,updatetime]
        doms.append(dom)
        block["doms"] = doms
        block["updatetime"] = updatetime
        update_aim(block_id,block)
        self.finish({"info":"ok","dom_sequence":dom_sequence})

        if dom_type in ["text"]:
            dom_content = """
            <div class="section">text</div>
            """
        elif dom_type in ["img"]:
            dom_content = """
            <div class="section"><img src="/static/img/need_add_img.png"></div>
            """
        elif dom_type in ["video"]:
            dom_content = """
            <div class="section" contenteditable="false"><span class="novideospan">视频未设置</span></div>
            """
        elif dom_type in ["iframe"]:
            dom_content = """
            <div class="section" contenteditable="false">iframe暂未设置</div>
            """
        content_data = {
            "dom_current":dom_sequence,
            "dom_content":dom_content,
            "dom_position_x":dom_position["x"],
            "dom_position_y":dom_position["y"],
            "dom_position_w":dom_position["w"],
            "dom_position_h":dom_position["h"],
            "dom_position_z":dom_position["z"],
            "dom_scroll":dom_position["s"],
            "dom_type":dom_type,
        }
        msgtype = "COMMENTPAGEADDDOM"
        msg = [msgtype, {
            "content": content_data,
            "nickname": "",
            "headimgurl": "/static/img/oflogo.png",
            "tel": "",
            "time": updatetime,
            "user_id": user_id,
            "sequence": "",
            "comment_id": ""
        }, block_id]
        DataWebSocket.send_to_all(json_encode(msg))
class PageDelDomAPIHandler(WebRequest):
    def post(self):
        if not self.current_user:
            self.finish({"info":"error","about":"no login"})
            return
        user_id = self.current_user["id"]
        block_id = self.get_argument("block_id",None)
        dom_owner = self.get_argument("dom_owner",None)
        dom_current = self.get_argument("dom_current",None)

        block = get_aim(block_id)
        #判断是否为编辑者
        if user_id not in block.get("editors",[block.get("owner",None)]):
        # if block.get("owner",None) != user_id:
            self.finish({"info":"error","about":"no in editors"})
            return
        doms = block.get("doms",[])
        dom_tree = dom_current.split("_")
        dom_aim = None
        doms = block.get("doms",[])

        _doms = doms
        for dom in dom_tree:
            _doms = _doms
            for _dom in _doms:
                if dom == _dom[0]:
                    if dom_owner == _dom[0]:
                        dom_aim = _dom
                        _doms.remove(_dom)
                        break
                    _doms = _dom[5]
                    break
        if not dom_aim:
            self.finish({"info":"error","about":"no dom"})
            return
        dom_content = ""
        updatetime = int(time.time())
        block["doms"] = doms
        block["updatetime"] = updatetime
        update_aim(block_id,block)
        self.finish({"info":"ok",})
        content_data = {
            "dom_current":dom_current,
            "dom_content":dom_content,
        }
        msgtype = "COMMENTPAGEDELDOM"
        msg = [msgtype, {
            "content": content_data,
            "nickname": "",
            "headimgurl": "/static/img/oflogo.png",
            "tel": "",
            "time": updatetime,
            "user_id": user_id,
            "sequence": "",
            "comment_id": ""
        }, block_id]
        DataWebSocket.send_to_all(json_encode(msg))
class PageUpdateHeadimgurlAPIHandler(WebRequest):
    def post(self):
        if not self.current_user:
            self.finish({"info":"error","about":"no login"})
            return
        user_id = self.current_user["id"]
        block_id = self.get_argument("block_id",None)
        dom_content = self.get_argument("dom_content",None)
        
        headimgurl = json_decode(dom_content).get("headimgurl","")
        updatetime = int(time.time())

        block = get_aim(block_id)

        #判断是否为编辑者
        if user_id not in block.get("editors",[block.get("owner",None)]):
        # if block.get("owner",None) != user_id:
            self.finish({"info":"error","about":"no in editors"})
            return
        old_headimgurl = block.get("headimgurl","")
        if headimgurl == old_headimgurl:
            self.finish({"info":"ok","about":"same headimgurl"})
            return
        block["headimgurl"]=headimgurl
        block["updatetime"]=updatetime
        update_aim(block_id,block)
        self.finish({"info":"ok"})
        content_data = {
            "dom_content":dom_content,
        }
        msgtype = "COMMENTPAGEUPDATEHEADIMGURL"
        msg = [msgtype, {
            "content": content_data,
            "nickname": "",
            "headimgurl": "/static/img/oflogo.png",
            "tel": "",
            "time": updatetime,
            "user_id": user_id,
            "sequence": "",
            "comment_id": ""
        }, block_id]
        DataWebSocket.send_to_all(json_encode(msg))

class PageUpdateTitleAPIHandler(WebRequest):
    # @tornado.gen.coroutine
    def post(self):
        if not self.current_user:
            self.finish({"info":"error","about":"no login"})
            return
        user_id = self.current_user["id"]
        block_id = self.get_argument("block_id",None)
        dom_content = self.get_argument("dom_content",None)
        
        title = json_decode(dom_content).get("title","")
        updatetime = int(time.time())

        block = get_aim(block_id)

        #判断是否为编辑者
        if user_id not in block.get("editors",[block.get("owner",None)]):
        # if block.get("owner",None) != user_id:
            self.finish({"info":"error","about":"no in editors"})
            return
        old_title = block.get("title","")
        if title == old_title:
            self.finish({"info":"ok","about":"same title"})
            return
        block["title"]=title
        block["updatetime"]=updatetime
        update_aim(block_id,block)
        self.finish({"info":"ok"})
        content_data = {
            "dom_content":dom_content,
        }
        msgtype = "COMMENTPAGEUPDATETITLE"
        msg = [msgtype, {
            "content": content_data,
            "nickname": "",
            "headimgurl": "/static/img/oflogo.png",
            "tel": "",
            "time": updatetime,
            "user_id": user_id,
            "sequence": "",
            "comment_id": ""
        }, block_id]
        DataWebSocket.send_to_all(json_encode(msg))
class PageUpdateDescAPIHandler(WebRequest):
    # @tornado.gen.coroutine
    def post(self):
        if not self.current_user:
            self.finish({"info":"error","about":"no login"})
            return
        user_id = self.current_user["id"]
        block_id = self.get_argument("block_id",None)
        dom_content = self.get_argument("dom_content",None)
        
        desc = json_decode(dom_content).get("desc","")
        updatetime = int(time.time())

        block = get_aim(block_id)

        #判断是否为编辑者
        if user_id not in block.get("editors",[block.get("owner",None)]):
        # if block.get("owner",None) != user_id:
            self.finish({"info":"error","about":"no in editors"})
            return
        old_desc = block.get("desc","")
        if desc == old_desc:
            self.finish({"info":"ok","about":"same desc"})
            return
        block["desc"]=desc
        block["updatetime"]=updatetime
        update_aim(block_id,block)
        self.finish({"info":"ok"})
        content_data = {
            "dom_content":dom_content,
        }
        msgtype = "COMMENTPAGEUPDATEDESC"
        msg = [msgtype, {
            "content": content_data,
            "nickname": "",
            "headimgurl": "/static/img/oflogo.png",
            "tel": "",
            "time": updatetime,
            "user_id": user_id,
            "sequence": "",
            "comment_id": ""
        }, block_id]
        DataWebSocket.send_to_all(json_encode(msg))
class PageUpdateMainAreaAPIHandler(WebRequest):
    # @tornado.gen.coroutine
    def post(self):
        if not self.current_user:
            self.finish({"info":"error","about":"no login"})
            return
        user_id = self.current_user["id"]
        block_id = self.get_argument("block_id",None)
        dom_content = self.get_argument("dom_content",None)
        
        w = int(json_decode(dom_content).get("text").get("w","1024"))
        h = int(json_decode(dom_content).get("text").get("h","0"))
        updatetime = int(time.time())
        
        block = get_aim(block_id)
        
        #判断是否为编辑者
        if user_id not in block.get("editors",[block.get("owner",None)]):
        # if block.get("owner",None) != user_id:
            self.finish({"info":"error","about":"no in editors"})
            return
        old_main_area = block.get("main_area",{})
        if w == int(old_main_area.get("w","1024")) and h == int(old_main_area.get("h","0")):
            self.finish({"info":"ok","about":"same main_area"})
            return
        block["updatetime"]=updatetime
        block["main_area"]={
            "w":w,
            "h":h,
        }
        update_aim(block_id,block)
        self.finish({"info":"ok"})
        content_data = {
            "dom_content":dom_content,
        }
        msgtype = "COMMENTPAGEMAINAREA"
        msg = [msgtype, {
            "content": content_data,
            "nickname": "",
            "headimgurl": "/static/img/oflogo.png",
            "tel": "",
            "time": updatetime,
            "user_id": user_id,
            "sequence": "",
            "comment_id": ""
        }, block_id]
        DataWebSocket.send_to_all(json_encode(msg))
class PageUpdateGridGraphAPIHandler(WebRequest):
    # @tornado.gen.coroutine
    def post(self):
        if not self.current_user:
            self.finish({"info":"error","about":"no login"})
            return
        user_id = self.current_user["id"]
        block_id = self.get_argument("block_id",None)
        dom_content = self.get_argument("dom_content",None)
        
        w = int(json_decode(dom_content).get("text").get("w","30"))
        h = int(json_decode(dom_content).get("text").get("h","30"))
        updatetime = int(time.time())
        
        block = get_aim(block_id)
        
        #判断是否为编辑者
        if user_id not in block.get("editors",[block.get("owner",None)]):
        # if block.get("owner",None) != user_id:
            self.finish({"info":"error","about":"no in editors"})
            return
        old_grid_graph = block.get("grid_graph",{})
        if w == int(old_grid_graph.get("w","30")) and h == int(old_grid_graph.get("h","30")):
            self.finish({"info":"ok","about":"same grid graph"})
            return
        block["updatetime"]=updatetime
        block["grid_graph"]={
            "w":w,
            "h":h,
        }
        update_aim(block_id,block)
        self.finish({"info":"ok"})
        content_data = {
            "dom_content":dom_content,
        }
        msgtype = "COMMENTPAGEGRIDGRAPH"
        msg = [msgtype, {
            "content": content_data,
            "nickname": "",
            "headimgurl": "/static/img/oflogo.png",
            "tel": "",
            "time": updatetime,
            "user_id": user_id,
            "sequence": "",
            "comment_id": ""
        }, block_id]
        DataWebSocket.send_to_all(json_encode(msg))
class PageUpdateDomsAPIHandler(WebRequest):
    @tornado.gen.coroutine
    def post(self):
        if not self.current_user:
            self.finish({"info":"error","about":"no login"})
            return
        user_id = self.current_user["id"]
        block_id = self.get_argument("block_id",None)
        updates = self.get_argument("updates","[]")
        if updates == "[]":
            self.finish({"info":"error","about":"no update"})
            return
        dom_content = self.get_argument("dom_content",None)
        updates = json_decode(updates)
        updatetime = int(time.time())
        block = get_aim(block_id)
        #判断是否为编辑者
        if user_id not in block.get("editors",[block.get("owner",None)]):
        # if block.get("owner",None) != user_id:
            self.finish({"info":"error","about":"no in editors"})
            return
        doms = block.get("doms",[])
        for dom in doms:
            for update in updates:
                if dom[0] == update["dom_id"]:
                    dom[2]["x"]=update["x"]
                    dom[2]["y"]=update["y"]
                    dom[2]["w"]=update["w"]
                    dom[2]["h"]=update["h"]
        block["doms"]=doms
        block["updatetime"]=updatetime
        update_aim(block_id,block)
        self.finish({"info":"ok"})
        content_data = {
            "updates":updates,
            "dom_content":{
                "uuid":dom_content
            },
        }
        msgtype = "COMMENTPAGEUPDATEDOMS"
        msg = [msgtype, {
            "content": content_data,
            "nickname": "",
            "headimgurl": "/static/img/oflogo.png",
            "tel": "",
            "time": updatetime,
            "user_id": user_id,
            "sequence": "",
            "comment_id": ""
        }, block_id]
        DataWebSocket.send_to_all(json_encode(msg))

class PageUpdateDomAPIHandler(WebRequest):
    @tornado.gen.coroutine
    def post(self):
        if not self.current_user:
            self.finish({"info":"error","about":"no login"})
            return
        user_id = self.current_user["id"]
        block_id = self.get_argument("block_id",None)
        dom_owner = self.get_argument("dom_owner",None)
        dom_current = self.get_argument("dom_current",None)
        dom_position_x = int(float(self.get_argument("dom_position_x","0")))
        dom_position_y = int(float(self.get_argument("dom_position_y","0")))
        dom_position_w = int(float(self.get_argument("dom_position_w","0")))
        dom_position_h = int(float(self.get_argument("dom_position_h","0")))
        dom_position_z = int(float(self.get_argument("dom_position_z","0")))
        dom_scroll = self.get_argument("dom_scroll","")
        dom_scroll_relative = self.get_argument("dom_scroll_relative","")
        
        updatetime = int(time.time())
        
        block = get_aim(block_id)
        
        #判断是否为编辑者
        if user_id not in block.get("editors",[block.get("owner",None)]):
        # if block.get("owner",None) != user_id:
            self.finish({"info":"error","about":"no in editors"})
            return
        dom_tree = dom_current.split("_")
        dom_aim = None
        doms = block.get("doms",[])

        _doms = doms
        for dom in dom_tree:
            _doms = _doms
            for _dom in _doms:
                if dom == _dom[0]:
                    if dom_owner == _dom[0]:
                        dom_aim = _dom
                        dom_aim[2]={
                            "x":dom_position_x,
                            "y":dom_position_y,
                            "w":dom_position_w,
                            "h":dom_position_h,
                            "z":dom_position_z,
                            "s":dom_scroll,
                            "r":dom_scroll_relative,
                        }
                        dom_aim[6]=updatetime
                        break
                    _doms = _dom[5]
                    break
        block["doms"]=doms
        block["updatetime"]=updatetime
        update_aim(block_id,block)
        self.finish({"info":"ok"})
        content_data = {
            "dom_current":dom_current,
            "dom_position_x":dom_position_x,
            "dom_position_y":dom_position_y,
            "dom_position_w":dom_position_w,
            "dom_position_h":dom_position_h,
            "dom_position_z":dom_position_z,
            "dom_scroll":dom_scroll,
            "dom_scroll_relative":dom_scroll_relative,
        }

        msgtype = "COMMENTPAGEUPDATEDOM"
        msg = [msgtype, {
            "content": content_data,
            "nickname": "",
            "headimgurl": "/static/img/oflogo.png",
            "tel": "",
            "time": updatetime,
            "user_id": user_id,
            "sequence": "",
            "comment_id": ""
        }, block_id]
        DataWebSocket.send_to_all(json_encode(msg))
class PageUpdateDomFileAPIHandler(WebRequest):
    def post(self):
        if not self.current_user:
            self.finish({"info":"error","about":"no login"})
            return
        user_id = self.current_user["id"]
        block_id = self.get_argument("block_id",None)
        dom_owner = self.get_argument("dom_owner",None)
        dom_current = self.get_argument("dom_current",None)
        dom_content = self.get_argument("dom_content",None)
        
        updatetime = int(time.time())
        
        block = get_aim(block_id)
        #判断是否为编辑者
        if user_id not in block.get("editors",[block.get("owner",None)]):
            self.finish({"info":"error","about":"no in editors"})
            return
        dom_tree = dom_current.split("_")
        dom_aim = None
        doms = block.get("doms",[])

        _doms = doms
        for dom in dom_tree:
            _doms = _doms
            for _dom in _doms:
                if dom == _dom[0]:
                    if dom_owner == _dom[0]:
                        dom_aim = _dom
                        dom_aim[3] = json_decode(dom_content).get("text",{})
                        dom_aim[6] =updatetime
                        break
                    _doms = _dom[5]
                    break
        block["doms"]=doms
        block["updatetime"]=updatetime

        update_aim(block_id,block)
        self.finish({"info":"ok"})
        content_data = {
            "dom_current":dom_current,
            "dom_content":dom_content,
        }
        msgtype = "COMMENTPAGEUPDATEDOMFILE"
        msg = [msgtype, {
            "content": content_data,
            "nickname": "",
            "headimgurl": "/static/img/oflogo.png",
            "tel": "",
            "time": updatetime,
            "user_id": user_id,
            "sequence": "",
            "comment_id": ""
        }, block_id]
        DataWebSocket.send_to_all(json_encode(msg))
class PageUpdateDomVideoAPIHandler(WebRequest):
    def post(self):
        if not self.current_user:
            self.finish({"info":"error","about":"no login"})
            return
        user_id = self.current_user["id"]
        block_id = self.get_argument("block_id",None)
        dom_owner = self.get_argument("dom_owner",None)
        dom_current = self.get_argument("dom_current",None)
        dom_content = self.get_argument("dom_content",None)
        
        updatetime = int(time.time())
        
        block = get_aim(block_id)
        #判断是否为编辑者
        if user_id not in block.get("editors",[block.get("owner",None)]):
            self.finish({"info":"error","about":"no in editors"})
            return
        dom_tree = dom_current.split("_")
        dom_aim = None
        doms = block.get("doms",[])

        _doms = doms
        for dom in dom_tree:
            _doms = _doms
            for _dom in _doms:
                if dom == _dom[0]:
                    if dom_owner == _dom[0]:
                        dom_aim = _dom
                        dom_aim[3] = json_decode(dom_content).get("text",{})
                        dom_aim[6] =updatetime
                        break
                    _doms = _dom[5]
                    break
        block["doms"]=doms
        block["updatetime"]=updatetime

        update_aim(block_id,block)
        self.finish({"info":"ok"})
        content_data = {
            "dom_current":dom_current,
            "dom_content":dom_content,
        }
        msgtype = "COMMENTPAGEUPDATEDOMVIDEO"
        msg = [msgtype, {
            "content": content_data,
            "nickname": "",
            "headimgurl": "/static/img/oflogo.png",
            "tel": "",
            "time": updatetime,
            "user_id": user_id,
            "sequence": "",
            "comment_id": ""
        }, block_id]
        DataWebSocket.send_to_all(json_encode(msg))
class PageUpdateDomContentAPIHandler(WebRequest):
    # @tornado.gen.coroutine
    def post(self):
        if not self.current_user:
            self.finish({"info":"error","about":"no login"})
            return
        user_id = self.current_user["id"]
        block_id = self.get_argument("block_id",None)
        dom_owner = self.get_argument("dom_owner",None)
        dom_current = self.get_argument("dom_current",None)
        dom_content = self.get_argument("dom_content",None)
        
        updatetime = int(time.time())
        
        block = get_aim(block_id)
        #判断是否为编辑者
        if user_id not in block.get("editors",[block.get("owner",None)]):
            self.finish({"info":"error","about":"no in editors"})
            return
        dom_tree = dom_current.split("_")
        dom_aim = None
        doms = block.get("doms",[])

        update_aim_flag = False
        _doms = doms
        for dom in dom_tree:
            _doms = _doms
            for _dom in _doms:
                if dom == _dom[0]:
                    if dom_owner == _dom[0]:
                        dom_aim = _dom
                        dom_aim_3_text = json_decode(dom_content).get("text","")
                        if dom_aim[3] != dom_aim_3_text:
                            dom_aim[3] = dom_aim_3_text
                            update_aim_flag = True
                        dom_aim[6] =updatetime
                        break
                    _doms = _dom[5]
                    break
        if not update_aim_flag:
            self.finish({"info":"error","about":"same content"})
            return
        block["doms"]=doms
        block["updatetime"]=updatetime

        update_aim(block_id,block)
        self.finish({"info":"ok"})
        content_data = {
            "dom_current":dom_current,
            "dom_content":dom_content,
        }
        msgtype = "COMMENTPAGEUPDATEDOMCONTENT"
        msg = [msgtype, {
            "content": content_data,
            "nickname": "",
            "headimgurl": "/static/img/oflogo.png",
            "tel": "",
            "time": updatetime,
            "user_id": user_id,
            "sequence": "",
            "comment_id": ""
        }, block_id]
        DataWebSocket.send_to_all(json_encode(msg))
class PageUpdateDomIframeAPIHandler(WebRequest):
    def post(self):
        if not self.current_user:
            self.finish({"info":"error","about":"no login"})
            return
        user_id = self.current_user["id"]
        block_id = self.get_argument("block_id",None)
        dom_owner = self.get_argument("dom_owner",None)
        dom_current = self.get_argument("dom_current",None)
        dom_content = self.get_argument("dom_content",None)
        
        updatetime = int(time.time())
        
        block = get_aim(block_id)
        #判断是否为编辑者
        if user_id not in block.get("editors",[block.get("owner",None)]):
            self.finish({"info":"error","about":"no in editors"})
            return
        dom_tree = dom_current.split("_")
        dom_aim = None
        doms = block.get("doms",[])

        _doms = doms
        for dom in dom_tree:
            _doms = _doms
            for _dom in _doms:
                if dom == _dom[0]:
                    if dom_owner == _dom[0]:
                        dom_aim = _dom
                        dom_aim[3] = json_decode(dom_content).get("text",{})
                        dom_aim[6] =updatetime
                        break
                    _doms = _dom[5]
                    break
        block["doms"]=doms
        block["updatetime"]=updatetime
        update_aim(block_id,block)
        self.finish({"info":"ok"})
        content_data = {
            "dom_current":dom_current,
            "dom_content":dom_content,
        }
        msgtype = "COMMENTPAGEUPDATEDOMIFRAME"
        msg = [msgtype, {
            "content": content_data,
            "nickname": "",
            "headimgurl": "/static/img/oflogo.png",
            "tel": "",
            "time": updatetime,
            "user_id": user_id,
            "sequence": "",
            "comment_id": ""
        }, block_id]
        DataWebSocket.send_to_all(json_encode(msg))

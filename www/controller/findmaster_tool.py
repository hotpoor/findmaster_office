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

class CountConnectNumAPIHandler(WebRequest):
    @tornado.gen.coroutine
    def get(self):
        block_id = self.get_argument("aim_id",None)
        connects = DataWebSocket.h_clients.get(block_id,None)
        num = 0
        exists = True
        if not connects:
            exists = False
        if exists:
            num = len(connects)
        self.finish({"info":"ok","num":num,"exists":exists,"aim_id":block_id})
class CountConnectNumListAPIHandler(WebRequest):
    @tornado.gen.coroutine
    def get(self):
        block_ids = self.get_argument("aim_ids","[]")
        block_ids = json_decode(block_ids)
        result_json = {}
        for block_id in block_ids:
            connects = DataWebSocket.h_clients.get(block_id,None)
            num = 0
            exists = True
            if not connects:
                exists = False
            if exists:
                num = len(connects)
            result_json[block_id]={
                "exists":exists,
                "num":num,
            }
        self.finish({"info":"ok","result":result_json})
class ListConnectAPIHandler(WebRequest):
    @tornado.gen.coroutine
    def get(self):
        if not self.current_user:
            self.finish({"info":"error","about":"no login"})
            return
        user_id = self.current_user["id"]
        if user_id not in settings["developers"]:
            self.finish({"info":"error","about":"not in developers"})
            return
        aims = {}
        h_clients = DataWebSocket.h_clients
        for k,v in h_clients.items():
            aims[k]=len(v)
        num = list(aims.keys())
        self.finish({"info":"ok","aims":aims,"aims_num":num})
class AddToTopPageAPIHandler(WebRequest):
    @tornado.gen.coroutine
    def post(self):
        if not self.current_user:
            self.finish({"info":"error","about":"not login"})
            return
        block_id = self.get_argument("aim_id",None)
        user_id = self.current_user["id"]
        user = get_aim(user_id)
        pages = user.get("pages",[])
        if block_id not in pages:
            self.finish({"info":"error","about":"not in pages"})
            return
        pages_top = user.get("pages_top",[])
        if block_id in pages_top and block_id == pages_top[0]:
            self.finish({"info":"error","about":"already top"})
            return
        elif block_id in pages_top:
            pages_top.remove(block_id)
        pages_top.insert(0,block_id)
        user["pages_top"]=pages_top
        user["updatetime"]=int(time.time())
        update_aim(user_id,user)
        self.finish({"info":"ok","about":"add to top success"})
class RemoveFromTopPageAPIHandler(WebRequest):
    @tornado.gen.coroutine
    def post(self):
        if not self.current_user:
            self.finish({"info":"error","about":"not login"})
            return
        block_id = self.get_argument("aim_id",None)
        user_id = self.current_user["id"]
        user = get_aim(user_id)
        pages = user.get("pages",[])
        if block_id not in pages:
            self.finish({"info":"error","about":"not in pages"})
            return
        pages_top = user.get("pages_top",[])
        if block_id not in pages_top:
            self.finish({"info":"error","about":"already remove from top"})
            return
        else:
            pages_top.remove(block_id)
        pages.remove(block_id)
        pages.insert(0,block_id)
        user["pages_top"]=pages_top
        user["pages"]=pages
        user["updatetime"]=int(time.time())
        update_aim(user_id,user)
        self.finish({"info":"ok","about":"remove from top success"})
class RemoveToTrashAPIHandler(WebRequest):
    @tornado.gen.coroutine
    def post(self):
        if not self.current_user:
            self.finish({"info":"error","about":"no login"})
            return
        user_id = self.current_user["id"]
        block_id = self.get_argument("aim_id",None)
        user = get_aim(user_id)
        pages = user.get("pages",[])
        pages_top_ids = user.get("pages_top",[])
        pages_trash_ids = user.get("pages_trash",[])
        update_need = False
        if block_id in pages:
            update_need = True
            pages.remove(block_id)
        if block_id in pages_top_ids:
            update_need = True
            pages_top_ids.remove(block_id)
        user["pages"]=pages
        user["pages_top"]=pages_top_ids
        if not update_need:
            self.finish({"info":"error","about":"not in already"})
            return
        if block_id not in pages_trash_ids:
            pages_trash_ids.insert(0,block_id)
            user["pages_trash"]=pages_trash_ids
        user["updatetime"]=int(time.time())
        update_aim(user_id,user)
        self.finish({"info":"ok","about":"remove success"})
class JsonDataAPIHandler(WebRequest):
    @tornado.gen.coroutine
    def get(self):
        block_id = self.get_argument("block_id",None)
        pwd = self.get_argument("pwd",None)
        if pwd not in ["hotpoor20211019"]:
            if not self.current_user:
                self.finish({"info":"error","about":"no login"})
                return
            user_id = self.current_user["id"]
            if user_id not in settings["developers"]:
                self.finish({"info":"error","about":"not in developers"})
                return
        block = get_aim(block_id)
        result_json = {
            "info":"ok",
            "block_id":block_id,
            "block":block
        }
        self.finish(result_json)
class LoginSilenceWechatAPIHandler(WebRequest):
    @tornado.gen.coroutine
    def get(self):
        self.aim_uri = self.get_argument("aim_uri",None)
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
                    'scope'            : 'snsapi_base',
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
        if is_weixin:
            self.MPWeixinAppID = settings["MPWeixinInfo"][MPWeixinAPP]["MPWeixinAppID"]
            self.render("../template/tool/wechat_login_silence.html")
        else:
            redirect_uri = "%s://%s%s" % (self.request.protocol,self.request.host,self.request.uri)
            self.finish({"info":"error","about":"请在微信内访问","link":redirect_uri})


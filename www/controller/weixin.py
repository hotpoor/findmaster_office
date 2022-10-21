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
import xmltodict

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

from .data import DataWebSocket

weixin_access_token_for_apps = {}
update_access_token_new = "1"

class WeixinJSSDKSign(object):
    def __init__(self, jsapi_ticket, timestamp, url):
        self.ret = {
            'nonceStr': self.__create_nonce_str(),
            'jsapi_ticket': jsapi_ticket,
            'timestamp': timestamp,
            'url': url
        }

    def __create_nonce_str(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))

    def sign(self):
        string = '&'.join(['%s=%s' % (key.lower(), self.ret[key]) for key in sorted(self.ret)])
        self.ret['signature'] = hashlib.sha1(string.encode("utf8")).hexdigest()
        return self.ret

class ShowAccessTokenAPIHandler(WebRequest):
    def get(self):
        password = self.get_argument("pwd","")
        if password != "hotpoorinchina":
            if not self.current_user:
                return
            user_id = self.current_user["id"]
            if not user_id in settings["developers"]:
                return
        weixin_info = weixin_access_token_for_apps
        weixin_info_setting = settings["MPWeixinInfo"]
        self.finish({"data":weixin_info,"data_setting":weixin_info_setting})
class GetWeixinUserInfoAPIHandler(WebRequest):
    @tornado.gen.coroutine
    def get(self):
        app = self.get_argument("app",settings["MPWeixinAppDefault"])
        openid = self.get_argument("openid",None)
        if not openid:
            if not self.current_user:
                self.finish({"info":"error","about":"no openid and no login","data":None})    
                return
            user_id = self.current_user["id"]
            user = get_aim(user_id)
            openid = user.get("weixin_openids",{app:[None]}).get(app,[None])[0]
            if not openid:
                self.finish({"info":"error","about":"current login without openid","data":None})
                return
        accessToken = settings["MPWeixinInfo"][app]["accessToken"]
        accessToken1 = weixin_access_token_for_apps.get(settings["MPWeixinInfo"][app]["MPWeixinID"],{}).get("accessToken",None)
        if accessToken != accessToken1:
            accessToken = accessToken1
            print("accessToken is not accessToken1")
        else:
            print("accessToken is accessToken1")
        http_client = tornado.httpclient.AsyncHTTPClient()
        url = "https://api.weixin.qq.com/cgi-bin/user/info?access_token=%s&openid=%s&lang=zh_CN"%(accessToken,openid)
        response = yield http_client.fetch(url)
        data = tornado.escape.json_decode(response.body)
        print(data)
        self.finish({"info":"ok","about":"get weixin user info success","data":data})

class ServerWeixinAPIHandler(WebRequest):
    MESSAGE_SIGNATURE_TOKEN = ""
    MESSAGE_SIGNATURE_BLOCK_ID = ""
    def check_message_signature(self):
        self.MESSAGE_SIGNATURE_BLOCK_ID = self.get_argument("block_id",None)
        self.MESSAGE_SIGNATURE_TOKEN = self.get_argument("token",None)
        signature = self.get_argument("signature", None)
        timestamp = self.get_argument("timestamp", None)
        nonce = self.get_argument("nonce", None)
        if signature and timestamp and nonce:
            param = sorted([self.MESSAGE_SIGNATURE_TOKEN, timestamp, nonce])
            sha = hashlib.sha1("".join(param).encode("utf8")).hexdigest()
            if sha == signature:
                return True
        return False
    def get(self):
        if self.check_message_signature():
            echostr = self.get_argument("echostr")
            self.finish(echostr)
    @tornado.gen.coroutine
    def post(self):
        self.my_weixin_apps_key_value = {}
        self.my_weixin_apps = []
        if not self.check_message_signature():
            self.finish()
            return
        # if self.MESSAGE_SIGNATURE_TOKEN in ["gh_be9ef987bd2e"]:
        #     wxapp_request = self.request.body
        #     print wxapp_request
        #     print u"=== 来自微信小程序 ==="
        #     self.finish()
        #     return
        request = xmltodict.parse(self.request.body)
        print(request)
        self.finish()



class ShowBatchgetMaterialAPIHandler(WebRequest):
    def get(self):
        self.post()
    @tornado.gen.coroutine
    def post(self):
        if not self.current_user:
            self.finish({"error":"no login"})
            return
        user_id = self.current_user["id"]
        if not user_id in settings["developers"]:
            self.finish({"error":"no developer"})
            return
        access_token = self.get_argument("access_token",None)
        if not access_token:
            self.finish({"error":"no access_token"})
            return
        TYPE = self.get_argument("type",None)
        OFFSET = self.get_argument("offset",None)
        COUNT = self.get_argument("count",None)
        if not TYPE or not OFFSET or not COUNT:
            self.finish({"error":"no data"})
            return
        http_client = tornado.httpclient.AsyncHTTPClient()
        headers = {"Content-type": "application/json", "Accept": "text/plain"}
        url = "https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token="+access_token
        json = {
            "type":TYPE,
            "offset":OFFSET,
            "count":COUNT
        }
        body = json_encode(json)
        request = tornado.httpclient.HTTPRequest(
                    url = url,
                    method = "POST",
                    body = body,
                    headers = headers,
                    validate_cert = False)
        response = yield http_client.fetch(request)
        data = tornado.escape.json_decode(response.body)
        self.finish({"data":data})

@tornado.gen.coroutine
def weixin_JS_SDK_check(weixinID,appID,appSecret,force=False):
    result = conn.query("SELECT * FROM index_weixin_gh WHERE weixin_id = %s and app_id = %s and app_secret = %s and done = 0", weixinID, appID, appSecret)
    if result:
        result_info = result[0]
        accessToken = result_info["access_token"]
        accessTokenTimer = int(result_info["updatetime"])
        ticket = result_info["ticket"]
        owner_id = result_info["user_id"]
        app = result_info["app"]
        name = result_info["name"]
        if not accessTokenTimer:
            accessTokenTimer = 0
        if (int(time.time()) - int(accessTokenTimer)) > 3000 or force == True:
            print("----- xialiwei update -----")
            accessTokenTimer = int(time.time())
            http_client = tornado.httpclient.AsyncHTTPClient()
            url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid="+appID+"&secret="+appSecret
            response = yield http_client.fetch(url)
            data = tornado.escape.json_decode(response.body)
            print(data)
            accessToken = data.get('access_token')
            url = "https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=%s&type=jsapi"%accessToken
            response = yield http_client.fetch(url)
            data = tornado.escape.json_decode(response.body)
            print(data)
            ticket = data.get('ticket')
            conn.execute("UPDATE index_weixin_gh SET access_token = %s, ticket = %s, updatetime = %s WHERE weixin_id = %s and app_id = %s and app_secret = %s and done = 0", accessToken, ticket, accessTokenTimer, weixinID, appID, appSecret)
        print("----- xialiwei weixin_JS_SDK_check -----")
        data = {
            "weixinID": weixinID,
            "appId": appID,
            "appSecret": appSecret,
            "accessToken": accessToken,
            "accessTokenTimer": accessTokenTimer,
            "ticket": ticket,
            "owner": owner_id,
            "name":name,
            "app":app,
        }
        weixin_access_token_for_apps[weixinID] = data
    else:
        data = None

@tornado.gen.coroutine
def update_access_token():
    for app in settings["MPWeixinApps"]:
        weixinID = settings["MPWeixinInfo"][app]["MPWeixinID"]
        appID = settings["MPWeixinInfo"][app]["MPWeixinAppID"]
        appSecret = settings["MPWeixinInfo"][app]["MPWeixinAppSecret"]
        global update_access_token_new
        if update_access_token_new=="1":
            yield weixin_JS_SDK_check(weixinID,appID,appSecret,True)
            update_access_token_new="0"
        else:
            yield weixin_JS_SDK_check(weixinID,appID,appSecret)
        data = weixin_access_token_for_apps.get(weixinID,None)
        if not data:
            return

        settings["MPWeixinInfo"][app]["accessToken"]        = data["accessToken"]
        settings["MPWeixinInfo"][app]["ticket"]             = data["ticket"]
        settings["MPWeixinInfo"][app]["accessTokenTimer"]   = data["accessTokenTimer"]
        print(settings["MPWeixinInfo"][app]["accessToken"])
        print(data["accessToken"])

tornado.ioloop.PeriodicCallback(update_access_token, 3600*1000).start()
tornado.ioloop.IOLoop.instance().add_callback(update_access_token)

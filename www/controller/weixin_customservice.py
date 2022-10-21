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

class KfsessionCreateAPIHandler(WebRequest):
    def get(self):
        self.post()
    @tornado.gen.coroutine
    def post(self):
        access_token = self.get_argument("access_token",None)
        kf_account = self.get_argument("kf_account",None)
        openid = self.get_argument("openid",None)
        if not self.current_user:
            self.finish({"error":"no login"})
            return
        user_id = self.current_user["id"]
        if not user_id in settings["developers"]:
            self.finish({"error":"no developer"})
            return
        if not access_token:
            self.finish({"error":"no access_token"})
            return
        if not openid or not kf_account:
            self.finish({"error":"no data"})
            return
        http_client = tornado.httpclient.AsyncHTTPClient()
        headers = {"Content-type": "application/json", "Accept": "text/plain"}
        url = "https://api.weixin.qq.com/customservice/kfsession/create?access_token="+access_token
        json = {
            "kf_account":kf_account,
            "openid":openid,
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
class KfsessionCloseAPIHandler(WebRequest):
    def get(self):
        self.post()
    @tornado.gen.coroutine
    def post(self):
        access_token = self.get_argument("access_token",None)
        kf_account = self.get_argument("kf_account",None)
        openid = self.get_argument("openid",None)
        if not self.current_user:
            self.finish({"error":"no login"})
            return
        user_id = self.current_user["id"]
        if not user_id in settings["developers"]:
            self.finish({"error":"no developer"})
            return
        if not access_token:
            self.finish({"error":"no access_token"})
            return
        if not openid or not kf_account:
            self.finish({"error":"no data"})
            return
        http_client = tornado.httpclient.AsyncHTTPClient()
        headers = {"Content-type": "application/json", "Accept": "text/plain"}
        url = "https://api.weixin.qq.com/customservice/kfsession/close?access_token="+access_token
        json = {
            "kf_account":kf_account,
            "openid":openid,
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
class MsgrecordGetmsgListAPIHandler(WebRequest):
    def get(self):
        self.post()
    @tornado.gen.coroutine
    def post(self):
        access_token = self.get_argument("access_token",None)
        starttime = self.get_argument("starttime",None)
        endtime = self.get_argument("endtime",None)
        msgid = self.get_argument("msgid",None)
        number = self.get_argument("number",None)
        if not self.current_user:
            self.finish({"error":"no login"})
            return
        user_id = self.current_user["id"]
        if not user_id in settings["developers"]:
            self.finish({"error":"no developer"})
            return
        if not access_token:
            self.finish({"error":"no access_token"})
            return
        if not starttime or not endtime or not msgid or not number:
            self.finish({"error":"no data"})
            return
        http_client = tornado.httpclient.AsyncHTTPClient()
        headers = {"Content-type": "application/json", "Accept": "text/plain"}
        url = "https://api.weixin.qq.com/customservice/msgrecord/getmsglist?access_token="+access_token
        json = {
            "starttime": int(starttime),
            "endtime": int(endtime),
            "msgid": int(msgid),
            "number": int(number),
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

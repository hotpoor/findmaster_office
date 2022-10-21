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

class GetUserPlusInfoAPIHandler(WebRequest):
    @tornado.gen.coroutine
    def get(self):
        if not self.current_user:
            self.finish({"info":"error","about":"no login"})
            return
        aim_id = self.get_argument("aim_id",None)
        if not aim_id:
            self.finish({"info":"error","about":"no aim_id"})
            return
        aim = get_aim(aim_id)
        if not aim:
            self.finish({"info":"error","about":"no aim"})
            return
        if aim.get("type",None) not in ["user"]:
            self.finish({"info":"error","about":"not a user"})
            return
        plus_info = aim.get("plus_info",{})
        self.finish({"info":"ok","about":"success","plus_info":plus_info})
class UpdateUserPlusInfoAPIHandler(WebRequest):
    def post(self):
        if not self.current_user:
            self.finish({"info":"error","about":"no login"})
            return
        aim_id = self.get_argument("aim_id",None)
        k = self.get_argument("k",None)
        v = self.get_argument("v",None)
        if not aim_id:
            self.finish({"info":"error","about":"no aim_id"})
            return
        user_id = self.current_user["id"]
        if user_id != aim_id:
            if user_id not in settings["developers"]:
                self.finish({"info":"error","about":"not in developers"})
                return
        aim = get_aim(aim_id)
        if not aim:
            self.finish({"info":"error","about":"no aim"})
            return
        if aim.get("type",None) not in ["user"]:
            self.finish({"info":"error","about":"not a user"})
            return
        plus_info = aim.get("plus_info",{})
        plus_info_v_old = plus_info.get(k,"")
        if plus_info_v_old == v:
            self.finish({"info":"ok","about":"same value","plus_info":plus_info})
            return
        plus_info[k]=v
        aim["plus_info"]=plus_info
        aim["updatetime"]=int(time.time())
        update_aim(aim_id,aim)
        self.finish({"info":"ok","about":"success","plus_info":plus_info})


class GetUserInfoAPIHandler(WebRequest):
    @tornado.gen.coroutine
    def get(self):
        if not self.current_user:
            self.finish({"info":"ok","name":"未登录","headimgurl":"/static/img/msh_icon/person.png"})
            return
        user_id = self.current_user["id"]
        user = get_aim(user_id)
        name = user.get("name","暂无昵称")
        email = user.get("email","暂无邮箱")
        headimgurl = user.get("headimgurl","/static/img/msh_icon/person.png")
        self.finish({"info":"ok","name":name,"headimgurl":headimgurl,"email":email})
class GetUserTokenCountAPIHandler(WebRequest):
    @tornado.gen.coroutine
    def get(self):
        if not self.current_user:
            self.finish({"info":"error","about":"no login"})
            return
        app = self.get_argument("app",settings["MPWeixinAppDefault"])
        user_id = self.current_user["id"]
        user = get_aim(user_id)

        token_info_id = user.get("msh_token_info",None)
        if not token_info_id:
            goods = user.get("msh_qrcodepackage",[])
            token_add_history = []
            for good in goods:
                if len(good)==3:
                    good_id = "QRCODE_%s_%s"%(good[0],good[1])
                    add_time = good[2]
                    token_amount = 69
                else:
                    good_id = "QRCODE_%s_%s"%(good[0],good[1])
                    add_time = good[2]
                    token_amount = good[3]
                token_add_history.insert(0,["GOOD",token_amount,good_id,add_time,{}])
            token_info = {
                "owner":user_id,
                "subtype":"msh_token_info",
                "token_add_list":{
                    "goods":goods,
                    "dailies":[],
                    "articles":[],
                },
                "token_add_history":token_add_history,
            }
            [token_info_id,token_info] = nomagic.block.create_block(token_info)
            user["msh_token_info"]=token_info_id
            update_aim(user_id,user)
        else:
            token_info = get_aim(token_info_id)
        token_count = 0
        for token_add_item in token_info.get("token_add_history",[]):
            token_count += int(token_add_item[1])
        self.finish({"info":"ok","token_count":token_count})
class CheckDailyAPIHandler(WebRequest):
    @tornado.gen.coroutine
    def post(self):
        if not self.current_user:
            self.finish({"info":"error","about":"no login"})
            return
        app = self.get_argument("app",settings["MPWeixinAppDefault"])
        user_id = self.current_user["id"]
        user = get_aim(user_id)
        token_info_id = user.get("msh_token_info",None)
        if not token_info_id:
            goods = user.get("msh_qrcodepackage",[])
            token_add_history = []
            for good in goods:
                if len(good)==3:
                    good_id = "QRCODE_%s_%s"%(good[0],good[1])
                    add_time = good[2]
                    token_amount = 69
                else:
                    good_id = "QRCODE_%s_%s"%(good[0],good[1])
                    add_time = good[2]
                    token_amount = good[3]
                token_add_history.insert(0,["GOOD",token_amount,good_id,add_time,{}])
            token_info = {
                "owner":user_id,
                "subtype":"msh_token_info",
                "token_add_list":{
                    "goods":goods,
                    "dailies":[],
                    "articles":[],
                },
                "token_add_history":token_add_history,
            }
            [token_info_id,token_info] = nomagic.block.create_block(token_info)
            user["msh_token_info"]=token_info_id
            update_aim(user_id,user)
        else:
            token_info = get_aim(token_info_id)

        token_add_list = token_info.get("token_add_list",{})
        dailies = token_add_list.get("dailies",[])
        time_now = int(time.time())
        token_amount = 1
        daily_str = "add one"
        if len(dailies)>0:
            last_daily = dailies[0]
            last_day = int((int(last_daily) + 8*60*60)/86400)
            time_now_day = int((int(time_now) + 8*60*60)/86400)
            print("last_day",last_day)
            print("time_now_day",time_now_day)
            print("time_now_day - last_day",time_now_day - last_day)
            if time_now_day - last_day < 1:
                self.finish({"info":"ok","about":"already checked","last_daily":last_daily})
                return
        dailies.insert(0,time_now)
        if len(dailies)>6:
            token_amount = 10
            daily_str = "add one with 10, great 7 day"
            dailies_check = dailies[1:7]
            dailies_check_last = int(time_now)
            for dailies_check_item in dailies_check:
                time_check = int((int(dailies_check_last)+8*60*60)/86400) - int((int(dailies_check_item)+8*60*60)/86400)
                if time_check > 1:
                    token_amount = 1
                    daily_str = "add one"
                    break
                dailies_check_last = dailies_check_item
        token_add_list["dailies"] = dailies
        token_info["token_add_list"]=token_add_list
        token_add_history = token_info.get("token_add_history",[])
        token_add_history.insert(0,["DAILY",token_amount,daily_str,time_now,{}])
        token_info["token_add_history"]=token_add_history
        update_aim(token_info_id,token_info)
        token_count = 0
        for token_add_item in token_info.get("token_add_history",[]):
            token_count += int(token_add_item[1])
        self.finish({"info":"ok","about":"check daily success","last_daily":time_now,"token_amount":token_amount,"token_count":token_count})




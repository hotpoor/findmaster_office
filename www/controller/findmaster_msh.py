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
class CreateBlockAPIHandler(WebRequest):
    @tornado.gen.coroutine
    def post(self):
        if not self.current_user:
            self.finish({"info":"error","about":"no login"})
            return
        user_id = self.current_user["id"]
        if user_id not in settings["developers"]:
            self.finish({"info":"error","about":"no permission"})
            return
        subtype = self.get_argument("subtype","msh_block")
        title = self.get_argument("title","new title")
        if subtype in ["msh_qrcodepackages"]:
            amount = self.get_argument("amount",None)
            if not amount:
                self.finish({"info":"error","about":"no amount"})
                return
            amount = int(amount)
            block = {
                "title":title,
                "owner":user_id,
                "subtype":subtype,
                "qrcodepackages":[],
                "amount":amount,
                "amountcreated":0,
                "amountused":0,
            }
            [block_id,block]=nomagic.block.create_block(block)
            createtime = int(time.time())
            conn.execute("INSERT INTO index_qrcodepackages (block_id,about,user_id,amount,amountcreated,amountused,status,createtime,updatetime) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)", block_id, title, user_id, amount, 0, 0, "", createtime, createtime)
            self.finish({"info":"ok","about":"new block","entity_id":block_id})
            return
        elif subtype in ["msh_qrcodepackage"]:
            qrcodepackages_entity_id = self.get_argument("aim_id",None)
            block = {
                "title":title,
                "owner":user_id,
                "subtype":subtype,
                "qrcodepackages_entity":qrcodepackages_entity_id
            }
            [block_id,block]=nomagic.block.create_block(block)

            qrcodepackages_entity = get_aim(qrcodepackages_entity_id)
            qrcodepackages = qrcodepackages_entity.get("qrcodepackages",[])
            qrcodepackages.append(block_id)
            qrcodepackages_entity["qrcodepackages"] = qrcodepackages
            update_aim(qrcodepackages_entity_id,qrcodepackages_entity)

            self.finish({"info":"ok","about":"new block","entity_id":block_id})
            return
        else:   
            block = {
                "title":title,
                "owner":user_id,
                "subtype":subtype,
            }
            [block_id,block]=nomagic.block.create_block(block)
            self.finish({"info":"ok","about":"new block","entity_id":block_id})
            return

class SetBlockRedirectAPIHandler(WebRequest):
    def post(self):
        if not self.current_user:
            self.finish({"info":"error","about":"no login"})
            return
        user_id = self.current_user["id"]
        block_id = self.get_argument("block_id",None)
        url = self.get_argument("url",None)
        block = get_aim(block_id)
        if not block:
            self.finish({"info":"error","about":"no block"})
            return
        owner = block.get("owner",None)
        if user_id not in [owner]:
            self.finish({"info":"error","about":"not owner"})
            return
        redirect_url = block.get("redirect_url",None)
        redirect_url = url
        block["redirect_url"] = redirect_url
        block["updatetime"] = int(time.time())
        update_aim(block_id,block)
        self.finish({"info":"ok","about":"update redirect url success","redirect_url":redirect_url})


class CreateQrcodeAPIHandler(WebRequest):
    @tornado.gen.coroutine
    def post(self):
        if not self.current_user:
            self.finish({"info":"error","about":"no login"})
            return
        user_id = self.current_user["id"]
        if user_id not in settings["developers"]:
            self.finish({"info":"error","about":"no permission"})
            return
        block_id = self.get_argument("block_id",None)
        num = int(self.get_argument("num","1"))
        block = get_aim(block_id)
        if block.get("subtype",None) not in ["msh_qrcodepackage"]:
            self.finish({"info":"error","about":"error block"})
            return
        qrcodes = block.get("qrcodes",[])
        used_qrcodes = block.get("used_qrcodes",[])
        bad_qrcodes = []
        for qrcode_num in range(0,num):
            while True:
                bad_qrcode = "".join(random.choice(string.ascii_lowercase+string.digits) for _ in range(32))
                if bad_qrcode not in qrcodes and bad_qrcode not in used_qrcodes:
                    break
            qrcodes.insert(0,bad_qrcode)
            bad_qrcodes.insert(0,bad_qrcode)
        qrcode_urls = ["https://msh.xialiwei.com/api/msh/qrcode/%s/%s"%(block_id,b) for b in bad_qrcodes]
        block["qrcodes"]=qrcodes
        block["updatetime"]=int(time.time())
        update_aim(block_id,block)
        self.finish({"info":"ok","qrcode":bad_qrcode,"block_id":block_id,"qrcode_urls":qrcode_urls})

class QrcodeAPIHandler(WebRequest):
    @tornado.gen.coroutine
    def get(self,block_id,qrcode):
        block = get_aim(block_id)
        if not block:
            self.redirect("/home/page/25290ab25c4f4934b398df8a36d67221")
            return
        qrcodes = block.get("qrcodes",[])
        used_qrcodes = block.get("used_qrcodes",[])
        if qrcode in used_qrcodes:
            self.redirect("/home/page/6ed6ca36e45a470bbde30e6552bb128f")
            return
        if qrcode not in qrcodes:
            self.redirect("/home/page/0d737d9ed3f2496793dcf89a4849554b")
            return
        redirect_url = block.get("redirect_url",None)
        if not redirect_url:
            self.redirect("/home/page/bf3dfd1f3af941d08e8ab802f88c28aa?b_id=%s&q_id=%s"%(block_id,qrcode))
            return
        if "?" not in redirect_url:
            redirect_url = "%s?"%redirect_url
        redirect_url = "%s&b_id=%s&q_id=%s"%(redirect_url,block_id,qrcode)
        self.redirect(redirect_url)

class QrcodeCheckAPIHandler(WebRequest):
    # @tornado.gen.coroutine
    def post(self):
        if not self.current_user:
            self.finish({"info":"error","about":"no login"})
            return
        user_id = self.current_user["id"]
        block_id = self.get_argument("block_id",None)
        qrcode = self.get_argument("qrcode",None)
        block = get_aim(block_id)
        if not block:
            self.finish({"info":"error","about":"no block"})
            return
        qrcodes = block.get("qrcodes",[])
        used_qrcodes = block.get("used_qrcodes",[])
        if qrcode in used_qrcodes:
            self.finish({"info":"error","about":"already used"})
            return
        if qrcode not in qrcodes:
            self.finish({"info":"error","about":"no qrcode"})
            return
        qrcodes.remove(qrcode)
        used_qrcodes.insert(0,qrcode)
        block["qrcodes"]=qrcodes
        block["used_qrcodes"]=used_qrcodes
        updatetime = int(time.time())
        block["updatetime"]=updatetime
        token_amount = int(block.get("token_amount",69))
        update_aim(block_id,block)
        user = get_aim(user_id)
        msh_qrcodepackage = user.get("msh_qrcodepackage",[])
        msh_qrcodepackage.insert(0,[block_id,qrcode,updatetime,token_amount])
        user["msh_qrcodepackage"]=msh_qrcodepackage
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
            # update_aim(user_id,user)
        else:
            token_info = get_aim(token_info_id)
            token_add_list = token_info.get("token_add_list",{})
            token_add_list_goods = token_add_list.get("goods",[])
            token_add_list_goods.insert(0,[block_id,qrcode,updatetime,token_amount])
            token_add_list["goods"]=token_add_list_goods
            token_info["token_add_list"]=token_add_list
            token_add_history = token_info.get("token_add_history",[])
            good_id = "QRCODE_%s_%s"%(block_id,qrcode)
            token_add_history.insert(0,["GOOD",token_amount,good_id,updatetime,{}])
            token_info["token_add_history"]=token_add_history
            update_aim(token_info_id,token_info)
        update_aim(user_id,user)
        self.finish({"info":"ok","about":"insert user msh_qrcodepackage success"})

class CheckLevelAPIHandler(WebRequest):
    @tornado.gen.coroutine
    def get(self):
        if not self.current_user:
            openid = self.get_argument("openid",None)
            app = self.get_argument("app",None)
            login = "weixin:%s_@@_%s"%(settings["MPWeixinInfo"][app]["MPWeixinID"],openid)
            result = conn.query("SELECT * FROM index_login WHERE login=%s",login)
            if not result:
                self.finish({"info":"error","about":"msh not login"})
                return
            user_id = result[0].get("entity_id",None)
        else:
            user_id = self.current_user["id"]
        user = get_aim(user_id)
        msh_qrcodepackage = user.get("msh_qrcodepackage",[])
        self.finish({"info":"ok","about":"check success","msh_qrcodepackage_num":len(msh_qrcodepackage)})




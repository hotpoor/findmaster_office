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
import nomagic.group
import nomagic.comment
from nomagic.cache import get_user, get_users, update_user, get_doc, get_docs, update_doc, get_aim, get_aims, update_aim, get_entity, get_entities, update_entity
from nomagic.cache import BIG_CACHE
from setting import settings
from setting import conn

# from user_agents import parse as uaparse #早年KJ用来判断设备使用

from .base import WebRequest
from .base import WebSocket
import pymail

from .data import DataWebSocket

class PageHollowsAPIHandler(WebRequest):
    def get(self):
        block_id = self.get_argument("block_id",None)
        block = get_aim(block_id)
        hollows = block.get("hollows",[])
        self.finish({"info":"ok","about":"hollows","hollows":hollows})

class PageAddHollowAPIHandler(WebRequest):
    def post(self):
        if not self.current_user:
            self.finish({"info":"ok","about":"no login"})
            return
        user_id = self.current_user["id"]
        block_id = self.get_argument("block_id",None)
        aim_hollow_id = self.get_argument("aim_hollow_id",None)

        block = get_aim(block_id)
        editors = block.get("editors",[block.get("owner",None)])
        hollows = block.get("hollows",[])
        updatetime = int(time.time())
        # permission = block.get("permission","private")
        if user_id not in editors and user_id not in settings["developers"]:
            self.finish({"info":"ok","about":"current user not in editors"})
            return
        if aim_hollow_id in hollows:
            self.finish({"info":"ok","about":"already in hollows"})
            return
        else:
            hollows.append(aim_hollow_id)
            block["hollows"]=hollows
            block["updatetime"]=updatetime
            update_aim(block_id,block)
            self.finish({"info":"ok","about":"add one hollow","aim_hollow_id":aim_hollow_id})
        content_data = {
            "aim_hollow_id":aim_hollow_id,
            "action":"add hollow"
        }
        msgtype = "COMMENTPAGEADDHOLLOW"
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

class PageDelHollowAPIHandler(WebRequest):
    def post(self):
        if not self.current_user:
            self.finish({"info":"ok","about":"no login"})
            return
        user_id = self.current_user["id"]
        block_id = self.get_argument("block_id",None)
        aim_hollow_id = self.get_argument("aim_hollow_id",None)

        block = get_aim(block_id)
        editors = block.get("editors",[block.get("owner",None)])
        hollows = block.get("hollows",[])
        updatetime = int(time.time())
        # permission = block.get("permission","private")
        if user_id not in editors and user_id not in settings["developers"]:
            self.finish({"info":"ok","about":"current user not in editors"})
            return
        if aim_hollow_id not in hollows:
            self.finish({"info":"ok","about":"already not in hollows"})
            return
        else:
            hollows.remove(aim_hollow_id)
            block["hollows"]=hollows
            block["updatetime"]=updatetime
            update_aim(block_id,block)
            self.finish({"info":"ok","about":"del one hollow","aim_hollow_id":aim_hollow_id})
        content_data = {
            "aim_hollow_id":aim_hollow_id,
            "action":"del hollow"
        }
        msgtype = "COMMENTPAGEDELHOLLOW"
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
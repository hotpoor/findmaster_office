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

def find_dict_with_list(list_now,result_list=[]):
    for i in list_now:
        if not isinstance(i,dict):
            result_list.append(i)
            continue
        key = list(i.keys())[0]
        result_list.append(key)
        result_list = find_dict_with_list(i.get(key,[]),result_list)
    return result_list

def find_dict_add_folder(list_now,key,add_folder_key):
    for i in list_now:
        if not isinstance(i,dict):
            continue
        key_now = list(i.keys())[0]
        if key_now == key:
            i[key_now].insert(0,{add_folder_key:[]})
        else:
            i[key_now] = find_dict_add_folder(i[key_now],key,add_folder_key)
    return list_now
def find_dict_add_block_id(list_now,key,add_block_id):
    for i in list_now:
        if not isinstance(i,dict):
            continue
        key_now = list(i.keys())[0]
        if key_now == key:
            if add_block_id not in i[key_now]:
                i[key_now].insert(0,add_block_id)
        else:
            i[key_now] = find_dict_add_block_id(i[key_now],key,add_block_id)
    return list_now

class OfficeAddPageAPIHandler(WebRequest):
    def post(self):
        if not self.current_user:
            self.finish({"info":"error","about":"no login"})
            return
        user_id = self.current_user["id"]
        title = self.get_argument("title","new page")
        desc = self.get_argument("desc","this is a new page")
        user = get_aim(user_id)
        aim_folder_id = self.get_argument("aim_folder_id",None)
        office_entity_id = user.get("office_entity",None)
        if not office_entity_id:
            self.finish({"info":"error","about":"no office_entity"})
            return
        office_entity = get_aim(office_entity_id)
        dashboard_map = office_entity.get("dashboard_map",[])
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
        dashboard_map_update = False
        dashboard_map_old = copy.deepcopy(dashboard_map)
        if not aim_folder_id:
            dashboard_map.insert(0,block_id)
            dashboard_map_update = True
        else:
            dashboard_map_new = find_dict_add_block_id(dashboard_map,aim_folder_id,block_id)
            if dashboard_map_new != dashboard_map_old:
                dashboard_map_update = True
                dashboard_map = dashboard_map_new
        if not dashboard_map_update:
            self.finish({"info":"error","about":"not update"})
            return
        office_entity["dashboard_map"]=dashboard_map
        update_aim(office_entity_id,office_entity)
        self.finish({"info":"ok","about":"create new page success","block_id":block_id,"aim_folder_id":aim_folder_id})

class OfficeAddFolderAPIHandler(WebRequest):
    def post(self):
        if not self.current_user:
            self.finish({"info":"error","about":"no login"})
            return
        folder_title = self.get_argument("title","Folder·文件夹")
        folder_desc = self.get_argument("desc","Folder·文件夹")
        aim_folder_id = self.get_argument("aim_folder_id",None)
        user_id = self.current_user["id"]
        user = get_aim(user_id)
        office_entity_id = user.get("office_entity",None)
        if not office_entity_id:
            self.finish({"info":"error","about":"no office_entity"})
            return
        office_entity = get_aim(office_entity_id)
        dashboard_map = office_entity.get("dashboard_map",[])
        block = {
            "owner":user_id,
            "subtype":"office_folder",
            "title":folder_title,
            "desc":folder_desc,
            "updatetime":int(time.time())
        }
        [folder_id,folder]=nomagic.block.create_block(block)
        folder_info = {folder_id:[]}
        dashboard_map_update = False
        dashboard_map_old = copy.deepcopy(dashboard_map)
        if not aim_folder_id:
            dashboard_map.insert(0,folder_info)
            dashboard_map_update = True
        else:
            dashboard_map_new = find_dict_add_folder(dashboard_map,aim_folder_id,folder_id)
            if dashboard_map_new != dashboard_map_old:
                dashboard_map_update = True
                dashboard_map = dashboard_map_new
        if not dashboard_map_update:
            self.finish({"info":"error","about":"not update"})
            return
        office_entity["dashboard_map"]=dashboard_map
        update_aim(office_entity_id,office_entity)
        finish_json = {
            "info":"ok",
            "about":"add folder success",
            "dashboard_map":dashboard_map,
            "folder_id":folder_id,
            "folder":folder,
            "aim_folder_id":aim_folder_id,
        }
        self.finish(finish_json)

class OfficeListAPIHandler(WebRequest):
    def get(self):
        if not self.current_user:
            self.finish({"info":"error","about":"no login"})
            return
        user_id = self.current_user["id"]
        user = get_aim(user_id)
        office_entity_id = user.get("office_entity",None)
        if not office_entity_id:
            block = {
                "owner":user_id,
                "subtype":"office_entity",
                "title":"Office Entity",
                "desc":"A office entity. ",
                "docs":[],
                "folders":[],
                "dashboard_map":[],
                "updatetime":int(time.time())
            }
            [office_entity_id,office_entity]=nomagic.block.create_block(block)
            user["office_entity"]=office_entity_id
            update_aim(user_id,user)
        else:
            office_entity = get_aim(office_entity_id)
        dashboard_map = office_entity.get("dashboard_map",[])
        block_ids = []
        block_ids = find_dict_with_list(dashboard_map,block_ids)
        block_ids = list(set(block_ids))
        finish_json = {
            "info":"ok",
            "about":"success",
            "dashboard_map":dashboard_map,
            "block_id":office_entity_id,
            "block_ids":block_ids
        }
        self.finish(finish_json)

class HomeHandler(WebRequest):
    @tornado.gen.coroutine
    def get(self):
        if not self.current_user:
            redirect_uri = "%s://%s%s" % (self.request.protocol,self.request.host,self.request.uri)
            args = {
                'redirect_uri': redirect_uri,
            }
            url = '/home/start?' + urllib.parse.urlencode(sorted(args.items())) + ''
            self.redirect(url)
            return
        is_weixin = False
        if "Mobile" in self.request.headers.get("User-Agent", "") and "MicroMessenger" in self.request.headers.get("User-Agent", ""):
            is_weixin = True
        self.is_weixin = is_weixin
        self.user_id = self.current_user["id"]
        user = get_aim(self.user_id)
        self.version = settings["version"]
        MPWeixinAPP = self.get_argument('app',settings["MPWeixinAppDefault"])
        self.findmaster_app = MPWeixinAPP
        self.user_headimgurl = user.get("headimgurl","/static/img/headimgurl.png")


        block_id = self.user_id
        websocket_protocol = "ws" if self.request.protocol == "http" else "wss"
        aim_host = self.request.host
        self.websocket_url = "%s://%s/api/data/ws?aim_id=%s" % (websocket_protocol, aim_host, block_id)
        self.host_url = "%s://%s"%(self.request.protocol,aim_host)
        self.render("../template/office/home.html")
class StartHandler(WebRequest):
    @tornado.gen.coroutine
    def get(self):
        self.redirect_uri = self.get_argument("redirect_uri","/")
        if not self.current_user:
            is_weixin = False
            if "Mobile" in self.request.headers.get("User-Agent", "") and "MicroMessenger" in self.request.headers.get("User-Agent", ""):
                is_weixin = True
            self.is_weixin = is_weixin

            self.user_id = "no_login:%s"%str(time.time())
            self.version = settings["version"]
            self.findmaster_app = settings["MPWeixinAppDefault"]
            block_id = "OFFICE"
            websocket_protocol = "ws" if self.request.protocol == "http" else "wss"
            aim_host = self.request.host
            self.websocket_url = "%s://%s/api/data/ws?aim_id=%s" % (websocket_protocol, aim_host, block_id)
            self.host_url = "%s://%s"%(self.request.protocol,aim_host)
            self.render("../template/office/start.html")
            return
        if "/home/start?" in self.redirect_uri:
            self.redirect("/home/office")
            return
        self.redirect(self.redirect_uri)
class BlockInfosAPIHandler(WebRequest):
    @tornado.gen.coroutine
    def get(self):
        if not self.current_user:
            self.finish({"info":"error","about":"no login"})
            return
        block_ids = json_decode(self.get_argument("block_ids",[]))
        block_ids = list(set(block_ids))
        blocks = get_aims(block_ids)
        result_json = {}
        for block_item in blocks:
            block_id = block_item[0]
            block = block_item[1]
            result = {
                "title":block.get("title",""),
                "subtype":block.get("subtype",None),
                "desc":block.get("desc",""),
                "updatetime":block.get("updatetime",None),
            }
            result_json[block_id]=result
        self.finish({"info":"ok","about":"success","result_json":result_json})
class UpdateInfoAPIHandler(WebRequest):
    def post(self):
        if not self.current_user:
            self.finish({"info":"error","about":"no login"})
            return
        block_id = self.get_argument("block_id",None)
        key = self.get_argument("key",None)
        value = self.get_argument("value",None)
        user_id = self.current_user["id"]
        if not key or not value:
            self.finish({"info":"error","about":"no key or value"})
            return
        block = get_aim(block_id)
        if not block:
            self.finish({"info":"error","about":"no block"})
            return
        if user_id != block.get("owner",None) and user_id not in block.get("editors",[]):
            self.finish({"info":"error","about":"no edit permission"})
            return
        if key not in ["title","desc"]:
            self.finish({"info":"error","about":"not allow keys"})
            return
        old_value = block.get(key,"")
        if old_value == value:
            self.finish({"info":"ok","about":"same value"})
            return
        block[key] = value
        block["updatetime"]=int(time.time())
        update_aim(block_id,block)
        self.finish({"info":"ok","about":"update success"})



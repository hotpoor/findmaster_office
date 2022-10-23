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

import jieba

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
class SearchAddFreePageAPIHandler(WebRequest):
    @tornado.gen.coroutine
    def post(self):
        token = self.get_argument("token","")
        if token not in ["xialiwei_follows_god"]:
            self.finish({"info":"error","about":"no login"})
            return
        user_id = self.get_argument("user_id","")
        # if not self.current_user:
        #     self.finish({"info":"error","about":"no login"})
        #     return
        # user_id = self.current_user["id"]
        block_id = self.get_argument("block_id",None)
        search_type = self.get_argument("type",None)
        search_content = self.get_argument("search",None)
        block_id_sequence = self.get_argument("block_id_sequence",None)
        if search_type in ["sequence"]:
            block_id_sequence_all = "%s_%s"%(block_id,block_id_sequence)
        if search_type not in settings["search_type"]:
            self.finish({"info":"error","about":"no in allowed"})
            return
        if not search_content:
            self.finish({"info":"error","about":"no content"})
            return
        if not block_id:
            self.finish({"info":"error","about":"no block_id"})
            return
        block = get_aim(block_id)
        if not block:
            self.finish({"info":"error","about":"no block"})
            return
        editors = block.get("editors",[block.get("owner",None)])
        if user_id not in editors and user_id not in settings["developers"]:
            self.finish({"info":"error","about":"current user not in editors"})
            return
        for current_dom in block.get("doms",[]):
            block_id_sequence = current_dom[0]
            block_id_sequence_all = "%s_%s"%(block_id,block_id_sequence)
            search_content = current_dom[3]

            search_content = search_content.lower()
            search_content_list_no = settings["search_no_str"]
            search_content_list_no = set(list(search_content_list_no))
            search_content_list = set(jieba.lcut(search_content))
            search_content_list = tuple(search_content_list-search_content_list_no)
            result = conn.query("SELECT * FROM index_search WHERE word in %s",search_content_list)
            result_json = {}
            result_has = []
            word_ids = []
            for item in result:
                item_word = item.get("word",None)
                item_entity_id = item.get("entity_id",None)
                word_ids.append(item_entity_id)
                result_has.append(item_word)
            not_result_has = set(search_content_list)-set(result_has)
            block_update = False
            for word in not_result_has:
                block_id_sequence_list = []
                if search_type in ["sequence"]:
                    block_id_sequence_list = [block_id_sequence_all]
                search_block = {
                    "word":word,
                    "owner":settings["developers"][0],
                    "subtype":"search",
                    "search_data":{
                        search_type:[block_id],
                        "block_id_sequence":block_id_sequence_list,
                    },
                    "entities":[block_id],
                }

                [search_block_id,search_block]=nomagic.block.create_block(search_block)
                conn.execute("INSERT INTO index_search (word, entity_id) VALUES(%s, %s)", word, search_block_id)
                block_update = True
            search_blocks = get_aims(word_ids)
            
            for search_block in search_blocks:
                search_block_id = search_block[0]
                search_block_body = search_block[1]
                search_block_update = False
                search_block_entities = search_block_body.get("entities",[])
                if block_id not in search_block_entities:
                    search_block_entities.insert(0,block_id)
                    search_block_update = True
                    block_update = True
                search_block_body["entities"]=search_block_entities
                search_block_search_data = search_block_body.get("search_data",{})
                search_block_search_data_type = search_block_search_data.get(search_type,[])
                search_block_search_data_sequence = search_block_search_data.get("block_id_sequence",[])
                if block_id not in search_block_search_data_type:
                    search_block_search_data_type.insert(0,block_id)
                    search_block_search_data[search_type]=search_block_search_data_type
                    search_block_update = True
                    block_update = True
                if search_type in ["sequence"]:
                    if block_id_sequence_all not in search_block_search_data_sequence:
                        search_block_search_data_sequence.insert(0,block_id_sequence_all)
                        search_block_search_data["block_id_sequence"]=search_block_search_data_sequence
                        search_block_update = True
                        block_update = True
                search_block_body["search_data"]=search_block_search_data
                if search_block_update:
                    search_block_body["updatetime"]=int(time.time())
                    update_aim(search_block_id,search_block_body)
            if block_update:
                block_search_words = block.get("search_words",{})
                block_search_words_leave = block.get("search_words_leave",{})

                block_search_words_old = set(block_search_words.get(search_type,[]))
                block_search_words_new = set(search_content_list)

                block_search_words_leave_update = block_search_words_old - block_search_words_new
                block_search_words_leave_old = set(block_search_words_leave.get(search_type,[]))
                block_search_words_leave_now = block_search_words_leave_update|block_search_words_leave_old
                print("block_search_words_leave_now",block_search_words_leave_now)
                leave_word_ids = []
                result = conn.query("SELECT * FROM index_search WHERE word in %s",tuple(block_search_words_leave_now))
                for item in result:
                    item_word = item.get("word",None)
                    item_entity_id = item.get("entity_id",None)
                    leave_word_ids.append(item_entity_id)
                leave_blocks = get_aims(list(leave_word_ids))
                for leave_block in leave_blocks:
                    leave_block_id = leave_block[0]
                    leave_block_body = leave_block[1]
                    leave_block_update = False
                    leave_block_word = leave_block_body.get("word",None)
                    leave_block_entities = leave_block_body.get("entities",[])
                    if block_id in leave_block_entities:
                        leave_block_entities.remove(block_id)
                        leave_block_update = True
                    leave_block_body["entities"]=leave_block_entities
                    leave_block_search_data = leave_block_body.get("search_data",{})
                    leave_block_search_data_type = leave_block_search_data.get(search_type,[])
                    leave_block_search_data_sequence = leave_block_search_data.get("block_id_sequence",[])
                    if block_id in leave_block_search_data_type:
                        leave_block_search_data_type.remove(block_id)
                        leave_block_search_data[search_type]=leave_block_search_data_type
                        leave_block_update = True
                    if search_type in ["sequence"]:
                        if block_id_sequence_all in leave_block_search_data_sequence:
                            leave_block_search_data_sequence.remove(block_id_sequence_all)
                            leave_block_search_data["block_id_sequence"]=leave_block_search_data_sequence
                            leave_block_update = True
                    leave_block_body["search_data"]=leave_block_search_data
                    if leave_block_update:
                        leave_block_body["updatetime"]=int(time.time())
                        block_search_words_leave_now.remove(leave_block_word)
                        update_aim(leave_block_id,leave_block_body)

                block_search_words[search_type]=list(block_search_words_new)
                block["search_words"]=block_search_words
                block_search_words_leave[search_type]=list(block_search_words_leave_now)
                block["search_words_leave"]=block_search_words_leave
                block["updatetime"]=time.time()
                update_aim(block_id,block)
                # self.finish({"info":"ok","about":"add success"})
                # return
            # else:
                # self.finish({"info":"ok","about":"same search words"})
        self.finish({"info":"ok","about":"add free page"})
class SearchAddFreeAPIHandler(WebRequest):
    @tornado.gen.coroutine
    def post(self):
        token = self.get_argument("token","")
        if token not in ["xialiwei_follows_god"]:
            self.finish({"info":"error","about":"no login"})
            return
        user_id = self.get_argument("user_id","")
        # if not self.current_user:
        #     self.finish({"info":"error","about":"no login"})
        #     return
        # user_id = self.current_user["id"]
        search_content= self.get_argument("search",None)
        search_type = self.get_argument("type",None)
        block_id = self.get_argument("block_id",None)
        block_id_sequence = self.get_argument("block_id_sequence",None)
        if search_type in ["sequence"]:
            block_id_sequence_all = "%s_%s"%(block_id,block_id_sequence)
        if search_type not in settings["search_type"]:
            self.finish({"info":"error","about":"no in allowed"})
            return
        if not search_content:
            self.finish({"info":"error","about":"no content"})
            return
        if not block_id:
            self.finish({"info":"error","about":"no block_id"})
            return
        block = get_aim(block_id)
        if not block:
            self.finish({"info":"error","about":"no block"})
            return
        editors = block.get("editors",[block.get("owner",None)])
        if user_id not in editors and user_id not in settings["developers"]:
            self.finish({"info":"error","about":"current user not in editors"})
            return
        search_content = search_content.lower()
        search_content_list_no = settings["search_no_str"]
        search_content_list_no = set(list(search_content_list_no))
        search_content_list = set(jieba.lcut(search_content))
        search_content_list = tuple(search_content_list-search_content_list_no)
        result = conn.query("SELECT * FROM index_search WHERE word in %s",search_content_list)
        result_json = {}
        result_has = []
        word_ids = []
        for item in result:
            item_word = item.get("word",None)
            item_entity_id = item.get("entity_id",None)
            word_ids.append(item_entity_id)
            result_has.append(item_word)
        not_result_has = set(search_content_list)-set(result_has)
        block_update = False
        for word in not_result_has:
            block_id_sequence_list = []
            if search_type in ["sequence"]:
                block_id_sequence_list = [block_id_sequence_all]
            search_block = {
                "word":word,
                "owner":settings["developers"][0],
                "subtype":"search",
                "search_data":{
                    search_type:[block_id],
                    "block_id_sequence":block_id_sequence_list,
                },
                "entities":[block_id],
            }

            [search_block_id,search_block]=nomagic.block.create_block(search_block)
            conn.execute("INSERT INTO index_search (word, entity_id) VALUES(%s, %s)", word, search_block_id)
            block_update = True
        search_blocks = get_aims(word_ids)
        
        for search_block in search_blocks:
            search_block_id = search_block[0]
            search_block_body = search_block[1]
            search_block_update = False
            search_block_entities = search_block_body.get("entities",[])
            if block_id not in search_block_entities:
                search_block_entities.insert(0,block_id)
                search_block_update = True
                block_update = True
            search_block_body["entities"]=search_block_entities
            search_block_search_data = search_block_body.get("search_data",{})
            search_block_search_data_type = search_block_search_data.get(search_type,[])
            search_block_search_data_sequence = search_block_search_data.get("block_id_sequence",[])
            if block_id not in search_block_search_data_type:
                search_block_search_data_type.insert(0,block_id)
                search_block_search_data[search_type]=search_block_search_data_type
                search_block_update = True
                block_update = True
            if search_type in ["sequence"]:
                if block_id_sequence_all not in search_block_search_data_sequence:
                    search_block_search_data_sequence.insert(0,block_id_sequence_all)
                    search_block_search_data["block_id_sequence"]=search_block_search_data_sequence
                    search_block_update = True
                    block_update = True
            search_block_body["search_data"]=search_block_search_data
            if search_block_update:
                search_block_body["updatetime"]=int(time.time())
                update_aim(search_block_id,search_block_body)
        if block_update:
            block_search_words = block.get("search_words",{})
            block_search_words_leave = block.get("search_words_leave",{})

            block_search_words_old = set(block_search_words.get(search_type,[]))
            block_search_words_new = set(search_content_list)

            block_search_words_leave_update = block_search_words_old - block_search_words_new
            block_search_words_leave_old = set(block_search_words_leave.get(search_type,[]))
            block_search_words_leave_now = block_search_words_leave_update|block_search_words_leave_old
            print("block_search_words_leave_now",block_search_words_leave_now)
            leave_word_ids = []
            result = conn.query("SELECT * FROM index_search WHERE word in %s",tuple(block_search_words_leave_now))
            for item in result:
                item_word = item.get("word",None)
                item_entity_id = item.get("entity_id",None)
                leave_word_ids.append(item_entity_id)
            leave_blocks = get_aims(list(leave_word_ids))
            for leave_block in leave_blocks:
                leave_block_id = leave_block[0]
                leave_block_body = leave_block[1]
                leave_block_update = False
                leave_block_word = leave_block_body.get("word",None)
                leave_block_entities = leave_block_body.get("entities",[])
                if block_id in leave_block_entities:
                    leave_block_entities.remove(block_id)
                    leave_block_update = True
                leave_block_body["entities"]=leave_block_entities
                leave_block_search_data = leave_block_body.get("search_data",{})
                leave_block_search_data_type = leave_block_search_data.get(search_type,[])
                leave_block_search_data_sequence = leave_block_search_data.get("block_id_sequence",[])
                if block_id in leave_block_search_data_type:
                    leave_block_search_data_type.remove(block_id)
                    leave_block_search_data[search_type]=leave_block_search_data_type
                    leave_block_update = True
                if search_type in ["sequence"]:
                    if block_id_sequence_all in leave_block_search_data_sequence:
                        leave_block_search_data_sequence.remove(block_id_sequence_all)
                        leave_block_search_data["block_id_sequence"]=leave_block_search_data_sequence
                        leave_block_update = True
                leave_block_body["search_data"]=leave_block_search_data
                if leave_block_update:
                    leave_block_body["updatetime"]=int(time.time())
                    block_search_words_leave_now.remove(leave_block_word)
                    update_aim(leave_block_id,leave_block_body)

            block_search_words[search_type]=list(block_search_words_new)
            block["search_words"]=block_search_words
            block_search_words_leave[search_type]=list(block_search_words_leave_now)
            block["search_words_leave"]=block_search_words_leave
            block["updatetime"]=int(time.time())
            update_aim(block_id,block)
            self.finish({"info":"ok","about":"add success"})
            return
        else:
            self.finish({"info":"ok","about":"same search words"})
class SearchAddAPIHandler(WebRequest):
    @tornado.gen.coroutine
    def post(self):
        if not self.current_user:
            self.finish({"info":"error","about":"no login"})
            return
        user_id = self.current_user["id"]
        search_content= self.get_argument("search",None)
        search_type = self.get_argument("type",None)
        block_id = self.get_argument("block_id",None)
        block_id_sequence = self.get_argument("block_id_sequence",None)
        if search_type in ["sequence"]:
            block_id_sequence_all = "%s_%s"%(block_id,block_id_sequence)
        if search_type not in settings["search_type"]:
            self.finish({"info":"error","about":"no in allowed"})
            return
        if not search_content:
            self.finish({"info":"error","about":"no content"})
            return
        if not block_id:
            self.finish({"info":"error","about":"no block_id"})
            return
        block = get_aim(block_id)
        if not block:
            self.finish({"info":"error","about":"no block"})
            return
        editors = block.get("editors",[block.get("owner",None)])
        if user_id not in editors and user_id not in settings["developers"]:
            self.finish({"info":"error","about":"current user not in editors"})
            return
        search_content = search_content.lower()
        search_content_list_no = settings["search_no_str"]
        search_content_list_no = set(list(search_content_list_no))
        search_content_list = set(jieba.lcut(search_content))
        search_content_list = tuple(search_content_list-search_content_list_no)
        result = conn.query("SELECT * FROM index_search WHERE word in %s",search_content_list)
        result_json = {}
        result_has = []
        word_ids = []
        for item in result:
            item_word = item.get("word",None)
            item_entity_id = item.get("entity_id",None)
            word_ids.append(item_entity_id)
            result_has.append(item_word)
        not_result_has = set(search_content_list)-set(result_has)
        block_update = False
        for word in not_result_has:
            block_id_sequence_list = []
            if search_type in ["sequence"]:
                block_id_sequence_list = [block_id_sequence_all]
            search_block = {
                "word":word,
                "owner":settings["developers"][0],
                "subtype":"search",
                "search_data":{
                    search_type:[block_id],
                    "block_id_sequence":block_id_sequence_list,
                },
                "entities":[block_id],
            }

            [search_block_id,search_block]=nomagic.block.create_block(search_block)
            conn.execute("INSERT INTO index_search (word, entity_id) VALUES(%s, %s)", word, search_block_id)
            block_update = True
        search_blocks = get_aims(word_ids)
        
        for search_block in search_blocks:
            search_block_id = search_block[0]
            search_block_body = search_block[1]
            search_block_update = False
            search_block_entities = search_block_body.get("entities",[])
            if block_id not in search_block_entities:
                search_block_entities.insert(0,block_id)
                search_block_update = True
                block_update = True
            search_block_body["entities"]=search_block_entities
            search_block_search_data = search_block_body.get("search_data",{})
            search_block_search_data_type = search_block_search_data.get(search_type,[])
            search_block_search_data_sequence = search_block_search_data.get("block_id_sequence",[])
            if block_id not in search_block_search_data_type:
                search_block_search_data_type.insert(0,block_id)
                search_block_search_data[search_type]=search_block_search_data_type
                search_block_update = True
                block_update = True
            if search_type in ["sequence"]:
                if block_id_sequence_all not in search_block_search_data_sequence:
                    search_block_search_data_sequence.insert(0,block_id_sequence_all)
                    search_block_search_data["block_id_sequence"]=search_block_search_data_sequence
                    search_block_update = True
                    block_update = True
            search_block_body["search_data"]=search_block_search_data
            if search_block_update:
                search_block_body["updatetime"]=int(time.time())
                update_aim(search_block_id,search_block_body)
        if block_update:
            block_search_words = block.get("search_words",{})
            block_search_words_leave = block.get("search_words_leave",{})

            block_search_words_old = set(block_search_words.get(search_type,[]))
            block_search_words_new = set(search_content_list)

            block_search_words_leave_update = block_search_words_old - block_search_words_new
            block_search_words_leave_old = set(block_search_words_leave.get(search_type,[]))
            block_search_words_leave_now = block_search_words_leave_update|block_search_words_leave_old
            print("block_search_words_leave_now",block_search_words_leave_now)
            leave_word_ids = []
            result = conn.query("SELECT * FROM index_search WHERE word in %s",tuple(block_search_words_leave_now))
            for item in result:
                item_word = item.get("word",None)
                item_entity_id = item.get("entity_id",None)
                leave_word_ids.append(item_entity_id)
            leave_blocks = get_aims(list(leave_word_ids))
            for leave_block in leave_blocks:
                leave_block_id = leave_block[0]
                leave_block_body = leave_block[1]
                leave_block_update = False
                leave_block_word = leave_block_body.get("word",None)
                leave_block_entities = leave_block_body.get("entities",[])
                if block_id in leave_block_entities:
                    leave_block_entities.remove(block_id)
                    leave_block_update = True
                leave_block_body["entities"]=leave_block_entities
                leave_block_search_data = leave_block_body.get("search_data",{})
                leave_block_search_data_type = leave_block_search_data.get(search_type,[])
                leave_block_search_data_sequence = leave_block_search_data.get("block_id_sequence",[])
                if block_id in leave_block_search_data_type:
                    leave_block_search_data_type.remove(block_id)
                    leave_block_search_data[search_type]=leave_block_search_data_type
                    leave_block_update = True
                if search_type in ["sequence"]:
                    if block_id_sequence_all in leave_block_search_data_sequence:
                        leave_block_search_data_sequence.remove(block_id_sequence_all)
                        leave_block_search_data["block_id_sequence"]=leave_block_search_data_sequence
                        leave_block_update = True
                leave_block_body["search_data"]=leave_block_search_data
                if leave_block_update:
                    leave_block_body["updatetime"]=int(time.time())
                    block_search_words_leave_now.remove(leave_block_word)
                    update_aim(leave_block_id,leave_block_body)

            block_search_words[search_type]=list(block_search_words_new)
            block["search_words"]=block_search_words
            block_search_words_leave[search_type]=list(block_search_words_leave_now)
            block["search_words_leave"]=block_search_words_leave
            block["updatetime"]=int(time.time())
            update_aim(block_id,block)
            self.finish({"info":"ok","about":"add success"})
            return
        else:
            self.finish({"info":"ok","about":"same search words"})
class SearchListAPIHandler(WebRequest):
    @tornado.gen.coroutine
    def get(self):
        search_content= self.get_argument("search",None)
        search_type = self.get_argument("type",None)
        if not search_content:
            self.finish({"info":"error","about":"no content"})
            return
        search_content_list_no = settings["search_no_str"]
        search_content_list_no = set(list(search_content_list_no))
        search_content_list = set(jieba.lcut(search_content))
        search_content_list = tuple(search_content_list-search_content_list_no)
        result = conn.query("SELECT * FROM index_search WHERE word in %s",search_content_list)
        result_json = {}
        result_has = []
        word_ids = []
        for item in result:
            item_word = item.get("word",None)
            item_entity_id = item.get("entity_id",None)
            word_ids.append(item_entity_id)
            result_has.append(item_word)
        search_blocks = get_aims(word_ids)
        result_search_ids = set([])
        result_search_ids_count = {}
        for search_block in search_blocks:
            search_block_id = search_block[0]
            search_block_body = search_block[1]
            search_block_word = search_block_body.get("word",None)
            search_block_search_data = search_block_body.get("search_data",{})
            if not search_block_word:
                continue
            if search_type not in settings["search_type"]:
                result_json[search_block_word]={
                    "search_data":search_block_search_data
                }
                for k,v in search_block_search_data.items():
                    result_search_ids = result_search_ids | set(v)
                    for v_i in v:
                        num = int(result_search_ids_count.get(v_i,0))+1
                        result_search_ids_count[v_i]=num
            else:
                result_json[search_block_word]={
                    "search_data":{
                        search_type:search_block_search_data.get(search_type,[])
                    }
                }
                result_search_ids = result_search_ids | set(search_block_search_data.get(search_type,[]))
                for v_i in search_block_search_data.get(search_type,[]):
                    num = int(result_search_ids_count.get(v_i,0))+1
                    result_search_ids_count[v_i]=num
        result_search_json = {}
        result_search_ids_check = []
        result_search_ids_check_json = {}
        for result_search_ids_item in result_search_ids:
            result_search_ids_item_list = result_search_ids_item.split("_")
            result_search_ids_item_id = result_search_ids_item_list[0]
            if result_search_ids_item_id not in result_search_ids_check:
                result_search_ids_check.append(result_search_ids_item_id)
            if len(result_search_ids_item_list)>1:
                result_search_ids_item_id_sequence = result_search_ids_item_list[1]
                result_search_ids_check_json_list = result_search_ids_check_json.get(result_search_ids_item_id,[])
                if result_search_ids_item_id_sequence not in result_search_ids_check_json_list:
                    result_search_ids_check_json_list.append(result_search_ids_item_id_sequence)
                result_search_ids_check_json[result_search_ids_item_id]=result_search_ids_check_json_list

        result_search_ids = result_search_ids_check
        result_searchs = get_aims(result_search_ids)
        for result_search in result_searchs:
            result_search_id = result_search[0]
            result_search_body = result_search[1]

            result_title = result_search_body.get("title","Title")
            result_desc = result_search_body.get("desc","Desc")
            result_type = result_search_body.get("type","block")
            result_subytpe = result_search_body.get("subtype","block")
            result_doms = result_search_body.get("doms",[])
            result_permission = result_search_body.get("permission","private")
            if result_type in ["user"]:
                result_title = result_search_body.get("name","暂无昵称")
                result_desc = result_search_body.get("plus_info",{}).get("角色","")

            # elif result_type in ["product"] to find the owner or store to get score count with one product or just in on card
            # 搜索商品时，一种是集中搜索词呈现，根据店铺分和商品分综合展示，另一种模式是商铺合集展示
            sequence_list=[]
            for dom in result_doms:
                if dom[0] in result_search_ids_check_json.get(result_search_id,[]):
                    sequence_list.append(dom)
            result_search_json[result_search_id]={
                "title":result_title,
                "desc":result_desc,
                "type":result_type,
                "subtype":result_subytpe,
                "sequence":sequence_list,
                "permission":result_permission,
            }
        self.finish({
            "info":"ok",
            "about":"success",
            "result":result_json,
            "result_search_ids":list(result_search_ids),
            "result_search_json":result_search_json,
            "result_search_ids_count":result_search_ids_count,
            })
class SearchListForceAPIHandler(WebRequest):
    @tornado.gen.coroutine
    def get(self):
        search_content= self.get_argument("search",None)
        search_type = self.get_argument("type",None)
        if not search_content:
            self.finish({"info":"error","about":"no content"})
            return
        search_content_list_no = settings["search_no_str"]
        search_content_list_no = set(list(search_content_list_no))
        search_content_list = set(jieba.lcut(search_content))
        search_content_list = tuple(search_content_list-search_content_list_no)
        result = conn.query("SELECT * FROM index_search WHERE word in %s",search_content_list)
        result_json = {}
        result_has = []
        word_ids = []
        for item in result:
            item_word = item.get("word",None)
            item_entity_id = item.get("entity_id",None)
            word_ids.append(item_entity_id)
            result_has.append(item_word)
        search_blocks = get_aims(word_ids)
        result_search_ids = set([])
        result_search_ids_count = {}
        result_search_ids_list = []
        for search_block in search_blocks:
            result_search_ids_list_item = set()
            search_block_id = search_block[0]
            search_block_body = search_block[1]
            search_block_word = search_block_body.get("word",None)
            search_block_search_data = search_block_body.get("search_data",{})
            if not search_block_word:
                continue
            if search_type not in settings["search_type"]:
                result_json[search_block_word]={
                    "search_data":search_block_search_data
                }
                for k,v in search_block_search_data.items():
                    result_search_ids_list_item = result_search_ids_list_item |set(v)
                    result_search_ids = result_search_ids | set(v)
                    for v_i in v:
                        num = int(result_search_ids_count.get(v_i,0))+1
                        result_search_ids_count[v_i]=num
            else:
                result_json[search_block_word]={
                    "search_data":{
                        search_type:search_block_search_data.get(search_type,[])
                    }
                }
                result_search_ids_list_item = result_search_ids_list_item |set(v)
                result_search_ids = result_search_ids | set(search_block_search_data.get(search_type,[]))
                for v_i in search_block_search_data.get(search_type,[]):
                    num = int(result_search_ids_count.get(v_i,0))+1
                    result_search_ids_count[v_i]=num
            result_search_ids_list.append(result_search_ids_list_item)
        e = set()
        f = True
        for i in result_search_ids_list:
            print(len(i))
            if f:
                e = e | i
                f = False
            else:
                e = e & i
        result_search_ids = e

        result_search_json = {}
        result_search_ids_check = []
        result_search_ids_check_json = {}
        old_result_search_ids = result_search_ids
        for result_search_ids_item in result_search_ids:
            result_search_ids_item_list = result_search_ids_item.split("_")
            result_search_ids_item_id = result_search_ids_item_list[0]
            if result_search_ids_item_id not in result_search_ids_check:
                result_search_ids_check.append(result_search_ids_item_id)
            if len(result_search_ids_item_list)>1:
                result_search_ids_item_id_sequence = result_search_ids_item_list[1]
                result_search_ids_check_json_list = result_search_ids_check_json.get(result_search_ids_item_id,[])
                if result_search_ids_item_id_sequence not in result_search_ids_check_json_list:
                    result_search_ids_check_json_list.append(result_search_ids_item_id_sequence)
                result_search_ids_check_json[result_search_ids_item_id]=result_search_ids_check_json_list

        result_search_ids = result_search_ids_check
        result_searchs = get_aims(result_search_ids)
        for result_search in result_searchs:
            result_search_id = result_search[0]
            result_search_body = result_search[1]

            result_title = result_search_body.get("title","Title")
            result_desc = result_search_body.get("desc","Desc")
            result_type = result_search_body.get("type","block")
            result_subytpe = result_search_body.get("subtype","block")
            result_doms = result_search_body.get("doms",[])
            result_permission = result_search_body.get("permission","private")
            if result_type in ["user"]:
                result_title = result_search_body.get("name","暂无昵称")
                result_desc = result_search_body.get("plus_info",{}).get("角色","")

            # elif result_type in ["product"] to find the owner or store to get score count with one product or just in on card
            # 搜索商品时，一种是集中搜索词呈现，根据店铺分和商品分综合展示，另一种模式是商铺合集展示
            sequence_list=[]
            for dom in result_doms:
                if dom[0] in result_search_ids_check_json.get(result_search_id,[]):
                    block_id_sequence = "%s_%s"%(result_search_id,dom[0])
                    if block_id_sequence in old_result_search_ids:
                        sequence_list.append(dom)
            result_search_json[result_search_id]={
                "title":result_title,
                "desc":result_desc,
                "type":result_type,
                "subtype":result_subytpe,
                "sequence":sequence_list,
                "permission":result_permission,
            }
        self.finish({
            "info":"ok",
            "about":"success",
            "result":result_json,
            "result_search_ids":list(result_search_ids),
            "result_search_json":result_search_json,
            "result_search_ids_count":result_search_ids_count,
            })
class SearchListMoreAPIHandler(WebRequest):
    @tornado.gen.coroutine
    def get(self):
        search_content= self.get_argument("search",None)
        search_types = self.get_argument("types","").split(",")
        if not search_content:
            self.finish({"info":"error","about":"no content"})
            return
        search_content_list_no = settings["search_no_str"]
        search_content_list_no = set(list(search_content_list_no))
        search_content_list = set(jieba.lcut(search_content))
        search_content_list = tuple(search_content_list-search_content_list_no)
        result = conn.query("SELECT * FROM index_search WHERE word in %s",search_content_list)
        result_json = {}
        result_has = []
        word_ids = []
        for item in result:
            item_word = item.get("word",None)
            item_entity_id = item.get("entity_id",None)
            word_ids.append(item_entity_id)
            result_has.append(item_word)
        search_blocks = get_aims(word_ids)
        result_search_ids = set([])
        result_search_ids_count = {}
        for search_block in search_blocks:
            search_block_id = search_block[0]
            search_block_body = search_block[1]
            search_block_word = search_block_body.get("word",None)
            search_block_search_data = search_block_body.get("search_data",{})
            if not search_block_word:
                continue

            result_json[search_block_word]={
                "search_data":{}
            }
            for search_type in search_types:
                if search_type in settings["search_type"]:
                    result_json[search_block_word]["search_data"][search_type]=search_block_search_data.get(search_type,[])
                    result_search_ids = result_search_ids | set(search_block_search_data.get(search_type,[]))
                    for v_i in search_block_search_data.get(search_type,[]):
                        num = int(result_search_ids_count.get(v_i,0))+1
                        result_search_ids_count[v_i]=num
        result_search_json = {}
        result_searchs = get_aims(result_search_ids)
        for result_search in result_searchs:
            result_search_id = result_search[0]
            result_search_body = result_search[1]

            result_title = result_search_body.get("title","Title")
            result_desc = result_search_body.get("desc","Desc")
            result_type = result_search_body.get("type","block")
            result_subytpe = result_search_body.get("subtype","block")
            result_product_title = result_search_body.get("product_title","Product Title")
            result_product_desc = result_search_body.get("product_desc","Product Desc")
            if result_type in ["user"]:
                result_title = result_search_body.get("name","no name")
                result_desc = result_search_body.get("plus_info",{}).get("role","")

            # elif result_type in ["product"] to find the owner or store to get score count with one product or just in on card
            # 搜索商品时，一种是集中搜索词呈现，根据店铺分和商品分综合展示，另一种模式是商铺合集展示

            result_search_json[result_search_id]={
                "title":result_title,
                "desc":result_desc,
                "type":result_type,
                "subtype":result_subytpe,
                "product_title":result_product_title,
                "product_desc":result_product_desc,
            }
        self.finish({
            "info":"ok",
            "about":"success",
            "result":result_json,
            "result_search_ids":list(result_search_ids),
            "result_search_json":result_search_json,
            "result_search_ids_count":result_search_ids_count,
            })







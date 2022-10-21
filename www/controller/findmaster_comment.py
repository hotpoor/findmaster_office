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

@tornado.gen.coroutine
def push_weixin_template_to_user_ids(user_ids,firstkw,kw1,kw2,kw3,kw4,remarkkw,redirect_uri):
    users = get_aims(user_ids)
    for user_entity in users:
        user = user_entity[1]
        for k,v in user.get("weixin_data",{}).items():
            openid = v.get("openid",None)
            template_id = settings["MPWeixinInfo"][k].get("MPWeixinTemplateHollowNotice","")
            if not openid or (template_id in ["",None]):
                continue
            access_token = settings["MPWeixinInfo"][k]["accessToken"]
            http_client = tornado.httpclient.AsyncHTTPClient()
            url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s"%(access_token)
            if template_id in ["zQgfAxAWwkztX2l1Qmdum2Hs2nsdtwv6k5y_sxcnTEM","ekDThwkOVQO1QkhznXI2AarDnZjlQiJHSnoHhvYP2Fg"]:
                json = {
                    "touser":openid,
                    "template_id":template_id,
                    "url":redirect_uri,
                    "topcolor":"#3c447b",
                    "data":{
                        "first":{"value":firstkw,"color":"#666666"},
                        "keyword1":{"value":kw1,"color":"#666666"},
                        "keyword2":{"value":kw2,"color":"#3c447b"},
                        "keyword3":{"value":kw3,"color":"#666666"},
                        "keyword4":{"value":kw4,"color":"#3c447b"},
                        "remark":{"value":remarkkw,"color":"#666666"},
                    },
                }
            else:
                json = {
                    "touser":openid,
                    "template_id":template_id,
                    "url":redirect_uri,
                    "topcolor":"#3c447b",
                    "data":{
                        "first":{"value":firstkw,"color":"#666666"},
                        "keyword1":{"value":kw1,"color":"#666666"},
                        "keyword2":{"value":kw2,"color":"#3c447b"},
                        "keyword3":{"value":kw3,"color":"#666666"},
                        "keyword4":{"value":kw4,"color":"#3c447b"},
                        "remark":{"value":remarkkw,"color":"#666666"},
                    },
                }
            body = json_encode(json)
            request = tornado.httpclient.HTTPRequest(
                        url = url,
                        method = "POST",
                        body = body,
                        validate_cert = False)
            response = yield http_client.fetch(request)

class AddCommentForceAPIHandler(WebRequest):
    def post(self):
        if not self.current_user:
            self.finish({"info":"error","about":"no login"})
            return
        user_id = self.current_user["id"]
        block_id = self.get_argument("block_id",None)
        block = get_aim(block_id)
        #判断是否为编辑者
        if not block:
            self.finish({"info":"error","about":"no block"})
            return
        comment_entities = block.get("comment_entities",[])
        group = {
            "owner":block_id,
            "editors":block.get("editors",[]),
            "subtype":"page_comment",
            "owner_type":"page",
            "help_creater":user_id,
        }
        [group_id,group] = nomagic.group.create_chat(group)
        comment_entities.append(group_id)
        block["comment_entities"]=comment_entities
        updatetime = int(time.time())
        block["updatetime"]=updatetime
        update_aim(block_id,block)
        self.finish({"info":"ok","about":"add comment success","comment_entity":group_id})
class AddCommentAPIHandler(WebRequest):
    def post(self):
        if not self.current_user:
            self.finish({"info":"error","about":"no login"})
            return
        user_id = self.current_user["id"]
        block_id = self.get_argument("block_id",None)
        block = get_aim(block_id)
        #判断是否为编辑者
        if user_id not in block.get("editors",[block.get("owner",None)]):
        # if block.get("owner",None) != user_id:
            self.finish({"info":"error","about":"no in editors"})
            return
        comment_entities = block.get("comment_entities",[])
        group = {
            "owner":block_id,
            "editors":block.get("editors",[]),
            "subtype":"page_comment",
            "owner_type":"page",
        }
        [group_id,group] = nomagic.group.create_chat(group)
        comment_entities.append(group_id)
        block["comment_entities"]=comment_entities
        updatetime = int(time.time())
        block["updatetime"]=updatetime
        update_aim(block_id,block)
        self.finish({"info":"ok","about":"add comment success","comment_entity":group_id})
class GetCommentAPIHandler(WebRequest):
    def get(self):
        if not self.current_user:
            self.finish({"info":"error","about":"no login"})
            return
        user_id = self.current_user["id"]
        block_id = self.get_argument("block_id",None)
        block = get_aim(block_id)
        if user_id not in block.get("editors",[block.get("owner",None)]):
        # if block.get("owner",None) != user_id:
            self.finish({"info":"error","about":"no in editors"})
            return
        comment_entities = block.get("comment_entities",[])
        self.finish({"info":"ok","about":"get comment success","comment_entities":comment_entities})
class CommentSubmitAPIHandler(WebRequest):
    def post(self):
        self.set_header("Access-Control-Allow-Origin", self.request.headers.get("Origin"))
        self.set_header("Access-Control-Allow-Credentials", "true")
        if not self.current_user:
            self.finish({"info":"error","about":"no login"})
            return
        user_id = self.current_user["id"]
        block_id = self.get_argument("block_id",None)
        chat_id = self.get_argument("chat_id",None)
        content = self.get_argument("content", None)
        uuid = self.get_argument("uuid",None)
        chat = get_aim(chat_id)
        last_comment_time = 0
        print(chat_id,content)
        print(not chat,content=="",not content)
        comment_push = False
        if not chat or content == "" or not content:
            self.finish({"info":"error","about":"no chat or content"})
            return
        chat["comment_members"]=chat.get("comment_members",[])
        if user_id not in chat["comment_members"]:
            chat["comment_members"].append(user_id)
        comment_type = u"COMMENT"
        chat["comment_ids"] = chat.get("comment_ids", [])
        if not chat["comment_ids"]:
            comments = []
            comment_entity = {
                "owner": chat_id,
                "owner_type": chat["type"],
                "comments": comments,
            }
            [comment_id, comment_entity] = nomagic.comment.create_comment(comment_entity)
            chat["comment_ids"].append(comment_id)
            chat["last_comment_entity"] = comment_entity
            update_aim(chat_id,chat)
            last_comment_time = 0
        else:
            comment_id = chat["comment_ids"][-1]
            if chat.get("last_comment_entity", None):
                comment_entity = chat["last_comment_entity"]
            else:
                comment_entity = get_aim(comment_id)
            comments = comment_entity.get("comments", [])
            if(len(comments)>0):
                last_comment_time = comments[-1][2]
            if(len(comments)>=100):
                update_aim(comment_id,comment_entity)
                comments = []
                comment_entity = {
                    "owner": chat_id,
                    "owner_type": chat["type"],
                    "comments": comments,
                    "type": "comment",
                    "last_comment_id": comment_id
                }
                [comment_id, comment_entity] = nomagic.comment.create_comment(comment_entity)
                chat["comment_ids"].append(comment_id)
        comment_sequence = "".join(random.choice(string.ascii_lowercase+string.digits) for _ in range(6))
        comment_time = time.time()
        comment_push = True
        comment_plus = {}
        comment_del = 0
        comments.append([comment_sequence, user_id, comment_time, comment_type, content, comment_plus, comment_del])
        comment_entity["comments"] = comments
        chat["last_comment_entity"] = comment_entity
        update_aim(chat_id,chat)
        user = get_aim(user_id)
        user_name = user.get("name","")
        user_headimgurl = user.get("headimgurl","/static/img/headimgurl.png")
        msgtype = comment_type
        time_now = int(time.time())

        self.finish({"info": "ok","comment_id":comment_id,"sequence":comment_sequence,"time":time_now,"msgtype":msgtype})

        msg = [msgtype, {
            "content": content,
            "nickname": user_name,
            "headimgurl": user_headimgurl,
            "time": time_now,
            "user_id": user_id,
            "sequence": comment_sequence,
            "comment_id": comment_id,
            "uuid":uuid,
        }, chat_id]
        if not block_id:
            DataWebSocket.send_to_all(json_encode(msg))
        else:
            DataWebSocket.send_to_target_room(json_encode(msg),block_id)
class CommentLoadOneAPIHandler(WebRequest):
    @tornado.gen.coroutine
    def get(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        chat_id = self.get_argument("chat_id",None)
        uuid = self.get_argument("uuid",None)
        comment_id = self.get_argument("comment_id",None)
        comment_sequence = self.get_argument("comment_sequence",None)
        remark_id = self.get_argument("remark_id",None)

        if not (comment_id and comment_sequence):
            self.finish({"info":"error","about":"no comment_id or comment_sequence"})
            return
        chat = get_aim(chat_id)
        comment_push = False
        if not chat:
            self.finish({"info":"error","about":"no chat"})
            return
        allow_user_ids = []
        if chat["owner_type"] in ["page"]:
            aim_id = chat["owner"]
            aim = get_aim(aim_id)
            editors = aim.get("editors",[aim["owner"]])
            allow_user_ids = editors
        comment_ids = chat.get("comment_ids",[])
        time_now = int(time.time())

        recent_comment_member_ids = []
        last_comment_id = ""
        if comment_id == comment_ids[-1]:
            comment_entity = chat["last_comment_entity"]
        else:
            comment_entity = get_aim(comment_id)
        last_comment_id = comment_entity.get("last_comment_id", None)
        comments = comment_entity.get("comments",[])
        comments_update = False
        render_comments = []
        one_render_comments = []
        one_recent_comment_member_ids = []
        for comment in comments:
            current_one_recent_comment_member_ids = []
            if not type(comment[5]) == dict:
                comments_update = True
                comment_plus = {
                    "content": comment[5]
                }
                comment[5] = comment_plus
            else:
                remarks = comment[5].get("remarks",[])
                for remark in remarks:
                    if len(remark)==3:
                        comments_update = True
                        remark_id = "".join(random.choice(string.ascii_lowercase+string.digits) for _ in range(6))
                        remark.append(remark_id)
                    recent_comment_member_ids.append(remark[0])
                    current_one_recent_comment_member_ids.append(remark[0])
                comment[5]["remarks"]=remarks
                likes = comment[5].get("likes",[])
                recent_comment_member_ids = list(set(likes).union(set(recent_comment_member_ids))) #求并集
                current_one_recent_comment_member_ids = list(set(likes).union(set(current_one_recent_comment_member_ids))) #求并集
            recent_comment_member_ids.append(comment[1])
            current_one_recent_comment_member_ids.append(comment[1])
            if comment[6] == 0:
                render_comments.append(comment)
            if comment[6] == 0 and comment[0] == comment_sequence:
                one_render_comments.append(comment)
                one_recent_comment_member_ids = current_one_recent_comment_member_ids
        if comments_update:
            comment_entity["comments"] = comments
            if comment_id == comment_ids[-1]:
                chat["last_comment_entity"] = comment_entity
                update_aim(chat_id,chat)
            else:
                update_aim(comment_id,comment_entity)
        members_ids = set(recent_comment_member_ids)
        members_ids = set(one_recent_comment_member_ids)
        members = get_aims(members_ids)
        members_json = {}
        for member in members:
            member_name = member[1].get("name","")
            member_headimgurl = member[1].get("headimgurl","/static/img/headimgurl.png")
            members_json[member[0]] = {"name":member_name ,"headimgurl":member_headimgurl}
        # self.finish({"info":"ok","last_comment_id":last_comment_id,"comments":render_comments,"members":members_json,"comment_id":comment_id,"chat_id":chat_id})
        self.finish({"info":"ok","about":"load one","last_comment_id":last_comment_id,"comments":one_render_comments,"members":members_json,"comment_id":comment_id,"chat_id":chat_id})
class CommentLoadAPIHandler(WebRequest):
    @tornado.gen.coroutine
    def get(self):
        # self.set_header("Access-Control-Allow-Origin", "*")
        chat_id = self.get_argument("chat_id",None)
        comment_id = self.get_argument("comment_id", None)
        chat = get_aim(chat_id)
        if not chat:
            self.finish({"info":"error","about":"no chat"})
            return
        comment_ids = chat.get("comment_ids",[])
        if not comment_id and len(comment_ids)>0 :
            comment_id = comment_ids[-1]
        if comment_id not in comment_ids:
            self.finish({"info":"error","about":"no chat's comment"})
            return
        recent_comment_member_ids = []
        last_comment_id = ""
        if comment_id == comment_ids[-1]:
            comment_entity = chat["last_comment_entity"]
        else:
            comment_entity = get_aim(comment_id)
        last_comment_id = comment_entity.get("last_comment_id", None)
        comments = comment_entity.get("comments",[])
        comments_update = False
        render_comments = []
        for comment in comments:
            if not type(comment[5]) == dict:
                comments_update = True
                comment_plus = {
                    "content": comment[5]
                }
                comment[5] = comment_plus
            else:
                remarks = comment[5].get("remarks",[])
                for remark in remarks:
                    if len(remark)==3:
                        comments_update = True
                        remark_id = "".join(random.choice(string.ascii_lowercase+string.digits) for _ in range(6))
                        remark.append(remark_id)
                    recent_comment_member_ids.append(remark[0])
                comment[5]["remarks"]=remarks
                likes = comment[5].get("likes",[])
                recent_comment_member_ids = list(set(likes).union(set(recent_comment_member_ids))) #求并集
            recent_comment_member_ids.append(comment[1])
            if comment[6] == 0:
                render_comments.append(comment)
        if comments_update:
            comment_entity["comments"] = comments
            if comment_id == comment_ids[-1]:
                chat["last_comment_entity"] = comment_entity
                update_aim(chat_id,chat)
            else:
                update_aim(comment_id,comment_entity)
        members_ids = set(recent_comment_member_ids)
        members = get_aims(members_ids)
        members_json = {}
        for member in members:
            member_name = member[1].get("name","")
            member_headimgurl = member[1].get("headimgurl","/static/img/headimgurl.png")
            members_json[member[0]] = {"name":member_name ,"headimgurl":member_headimgurl}
        self.finish({"info":"ok","last_comment_id":last_comment_id,"comments":render_comments,"members":members_json,"comment_id":comment_id,"chat_id":chat_id})
class RemarkAPIHandler(WebRequest):
    @tornado.gen.coroutine
    def post(self):
        self.set_header("Access-Control-Allow-Origin", self.request.headers.get("Origin"))
        self.set_header("Access-Control-Allow-Credentials", "true")
        if not self.current_user:
            self.finish({"info":"error","about":"no login"})
            return
        user_id = self.current_user["id"]
        block_id = self.get_argument("block_id",None)
        chat_id = self.get_argument("chat_id",None)
        content = self.get_argument("content", None)
        uuid = self.get_argument("uuid",None)
        comment_id = self.get_argument("comment_id",None)
        comment_sequence = self.get_argument("comment_sequence",None)
        remark_content = self.get_argument("remark_content",None)

        if not (comment_id and comment_sequence and remark_content):
            self.finish({"info":"error","about":"no comment_id or comment_sequence or remark_content"})
            return
        chat = get_aim(chat_id)
        # print(chat_id,content)
        # print(not chat,content=="",not content)
        comment_push = False
        if not chat or content == "" or not content:
            self.finish({"info":"error","about":"no chat or content"})
            return
        allow_user_ids = []
        if chat["owner_type"] in ["page"]:
            aim_id = chat["owner"]
            aim = get_aim(aim_id)
            editors = aim.get("editors",[aim["owner"]])
            allow_user_ids = editors
        comment_ids = chat.get("comment_ids",[])

        time_now = int(time.time())
        remark_id = "".join(random.choice(string.ascii_lowercase+string.digits) for _ in range(6))
        remark = [user_id,remark_content,time_now,remark_id]
        remark_num = 0
        push_user_ids = []
        push_remark_user_name = ""
        push_remark_content = ""
        push_remark_fake = None
        firstkw = "您好，您有一条新的评论留言！"
        if comment_id == comment_ids[-1]:
            comment_entity = chat.get("last_comment_entity")
            comments = comment_entity.get("comments")
            ci = 0
            for i in comments:
                if i[0] == comment_sequence:
                    # allow_user_ids = list(set(settings["developers"]) | set([comments[ci][1]]) | set(allow_user_ids))
                    # if not user_id in allow_user_ids:
                    #     self.finish({"info":"error","about":"no permission"})
                    #     return
                    push_remark_content_list = remark_content.split("[BYSECRETUSER]")
                    push_remark_content = push_remark_content_list[0]
                    if len(push_remark_content_list)>1:
                        push_remark_content_secret_user_json_str = push_remark_content_list[1]
                        push_remark_content_secret_user_json = json_decode(push_remark_content_secret_user_json_str)
                        push_remark_fake = push_remark_content_secret_user_json.get("fake","false")
                        push_remark_user_name = push_remark_content_secret_user_json.get("name","")
                    if push_remark_content.startswith("HCALLUSER//"):
                        remark_content_list = push_remark_content.split("//")
                        if len(remark_content_list)>2:
                            add_user_id = remark_content_list[1].split("_")[0]
                            push_user_ids.append(add_user_id)
                            push_remark_content = remark_content_list[2]
                            firstkw = "您好，您有一条新的评论留言回复！"
                    push_user_ids = list(set(push_user_ids) | set([comments[ci][1]]))
                    remarks = comments[ci][5].get("remarks",[])
                    remarks.append(remark)
                    comments[ci][5]["remarks"] = remarks
                    remark_num = len(remarks)
                    comment_entity["comments"] = comments
                    chat["last_comment_entity"] = comment_entity
                    update_aim(chat_id,chat)
                else:
                    ci = ci + 1
                    continue
        else:
            comment_entity = get_aim(comment_id)
            comments = comment_entity.get("comments")
            ci = 0
            for i in comments:
                if i[0] == comment_sequence:
                    # [comment_sequence, user_id, comment_time, comment_type, content, comment_plus, comment_del]
                    # allow_user_ids = list(set(settings["developers"]) | set([comments[ci][1]]) | set(allow_user_ids))
                    # if user_id not in allow_user_ids:
                    #     self.finish({"info":"error","about":"no permission"})
                    #     return
                    remarks = comments[ci][5].get("remarks",[])
                    remarks.append(remark)
                    comments[ci][5]["remarks"] = remarks
                    remark_num = len(remarks)
                    comment_entity["comments"] = comments
                    update_aim(comment_id, comment_entity)
                else:
                    ci = ci + 1
                    continue

        user = get_aim(user_id)
        user_name = user.get("name","")
        user_headimgurl = user.get("headimgurl","/static/img/headimgurl.png")
        msgtype = "COMMENTREMARK"

        self.finish({"info": "ok","comment_id":comment_id,"sequence":comment_sequence,"time":time_now,"msgtype":msgtype})

        msg = [msgtype, {
            "remark":remark,
            "remarks_num":remark_num,
            "nickname": user_name,
            "headimgurl": user_headimgurl,
            "time": time_now,
            "user_id": user_id,
            "sequence": comment_sequence,
            "comment_id": comment_id,
            "uuid":uuid,
        }, chat_id]
        if not block_id:
            DataWebSocket.send_to_all(json_encode(msg))
        else:
            DataWebSocket.send_to_target_room(json_encode(msg),block_id)

        firstkw = firstkw
        kw1 = "阡上花·树洞"
        if push_remark_fake in [None]:
            kw2 = "来自%s"%user_name    
        elif push_remark_fake in ["true"]:
            kw2 = "来自%s[%s]"%(push_remark_user_name,"匿名")
        elif push_remark_fake in ["false"]:
            kw2 = "来自%s[%s]"%(push_remark_user_name,user_name)
        kw3 = time.strftime('%Y-%m-%d %H:%M')
        kw4 = "%s"%push_remark_content
        if len(kw4)>60:
            kw4 = "%s... （点击全文）"%(kw4[0:55])
        remarkkw = "PUCO噗叩，国货美妆新发现，和我们一起发现中国美！"
        redirect_uri = "https://www.qianshanghua.com/home/msh/hollow/%s?chat_id=%s&comment_id=%s&comment_sequence=%s"%(block_id,chat_id,comment_id,comment_sequence)
        if user_id in push_user_ids:
            push_user_ids.remove(user_id)
        push_weixin_template_to_user_ids(push_user_ids,firstkw,kw1,kw2,kw3,kw4,remarkkw,redirect_uri)
class RemarkDelAPIHandler(WebRequest):
    @tornado.gen.coroutine
    def post(self):
        self.set_header("Access-Control-Allow-Origin", self.request.headers.get("Origin"))
        self.set_header("Access-Control-Allow-Credentials", "true")
        if not self.current_user:
            self.finish({"info":"error","about":"no login"})
            return
        user_id = self.current_user["id"]
        block_id = self.get_argument("block_id",None)
        chat_id = self.get_argument("chat_id",None)
        content = self.get_argument("content", None)
        uuid = self.get_argument("uuid",None)
        comment_id = self.get_argument("comment_id",None)
        comment_sequence = self.get_argument("comment_sequence",None)
        remark_content = self.get_argument("remark_content",None)
        remark_id = self.get_argument("remark_id",None)

        if not (comment_id and comment_sequence and remark_id):
            self.finish({"info":"error","about":"no comment_id or comment_sequence or remark_id"})
            return
        chat = get_aim(chat_id)
        print(chat_id,content)
        print(not chat,content=="",not content)
        comment_push = False
        if not chat or content == "" or not content:
            self.finish({"info":"error","about":"no chat or content"})
            return
        allow_user_ids = []
        if chat["owner_type"] in ["page"]:
            aim_id = chat["owner"]
            aim = get_aim(aim_id)
            editors = aim.get("editors",[aim["owner"]])
            allow_user_ids = editors
        comment_ids = chat.get("comment_ids",[])
        time_now = int(time.time())
        remark_num = 0
        if comment_id == comment_ids[-1]:
            comment_entity = chat.get("last_comment_entity")
            comments = comment_entity.get("comments")
            ci = 0
            for i in comments:
                if i[0] == comment_sequence:
                    allow_user_ids = list(set(settings["developers"]) | set([comments[ci][1]]) | set(allow_user_ids))
                    # if user_id not in allow_user_ids:
                    #     self.finish({"info":"error","about":"no permission"})
                    #     return
                    remarks = comments[ci][5].get("remarks",[])
                    for rm in remarks:
                        if len(rm)<4:
                            return
                        if rm[3] == remark_id:
                            if user_id not in list(set(allow_user_ids)|set(rm[0])):
                                self.finish({"info":"error","about":"no permission"})
                                return
                            remarks.remove(rm)
                            break
                    comments[ci][5]["remarks"] = remarks
                    remark_num = len(remarks)
                    comment_entity["comments"] = comments
                    chat["last_comment_entity"] = comment_entity
                    update_aim(chat_id,chat)
                else:
                    ci = ci + 1
                    continue
        else:
            comment_entity = get_aim(comment_id)
            comments = comment_entity.get("comments")
            ci = 0
            for i in comments:
                if i[0] == comment_sequence:
                    # [comment_sequence, user_id, comment_time, comment_type, content, comment_plus, comment_del]
                    allow_user_ids = list(set(settings["developers"]) | set([comments[ci][1]]) | set(allow_user_ids))
                    # if user_id not in allow_user_ids:
                    #     self.finish({"info":"error","about":"no permission"})
                    #     return
                    remarks = comments[ci][5].get("remarks",[])
                    for rm in remarks:
                        if len(rm)<4:
                            return
                        if rm[3] == remark_id:
                            if user_id not in list(set(allow_user_ids)|set(rm[0])):
                                self.finish({"info":"error","about":"no permission"})
                                return
                            remarks.remove(rm)
                            break
                    comments[ci][5]["remarks"] = remarks
                    remark_num = len(remarks)
                    comment_entity["comments"] = comments
                    update_aim(comment_id, comment_entity)
                else:
                    ci = ci + 1
                    continue

        user = get_aim(user_id)
        user_name = user.get("name","")
        user_headimgurl = user.get("headimgurl","/static/img/headimgurl.png")
        msgtype = "COMMENTREMARKDEL"

        self.finish({"info": "ok","comment_id":comment_id,"sequence":comment_sequence,"time":time_now,"msgtype":msgtype})

        msg = [msgtype, {
            "remark_id":remark_id,
            "remarks_num":remark_num,
            "nickname": user_name,
            "headimgurl": user_headimgurl,
            "time": time_now,
            "user_id": user_id,
            "sequence": comment_sequence,
            "comment_id": comment_id,
            "uuid":uuid,
        }, chat_id]
        if not block_id:
            DataWebSocket.send_to_all(json_encode(msg))
        else:
            DataWebSocket.send_to_target_room(json_encode(msg),block_id)
class LikeAPIHandler(WebRequest):
    @tornado.gen.coroutine
    def post(self):
        self.set_header("Access-Control-Allow-Origin", self.request.headers.get("Origin"))
        self.set_header("Access-Control-Allow-Credentials", "true")
        if not self.current_user:
            self.finish({"info":"error","about":"no login"})
            return
        user_id = self.current_user["id"]
        block_id = self.get_argument("block_id",None)
        chat_id = self.get_argument("chat_id",None)
        content = self.get_argument("content", None)
        uuid = self.get_argument("uuid",None)
        comment_id = self.get_argument("comment_id",None)
        comment_sequence = self.get_argument("comment_sequence",None)
        like_content = self.get_argument("like_content",None)
        like_content_update = False
        if not (comment_id and comment_sequence):
            self.finish({"info":"error","about":"no comment_id or comment_sequence"})
            return
        chat = get_aim(chat_id)
        print(chat_id,content)
        print(not chat,content=="",not content)
        comment_push = False
        if not chat or content == "" or not content:
            self.finish({"info":"error","about":"no chat or content"})
            return
        allow_user_ids = []
        if chat["owner_type"] in ["page"]:
            aim_id = chat["owner"]
            aim = get_aim(aim_id)
            editors = aim.get("editors",[aim["owner"]])
            allow_user_ids = editors
        comment_ids = chat.get("comment_ids",[])
        likes_num = 0
        push_user_ids = []
        if comment_id == comment_ids[-1]:
            comment_entity = chat.get("last_comment_entity")
            comments = comment_entity.get("comments")
            ci = 0
            for i in comments:
                if i[0] == comment_sequence:
                    # allow_user_ids = list(set(settings["developers"]) | set([comments[ci][1]]) | set(allow_user_ids))
                    # if user_id not in allow_user_ids:
                    #     self.finish({"info":"error","about":"no permission"})
                    #     return
                    likes = comments[ci][5].get("likes",[])
                    if like_content == "like":
                        if user_id not in likes:
                            push_user_ids = list(set(push_user_ids) | set([comments[ci][1]]))
                            likes.append(user_id)
                            like_content_update = True
                    elif like_content == "dislike":
                        if user_id in likes:
                            likes.remove(user_id)
                            like_content_update = True
                    comments[ci][5]["likes"] = likes
                    likes_num = len(likes)
                    comment_entity["comments"] = comments
                    chat["last_comment_entity"] = comment_entity
                    if like_content_update:
                        update_aim(chat_id,chat)
                        break
                else:
                    ci = ci + 1
                    continue
        else:
            comment_entity = get_aim(comment_id)
            comments = comment_entity.get("comments")
            ci = 0
            for i in comments:
                if i[0] == comment_sequence:
                    # [comment_sequence, user_id, comment_time, comment_type, content, comment_plus, comment_del]
                    # allow_user_ids = list(set(settings["developers"]) | set([comments[ci][1]]) | set(allow_user_ids))
                    # if user_id not in allow_user_ids:
                    #     self.finish({"info":"error","about":"no permission"})
                    #     return
                    likes = comments[ci][5].get("likes",[])
                    if like_content == "like":
                        if user_id not in likes:
                            push_user_ids = list(set(push_user_ids) | set([comments[ci][1]]))
                            likes.append(user_id)
                            like_content_update = True
                    elif like_content == "dislike":
                        if user_id in likes:
                            likes.remove(user_id)
                            like_content_update = True
                    comments[ci][5]["likes"] = likes
                    likes_num = len(likes)
                    comment_entity["comments"] = comments
                    if like_content_update:
                        update_aim(comment_id, comment_entity)
                        break
                else:
                    ci = ci + 1
                    continue

        user = get_aim(user_id)
        user_name = user.get("name","")
        user_headimgurl = user.get("headimgurl","/static/img/headimgurl.png")
        msgtype = "COMMENTLIKE"
        time_now = int(time.time())

        self.finish({"info": "ok","comment_id":comment_id,"sequence":comment_sequence,"time":time_now,"msgtype":msgtype})

        msg = [msgtype, {
            "like":like_content,
            "likes_num":likes_num,
            "nickname": user_name,
            "headimgurl": user_headimgurl,
            "time": time_now,
            "user_id": user_id,
            "sequence": comment_sequence,
            "comment_id": comment_id,
            "uuid":uuid,
        }, chat_id]
        if not block_id:
            DataWebSocket.send_to_all(json_encode(msg))
        else:
            DataWebSocket.send_to_target_room(json_encode(msg),block_id)

        firstkw = "您好，您所关注的消息有互动更新！"
        kw1 = "阡上花·树洞"
        kw2 = "来自%s"%user_name
        kw3 = time.strftime('%Y-%m-%d %H:%M')
        kw4 = "点赞+1"
        remarkkw = "PUCO噗叩，国货美妆新发现，和我们一起发现中国美！"
        redirect_uri = "https://www.qianshanghua.com/home/msh/hollow/%s?chat_id=%s&comment_id=%s&comment_sequence=%s"%(block_id,chat_id,comment_id,comment_sequence)
        if user_id in push_user_ids:
            push_user_ids.remove(user_id)
        push_weixin_template_to_user_ids(push_user_ids,firstkw,kw1,kw2,kw3,kw4,remarkkw,redirect_uri)
class RefAPIHandler(WebRequest):
    @tornado.gen.coroutine
    def post(self):
        pass
class RefAddAPIHandler(WebRequest):
    @tornado.gen.coroutine
    def post(self):
        self.set_header("Access-Control-Allow-Origin", self.request.headers.get("Origin"))
        self.set_header("Access-Control-Allow-Credentials", "true")
        if not self.current_user:
            self.finish({"info":"error","about":"no login"})
            return
        user_id = self.current_user["id"]
        block_id = self.get_argument("block_id",None)
        chat_id = self.get_argument("chat_id",None)
        content = self.get_argument("content", None)
        uuid = self.get_argument("uuid",None)
        comment_id = self.get_argument("comment_id",None)
        comment_sequence = self.get_argument("comment_sequence",None)
        ref_content = self.get_argument("ref_content","one coming from ref_id")
        ref_id = self.get_argument("ref_id",None)
        if not (comment_id and comment_sequence):
            self.finish({"info":"error","about":"no comment_id or comment_sequence"})
            return
        chat = get_aim(chat_id)
        print(chat_id,content)
        print(not chat,content=="",not content)
        comment_push = False
        if not chat or content == "" or not content:
            self.finish({"info":"error","about":"no chat or content"})
            return
        allow_user_ids = []
        ref_num = 0
        if chat["owner_type"] in ["page"]:
            aim_id = chat["owner"]
            aim = get_aim(aim_id)
            editors = aim.get("editors",[aim["owner"]])
            allow_user_ids = editors
        comment_ids = chat.get("comment_ids",[])
        if comment_id == comment_ids[-1]:
            comment_entity = chat.get("last_comment_entity")
            comments = comment_entity.get("comments")
            ci = 0
            for i in comments:
                if i[0] == comment_sequence:
                    ref_content_update = False
                    ref_list = comments[ci][5].get("ref_list",[])
                    if user_id not in ref_list:
                        ref_content = u"add"
                        ref_list.append(user_id)
                        ref_content_update = True
                    ref_num = len(ref_list)
                    # 第一次登陆时渠道锁定使用
                    ref_info = comments[ci][5].get("ref_info",{})
                    ref_info_list = ref_info.get(ref_id,[])
                    # 第二次登陆时渠道归档使用
                    ref_info_more = comments[ci][5].get("ref_info_more",{})
                    ref_info_more_list = ref_info_more.get(ref_id,[])
                    if ref_content_update:
                        if user_id not in ref_info_list:
                            ref_info_list.append(user_id)
                            ref_info[ref_id]=ref_info_list
                            ref_content_update = True
                    else:
                        if user_id not in ref_info_more_list:
                            ref_info_more_list.append(user_id)
                            ref_info_more[ref_id]=ref_info_more_list
                            ref_content_update = True

                    comments[ci][5]["ref_list"]=ref_list
                    comments[ci][5]["ref_info"]=ref_info
                    comments[ci][5]["ref_info_more"]=ref_info_more
                    comment_entity["comments"] = comments
                    chat["last_comment_entity"] = comment_entity
                    if ref_content_update:
                        update_aim(chat_id,chat)
                        break
                else:
                    ci = ci + 1
                    continue
        else:
            comment_entity = get_aim(comment_id)
            comments = comment_entity.get("comments")
            ci = 0
            for i in comments:
                if i[0] == comment_sequence:
                    ref_content_update = False
                    ref_list = comments[ci][5].get("ref_list",[])
                    if user_id not in ref_list:
                        ref_content = u"add"
                        ref_list.append(user_id)
                        ref_content_update = True
                    ref_num = len(ref_list)
                    # 第一次登陆时渠道锁定使用
                    ref_info = comments[ci][5].get("ref_info",{})
                    ref_info_list = ref_info.get(ref_id,[])
                    # 第二次登陆时渠道归档使用
                    ref_info_more = comments[ci][5].get("ref_info_more",{})
                    ref_info_more_list = ref_info_more.get(ref_id,[])
                    if ref_content_update:
                        if user_id not in ref_info_list:
                            ref_info_list.append(user_id)
                            ref_info[ref_id]=ref_info_list
                            ref_content_update = True
                    else:
                        if user_id not in ref_info_more_list:
                            ref_info_more_list.append(user_id)
                            ref_info_more[ref_id]=ref_info_more_list
                            ref_content_update = True

                    comments[ci][5]["ref_list"]=ref_list
                    comments[ci][5]["ref_info"]=ref_info
                    comments[ci][5]["ref_info_more"]=ref_info_more
                    comment_entity["comments"] = comments
                    chat["last_comment_entity"] = comment_entity
                    if ref_content_update:
                        update_aim(chat_id,chat)
                        break
                else:
                    ci = ci + 1
                    continue
        user = get_aim(user_id)
        user_name = user.get("name","")
        user_headimgurl = user.get("headimgurl","/static/img/headimgurl.png")
        msgtype = "COMMENTREFID"
        time_now = int(time.time())
        self.finish({"info": "ok","comment_id":comment_id,"sequence":comment_sequence,"time":time_now,"msgtype":msgtype,"ref_num":ref_num})
        msg = [msgtype, {
            "ref_num":ref_num,
            "ref":ref_content,
            "nickname": user_name,
            "headimgurl": user_headimgurl,
            "time": time_now,
            "user_id": user_id,
            "sequence": comment_sequence,
            "comment_id": comment_id,
            "uuid":uuid,
        }, chat_id]
        if not block_id:
            DataWebSocket.send_to_all(json_encode(msg))
        else:
            DataWebSocket.send_to_target_room(json_encode(msg),block_id)
class DelAPIHandler(WebRequest):
    @tornado.gen.coroutine
    def post(self):
        self.set_header("Access-Control-Allow-Origin", self.request.headers.get("Origin"))
        self.set_header("Access-Control-Allow-Credentials", "true")
        if not self.current_user:
            self.finish({"info":"error","about":"no login"})
            return
        user_id = self.current_user["id"]
        block_id = self.get_argument("block_id",None)
        chat_id = self.get_argument("chat_id",None)
        content = self.get_argument("content", None)
        uuid = self.get_argument("uuid",None)
        comment_id = self.get_argument("comment_id",None)
        comment_sequence = self.get_argument("comment_sequence",None)
        like_content = self.get_argument("like_content",None)
        like_content_update = False
        if not (comment_id and comment_sequence):
            self.finish({"info":"error","about":"no comment_id or comment_sequence"})
            return
        chat = get_aim(chat_id)
        print(chat_id,content)
        print(not chat,content=="",not content)
        comment_push = False
        if not chat or content == "" or not content:
            self.finish({"info":"error","about":"no chat or content"})
            return
        allow_user_ids = []
        if chat["owner_type"] in ["page"]:
            aim_id = chat["owner"]
            aim = get_aim(aim_id)
            editors = aim.get("editors",[aim["owner"]])
            allow_user_ids = editors
        comment_ids = chat.get("comment_ids",[])
        if comment_id == comment_ids[-1]:
            comment_entity = chat.get("last_comment_entity")
            comments = comment_entity.get("comments")
            ci = 0
            for i in comments:
                if i[0] == comment_sequence:
                    allow_user_ids = list(set(settings["developers"]) | set([comments[ci][1]]) | set(allow_user_ids))
                    if user_id not in allow_user_ids:
                        self.finish({"info":"error","about":"no permission"})
                        return
                    if comments[ci][6] == 0:
                        comments[ci][6] = 1
                        like_content_update = True
                    comment_entity["comments"] = comments
                    chat["last_comment_entity"] = comment_entity
                    if like_content_update:
                        update_aim(chat_id,chat)
                        break
                else:
                    ci = ci + 1
                    continue
        else:
            comment_entity = get_aim(comment_id)
            comments = comment_entity.get("comments")
            ci = 0
            for i in comments:
                if i[0] == comment_sequence:
                    # [comment_sequence, user_id, comment_time, comment_type, content, comment_plus, comment_del]
                    allow_user_ids = list(set(settings["developers"]) | set([comments[ci][1]]) | set(allow_user_ids))
                    if user_id not in allow_user_ids:
                        self.finish({"info":"error","about":"no permission"})
                        return
                    if comments[ci][6] == 0:
                        comments[ci][6] = 1
                        like_content_update = True
                    comment_entity["comments"] = comments
                    if like_content_update:
                        update_aim(comment_id, comment_entity)
                        break
                else:
                    ci = ci + 1
                    continue

        user = get_aim(user_id)
        user_name = user.get("name","")
        user_headimgurl = user.get("headimgurl","/static/img/headimgurl.png")
        msgtype = "COMMENTDEL"
        time_now = int(time.time())

        self.finish({"info": "ok","comment_id":comment_id,"sequence":comment_sequence,"time":time_now,"msgtype":msgtype})

        msg = [msgtype, {
            "del":like_content,
            "nickname": user_name,
            "headimgurl": user_headimgurl,
            "time": time_now,
            "user_id": user_id,
            "sequence": comment_sequence,
            "comment_id": comment_id,
            "uuid":uuid,
        }, chat_id]
        if not block_id:
            DataWebSocket.send_to_all(json_encode(msg))
        else:
            DataWebSocket.send_to_target_room(json_encode(msg),block_id)







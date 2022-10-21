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
import xmltodict
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

import traceback
from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient

from alipay.aop.api.domain.AlipayTradeCreateModel import AlipayTradeCreateModel
from alipay.aop.api.request.AlipayTradeCreateRequest import AlipayTradeCreateRequest
from alipay.aop.api.response.AlipayTradeCreateResponse import AlipayTradeCreateResponse

from alipay_plus import AliPay

from .data import DataWebSocket
class UnifiedWeixinAPIHandler(WebRequest):
    @tornado.gen.coroutine
    def post(self):
        if not self.current_user:
            self.finish({
                "info":"error",
                "about":"no login",
            })
            return
        if "Mobile" in self.request.headers.get("User-Agent", "") and "MicroMessenger" in self.request.headers.get("User-Agent", ""):
            price = self.get_argument("price","1")
            user_id = self.current_user["id"]
            aim_user_id = self.get_argument("user_id",user_id)
            block_id = self.get_argument("block_id",None)
            chat_id = self.get_argument("chat_id",None)
            MPWeixinAPP = self.get_argument("app",None)
            if MPWeixinAPP not in settings["MPWeixinApps"]:
                self.finish({"info":"error","about":"not in MPWeixinApps"})
                return
            user_agent = self.request.headers.get("User-Agent","")
            weixin_version = user_agent[user_agent.index('MicroMessenger/')+15:]
            weixin_version = int(weixin_version[:weixin_version.index('.')])
            weixin_pay = False
            if weixin_version >=5:
                weixin_pay = True
            if not weixin_pay:
                self.finish({
                        "info":"error",
                        "home_pay_type": "weixin_pay_error",
                        "about": "This Wechat Version is not ok for Payment!",
                    })
                return
            if MPWeixinAPP not in settings["MPWeixinApps"]:
                self.finish({
                        "info":"error",
                        "about":"not in MPWeixinApps",
                    })
                return

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

            user = get_aim(user_id)
            openid = user.get("weixin_openids",{}).get(MPWeixinAPP,[None])[0]
            if not openid:
                self.finish({
                        "info":"error",
                        "about":"no openid current app",
                    })
                return
            body = self.get_argument("title","OFCOURSE想当然·微信支付")
            price = int(price)
            remote_ip = self.request.headers.get("X-Forwarded-For", "").split(", ")[0] or self.request.remote_ip
            trade_no = str(time.time()).replace(".","")
            nonce = wx_noncestr
            output = """<xml>
    <appid>%s</appid>
    <attach>%s_%s_%s_%s</attach>
    <body>%s</body>
    <mch_id>%s</mch_id>
    <nonce_str>%s</nonce_str>
    <notify_url>https://new.ofcourse.io/api/pay/weixin/callback/%s</notify_url>
    <openid>%s</openid>
    <out_trade_no>%s</out_trade_no>
    <spbill_create_ip>%s</spbill_create_ip>
    <total_fee>%s</total_fee>
    <trade_type>JSAPI</trade_type>
    <sign>%s</sign>
</xml>""" % (   appID,
                MPWeixinAPP,
                user_id,
                block_id,
                chat_id,
                body,
                shopNumber,
                nonce,
                MPWeixinAPP,
                openid,
                trade_no,
                remote_ip,
                price,
                "%s")
            data = xmltodict.parse(output)["xml"]
            del data["sign"]
            print(data)
            temp_str = "&".join(["%s=%s" % (k, v) for k, v in data.items()])        
            temp_str += "&key=%s" % shopNumberKey
            sign = hashlib.md5(temp_str.encode("utf8")).hexdigest().upper()
            print(temp_str)
            print(sign)
            xml = output % sign
            http_client = tornado.httpclient.AsyncHTTPClient()
            request = tornado.httpclient.HTTPRequest(
                url = "https://api.mch.weixin.qq.com/pay/unifiedorder",
                method = "POST",
                body = xml,
                validate_cert = False)
            response = yield http_client.fetch(request)
            result = xmltodict.parse(response.body)["xml"]
            print(result)
            prepay_id = result["prepay_id"]
            timestamp = str(wx_timestamp)
            nonce = result["nonce_str"]

            data = {
                "appId": appID,
                "nonceStr": nonce,
                "timeStamp":timestamp,
                "package": "prepay_id=%s" % prepay_id,
                "signType": "MD5",
            }
            temp_str = "&".join(["%s=%s" % (k, data[k]) for k in sorted(data.keys())])
            temp_str += "&key=%s" % shopNumberKey
            pay_sign = hashlib.md5(temp_str.encode("utf8")).hexdigest().upper()

            self.finish({
                "info":"ok",
                "home_pay_type": "weixin_pay",
                "weixin_app": MPWeixinAPP,
                "prepay_id": prepay_id,
                "timestamp": timestamp,
                "nonce": nonce,
                "paysign": pay_sign,
            })
class CallbackWeixinAPIHandler(WebRequest):
    @tornado.gen.coroutine
    def post(self,MPWeixinAPP):
        if MPWeixinAPP not in settings["MPWeixinApps"]:
            raise tornado.web.HTTPError(403)
            return
        data = xmltodict.parse(self.request.body)["xml"]
        sign = data["sign"]
        print("sign:",sign)
        del data["sign"]
        temp_str = "&".join(["%s=%s" % (k, data[k]) for k in sorted(data.keys())])
        temp_str += "&key=%s" % settings["MPWeixinInfo"].get(MPWeixinAPP,{}).get("ShopNumberKey","")
        print("hashlib:",hashlib.md5(temp_str.encode("utf8")).hexdigest().upper())
        if sign != hashlib.md5(temp_str.encode("utf8")).hexdigest().upper():
            raise tornado.web.HTTPError(403)
            return
        fee = data["total_fee"]
        transaction_id = data["transaction_id"]
        out_trade_no = data["out_trade_no"]
        app,user_id,block_id,chat_id =  data["attach"].split("_")
        return_code = data["return_code"]
        content = data
        time_now = int(time.time())
        if return_code == "SUCCESS":
            check_result = conn.query("SELECT * FROM index_weixin_pay WHERE transaction_id = %s", transaction_id)
            if check_result:
                raise tornado.web.HTTPError(403)
                return
            # user_id = self.current_user["id"]
            # block_id = self.get_argument("block_id",None)
            # chat_id = self.get_argument("chat_id",None)
            # content = self.get_argument("content", None)
            # uuid = self.get_argument("uuid",None)
            uuid = None
            chat = get_aim(chat_id)
            last_comment_time = 0
            print(chat_id,content)
            print(not chat,content=="",not content)
            comment_push = False
            if not chat or content == "" or not content:
                # self.finish({"info":"error","about":"no chat or content"})
                return
            chat["comment_members"]=chat.get("comment_members",[])
            if user_id not in chat["comment_members"]:
                chat["comment_members"].append(user_id)
            comment_type = u"WEIXINPAYCALLBACKSUCCESS"
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
            self.finish()
            # self.finish({"info": "ok","comment_id":comment_id,"sequence":comment_sequence,"time":time_now,"msgtype":msgtype})
            conn.execute("INSERT INTO index_weixin_pay (user_id,block_id,chat_id,fee,app,createtime,transaction_id,out_trade_no,done,finishtime) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", user_id,block_id,chat_id,fee,app,time_now,transaction_id,out_trade_no,1,time_now)
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
class UnifiedPlusAlipayAPIHandler(WebRequest):
    @tornado.gen.coroutine
    def post(self):
        AlipayApp = self.get_argument("app","ofcourse")
        title = self.get_argument("title","OFCOURSE想当然·支付宝支付")
        user_id = self.current_user["id"]
        aim_user_id = self.get_argument("user_id",user_id)
        price = self.get_argument("price","1")
        block_id = self.get_argument("block_id",None)
        chat_id = self.get_argument("chat_id",None)

        price = "%.2f"%(int(price)/100.0)
        trade_no = str(time.time()).replace(".","")

        alipay = AliPay(
            appid=settings["AlipayInfo"][AlipayApp]["AlipayAppID"],
            app_notify_url=None,  # 默认回调url
            # app_private_key_string=settings["AlipayInfo"][AlipayApp]["AlipayPrivateKey"],
            # alipay_public_key_string=settings["AlipayInfo"][AlipayApp]["AlipayAppPublicKey"],
            # app_private_key_path=os.path.join(settings.BASE_DIR, "app_test/app_private_key.pem"),
            # alipay_public_key_path=os.path.join(settings.BASE_DIR, "app_test/alipay_public_key.pem"),
            app_private_key_string = open(os.path.join(os.path.dirname(__file__),'../%s'%settings["AlipayInfo"][AlipayApp]["AlipayPrivateKeyFile"])).read(),
            alipay_public_key_string = open(os.path.join(os.path.dirname(__file__),'../%s'%settings["AlipayInfo"][AlipayApp]["AlipayAppPublicKeyFile"])).read(),
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=False  # 默认False  配合沙箱模式使用
        )

        # 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=trade_no,
            total_amount=price,  # 将Decimal类型转换为字符串交给支付宝
            subject=title,
            # return_url=None,
            # notify_url=None  # 可选, 不填则使用默认notify url
            return_url="https://findmaster.xialiwei.com/home/page/46d23db454ba44d4ab6a28668378ab35",
            notify_url="https://new.ofcourse.io/api/pay/alipay/notify/%s/%s_%s_%s_%s"%(AlipayApp,AlipayApp,aim_user_id,block_id,chat_id),
        )
        # 让用户进行支付的支付宝页面网址
        ALIPAY_URL = "https://openapi.alipay.com/gateway.do"
        url = ALIPAY_URL + "?" + order_string
        self.finish({"info":"ok","about":"action redirect","redirect_url":url})
class NotifyAlipayAPIHandler(WebRequest):
    @tornado.gen.coroutine
    def post(self,AlipayApp,Attach):
        
        data = {k:v[0].decode("utf8") for k,v in self.request.arguments.items()}
        fee = data["total_amount"]
        transaction_id = data["trade_no"]
        out_trade_no = data["out_trade_no"]
        app,user_id,block_id,chat_id =  Attach.split("_")
        return_code = data["trade_status"]
        content = data
        time_now = int(time.time())
        if return_code == "TRADE_SUCCESS":
            check_result = conn.query("SELECT * FROM index_alipay_pay WHERE trade_no = %s", transaction_id)
            if check_result:
                raise tornado.web.HTTPError(403)
                return
            # user_id = self.current_user["id"]
            # block_id = self.get_argument("block_id",None)
            # chat_id = self.get_argument("chat_id",None)
            # content = self.get_argument("content", None)
            # uuid = self.get_argument("uuid",None)
            uuid = None
            chat = get_aim(chat_id)
            last_comment_time = 0
            print(chat_id,content)
            print(not chat,content=="",not content)
            comment_push = False
            if not chat or content == "" or not content:
                # self.finish({"info":"error","about":"no chat or content"})
                return
            chat["comment_members"]=chat.get("comment_members",[])
            if user_id not in chat["comment_members"]:
                chat["comment_members"].append(user_id)
            comment_type = u"ALIPAYPAYCALLBACKSUCCESS"
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
            self.finish()
            # self.finish({"info": "ok","comment_id":comment_id,"sequence":comment_sequence,"time":time_now,"msgtype":msgtype})
            conn.execute("INSERT INTO index_alipay_pay (user_id,block_id,chat_id,fee,app,createtime,trade_no,out_trade_no,done,finishtime) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", user_id,block_id,chat_id,fee,app,time_now,transaction_id,out_trade_no,1,time_now)
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

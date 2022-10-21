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
import nomagic.order
import nomagic.group
from nomagic.cache import get_user, get_users, update_user, get_doc, get_docs, update_doc, get_aim, get_aims, update_aim, get_entity, get_entities, update_entity
from nomagic.cache import BIG_CACHE
from setting import settings
from setting import conn

# from user_agents import parse as uaparse #早年KJ用来判断设备使用

from .base import WebRequest
from .base import WebSocket
import pymail

from .data import DataWebSocket

import stripe

class DashboardStoreHomeHandler(WebRequest):
    @tornado.gen.coroutine
    def get(self):
        if not self.current_user:
            self.finish({"info":"error","about":"no login"})
            return
        self.version = settings["version"]
        self.render("../template/winni_app/dashboard.html")
class SellerAppStoreHomeHandler(WebRequest):
    @tornado.gen.coroutine
    def get(self):
        if not self.current_user:
            self.finish({"info":"error","about":"no login"})
            return
        user_id = self.current_user["id"]
        user = get_aim(user_id)
        user_update = False
        winni_app_data = user.get("winni_app_data",{})
        shops_entity_id = winni_app_data.get("shops_entity",None)
        if not shops_entity_id:
            group = {
                "owner":user_id,
                "editors":[user_id],
                "subtype":"shops",
                "owner_type":"user",
            }
            [group_id,group] = nomagic.group.create_chat(group)
            shops_entity_id = group_id
            winni_app_data["shops_entity"]=shops_entity_id
            user_update = True
        if user_update:
            user["winni_app_data"]=winni_app_data
            user["updatetime"]=int(time.time())
            update_aim(user_id,user)
        self.shops_entity_id=shops_entity_id
        self.user_id = user_id
        self.user = user
        self.version = settings["version"]
        self.render("../template/winni_app/seller.html")
class LoginLinkStripeAppStoreAPIHandler(WebRequest):
    @tornado.gen.coroutine
    def post(self):
        if not self.current_user:
            self.finish({"info":"error","about":"no login"})
            return
        pay_type = self.get_argument("pay_type","test")
        shop_id = self.get_argument("shop_id",None)
        stripe_account_id = self.get_argument("stripe_account",None)
        user_id = self.current_user["id"]
        shop = get_aim(shop_id)
        if not shop:
            self.finish({"info":"error","about":"no shop"})
            return
        stripe.api_key = settings["stripe_api_key_test"]
        if pay_type in ["online"]:
            stripe.api_key = settings["stripe_api_key"]
        if not stripe_account_id:
            self.finish({"info":"error","about":"no account id"})
            return
        stripe_accounts = shop.get("stripe_accounts",{})
        shop_stripe_account_id = stripe_accounts.get(pay_type,{}).get("id",None)
        if shop_stripe_account_id != stripe_account_id:
            self.finish({"info":"error","about":"not shop's stripe account"})
            return
        result = stripe.AccountLink.create(
            account = stripe_account_id,
            refresh_url = "https://www.winni.app/home/store/app/shop/%s"%shop_id,
            return_url = "https://www.winni.app/home/store/app/shop/%s"%shop_id,
            type = "account_onboarding",
        )
        self.finish({"info":"ok","about":"success","result":result})
class RetrieveStripeShopAppStoreAPIHandler(WebRequest):
    @tornado.gen.coroutine
    def post(self):
        if not self.current_user:
            self.finish({"info":"error","about":"no login"})
            return
        pay_type = self.get_argument("pay_type","test")
        shop_id = self.get_argument("shop_id",None)
        stripe_account_id = self.get_argument("stripe_account",None)
        user_id = self.current_user["id"]
        shop = get_aim(shop_id)
        if not shop:
            self.finish({"info":"error","about":"no shop"})
            return
        stripe.api_key = settings["stripe_api_key_test"]
        if pay_type in ["online"]:
            stripe.api_key = settings["stripe_api_key"]
        if not stripe_account_id:
            self.finish({"info":"error","about":"no account id"})
            return
        stripe_accounts = shop.get("stripe_accounts",{})
        shop_stripe_account_id = stripe_accounts.get(pay_type,{}).get("id",None)
        if shop_stripe_account_id != stripe_account_id:
            self.finish({"info":"error","about":"not shop's stripe account"})
            return
        result = stripe.Account.retrieve(stripe_account_id)
        old_result = stripe_accounts[pay_type]
        if result == old_result:
            self.finish({"info":"ok","about":"same result","result":result})
            return
        stripe_accounts[pay_type] = result
        shop["stripe_accounts"]=stripe_accounts
        shop["updatetime"]=int(time.time())
        update_aim(shop_id,shop)
        self.finish({"info":"ok","about":"update result","result":result})

class ShopAppStoreHomeHandler(WebRequest):
    @tornado.gen.coroutine
    def get(self,shop_id):
        if not self.current_user:
            user_id = "no_login:%s"%str(time.time())
        else:
            user_id = self.current_user["id"]
        shop = get_aim(shop_id)
        if not shop:
            self.finish({"info":"error","about":"no shop"})
            return
        shop_update = False
        products_entity_id = shop.get("products_entity",None)
        if not products_entity_id:
            group = {
                "owner":shop_id,
                "editors":[user_id],
                "subtype":"products",
                "owner_type":"shop",
            }
            [group_id,group] = nomagic.group.create_chat(group)
            products_entity_id = group_id
            shop["products_entity"]=products_entity_id
            shop_update = True

        stripe_accounts = shop.get("stripe_accounts",{})

        stripe_account_id_test = stripe_accounts.get("test",{}).get("id",None)
        stripe_account_id_test_payouts_enabled = stripe_accounts.get("test",{}).get("payouts_enabled",False)
        if not stripe_account_id_test:
            account_type = "standard"
            stripe.api_key = settings["stripe_api_key_test"]
            result = stripe.Account.create(type = account_type)
            stripe_account_id_test = result.id
            stripe_account_id_test_payouts_enabled  = result.payouts_enabled
            stripe_accounts["test"]=result
            shop["stripe_accounts"]=stripe_accounts

            shop_update = True

        stripe_account_id_online = stripe_accounts.get("online",{}).get("id",None)
        stripe_account_id_online_payouts_enabled = stripe_accounts.get("online",{}).get("payouts_enabled",False)
        if not stripe_account_id_online:
            account_type = "standard"
            stripe.api_key = settings["stripe_api_key"]
            result = stripe.Account.create(type = account_type)
            stripe_account_id_online = result.id
            stripe_account_id_online_payouts_enabled  = result.payouts_enabled
            stripe_accounts["online"]=result
            shop["stripe_accounts"]=stripe_accounts
            shop_update = True

        hollow_entity_id = shop.get("hollow_entity",None)
        if not hollow_entity_id:
            group = {
                "owner":shop_id,
                "editors":[user_id],
                "subtype":"hollow",
                "owner_type":"shop",
            }
            [group_id,group] = nomagic.group.create_chat(group)
            hollow_entity_id = group_id
            shop["hollow_entity"]=hollow_entity_id
            shop_update = True

        if shop_update:
            update_aim(shop_id,shop)
        is_editors = False
        if user_id in shop.get("editors",[shop.get("owner",None)]):
            is_editors = True

        self.hollow_entity_id = hollow_entity_id
        self.stripe_account_id_test = stripe_account_id_test
        self.stripe_account_id_test_payouts_enabled = stripe_account_id_test_payouts_enabled
        self.stripe_account_id_online = stripe_account_id_online
        self.stripe_account_id_online_payouts_enabled = stripe_account_id_online_payouts_enabled
        self.products_entity_id = products_entity_id
        self.user_id = user_id
        self.is_editors = is_editors
        self.title = shop.get("title","")
        self.desc = shop.get("desc","")
        self.address = shop.get("address","")
        self.headimgurl = shop.get("headimgurl","")
        self.shop_id = shop_id
        self.version = settings["version"]
        self.render("../template/winni_app/shop.html")

class UserAppStoreHomeHandler(WebRequest):
    @tornado.gen.coroutine
    def get(self):
        if not self.current_user:
            self.finish({"info":"error","about":"no login"})
            return
        user_id = self.current_user["id"]
        user = get_aim(user_id)
        user_update = False
        winni_app_data = user.get("winni_app_data",{})
        orders_entity_id = winni_app_data.get("orders_entity",None)
        if not orders_entity_id:
            group = {
                "owner":user_id,
                "editors":[user_id],
                "subtype":"orders",
                "owner_type":"user",
            }
            [group_id,group] = nomagic.group.create_chat(group)
            orders_entity_id = group_id
            winni_app_data["orders_entity"]=orders_entity_id
            user_update = True
        collections_entity_id = winni_app_data.get("collections_entity",None)
        if not collections_entity_id:
            group = {
                "owner":user_id,
                "editors":[user_id],
                "subtype":"collections",
                "owner_type":"user",
            }
            [group_id,group] = nomagic.group.create_chat(group)
            collections_entity_id = group_id
            winni_app_data["collections_entity"]=collections_entity_id
            user_update = True
        likes_entity_id = winni_app_data.get("likes_entity",None)
        if not likes_entity_id:
            group = {
                "owner":user_id,
                "editors":[user_id],
                "subtype":"likes",
                "owner_type":"user",
            }
            [group_id,group] = nomagic.group.create_chat(group)
            likes_entity_id = group_id
            winni_app_data["likes_entity"]=likes_entity_id
            user_update = True
        if user_update:
            user["winni_app_data"]=winni_app_data
            user["updatetime"]=int(time.time())
            update_aim(user_id,user)

        self.orders_entity_id=orders_entity_id
        self.collections_entity_id=collections_entity_id
        self.likes_entity_id=likes_entity_id
        self.user_id = user_id
        self.user = user
        self.version = settings["version"]
        self.render("../template/winni_app/user.html")
class CreateShopAppStoreAPIHandler(WebRequest):
    def post(self):
        pass
        if not self.current_user:
            self.finish({"info":"error","about":"no login"})
            return
        user_id = self.current_user["id"]
        title = self.get_argument("title","A new shop")
        desc = self.get_argument("desc","A new shop comes here.")
        address = self.get_argument("address","A new shop is nearby.")
        headimgurl = self.get_argument("headimgurl","https://www.winni.app/static/img/winni_app/shops.png")

        shop = {
            "subtype":"shop",
            "title":title,
            "desc":desc,
            "owner":user_id,
            "address":address,
            "headimgurl":headimgurl,
            "editors":[user_id],
            "block_type":"shop",
        }
        [block_id,block]=nomagic.block.create_block(shop)
        self.finish({"info":"ok","about":"create success","block_id":block_id,"block_type":"shop"})



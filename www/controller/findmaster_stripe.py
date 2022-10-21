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


class PayOneCheckAPIHandler(WebRequest):
    @tornado.gen.coroutine
    def post(self):
        if not self.current_user:
            self.finish({"info":"error","about":"no login"})
            return
        user_id = self.current_user["id"]
        pay_type = self.get_argument("pay_type","test")
        stripe.api_key = settings["stripe_api_key_test"]
        if pay_type in ["online"]:
            stripe.api_key = settings["stripe_api_key"]

        one_stripe_account = self.get_argument("stripe_account","")
        stripe_account = one_stripe_account
        one_product_name = self.get_argument("product_name","")
        one_product_price = int(float(self.get_argument("product_price","0.5"))*100)
        one_product_quantity = int(self.get_argument("product_quantity","1"))
        one_product_tax_code = self.get_argument("product_tax_code","")
        one_shipping_name = self.get_argument("shipping_name","")
        one_shipping_price = int(float(self.get_argument("shipping_price","0.5"))*100)
        one_shipping_quantity = int(self.get_argument("shipping_quantity","0"))
        one_shipping_tax_code = self.get_argument("shipping_tax_code","")

        
        one_name = self.get_argument("name","Demo User")
        one_email = self.get_argument("email","franklin@example.com")
        one_country = self.get_argument("country","CA")
        one_line1 = self.get_argument("line1","Demo Line1")
        one_city = self.get_argument("city","Demo City")
        one_state = self.get_argument("state","MB")
        one_postal_code = self.get_argument("postal_code","postal_code")
        


        result_history_json = {
            "subscription_ready":[],
            "subscription":{},
            "subscription_show":[],
            "order_ready":[],
            "order":{},
            "payment_intent":{},
        }
        product = stripe.Product.create(
            name=one_product_name,
            tax_code=one_product_tax_code,
            stripe_account = stripe_account,
        )
        result_history_json["subscription_ready"].append(product)
        price = stripe.Price.create(
            unit_amount = one_product_price,
            currency = "cad",
            recurring = {
                "interval": "month"
            },
            product = product.id,
            tax_behavior = "exclusive",
            stripe_account = stripe_account,
        )
        result_history_json["subscription_ready"].append(price)
        shipping_product = stripe.Product.create(
            name=one_shipping_name,
            tax_code=one_shipping_tax_code,
            stripe_account = stripe_account,
        )
        result_history_json["subscription_ready"].append(shipping_product)
        shipping_price = stripe.Price.create(
            unit_amount = one_shipping_price,
            currency = "cad",
            recurring = {
                "interval": "month"
            },
            product = shipping_product.id,
            tax_behavior = "exclusive",
            stripe_account = stripe_account,
        )
        result_history_json["subscription_ready"].append(shipping_price)
        customer = stripe.Customer.create(
            description = "a new user",
            email = one_email,
            address = {
                "country": one_country,
                "state": one_state
            },
            expand = ["tax"],
            stripe_account = stripe_account,
        )
        result_history_json["subscription_ready"].append(customer)
        subscription = stripe.Subscription.create(
            customer=customer.id,
            items=[
                {
                  "price": price.id,
                  "quantity": one_product_quantity,
                },
                {
                  "price": shipping_price.id,
                  "quantity": one_shipping_quantity,
                },
            ],
            automatic_tax={
                "enabled": True,
            },
            payment_behavior='default_incomplete',
            expand=["latest_invoice"],
            stripe_account = stripe_account,
        )
        result_history_json["subscription_ready"].append(subscription)
        result_history_json["subscription"]=subscription
        amount_all = 0
        tax_amount_all = 0
        for data_info in subscription.latest_invoice.lines.data:
            amount_all = amount_all + data_info["amount"]
            result_history_json["subscription_show"].append(["pay","product","amount",data_info["amount"]])
            print("pay","amount",data_info["amount"])
            for tax in data_info["tax_amounts"]:
                tax_amount_all = tax_amount_all + tax["amount"]
                tax_rate = stripe.TaxRate.retrieve(
                  tax["tax_rate"],
                  stripe_account = stripe_account
                )
                result_history_json["subscription_show"].append(["tax",tax_rate.display_name,tax_rate.percentage,data_info["amount"]])
                print("tax:",tax_rate.display_name,tax_rate.percentage,tax["amount"])
        print("========")
        print("amount_all:",amount_all)
        result_history_json["subscription_show"].append(["pay in all","products","amount_all",amount_all])
        print("tax_amount_all:",tax_amount_all)
        result_history_json["subscription_show"].append(["tax in all","taxes","tax_amount_all",tax_amount_all])
        print("========")

        new_product = stripe.Product.create(
            name=one_product_name,
            tax_code=one_product_tax_code,
            stripe_account = stripe_account,
            type="good",
        )
        result_history_json["order_ready"].append(new_product)
        new_price = stripe.Price.create(
            unit_amount = one_product_price,
            currency = "cad",
            product = new_product.id,
            tax_behavior = "exclusive",
            stripe_account = stripe_account,
        )
        result_history_json["order_ready"].append(new_price)
        new_shipping_product = stripe.Product.create(
            name=one_shipping_name,
            tax_code=one_shipping_tax_code,
            stripe_account = stripe_account,
            type="good",
        )
        result_history_json["order_ready"].append(new_shipping_product)
        new_shipping_price = stripe.Price.create(
            unit_amount = one_shipping_price,
            currency = "cad",
            product = new_shipping_product.id,
            tax_behavior = "exclusive",
            stripe_account = stripe_account,
        )
        result_history_json["order_ready"].append(new_shipping_price)
        stripe.api_version = "2020-08-27; orders_beta=v2"
        stripe.api_account = stripe_account
        order = stripe.Order.create(
            stripe_account = stripe_account,
            line_items=[
                {
                    "price": new_price.id,
                    "quantity": one_product_quantity,
                },
                {
                    "price": new_shipping_price.id,
                    "quantity": one_shipping_quantity,
                },
            ],
            currency="cad",
            payment={
                "settings": {
                  "payment_method_types": ["card"],
                  "application_fee_amount":int(amount_all*0.1),
                },
            },
            shipping_details={
                "address": {
                    "line1": one_line1,
                    "city": one_city,
                    "state": one_state,
                    "postal_code": one_postal_code,
                    "country": one_country,
                },
                "name":one_name,
            },
            automatic_tax={
                "enabled": True,
            },
            expand=["line_items"],
        )
        print(order)
        result_history_json["order_ready"].append(order)
        result_history_json["order"]=order
        print("order ==== end")
        result = stripe.stripe_object.StripeObject(stripe_account=stripe_account).request('post', "/v1/orders/%s/submit"%(order.id), {
          "expected_total": order.amount_total,
          "expand": ['payment.payment_intent'],
        })
        print(result)
        result_history_json["payment_intent"]=result
        self.finish({
            "info":"ok",
            "about":"success",
            "result_history_json":result_history_json,
            "payment_intent":result,
            "stripe_account":stripe_account,
            })

class PayOneSuccessAPIHandler(WebRequest):
    def post(self):
        pass

class AccountListAPIHandler(WebRequest):
    @tornado.gen.coroutine
    def get(self):
        if not self.current_user:
            self.finish({"info":"error","about":"no login"})
            return
        user_id = self.current_user["id"]
        user = get_aim(user_id)
        pay_type = self.get_argument("pay_type","test")
        stripe_accounts = user.get("stripe_accounts",{}).get(pay_type,{})
        self.finish({"info":"ok","about":"success","stripe_accounts":stripe_accounts,"pay_type":pay_type})
class AccountAddAPIHandler(WebRequest):
    def post(self):
        if not self.current_user:
            self.finish({"info":"error","about":"no login"})
            return
        user_id = self.current_user["id"]
        user = get_aim(user_id)
        pay_type = self.get_argument("pay_type","test")
        # account_type = self.get_argument("type","standard")
        # delay_days = int(self.get_argument("delay_days","7"))
        # interval = self.get_argument("interval","daily")
        account_type = "standard"
        delay_days = 7
        interval = "daily"
        if account_type not in ["standard"]:
            self.finish({"info":"error","about":"type not in allowed"})
            return
        stripe.api_key = settings["stripe_api_key_test"]
        if pay_type in ["online"]:
            stripe.api_key = settings["stripe_api_key"]
        # if interval in ["manual"]:
        #     schedule = {
        #         "interval":interval
        #     }
        # else:
        #     schedule = {
        #         "delay_days":delay_days,
        #         "interval":interval
        #     }
        result = stripe.Account.create(
            type = account_type,
            # settings={
            #     "payouts":{
            #         "schedule":schedule
            #     }
            # },
        )

        stripe_accounts = user.get("stripe_accounts",{})
        stripe_accounts_pay_type = stripe_accounts.get(pay_type,{})
        stripe_accounts_pay_type[result.id]=result
        stripe_accounts[pay_type]=stripe_accounts_pay_type
        user["stripe_accounts"]=stripe_accounts
        user["updatetime"]=int(time.time())
        update_aim(user_id,user)
        self.finish({"info":"ok","about":"success","result":result,"pay_type":pay_type})
class AccountUpdateAPIHandler(WebRequest):
    def post(self):
        if not self.current_user:
            self.finish({"info":"error","about":"no login"})
            return
        user_id = self.current_user["id"]
        user = get_aim(user_id)
        pay_type = self.get_argument("pay_type","test")
        account_type = self.get_argument("type","standard")
        delay_days = int(self.get_argument("delay_days","7"))
        interval = self.get_argument("interval","daily")
        stripe_account_id = self.get_argument("stripe_account",None)
        stripe.api_key = settings["stripe_api_key_test"]
        if pay_type in ["online"]:
            stripe.api_key = settings["stripe_api_key"] 
        if not stripe_account_id:
            self.finish({"info":"error","about":"no account id"})
            return
        stripe_accounts = user.get("stripe_accounts",{})
        stripe_accounts_pay_type = stripe_accounts.get(pay_type,{})
        if not stripe_accounts_pay_type.get(stripe_account_id,None):
            self.finish({"info":"error","about":"no user's account id"})
            return
        if interval in ["manual"]:
            schedule = {
                "interval":interval
            }
        else:
            schedule = {
                "delay_days":delay_days,
                "interval":interval
            }
        result = stripe.Account.modify(
            stripe_account_id,
            settings={
                "payouts":{
                    "schedule":schedule
                }
            },
        )
        print(result)
        self.finish({"info":"ok","about":"success","result":result,"pay_type":pay_type})

class AccountAddLinkAPIHandler(WebRequest):
    def post(self):
        if not self.current_user:
            self.finish({"info":"error","about":"no login"})
            return
        user_id = self.current_user["id"]
        user = get_aim(user_id)
        pay_type = self.get_argument("pay_type","test")
        stripe.api_key = settings["stripe_api_key_test"]
        stripe_account_id = self.get_argument("stripe_account",None)
        if pay_type in ["online"]:
            stripe.api_key = settings["stripe_api_key"] 
        if not stripe_account_id:
            self.finish({"info":"error","about":"no account id"})
            return
        stripe_accounts = user.get("stripe_accounts",{})
        stripe_accounts_pay_type = stripe_accounts.get(pay_type,{})
        if not stripe_accounts_pay_type.get(stripe_account_id,None):
            self.finish({"info":"error","about":"no user's account id"})
            return
        result = stripe.AccountLink.create(
            account = stripe_account_id,
            refresh_url = "https://www.winni.app/reauth",
            return_url = "https://www.winni.app/return",
            type = "account_onboarding",
        )
        self.finish({"info":"ok","about":"success","result":result})

class AccountRetrieveAPIHandler(WebRequest):
    def post(self):
        if not self.current_user:
            self.finish({"info":"error","about":"no login"})
            return
        user_id = self.current_user["id"]
        user = get_aim(user_id)
        pay_type = self.get_argument("pay_type","test")
        stripe.api_key = settings["stripe_api_key_test"]
        stripe_account_id = self.get_argument("stripe_account",None)
        if pay_type in ["online"]:
            stripe.api_key = settings["stripe_api_key"]
        if not stripe_account_id:
            self.finish({"info":"error","about":"no account id"})
            return

        stripe_accounts = user.get("stripe_accounts",{})
        stripe_accounts_pay_type = stripe_accounts.get(pay_type,{})
        if not stripe_accounts_pay_type.get(stripe_account_id,None):
            self.finish({"info":"error","about":"no user's account id"})
            return

        result = stripe.Account.retrieve(stripe_account_id)

        stripe_account_pay_type_result = stripe_accounts_pay_type.get(stripe_account_id,{})
        if stripe_account_pay_type_result == result:
            self.finish({"info":"error","about":"same account info","result":result})
            return
        stripe_accounts_pay_type[stripe_account_id]=result
        stripe_accounts[pay_type] = stripe_accounts_pay_type
        user["stripe_accounts"]=stripe_accounts
        user["updatetime"]=int(time.time())
        update_aim(user_id,user)
        self.finish({"info":"ok","about":"success","result":result})

class CreateLoginLinkAPIHandler(WebRequest):
    def post(self):
        if not self.current_user:
            self.finish({"info":"error","about":"no login"})
            return
        user_id = self.current_user["id"]
        user = get_aim(user_id)
        pay_type = self.get_argument("pay_type","test")
        stripe.api_key = settings["stripe_api_key_test"]
        stripe_account_id = user.get("stripe_account",{}).get(pay_type,{}).get("id",None)
        if pay_type in ["online"]:
            stripe.api_key = settings["stripe_api_key"] 
        if not stripe_account_id:
            self.finish({"info":"error","about":"no account id"})
            return
        result = stripe.AccountLink.create(
            account = stripe_account_id,
            refresh_url = "https://www.winni.app/reauth",
            return_url = "https://www.winni.app/return",
            type = "account_onboarding",
        )
        self.finish({"info":"ok","about":"success","result":result})
class CreateAccountLinkAPIHandler(WebRequest):
    def post(self):
        if not self.current_user:
            self.finish({"info":"error","about":"no login"})
            return
        user_id = self.current_user["id"]
        user = get_aim(user_id)
        pay_type = self.get_argument("pay_type","test")
        stripe.api_key = settings["stripe_api_key_test"]
        stripe_account_id = user.get("stripe_account",{}).get(pay_type,{}).get("id",None)
        if pay_type in ["online"]:
            stripe.api_key = settings["stripe_api_key"] 
        if not stripe_account_id:
            self.finish({"info":"error","about":"no account id"})
            return
        result = stripe.AccountLink.create(
            account = stripe_account_id,
            refresh_url = "https://www.winni.app/reauth",
            return_url = "https://www.winni.app/return",
            type = "account_onboarding",
        )
        self.finish({"info":"ok","about":"success","result":result})
class RetrieveAccountAPIHandler(WebRequest):
    def post(self):
        if not self.current_user:
            self.finish({"info":"error","about":"no login"})
            return
        user_id = self.current_user["id"]
        user = get_aim(user_id)
        pay_type = self.get_argument("pay_type","test")
        stripe.api_key = settings["stripe_api_key_test"]
        if pay_type in ["online"]:
            stripe.api_key = settings["stripe_api_key"]
        stripe_account_id = user.get("stripe_account",{}).get(pay_type,{}).get("id",None)
        if not stripe_account_id:
            self.finish({"info":"error","about":"no account id"})
            return
        result = stripe.Account.retrieve(stripe_account_id)
        stripe_account = user.get("stripe_account",{})
        stripe_account_pay_type_result = stripe_account.get(pay_type,{})
        if stripe_account_pay_type_result == result:
            self.finish({"info":"error","about":"same account info","result":result})
            return    
        stripe_account[pay_type] = result
        user["stripe_account"]=stripe_account
        user["updatetime"]=int(time.time())
        update_aim(user_id,user)
        self.finish({"info":"ok","about":"success","result":result})

class CreateAccountAPIHandler(WebRequest):
    def post(self):
        if not self.current_user:
            self.finish({"info":"error","about":"no login"})
            return
        user_id = self.current_user["id"]
        user = get_aim(user_id)
        stripe_account_id = user.get("stripe_account",{}).get("id",None)
        account_type = self.get_argument("type","standard")
        if account_type not in ["standard"]:
            self.finish({"info":"error","about":"type not in allowed"})
            return
        pay_type = self.get_argument("pay_type","test")
        stripe.api_key = settings["stripe_api_key_test"]
        if pay_type in ["online"]:
            stripe.api_key = settings["stripe_api_key"]
        stripe_account_id = user.get("stripe_account",{}).get(pay_type,{}).get("id",None)            
        if stripe_account_id:
            self.finish({"info":"error","about":"already has stripe_account_id"})
            return
        result = stripe.Account.create(type = account_type)
        stripe_account = user.get("stripe_account",{})
        stripe_account[pay_type] = result
        user["stripe_account"]=stripe_account
        user["updatetime"]=int(time.time())
        update_aim(user_id,user)
        self.finish({"info":"ok","about":"success","result":result})

class HoldProductCaptureAPIHandler(WebRequest):
    @tornado.gen.coroutine
    def post(self):
        payment_intent_id = self.get_argument("payment_intent_id",None)
        payment_capture = int(self.get_argument("amount_to_capture",50))
        pay_type = self.get_argument("pay_type","test")
        stripe.api_key = settings["stripe_api_key_test"]
        if pay_type in ["online"]:
            stripe.api_key = settings["stripe_api_key"]
        intent = stripe.PaymentIntent.capture(
          payment_intent_id,
          amount_to_capture=payment_capture
        )
        self.finish({"info":"ok","about":"",})


class HoldProductCancelAPIHandler(WebRequest):
    def get(self):
        pass
class HoldProductAPIHandler(WebRequest):
    @tornado.gen.coroutine
    def post(self):
        pay_type = self.get_argument("pay_type","test")
        
        stripe.api_key = settings["stripe_api_key_test"]
        if pay_type in ["online"]:
            stripe.api_key = settings["stripe_api_key"]
        currency = self.get_argument("currency","usd")
        name = self.get_argument("name","DEMO Product")
        unit_amount = int(self.get_argument("unit_amount",50))
        quantity = int(self.get_argument("quantity",1))
        amount = unit_amount*quantity

        # customer = stripe.Customer.create()


        payment_intent = stripe.PaymentIntent.create(
          amount=amount,
          currency=currency,
          # payment_method_types=['card'],
          # confirm=True,
          capture_method='manual'
        )
        print(payment_intent)
        self.finish({"info":"ok","about":"hold product","payment_intent":payment_intent})

        # session = stripe.checkout.Session.create(
        #     line_items=[{
        #         "price_data": {
        #             "currency": currency,
        #             "product_data": {
        #                 "name": name,
        #                 "images":[
        #                     "http://fm-of-test0.xialiwei.com/659388851e8a4b2989de2203035331ba_7ae4379427cb2c6b0d302f67aef6460c?imageView2",
        #                     "http://fm-of-test0.xialiwei.com/659388851e8a4b2989de2203035331ba_f5d3e059a14d0e25be0cac2cbf34d5d4?imageView2",
        #                 ]
        #             },
        #             'unit_amount': unit_amount,
        #         },
        #         'quantity': quantity,
        #     }],
        #     mode='payment',
        #     success_url='https://findmaster.xialiwei.com/api/stripe/pay_success',
        #     cancel_url='https://findmaster.xialiwei.com/api/stripe/pay_cancel',
        # )
        # self.finish({"info":"ok","about":"pay product","redirect_uri":session.url})
class PayProductAPIHandler(WebRequest):
    def post(self):
        if not self.current_user:
            self.finish({"info":"error","about":"no login"})
            return
        user_id = self.current_user["id"]
        order_id = self.get_argument("order_id",None)
        store_id = self.get_argument("store_id",None)
        product_id = self.get_argument("product_id",None)
        block_id = self.get_argument("block_id",None)
        pay_type = self.get_argument("pay_type","test")
        customer_email = self.get_argument("email",None)
        stripe.api_key = settings["stripe_api_key_test"]
        if pay_type in ["online"]:
            stripe.api_key = settings["stripe_api_key"]
        currency = self.get_argument("currency","cad")
        name = self.get_argument("name","DEMO Product")
        unit_amount = int(self.get_argument("unit_amount",50))
        quantity = int(self.get_argument("quantity",1))
        image = self.get_argument("image","/static/img/msh_icon/logo.png")
        session = stripe.checkout.Session.create(
            customer_email = customer_email,
            billing_address_collection='auto',
            shipping_address_collection={
              'allowed_countries': ['CA'],
            },
            line_items=[
                {
                    "price_data": {
                        "currency": currency,
                        "product_data": {
                            "name": name,
                            "images":[
                                image
                            ],
                            "tax_code":"txcd_30060016",
                        },
                        'unit_amount': unit_amount,
                        "tax_behavior":"exclusive",
                        
                    },
                    'quantity': quantity,
                },      
            ],
            tax_id_collection={
                'enabled': True,
            },
            automatic_tax={'enabled': True},
            # automatic_tax={'enabled': False},
            mode='payment',
            success_url='https://www.winni.app/api/stripe/pay_success',
            cancel_url='https://www.winni.app/api/stripe/pay_cancel',
            stripe_account = "acct_1KV5xrPHs2ZcZy0K",
            payment_intent_data={
                'application_fee_amount': int(unit_amount*0.1),
                # "shipping":{
                #     "address":{
                #         "line1":"101 main street",
                #         "country": "CA",
                #         "state": "MB",
                #         "city":"winnipeg"
                #     },
                #     "name":"xlw",
                # }
            },
        )
        order_create = False
        if not order_id:
            order_create = True
        if not order_create:
            order = get_aim(order_id)
            if not order:
                order_create = True
        if order_create:
            order = {
                "subtype":"stripe_order",
                "product_id":product_id,
                "store_id":store_id,
                "owner":user_id,
                "rule":{},
                "checkout_sessions":[session]
            }
            [order_id,order] = nomagic.order.create_order(order)
        else:
            checkout_sessions = order.get("checkout_sessions",[])
            checkout_sessions.append(session)
            order["updatetime"]=int(time.time())
            update_aim(order_id.order)
        payment_intent = session.payment_intent
        fee = 0
        application_fee = 0
        app = settings["MPWeixinAppDefault"]
        time_now = int(time.time())
        transaction_id = None
        out_trade_no = None
        conn.execute("INSERT INTO index_stripe_pay (user_id,order_id,store_id,product_id,block_id,pay_type,fee,application_fee,app,createtime,payment_intent,transaction_id,out_trade_no,done,finishtime) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", user_id,order_id,store_id,product_id,block_id,pay_type,fee,application_fee,app,time_now,payment_intent,transaction_id,out_trade_no,0,time_now)
        self.finish({"info":"ok","about":"pay product","redirect_uri":session.url,"result":session})
class PaySuccessAPIHandler(WebRequest):
    def get(self):
        self.finish({"info":"ok","about":"pay success"})
class PayCancelAPIHandler(WebRequest):
    def get(self):
        self.finish({"info":"ok","about":"pay cancel"})

latest_request_body = None
class WebhookAPIHandler(WebRequest):
    def post(self):
        print("webhook")
        global latest_request_body
        latest_request_body = json_decode(self.request.body)
        print(latest_request_body)
        self.finish({"info":"ok"})
class LatestWebhookAPIHandler(WebRequest):
    def get(self):
        print(latest_request_body)
        self.finish({"info":"ok","about":"latest request body","data":latest_request_body})

class PayCreateAPIHandler(WebRequest):
    def post(self):
        if not self.current_user:
            self.finish({"info":"error","about":"no login"})
            return
        user_id = self.current_user["id"]
        pay_type = self.get_argument("pay_type","test")
        name = self.get_argument("name","DEMO Product")
        currency = self.get_argument("currency","cad")
        unit_amount = int(self.get_argument("unit_amount",50))
        quantity = int(self.get_argument("quantity",1))
        image = self.get_argument("image","/static/img/msh_icon/logo.png")
        stripe.api_key = settings["stripe_api_key_test"]
        if pay_type in ["online"]:
            stripe.api_key = settings["stripe_api_key"]
        stripe_account = self.get_argument("stripe_account",settings["stripe_account_default"])
        # payment_intent = stripe.PaymentIntent.create(
        #     amount=unit_amount*quantity,
        #     currency=currency,
        #     automatic_payment_methods={
        #         'enabled': True,
        #     },
        #     application_fee_amount=100,
        #     stripe_account = "acct_1KV5xrPHs2ZcZy0K",
        # )

        payment_link =stripe.PaymentLink.create(
            line_items=[
                {
                    "price_data": {
                        "currency": currency,
                        "product_data": {
                            "name": name,
                            "images":[
                                image
                            ],
                            "tax_code":"txcd_30060016",
                        },
                        'unit_amount': unit_amount,
                        "tax_behavior":"exclusive",
                        
                    },
                    "quantity": 1,
                },
            ],
            automatic_tax="true",
            on_behalf_of=stripe_account,
            application_fee_amount=int(unit_amount*0.1),
        )

        self.finish({"info":"ok","about":"success","result":payment_link})











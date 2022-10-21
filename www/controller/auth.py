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
from nomagic.cache import get_user, get_users, update_user, get_doc, get_docs, update_doc, get_aim, get_aims, update_aim, get_entity, get_entities, update_entity
from nomagic.cache import BIG_CACHE
from setting import settings
from setting import conn

# from user_agents import parse as uaparse #早年KJ用来判断设备使用

from .base import WebRequest
from .base import WebSocket
import pymail

class GetVcodeAPIHandler(WebRequest):
    @tornado.gen.coroutine
    def post(self):
        email = self.get_argument("email","")
        login = email
        email_subject = "Your verification code - Reset Password"
        time_now = int(time.time())
        if not pymail.check_email(email):
            self.finish({"info":"error","about":"Wrong email address."})
            return
        result = conn.query("SELECT * FROM index_login WHERE login = %s ORDER BY id ASC", login)
        if not result:
            self.finish({"info":"error","about":"Not registered."})
            return
        user_id = result[0].get("entity_id")
        user = get_aim(user_id)
        vcode = "".join(random.choice(string.ascii_letters+string.digits) for x in range(8))
        user["vcode"] = vcode
        user["vcode_finishtime"] = time_now+60*5
        user["update_timestamp"] = time.time()
        user_name = user.get("nickname",user_id)
        update_aim(user_id,user)
        # pymail.send_email_vcode("norelay@xialiwei.com", email, email_subject, "Xijia19900321",vcode,"https://www.xialiwei.com")
        # pymail.send_email_vcode("noreply@ofcourse.io", email, email_subject, "5TJmH7bYPgg9ejDM",vcode,"https://new.ofcourse.io",user_name)
        # pymail.send_email_vcode_hotmail("winniapp@outlook.com", email, email_subject, "winni_app_2022",vcode,"https://www.winni.app",user_name)
        # pymail.send_email_vcode_gmail("liwei.xia0223@gmail.com", email, email_subject, "njhclqrhvfqttnxj",vcode,"https://www.winni.app",user_name)
        # pymail.send_email_vcode_gmail("winniapp204@gmail.com", email, email_subject, "tqhwvdresmdlrjji",vcode,"https://www.winni.app",user_name)
        pymail.send_email_vcode_hotmail("zjjtgxaq2022@outlook.com", email, email_subject, "Hotpoorinchina2022",vcode,"https://office.xialiwei.com",user_name)
        self.finish({"info":"ok","about":"Verification code is sent to the email."})
class ResetPasswordAPIHandler(WebRequest):
    def post(self):
        email = self.get_argument("email",None)
        login = email
        vcode = self.get_argument("vcode",None)
        password0 = self.get_argument("password0",None)
        password1 = self.get_argument("password1",None)
        if not (email and vcode and password0 and password1):
            self.finish({"info":"error","about":"Not enough info."})
            return
        time_now = int(time.time())
        if not pymail.check_email(email):
            self.finish({"info":"error","about":"Wrong email address."})
            return
        result = conn.query("SELECT * FROM index_login WHERE login = %s ORDER BY id ASC", login)
        if not result:
            self.finish({"info":"error","about":"Not registered."})
            return
        user_id = result[0].get("entity_id")
        user = get_aim(user_id)
        old_vcode = user.get("vcode","")
        old_vcode_finishtime = user.get("vcode_finishtime",0)
        if time_now - old_vcode_finishtime > 0:
            self.finish({"info":"error","about":"The verification code is expired."})
            return
        user["vcode_finishtime"] = time_now
        user["update_timestamp"] = time.time()
        if old_vcode != vcode:
            update_aim(user_id,user)
            self.finish({"info":"error","about":"Wrong verification code. Please click and get a new one."})
            return
        if password0 != password1:
            update_aim(user_id,user)
            self.finish({"info":"error","about":"Different passwords. Please change and get a new verification code."})
            return
        hash_pwd = hashlib.sha1((password0 + user["salt"]).encode("utf8")).hexdigest()
        user["password"] = hash_pwd
        update_aim(user_id,user)
        self.finish({"info":"ok","about":"Reset Password Success."})

class ResetPasswordHandler(WebRequest):
    def get(self):
        self.time_now = int(time.time())
        self.version = settings["version"]
        self.render("../template/auth/reset_password.html")
class LogoutAPIHandler(WebRequest):
    def get(self):
        redirect_url = self.get_argument("next", "/")
        self.clear_cookie("user")
        # self.redirect(redirect_url)
        self.finish({"info":"ok","about":"logout success","action":"redirect","redirect":redirect_url})
class LogoutHandler(WebRequest):
    def get(self):
        redirect_url = self.get_argument("next", "/")
        self.clear_cookie("user")
        self.redirect(redirect_url)
class LoginAPIHandler(WebRequest):
    def post(self):
        if self.current_user:
            self.finish({"info":"ok","about":"already login"})
            return
        email = self.get_argument("email",None)
        password = self.get_argument("password",None)
        token = self.get_argument("token",None)
        redirect = self.get_argument("redirect",None)

        login = email
        result = conn.query("SELECT * FROM index_login WHERE login = %s ORDER BY id ASC", login)
        if not result:
            self.finish({"info":"error","about":"Not registered","redirect":"/#register_dom"})
            return
        user_id = result[0].get("entity_id",None)
        user = get_aim(user_id)
        hash_pwd = hashlib.sha1((password + user["salt"]).encode("utf8")).hexdigest()
        if user["password"] != hash_pwd:
            self.finish({"info":"error","about":"Wrong password or login.","redirect":"/#login_dom"})
            return
        if not redirect:
            redirect = "/"
        self.set_secure_cookie("user", tornado.escape.json_encode({"id": user_id, "v":1}),expires=time.time()+63072000,domain=settings.get("cookie_domain"))
        self.finish({"info":"ok","about":"redirect","redirect":redirect})
class RegisterAPIHandler(WebRequest):
    @tornado.gen.coroutine
    def post(self):
        if self.current_user:
            self.finish({"info":"ok","about":"already login"})
            return
        email = self.get_argument("email","")
        login = email
        email_subject = "Your verification code - Login"
        time_now = int(time.time())
        if not pymail.check_email(email):
            self.finish({"info":"error","about":"Wrong email address."})
            return
        result = conn.query("SELECT * FROM index_login WHERE login = %s ORDER BY id ASC", login)
        if result:
            self.finish({"info":"error","about":"Already registered."})
            return
        user = {}
        password_str = "".join(random.choice(string.ascii_letters+string.digits) for x in range(8))
        user["password"] = password_str
        user["name"] = login.split("@")[0]
        user["email"]=email
        [new_id, result] = nomagic.auth.create_user(user)
        conn.execute("INSERT INTO index_login (login, entity_id,app) VALUES(%s, %s, %s)", login, new_id,"")
        # pymail.send_email_gmail("winniapp204@gmail.com", email, email_subject, "tqhwvdresmdlrjji",password_str,"https://www.winni.app",user["name"])
        # pymail.send_email("noreply@ofcourse.io", email, email_subject, "5TJmH7bYPgg9ejDM",password_str,"https://new.ofcourse.io",user["name"])
        pymail.send_email_hotmail("zjjtgxaq2022@outlook.com", email, email_subject, "Hotpoorinchina2022",password_str,"https://office.xialiwei.com",user["name"])
        self.finish({"info":"ok","about":"Password is sent to the email, and go to login."})
class GetLoginAPIHandler(WebRequest):
    @tornado.gen.coroutine
    def get(self):
        if not self.current_user:
            self.finish({"info":"error","about":"not login"})
            return
        user_id = self.current_user["id"]
        result = conn.query("SELECT * FROM index_login WHERE entity_id = %s ORDER BY id ASC",user_id)
        if not result:
            self.finish({"info":"error","about":"no login"})
            return
        login = result[0].get("login",None)
        self.finish({"info":"ok","about":"get login info success","login":login})


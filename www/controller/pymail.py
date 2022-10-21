#!/bin/env python
#coding=utf-8
import sys
import os
import os.path
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

# import tornado
# import tornado.web
# import tornado.escape
# import tornado.websocket
# import tornado.httpclient
# import tornado.gen
# from tornado.escape import json_encode, json_decode

# import nomagic
# import nomagic.auth
# from nomagic.cache import get_user, get_users, update_user, get_doc, get_docs, update_doc, get_aim, get_aims, update_aim, get_entity, get_entities, update_entity
# from nomagic.cache import BIG_CACHE
# from setting import settings
# from setting import conn
# from setting import dconn

# from .base import WebRequest
# from .base import WebSocket

import smtplib
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

def check_email(email):
    if len(email) > 7:
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
            return 1
    return 0

def send_email(from_addr, to_addr, subject, password, email_code,host,user_name):
    msg = MIMEText("""
        <div style="
            background:#f9f9f9;
            padding:30px 10px 10px 10px;text-align:center;
            width:320px;height:auto;margin:20px;border-radius:4px;
            border:0px solid rgba(0,0,0,0.2);
            -webkit-box-shadow:0px 4px 12px rgba(0,0,0,0.2);
            box-shadow:0px 4px 12px rgba(0,0,0,0.2);">
        <div align="center">
            <img style="width:80px;height:80px;" src="https://office.xialiwei.com/static/img/oflogo.png">
        </div>
        <div style="font-size:22px;font-weight:bold;color:#333;">%s</div>
        <div style="font-size:14px;font-weight:bold;color:#666;">verification code</div>
        <div align="center">
            <p style="margin:15px;background:#f2f2f2;width:160px;font-weight:bold;padding:8px 0px;border-radius:2px;">%s</p>
        </div>
        <div style="font-size:14px;font-weight:nomarl;color:#666;">It's valiable for you to login, now!<br>With the verification code as a password.<br>You can change one after logging in for save.</div>
        <div style="margin:15px;">
            <a  href="%s"
                style="color:#2196F3;font-weight:bold;text-decoration:none;"
                >%s</a>
        </div>
        </div>
        """%(user_name,email_code,host,host),'html','utf-8')
    msg['From'] = '<%s>' % from_addr
    msg['To'] = '<%s>' % to_addr
    msg['Subject'] = subject
    msg['username'] = "Xialiwei"

    smtp = smtplib.SMTP_SSL('smtp.exmail.qq.com', 465)
    smtp.set_debuglevel(1)
    smtp.ehlo("smtp.exmail.qq.com")
    smtp.login(from_addr, password)
    smtp.sendmail(from_addr, [to_addr,], msg.as_string())
def send_email_gmail(from_addr, to_addr, subject, password, email_code,host,user_name):
    msg = MIMEText("""
        <div style="
            background:#f9f9f9;
            padding:30px 10px 10px 10px;text-align:center;
            width:320px;height:auto;margin:20px;border-radius:4px;
            border:0px solid rgba(0,0,0,0.2);
            -webkit-box-shadow:0px 4px 12px rgba(0,0,0,0.2);
            box-shadow:0px 4px 12px rgba(0,0,0,0.2);">
        <div align="center">
            <img style="width:200px;height:100px;object-fit:cover;" src="https://office.xialiwei.com/static/img/msh_icon/logo.png">
        </div>
        <div style="font-size:22px;font-weight:bold;color:#333;">%s</div>
        <div style="font-size:14px;font-weight:bold;color:#666;">verification code</div>
        <div align="center">
            <p style="margin:15px;background:#f2f2f2;width:160px;font-weight:bold;padding:8px 0px;border-radius:2px;">%s</p>
        </div>
        <div style="font-size:14px;font-weight:nomarl;color:#666;">It's valiable for you to login, now!<br>With the verification code as a password.<br>You can change one after logging in for save.</div>
        <div style="margin:15px;">
            <a  href="%s"
                style="color:#3c447b;font-weight:bold;text-decoration:none;"
                >%s</a>
        </div>
        </div>
        """%(user_name,email_code,host,host),'html','utf-8')
    msg['From'] = '<%s>' % from_addr
    msg['To'] = '<%s>' % to_addr
    msg['Subject'] = subject
    msg['username'] = "office"

    smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp.set_debuglevel(1)
    smtp.ehlo("smtp.gmail.com")
    smtp.login(from_addr, password)
    smtp.sendmail(from_addr, [to_addr,], msg.as_string())
def send_email_hotmail(from_addr, to_addr, subject, password, email_code,host,user_name):
    msg = MIMEText("""
        <div style="
            background:#f9f9f9;
            padding:30px 10px 10px 10px;text-align:center;
            width:320px;height:auto;margin:20px;border-radius:4px;
            border:0px solid rgba(0,0,0,0.2);
            -webkit-box-shadow:0px 4px 12px rgba(0,0,0,0.2);
            box-shadow:0px 4px 12px rgba(0,0,0,0.2);">
        <div align="center">
            <img style="width:200px;height:100px;object-fit:cover;" src="https://office.xialiwei.com/static/img/msh_icon/logo.png">
        </div>
        <div style="font-size:22px;font-weight:bold;color:#333;">%s</div>
        <div style="font-size:14px;font-weight:bold;color:#666;">verification code</div>
        <div align="center">
            <p style="margin:15px;background:#f2f2f2;width:160px;font-weight:bold;padding:8px 0px;border-radius:2px;">%s</p>
        </div>
        <div style="font-size:14px;font-weight:nomarl;color:#666;">It's valiable for you to login, now!<br>With the verification code as a password.<br>You can change one after logging in for save.</div>
        <div style="margin:15px;">
            <a  href="%s"
                style="color:#3c447b;font-weight:bold;text-decoration:none;"
                >%s</a>
        </div>
        </div>
        """%(user_name,email_code,host,host),'html','utf-8')
    msg['From'] = '<%s>' % from_addr
    msg['To'] = '<%s>' % to_addr
    msg['Subject'] = subject
    msg['username'] = "office"

    smtp = smtplib.SMTP('smtp.office365.com', 587)
    smtp.set_debuglevel(1)
    smtp.ehlo("smtp.office365.com")
    smtp.starttls()
    smtp.login(from_addr, password)
    smtp.sendmail(from_addr, [to_addr,], msg.as_string())

def send_email_vcode(from_addr, to_addr, subject, password, email_code, host,user_name):
    msg = MIMEText("""
        <div style="
            background:#f9f9f9;
            padding:30px 10px 10px 10px;text-align:center;
            width:320px;height:auto;margin:20px;border-radius:10px;
            border:0px solid rgba(0,0,0,0.2);
            -webkit-box-shadow:3.5px 3.5px 2.5px rgba(0,0,0,0.2);
            box-shadow:3.5px 3.5px 2.5px rgba(0,0,0,0.2);">
        <div align="center">
            <img style="width:80px;height:80px;" src="https://office.xialiwei.com/static/img/oflogo.png">
        </div>
        <div style="font-size:12px;font-weight:bold;color:#333333;margin:20px 0px 5px 0px;">%s</div>
        <div style="font-size:18px;font-weight:bold;color:#676767;">verification code</div>
        <div align="center">
            <p style="margin:15px;background:#f2f2f2;width:160px;font-weight:bold;padding:8px 0px;border-radius:2px;">%s</p>
        </div>
        <div style="font-size:14px;line-height:16px;font-weight:nomarl;color:#676767;">It's valiable in 5min.<br>And just for once.</div>
        <div style="margin:15px;">
            <a  href="%s"
                style="color:#6D41DC;font-weight:bold;text-decoration:none;font-size:15px;"
                >%s</a>
        </div>
        </div>
        """%(user_name,email_code,host,host.replace("https://","")),'html','utf-8')
    msg['From'] = '<%s>' % from_addr
    msg['To'] = '<%s>' % to_addr
    msg['Subject'] = subject
    msg['username'] = "Xialiwei"

    smtp = smtplib.SMTP_SSL('smtp.exmail.qq.com', 465)
    smtp.set_debuglevel(1)
    smtp.ehlo("smtp.exmail.qq.com")
    smtp.login(from_addr, password)
    smtp.sendmail(from_addr, [to_addr,], msg.as_string())
def send_email_vcode_gmail(from_addr, to_addr, subject, password, email_code, host,user_name):
    msg = MIMEText("""
        <div style="
            background:#f9f9f9;
            padding:30px 10px 10px 10px;text-align:center;
            width:320px;height:auto;margin:20px;border-radius:10px;
            border:0px solid rgba(0,0,0,0.2);
            -webkit-box-shadow:3.5px 3.5px 2.5px rgba(0,0,0,0.2);
            box-shadow:3.5px 3.5px 2.5px rgba(0,0,0,0.2);">
        <div align="center">
            <img style="width:200px;height:100px;object-fit:cover;" src="https://office.xialiwei.com/static/img/msh_icon/logo.png">
        </div>
        <div style="font-size:12px;font-weight:bold;color:#333333;margin:20px 0px 5px 0px;">%s</div>
        <div style="font-size:18px;font-weight:bold;color:#676767;">verification code</div>
        <div align="center">
            <p style="margin:15px;background:#f2f2f2;width:160px;font-weight:bold;padding:8px 0px;border-radius:2px;">%s</p>
        </div>
        <div style="font-size:14px;line-height:16px;font-weight:nomarl;color:#676767;">It's valiable in 5min.<br>And just for once.</div>
        <div style="margin:15px;">
            <a  href="%s"
                style="color:#3c447b;font-weight:bold;text-decoration:none;font-size:15px;"
                >%s</a>
        </div>
        </div>
        """%(user_name,email_code,host,host.replace("https://","")),'html','utf-8')
    msg['From'] = '<%s>' % from_addr
    msg['To'] = '<%s>' % to_addr
    msg['Subject'] = subject
    msg['username'] = "office"

    smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp.set_debuglevel(1)
    smtp.ehlo("smtp.gmail.com")
    smtp.login(from_addr, password)
    smtp.sendmail(from_addr, [to_addr,], msg.as_string())
def send_email_vcode_hotmail(from_addr, to_addr, subject, password, email_code, host,user_name):
    msg = MIMEText("""
        <div style="
            background:#f9f9f9;
            padding:30px 10px 10px 10px;text-align:center;
            width:320px;height:auto;margin:20px;border-radius:10px;
            border:0px solid rgba(0,0,0,0.2);
            -webkit-box-shadow:3.5px 3.5px 2.5px rgba(0,0,0,0.2);
            box-shadow:3.5px 3.5px 2.5px rgba(0,0,0,0.2);">
        <div align="center">
            <img style="width:100px;height:100px;" src="https://office.xialiwei.com/static/img/msh_icon/logo.png">
        </div>
        <div style="font-size:12px;font-weight:bold;color:#333333;margin:20px 0px 5px 0px;">%s</div>
        <div style="font-size:18px;font-weight:bold;color:#676767;">verification code</div>
        <div align="center">
            <p style="margin:15px;background:#f2f2f2;width:160px;font-weight:bold;padding:8px 0px;border-radius:2px;">%s</p>
        </div>
        <div style="font-size:14px;line-height:16px;font-weight:nomarl;color:#676767;">It's valiable in 5min.<br>And just for once.</div>
        <div style="margin:15px;">
            <a  href="%s"
                style="color:#3c447b;font-weight:bold;text-decoration:none;font-size:15px;"
                >%s</a>
        </div>
        </div>
        """%(user_name,email_code,host,host.replace("https://","")),'html','utf-8')
    msg['From'] = '<%s>' % from_addr
    msg['To'] = '<%s>' % to_addr
    msg['Subject'] = subject
    msg['username'] = "office"

    smtp = smtplib.SMTP('smtp.office365.com', 587)
    smtp.set_debuglevel(1)
    smtp.ehlo("smtp.office365.com")
    smtp.starttls()
    smtp.login(from_addr, password)
    smtp.sendmail(from_addr, [to_addr,], msg.as_string())

# class EmailCodeAPIHandler(WebRequest):
#     def get(self):
#         self.post()
#     @tornado.gen.coroutine
#     def post(self):
#         self.email_addr = self.get_argument("email_addr", None)
#         self.email_subject = self.get_argument("subject", u"Your OF COURSE verification code")
#         if check_email(self.email_addr):
#             login = self.email_addr
#             result = conn.query("SELECT * FROM index_login WHERE login = %s ORDER BY id ASC", login)
#             user_id = ""
#             if not result:
#                 self.finish({"info":"error","about":"start_no_email","action":"go_to_check_email"})
#                 return
#             user_id = result[0].get("entity_id","")
#             user = get_aim(user_id)
#             user_old_email_code = user.get("email_code",None)
#             # self.email_code = "".join(random.choice(string.digits) for x in range(4))
#             self.email_code = user_old_email_code
#             send_email(u"norelay@ofcourse.io", self.email_addr, self.email_subject, u"Paomian123",self.email_code)
#             self.finish({"info":"ok","about":"start_code_is_already_sent","email":self.email_addr})
#         else:
#             self.finish({"info":"error","about":"start_no_right_email_address"})

# 邮箱
# antlive_pro@hotpoor.com
# hotpoorinchina

# if __name__ == "__main__":
#     # 这里的密码是开启smtp服务时输入的客户端登录授权码，并不是邮箱密码
#     # 现在很多邮箱都需要先开启smtp才能这样发送邮件
#     # send_email(u"from_addr",u"to_addr",u"主题",u"password")
#     send_email(u"liwei_xia@hotpoor.org",u"1020517891@qq.com",u"主题",u"nzhcsmfegvwmbeha")



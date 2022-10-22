#!/bin/env python
#coding=utf-8
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/vendor/')
#os.chdir(os.path.dirname(os.path.abspath(__file__)))

import logging
import uuid
from version import version_num

settings = {
    "static_path": os.path.join(os.path.dirname(__file__),"static"),
    "demos_path": os.path.join(os.path.dirname(__file__),"demos"),
    "cookie_secret": "hotpoorinchina",
    "cookie_domain": "",
    "QiniuAccessKey": "mur-IT5gTofLZB_TVXMDCgpN8X7pBaE3ubNhSdcT",
    "QiniuSecretKey": "ayjHlbhzXDM6EAwP3jNMClXvBj3bHdcwt0mwPVt4",
    "QQMailSecretKey":"5TJmH7bYPgg9ejDM",
    "QQMailSecretKey1":"ChBBiPZy2ebawGJW",
    "MPWeixinJSMP":[],
    "MPWeixinAppDefault":"office",
    "MPWeixinApps":[],
    "MPWeixinInfo":{
        "office":{
            "MPWeixinID":"",
            "MPWeixinAppID":"",
            "MPWeixinAppSecret":"",
            "ShopNumber":"",
            "ShopNumberKey":"",
            "ShopNumberKeyV3":"",
            "accessToken":"",
            "ticket":"",
            "accessTokenTimer":0,
            "ca_certs":"",
            "client_key":"",
            "client_cert":"",
            "name":"",
            "MPWeixinTemplateHollowNotice":"",
        },
    },
    "AlipayApps":[],
    "AlipayInfo":{
        "office":{
            "AlipayAppID":"",
            "AlipayPrivateKey":"",
            "AlipayPublicKey":"",
            "AlipayAppPublicKey":"",
            "AlipayPrivateKeyFile":"",
            "AlipayPublicKeyFile":"",
            "AlipayAppPublicKeyFile":"",
        },
    },
    "AgoraAppID":"8b92e0b356c2411a8dc4f8ac28c78690",
    "AgoraAppCertificate":"ad58e10b3df9432c8c5b633069c90ec7",
    "BaiduYuyinAppID": "",
    "BaiduYuyinAPIKey": "",
    "BaiduYuyinSecretKey":"",
    "debug": True,
    # "debug": False,
    "wss_port":8100,
    "LoginCode":"automove",
    "developers":[
        "e332ed4385cc47ed8d908825eb6b493c",#夏力维邮箱1020517891@qq.com
    ],
    "uri_mapping":{
        "/"                 :"5bd603bfc032481d9a1947ae43d567f9",#首页
        "/mobile"           :"5bd603bfc032481d9a1947ae43d567f9",#手机端首页
        "/register"         :"f72eabff7f2c42daa6cc65d778457f2b",
        "/login"            :"798aa8035b7e4de1988f38033c4aeb3b",
        "/forget_pwd"       :"3ff85716e7664d5288b3699d3aa5dc28",
        "/support"          :"3fe2fe0659094e45a0b949a4a7c1d9c8",
    },
    # "msh_hollow":"a220ce8a87294ab087a2696803cf4f0d",
    # "msh_hollow_data":"2c1ae9b7f42f4c6a9495150bb75c9498",
    # "msh_login_scan":"ce49130f9a82472ba7e0cbe057beb11a",
    "store_ground":"4193deec8fa24a42ab45769203974f3d",
    "store_search":"732c378707e845838fd2a1d0343a47c6",
    "store_hollow":"8c1c2b542cf242a0ab2f106f06a0b60f",
    "stripe_public_key":"",
    "stripe_api_key":"",
    "stripe_public_key_test":"",
    "stripe_api_key_test":"",
    "stripe_webhook_secret_test":"",
    "stripe_webhook_secret":"",
    "stripe_account_default":"",
    "version":version_num,
    "base_ca_tax_id":"",
    "base_ca_company":"",
    "search_type":["title","desc","tags","doms","product_title","product_desc","sequence"],
    "search_no_str":" !\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~！？｡＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘'‛“”„‟…‧﹏.",
}

try:
    import torndb as database
    conn = database.Connection("127.0.0.1:3306", "office", "root", "root")
    conn1 = database.Connection("127.0.0.1:3306", "office1", "root", "root")
    conn2 = database.Connection("127.0.0.1:3306", "office2", "root", "root")
    ring = [conn1, conn2]
except:
    pass

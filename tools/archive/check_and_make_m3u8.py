#!/bin/env python
#coding=utf-8
import sys
import os
import qiniu
import time
import hashlib
import json
import urllib
import requests

from setting import settings

target_folder = "upload_ready"

def file_md5(file_path):
    with open(file_path, 'rb') as fp:
        data = fp.read()
    file_md5= hashlib.md5(data).hexdigest()
    return file_md5

def file_name_dir(file_dir,target_num=0):
    i = 0
    for root, dirs, files in os.walk(file_dir):
        print("file_name_dir:%s/%s"%(i,target_num))
        i = i+1
        if i > target_num:
            break
    return root,dirs,files

def file_name_cut(file_dir,block_id):
    for root, dirs, files in os.walk(file_dir):
        # print(root, dirs, files)
        #备注root返回当前目录路径；dirs返回当前路径下所有子目录；files返回当前路径下所有非目录子文件
        files_data = []
        for file_item in files:
            file_item_list = file_item.split(".")
            if file_item_list[-1] in ["mp4","m4a","mov","m4v","mkv"]:
                path_current = "%s/%s"%(root,file_item)
                file_md5_str = file_md5(path_current)
                qiniu_file_key = "%s_m3u8_%s_ts"%(block_id,file_md5_str)
                # os.system("ffmpeg -i %s -codec copy  -hls_list_size 0  -hls_wrap 0 -strict -2  -vbsf h264_mp4toannexb -absf aac_adtstoasc -f hls -hls_base_url https://cdn1.ofcourse.io/ %s/%s.m3u8"%(path_current,root,qiniu_file_key))
                os.system("ffmpeg -i \"%s\" -codec copy  -hls_list_size 0  -hls_flags 0 -strict -2  -vbsf h264_mp4toannexb -absf aac_adtstoasc -f hls -hls_base_url https://cdn1.ofcourse.io/ \"%s/%s.m3u8\""%(path_current,root,qiniu_file_key))
                
                print("video:%s.m3u8"%qiniu_file_key)
def file_name_upload(file_dir,block_id):
    for root, dirs, files in os.walk(file_dir):
        # print(root, dirs, files)
        #备注root返回当前目录路径；dirs返回当前路径下所有子目录；files返回当前路径下所有非目录子文件
        files_data = []
        for file_item in files:
            # print("file:%s/%s"%(root,file_item))
            path_now = "%s/%s/%s"%(block_id,root,file_item)
            path_current = "%s/%s"%(root,file_item)
            file_md5_str = file_md5(path_current)
            file_item_list = file_item.split(".")

            if file_item_list[-1] in ["m3u8","ts"]:
                qiniu_file_key = file_item
            else:
                qiniu_file_key = "%s_s_%s"%(block_id,file_md5_str)
            file_info = {
                "name":file_item,
                "path":path_now,
                "md5":file_md5_str,
                "link":"http://cdn1.ofcourse.io/%s"%qiniu_file_key,
                "cdn_type":"secret",
            }
            files_list.append(file_info)
            files_data.append(file_info)
            print(file_info)
            q = qiniu.Auth(settings["QiniuAccessKey"], settings["QiniuSecretKey"])
            # uptoken = q.upload_token("audio", key, 3600, policy)
            uptoken = q.upload_token("ofcourse-secret")
            localfile = os.path.join(os.path.dirname(__file__), path_current)
            ret, info = qiniu.put_file(uptoken, qiniu_file_key, localfile)
        file_name_data = {
            "root":root,
            "dirs":dirs,
            "files":files,
            "files_data":files_data,
        }
        files_tree.append(file_name_data)

def check_dir(dir_item):
    print("check dir_item:",dir_item)
    url = "https://new.ofcourse.io/api/page/add_free"
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    }
    data = {
        "token": "xialiwei_follows_god",
        "user_id": "fcdb4ff181a74be2bb2b49057a891427",
        "title": dir_item,
        "desc": dir_item,
    }
    request = requests.post(url, headers=header, data=data)
    request_json = json.loads(request.text)
    block_id = request_json["block_id"]
    print(block_id)
    target_folder_now = "%s/%s"%(target_folder,dir_item)
    print("target_folder_now:",target_folder_now)
    file_name_cut(target_folder_now,block_id)
    file_name_upload(target_folder_now,block_id)
    print(len(files_list))
    data_json = {
        "folder_name":dir_item,
        "block_id":block_id,
        "data":files_list,
        "tree":files_tree,
    }
    with open("%s.json"%block_id, "w", encoding="utf-8") as file:
        file.write(json.dumps(data_json, indent=2, ensure_ascii=False)) #ensure_ascii=False可以消除json包含中文的乱码问题

root,dirs,files = file_name_dir(target_folder,0)
print(root,dirs,files)

for dir_item in dirs:
    files_list = []
    files_tree = []
    print(dir_item)
    check_dir(dir_item)



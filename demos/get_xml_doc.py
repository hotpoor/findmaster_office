#!/bin/env python
#coding=utf-8
import docx
from docx.shared import Length, Pt, RGBColor
from lxml import etree
import xmltodict
import json
import time
import string
import random
import requests
import jieba

from xml.dom.minidom import parseString

from zipfile import ZipFile
from bs4 import BeautifulSoup

# document = ZipFile('test.docx')
# xml = document.read("word/document.xml")
# wordObj = BeautifulSoup(xml.decode("utf-8"))
# texts = wordObj.findAll("w:t")
# str = ''
# for text in texts:
#     if text.text is not None:
#         # print(text.text)
#         str = str + text.text



filename = "1311工作面注氮安全技术措施.doc"

def upload_doc(filename):
    print(filename)
    document = ZipFile(filename)
    
    xml = document.read("word/document.xml")
    print(xml)
upload_doc(filename)
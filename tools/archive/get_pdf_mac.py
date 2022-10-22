import pathlib
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams, LTTextBox, LTFigure, LTImage
from pdfminer.converter import PDFPageAggregator
import json
import requests
from setting import settings

# path = list(pathlib.Path.cwd().parents)[1].joinpath('data/automate/002pdf')
# f_path = 'a.pdf'

def upload_pdf(filename,download_link=""):
    f_path = filename
    p_list = [
        "文件名: %s"%filename,
        "下载地址: %s"%download_link
    ]
    with open(f_path, 'rb') as f:
        parser = PDFParser(f)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
            layout = device.get_result()
            for x in layout:
                # 获取文本对象
                if isinstance(x, LTTextBox):
                    print(x.get_text().strip())
                    p_list.append(x.get_text().strip())
                # 获取图片对象
                if isinstance(x,LTImage):
                    print('这里获取到一张图片')
                    p_list.append("[图片]")
                # 获取 figure 对象
                if isinstance(x,LTFigure):
                    print('这里获取到一个 figure 对象')
                    p_list.append("[figure对象]")

    p_list_str = json.dumps(p_list)
    print("文档行数:",len(p_list))
    url = "https://office.xialiwei.com/api/page/add_free_pdf"
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    }
    data = {
        "token": "xialiwei_follows_god",
        "user_id": settings["user_id"],
        "title": filename,
        "desc": filename,
        "xml1":"{}",
        "xml2":"{}",
        "pre_p_list":p_list_str,
    }
    request = requests.post(url, headers=header, data=data)
    request_json = json.loads(request.text)
    block_id = request_json["block_id"]
    print(block_id)
    url = "https://office.xialiwei.com/api/search/add_free_page"
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    }

    data = {
        "token": "xialiwei_follows_god",
        "user_id": settings["user_id"],
        "search":"add free page default",
        "block_id":block_id,
        "type":"sequence",
        "block_id_sequence":"add free page default",
        "search":"add free page",
    }
    request = requests.post(url, headers=header, data=data)
    request_json = json.loads(request.text)

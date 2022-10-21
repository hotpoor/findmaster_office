from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams,LTTextBox,LTFigure,LTImage,LTTextLine,LTChar,LTPage
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed

pdf_path = 'test2.pdf'
result_list = []

def parse_pdf():
    fp = open(pdf_path, 'rb')
    # 用文件对象创建一个PDF文档分析器
    parser = PDFParser(fp)
    # 创建一个PDF文档
    doc = PDFDocument()
    # 连接分析器，与文档对象
    parser.set_document(doc)
    doc.set_parser(parser)
    # 提供初始化密码，如果没有密码，就创建一个空的字符串
    doc.initialize()
    # 检测文档是否提供txt转换，不提供就忽略
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建PDF，资源管理器，来共享资源
        rsrcmgr = PDFResourceManager()
        # 创建一个PDF设备对象
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr,laparams=LAParams())#laparams=laparams
        # 创建一个PDF解释其对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        # 循环遍历列表，每次处理一个page内容
        doc.get_pages() #获取page列表
        first_page = 1
        for page in doc.get_pages():
            interpreter.process_page(page)
            # 接受该页面的LTPage对象
            layout = device.get_result()
            # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象
            # 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等
            # 想要获取文本就获得对象的text属性，
            print(page.mediabox)

            for x in layout:
                # print(x)
                if isinstance(x, LTTextBoxHorizontal):
                    # print(x.x0,x.x1,x.y0,x.y1)
                    result = x.get_text()
                    # print(result)
                    result_json ={
                        "x0":x.x0,
                        "x1": x.x1,
                        "y0": x.y0,
                        "y1": x.y1,
                        "page":first_page,
                        "text":result
                    }
                    result_list.append(result_json)

            first_page += 1

if __name__ == '__main__':
    parse_pdf()

# print('a=',result_list)
import pathlib
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams, LTTextBox, LTFigure, LTImage
from pdfminer.converter import PDFPageAggregator

# path = list(pathlib.Path.cwd().parents)[1].joinpath('data/automate/002pdf')
# f_path = 'a.pdf'

def upload_pdf(filename):
    f_path = filename
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
                # 获取图片对象
                if isinstance(x,LTImage):
                    print('这里获取到一张图片')
                # 获取 figure 对象
                if isinstance(x,LTFigure):
                    print('这里获取到一个 figure 对象')

upload_pdf('a.pdf')
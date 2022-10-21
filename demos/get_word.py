import docx
from docx.shared import Length, Pt, RGBColor

file=docx.Document("template.docx")

text_list=[]
font_list=[]

def read_docx(file):
    n=1
    for p in file.paragraphs:
        p_line = {
            "paragraph":n,
            "text":p.text,
            "font_color":[]
        }
        for run in p.runs:
            name = run.font.name
            size = run.font.size
            bold = run.bold
            text = run.text
            rgb = run.font.color.rgb
            print(type(rgb))
            print("============")
            print(name,size,bold,text)
            if bold in [None]:
                bold = 0
            else:
                bold = 1
            if name in[None]:
                name = '宋体'
            if name in "仿宋_GB2312":
                    name = '仿宋'
            if size in [None]:
                size = 200000
            if run.font.color.rgb in [None]:
               rgb = [0,0,0]
            result_json = {
                "color":list(rgb),
                "text":run.text,
                "size":size,
                "name":name,
                "bold":bold
            }
            p_line["font_color"].append(result_json)
        font_list.append(p_line)
        n+=1
    print(font_list)
    return font_list

print('docx=',read_docx(file))

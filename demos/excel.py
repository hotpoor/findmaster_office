import xlrd

filename = r"D:\github\1\hotpoor_autoclick_xhs\费用报销单模板-12月.xls"
filename1=r"D:\github\1\hotpoor_autoclick_xhs\费用报销单模板-12月.xlsx"
filename2=r"D:\github\1\hotpoor_autoclick_xhs\12月统计新总表(4)(1).xls"
book = xlrd.open_workbook(filename2, formatting_info=True)
sheet_1 = book.sheet_by_index(0)
rowNum = sheet_1.nrows  # sheet行数
colNum = sheet_1.ncols  # sheet列数

def getBGColor(book, sheet, row, col):
    bgfx = sheet.cell_xf_index(row, col)
    xf = book.xf_list[bgfx]
    bgx = xf.background.pattern_colour_index
    pattern_colour = book.colour_map[bgx]
    return pattern_colour

def get_front_color(book, sheet, row, col):
    xf_list = book.xf_list
    cell_xf_index = sheet_1.cell_xf_index(row, col)
    cell_xf = xf_list[cell_xf_index]
    font_list = book.font_list
    font_index = cell_xf.font_index
    font = font_list[font_index]
    font_color = font.colour_index
    pattern_color = book.colour_map[font_color]
    return pattern_color

def get_font_bold(book,sheet):
    font = book.font_list
    cell_xf = book.xf_list[sheet.cell_xf_index(row, col)]
    return font[cell_xf.font_index].bold

def get_font_name(book,sheet,row,col):
    xf_list = book.xf_list
    cell_xf_index = sheet.cell_xf_index(row, col)
    cell_xf = xf_list[cell_xf_index]
    font_list = book.font_list
    font_index = cell_xf.font_index
    font = font_list[font_index]
    font_name = font.name
    return font_name

def get_font_italic(book,sheet,row,col):
    xf_list = book.xf_list
    cell_xf_index = sheet.cell_xf_index(row, col)
    cell_xf = xf_list[cell_xf_index]
    font_list = book.font_list
    font_index = cell_xf.font_index
    font = font_list[font_index]
    font_italic = font.italic
    return font_italic

def get_alignment(book,sheet,row,col):
    xf_list = book.xf_list
    cell_xf_index = sheet.cell_xf_index(row, col)
    cell_xf = xf_list[cell_xf_index]
    alignment = cell_xf.alignment
    return alignment.hor_align

def get_font_size(book,sheet,row,col):
    xf_list = book.xf_list
    cell_xf_index = sheet.cell_xf_index(row, col)
    cell_xf = xf_list[cell_xf_index]
    font_list = book.font_list
    font_index = cell_xf.font_index
    font = font_list[font_index]
    font_size = font.height
    return font_size

def reader():
    data = xlrd.open_workbook(filename2)
    table = data.sheets()[0]
    merged_cells=[]
    for i in table.merged_cells:
        merged_cells.append(list(i))
    company = []
    for i in range(0,table.nrows):
        company.append(table.row_values(i))
        # print(table.row_values(i))
    print('b=',company)
    print('c=',merged_cells)
reader()

BG_list=[]
for i in range(0,rowNum):
    for j in range(0,colNum):
        if getBGColor(book,sheet_1,i,j) == None:
            print('')
        else:
            data_json = {
                "row":i,
                "col":j,
                "rgb":list(getBGColor(book,sheet_1,i,j))
            }
            BG_list.append(data_json)
print('background=',BG_list)

font_bold=[]
for row in range(0,sheet_1.nrows):
    for col in range(0,sheet_1.ncols):
        if get_font_bold(book,sheet_1) == 1:
            data_json = {
                "row": row,
                "col": col,
                "bold": get_font_bold(book,sheet_1)
            }

            font_bold.append(data_json)
print('font_bold=',font_bold)

font_color = []
for row in range(0,sheet_1.nrows):
    for col in range(0,sheet_1.ncols):
        if get_front_color(book,sheet_1,row,col) != None:
                data_json = {
                    "row": row,
                    "col": col,
                    "rgb": list(get_front_color(book,sheet_1,row,col))
                }
                font_color.append(data_json)
print('font_color=',font_color)

font_name = []
for row in range(0,sheet_1.nrows):
    for col in range(0,sheet_1.ncols):
        if get_font_name(book,sheet_1,row,col) != None:
                data_json = {
                    "row": row,
                    "col": col,
                    "name": get_font_name(book,sheet_1,row,col)
                }
                font_name.append(data_json)
print('font_name=',font_name)

font_italic = []
for row in range(0,sheet_1.nrows):
    for col in range(0,sheet_1.ncols):
        if get_font_italic(book,sheet_1,row,col) != None:
                data_json = {
                    "row": row,
                    "col": col,
                    "italic": get_font_italic(book,sheet_1,row,col)
                }
                font_italic.append(data_json)
print('font_italic=',font_italic)

font_size = []
for row in range(0,sheet_1.nrows):
    for col in range(0,sheet_1.ncols):
        if get_font_size(book,sheet_1,row,col) != None:
                data_json = {
                    "row": row,
                    "col": col,
                    "size": get_font_size(book,sheet_1,row,col)
                }
                font_size.append(data_json)
print('font_size=',font_size)

font_align = []
for row in range(0,sheet_1.nrows):
    for col in range(0,sheet_1.ncols):
        if get_alignment(book,sheet_1,row,col) != None:
                data_json = {
                    "row": row,
                    "col": col,
                    "align": get_alignment(book,sheet_1,row,col)
                }
                font_size.append(data_json)
print('font_align=',font_align)
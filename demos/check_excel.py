import xlrd
filename = r"demo4.xlsx"
data_type = {
    0: 'empty（空的）',
    1: 'string（text）',
    2: 'number',
    3: 'date',
    4: 'boolean',
    5: 'error',
    6: 'blank(空白表格)'
}
def reader():
    if ".xlsx" in filename:
        data = xlrd.open_workbook(filename)
    else:
        data = xlrd.open_workbook(filename,formatting_info=True)
        
    table = data.sheets()[0]
    merged_cells=[]
    for i in table.merged_cells:
        merged_cells.append(list(i))
    company = []
    for i in range(0,table.nrows):
        company.append(table.row_values(i))
        # print(table.row_values(i))
    print(company)
    print(merged_cells)

    cell_item = table.cell(22,2)
    cell_index = cell_item.xf_index
    xf_style = data.xf_list[cell_index]
    xf_background = xf_style.background
    fill_pattern = xf_background.fill_pattern
    pattern_colour_index = xf_background.pattern_colour_index
    background_colour_index = xf_background.background_colour_index

    pattern_colour = data.colour_map[pattern_colour_index]
    background_colour = data.colour_map[background_colour_index]
    print(fill_pattern)
    print(pattern_colour)
    print(background_colour)

    cell_value=table.cell_value(22, 2)
    cell_type=table.cell_type(22, 2)
    print("cell_value:",cell_value)
    print("cell_type:",data_type[cell_type])
    print()
    data_str_set = xlrd.xldate_as_tuple(cell_value,data.datemode)
    print(data_str_set)
    data_str_list = []
    for i in data_str_set:
        data_str_list.append("%s"%i)
    print(data_str_list)
    print("/".join(data_str_list))
reader()
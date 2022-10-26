import xlrd
import time
import json
# filename = r"demo4.xlsx"

filename = "瓦斯日报 10.18.xlsx"
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
    stations = []
    date_hours = [
        "23:00",
        "00:00",
        "01:00",
        "02:00",
        "03:00",
        "04:00",
        "05:00",
        "06:00",
        "07:00",
        "08:00",
        "09:00",
        "10:00",
        "11:00",
        "12:00",
        "13:00",
        "14:00",
        "15:00",
        "16:00",
        "17:00",
        "18:00",
        "19:00",
        "20:00",
        "21:00",
        "22:00",
        "23:00",
    ]
    data_list = []
    data_men = {}
    rows = []
    for row in range(0,table.nrows):
        is_station = False
        cols = table.row_values(row)
        
        col_num = 0
        for col in range(0, table.ncols):
            if table.cell(row, col).ctype == 3 and type(table.cell(row, col).value) is float:
                date_value = xlrd.xldate_as_datetime(table.cell(row, col).value, data.datemode)
                if str(date_value).endswith("00:00:00") or str(date_value).endswith("0:00"):
                    cols[col] = str(date_value).split(" ")[0]
                    date_value_list = cols[col].split(":")
                    if len(date_value_list)>1:
                        cols[col] = "%s:%s"%(date_value_list[0],date_value_list[1])
                        is_station = True
                        data_men_current_base_json = {
                            "first":"",
                            "col_nums":[],
                            "col_nums_json":{},
                        }
                        data_men_current = data_men.get(cols[col+1],data_men_current_base_json)
                        data_men_current_col_nums = data_men_current.get("col_nums",[])
                        if "%s"%col_num not in data_men_current_col_nums:
                            data_men_current_col_nums.append("%s"%col_num)
                            data_men_current["col_nums"]=data_men_current_col_nums
                        data_men_current_col_nums_list = data_men_current.get("col_nums_json",{}).get(col_num,[])
                        data_men_current_col_nums_list.append([cols[col],cols[0],col_num])
                        data_men_current["col_nums_json"][col_num]=data_men_current_col_nums_list
                        data_men[cols[col+1]]=data_men_current
                    print(date_value_list)

                elif str(date_value).startswith("1899-12-31"):
                    cols[col] = str(date_value).split(" ")[1]
                    date_value_list = cols[col].split(":")
                    if len(date_value_list)>1:
                        cols[col] = "%s:%s"%(date_value_list[0],date_value_list[1])
                        is_station = True
                        data_men_current_base_json = {
                            "first":"",
                            "col_nums":[],
                            "col_nums_json":{},
                        }
                        data_men_current = data_men.get(cols[col+1],data_men_current_base_json)
                        data_men_current_col_nums = data_men_current.get("col_nums",[])
                        if "%s"%col_num not in data_men_current_col_nums:
                            data_men_current_col_nums.append("%s"%col_num)
                            data_men_current["col_nums"]=data_men_current_col_nums
                        data_men_current_col_nums_list = data_men_current.get("col_nums_json",{}).get(col_num,[])
                        data_men_current_col_nums_list.append([cols[col],cols[0],col_num])
                        data_men_current["col_nums_json"][col_num]=data_men_current_col_nums_list
                        data_men[cols[col+1]]=data_men_current
                    print(date_value_list)
                else:
                    cols[col] = date_value
                    print(cols[col])
            col_num +=1
        if is_station:
            stations.append(cols[0])
        # company.append(table.row_values(i))
        rows.append(cols)
    company = rows
        # print(table.row_values(i))
    # print(company)
    # print(merged_cells)

    # cell_item = table.cell(22,2)
    # cell_index = cell_item.xf_index
    # xf_style = data.xf_list[cell_index]
    # xf_background = xf_style.background
    # fill_pattern = xf_background.fill_pattern
    # pattern_colour_index = xf_background.pattern_colour_index
    # background_colour_index = xf_background.background_colour_index

    # pattern_colour = data.colour_map[pattern_colour_index]
    # background_colour = data.colour_map[background_colour_index]
    # print(fill_pattern)
    # print(pattern_colour)
    # print(background_colour)

    # cell_value=table.cell_value(22, 2)
    # cell_type=table.cell_type(22, 2)
    # print("cell_value:",cell_value)
    # print("cell_type:",data_type[cell_type])
    # print()
    # data_str_set = xlrd.xldate_as_tuple(cell_value,data.datemode)
    # print(data_str_set)
    # data_str_list = []
    # for i in data_str_set:
    #     data_str_list.append("%s"%i)
    # print(data_str_list)
    # print("/".join(data_str_list))
    
    

    data_json = {
        "filename":filename,
        "company":company,
        "merged_cells":merged_cells,
        "stations":stations,
        "data_base":company[1][0],
        "date_hours":date_hours,
        "data_list":data_list,
        "data_men":data_men,

        # "fill_pattern":fill_pattern,
        # "pattern_colour":pattern_colour,
        # "background_colour":background_colour,
    }
    with open("%s.json"%(int(time.time())), "w", encoding="utf-8") as file:
        file.write(json.dumps(data_json, indent=2, ensure_ascii=False)) #ensure_ascii=False可以消除json包含中文的乱码问题
reader()
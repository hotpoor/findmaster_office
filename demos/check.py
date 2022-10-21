import xlrd
filename = r"a.xlsx"
data_type = {
    0: 'empty（空的）',
    1: 'string（text）',
    2: 'number',
    3: 'date',
    4: 'boolean',
    5: 'error',
    6: 'blank(空白表格)'
}
if ".xlsx" in filename:
    data = xlrd.open_workbook(filename)
else:
    data = xlrd.open_workbook(filename,formatting_info=True)
table = data.sheets()[0]
print(table.row_values(0))
dict_now={}
for i in range(0,table.nrows):
    line = table.row_values(i)
    province = line[5]
    city = line[6]
    district = line[7]
    street = line[8]
    k = "%s-%s-%s"%(province,city,district)
    dict_now_value = dict_now.get(k,0)+1
    dict_now[k] = dict_now_value
print(dict_now)
print(len(set(dict_now.keys())))
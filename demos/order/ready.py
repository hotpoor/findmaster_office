import xlrd
import xlwt
filename = r"demo.xls"
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
dict_now = {}
out_list = []
base_num = 10000
base_num_len = 1
base_num_len_end = 5
id_name = "20220307_xlw_@@_pq_@@_01_"
product_list = []
for i in range(0,table.nrows):
    
    line = table.row_values(i)
    product = line[3]
    product_list.append(product)
    name = line[7]
    tel = line[8]
    address = line[12]
    num = line[4]
    dict_now_key = "%s%s%s"%(name,tel,address)
    dict_now_current = dict_now.get(dict_now_key,None)
    if not dict_now_current:
        base_num +=1
        id_name_now = "%s%s"%(id_name,str(base_num)[base_num_len:base_num_len_end])
        dict_now[dict_now_key]=id_name_now
    else:
        id_name_now = dict_now_current
    out_list_item = [id_name_now,num,name,tel,address,product]
    out_list.append(out_list_item)

workbook = xlwt.Workbook(encoding = 'utf-8')
worksheet = workbook.add_sheet('sheet1')
hang = 0
lie = 0
for out_hang in out_list:
    lie = 0
    for out_lie in out_hang:
        worksheet.write(hang,lie, label = out_lie)
        lie +=1
    hang +=1
    print(out_hang)
workbook.save('out.xls')
print("======")
for i in set(product_list):
    print(i)

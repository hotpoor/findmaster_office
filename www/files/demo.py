import copy

a=[{"1":["2","3",{"4":["5","6"]}]},{"1":["2","3",{"4":["5","6"]}]}]

b=[{"1":["2","3",{"4":["5",{"6":["7"]},"8",{"9":["10"]}]}]}]

out_a=[]
out_b=[]

def check_dict(list_now,result_list=[]):
    for i in list_now:
        if not isinstance(i,dict):
            result_list.append(i)
            continue
        key = list(i.keys())[0]
        result_list.append(key)
        result_list = check_dict(i.get(key,[]),result_list)
    return result_list
out_a = check_dict(a,out_a)
print("----")
print(a)
print("out_a:",out_a)
print("----")
print(b)
out_b = check_dict(b,out_b)
print("out_b:",out_b)

aim_paths = []
def find_dict(list_now,key,add_folder_key):
    print(list_now)
    for i in list_now:
        print(i)
        if not isinstance(i,dict):
            continue
        key_now = list(i.keys())[0]
        if key_now == key:
            i[key_now].append({add_folder_key:[]})
        else:
            i[key_now] = find_dict(i[key_now],key,add_folder_key)
    return list_now
print("---- find_dict ----")
find_dict(a,"1","add_folder_key")
print(a)
print("----")
find_dict(b,"6","add_folder_key")
print(b)


def find_dict_add_folder(list_now,key,add_folder_key):
    # print(list_now)
    for i in list_now:
        # print(i)
        if not isinstance(i,dict):
            continue
        key_now = list(i.keys())[0]
        if key_now == key:
            i[key_now].append({add_folder_key:[]})
        else:
            i[key_now] = find_dict_add_folder(i[key_now],key,add_folder_key)
    return list_now

dashboard_map = a
dashboard_map_old = copy.deepcopy(dashboard_map)
folder_id = "add_folder_key_new"
aim_folder_id = "add_folder_key"

folder_info = {folder_id:[]}
dashboard_map_update = False
if not aim_folder_id:
    print("not aim_folder_id")
    dashboard_map.append(folder_info)
    dashboard_map_update = True
else:
    print("aim_folder_id")
    dashboard_map_new = find_dict_add_folder(dashboard_map,aim_folder_id,folder_id)
    if dashboard_map_new != dashboard_map_old:
        dashboard_map_update = True
        dashboard_map = dashboard_map_new
if not dashboard_map_update:
    print("no update")
else:
    print(dashboard_map)

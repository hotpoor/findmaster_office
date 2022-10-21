a=[0,1,2,3,4,5,6,7,8,9,10,11]
def a_change(list_now,aim_num):
    result = []
    if len(a)%aim_num==0:
        result_num = int(len(a)/aim_num)
    else:
        result_num = int(len(a)/aim_num)+1
    for i in range(0,result_num):
        result.append(list_now[i*aim_num:(i+1)*aim_num])
    return result
result_now = a_change(a,4)
print(result_now)

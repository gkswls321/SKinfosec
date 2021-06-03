import json
import gzip
import os 
import sys
from ast import literal_eval

ct_path = 'C:/Users/dolif/Desktop/프로젝트/log/ctlog/2021/5/29/46d4769b089966df22b868/000001.gz'

# -- gzip으로 파일 읽기 -- 일단 절대 경로로 읽어오기!

# -- ct 로그 읽기 -> json형식인 것 같음 -> 근데 json으로 못불러옴..
ct_rb = gzip.open(ct_path,'rb')
ct_rb_data = ct_rb.readlines()
ct_str = str(ct_rb_data) # 일단 str로 변환

ct_dic1 = literal_eval(ct_str) # dic형식으로 데이터 변환
# print(type(ct_dictionary1)) # 근데 list 형식으로 변환됨
# print(ct_dictionary1,'----------',sep='\n')

# print(type(ct_dic1[1]),'----------',sep='\n') # 이건 bytes 형식

ct_dic2 = str(ct_dic1[1]) # list에서 첫번째 요소를 str
# print(type(ct_dic2),'----------',sep='\n')

# ct_dic3 = list(ct_dic2) # list의 첫번째 요소를 list로 변환 -> 실패
# print(type(ct_dic3),'----------',sep='\n') 

ct_dic3 = ct_dic2.split(',')
ct_dic4 = ct_dic3[6] # userName : user4
# print(ct_dic4)

ct_user_list = [] # user명만 모은 리스트

print(len(ct_dic1))
for i in range(len(ct_dic1)):
    if 'userName' in str(ct_dic1[i]).split(',')[6]:
        ct_user_list.append(str(ct_dic1[i]).split(',')[6])

for i in ct_user_list:
    print(i)

n_u = 0
n_u1 = 0
n_u2 = 0
n_u3 = 0
n_u4 = 0
n_u5 = 0
n_u6 = 0

for i in range(len(ct_user_list)):
    if 'user1' in ct_user_list[i]:
        n_u1 += 1
    elif 'user2' in ct_user_list[i]:
        n_u2 += 1
    elif 'user3' in ct_user_list[i]:
        n_u3 += 1
    elif 'user4' in ct_user_list[i]:
        n_u4 += 1
    elif 'user5' in ct_user_list[i]:
        n_u5 += 1
    elif 'user6' in ct_user_list[i]:
        n_u6 += 1
    elif 'root' in ct_user_list[i]:
        n_u += 1
    else:
        print("no")

print(n_u1)
print(n_u4)

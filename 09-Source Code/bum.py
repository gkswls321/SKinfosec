import json
import gzip
import os 
import sys
from ast import literal_eval
from matplotlib import pyplot as plt
from datetime import date
import datetime
import pandas as pd



ct_path = './0000001.gz'

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

# for i in ct_user_list:
    # print(i)

num =[]
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
num.append(n_u1)
num.append(n_u2)
num.append(n_u3)
num.append(n_u4)
num.append(n_u5)
num.append(n_u6)
num.append(n_u)


# print(n_u1)
# print(n_u4)


# print('1',ct_user_list)
# print('2',num)
y = num
x = ['user1', 'user2','user3', 'user4','user5', 'user6', 'root']
plt.bar(x,y,width=0.7,color = 'green')
plt.xlabel('USER NAME')
plt.ylabel("NUMBER")
plt.title('CT_LOG')
# plt.title("CT_LOG")
# plt.show()

raw_data={'user1':num[0],
'user2':num[1],
'user3':num[2],
'user4':num[3],
'user5':num[4],
'user6':num[5],
'root':num[6]
}

raw_data=pd.DataFrame(raw_data,index=["접근 횟수"])

# print(raw_data)
today = date.today()

now = datetime.datetime.now()
nowDate = str(now.strftime('%Y-%m-%d'))
nowTime = str(now.strftime('%H-%M-%S'))


plt.savefig('./{0}-{1}_CT_LOG.jpg'.format(nowDate,nowTime))
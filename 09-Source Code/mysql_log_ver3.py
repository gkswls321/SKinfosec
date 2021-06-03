import json
import gzip
import os 
import sys
import matplotlib.pyplot as plt
import numpy as np
from datetime import date
import datetime

mysql_path = 'C:/Users/dolif/Desktop/프로젝트/log/mysqllog/2021/5/29/46d4769b089966df22b862/000000.gz'

# -- gzip으로 파일 읽기 -- 일단 절대 경로로 읽어오기!

# -- mysql 로그 읽기 -> json형식으로 안되어 있음
mysql_rb = gzip.open(mysql_path,'rb')
mysql_rb_data = mysql_rb.readlines()

mysql_split = []
for line in mysql_rb_data: # 한줄 한줄 읽어오기 utf-8로 해야 깔끔이 읽어옴
    str_line = str(line, "utf-8")
    mysql_split.append(str_line)

# print("str_lines: ")
# for line in mysql_split:
#     print(line)

# 시간만 저장되어 있는 리스트, 내용만 저장되어 있는 리스트 만들기

list_ERROR = [] # error로그만 담을 리스트
list_Warning = [] # warning로그만 담을 리스트
list_Note = [] # error로그 중에 내용을 담을 리스트
list_t = [] # error로그 중에 시간만 담을 리스트
list_d_t = [] # date가 str형식이라 date형식으로 변환

# 
for i in range(len(mysql_split)):
    if '[Note]' in mysql_split[i]:
        list_ERROR.append(mysql_split[i])
        
for i in range(len(mysql_split)):
    if '[Warning]' in mysql_split[i]:
        list_Warning.append(mysql_split[i])

# print('[NOTE]LOG','\n\n') # list_ERROR 출력
# for i in list_ERROR:
#     print(i)

# -- 시간 리스트
for i in range(len(list_ERROR)):
    split_ex_t = list_ERROR[i][0:24] # 시간 부분만 자르기
    if split_ex_t.endswith('Z') : # 시간만 자른 내용 중에 z로 끝난 것만 추가함, Z로 끝난 데이터는 시간 데이터가 아니기 때문
        list_t.append(split_ex_t)

# -- 데이터 리스트
S_NOTE = list_ERROR[0].find('[Note]') # 데이터에서 [NOTE인] 위치 찾기

for i in range(len(list_ERROR)):
    split_ex_d = list_ERROR[i][S_NOTE:]
    if split_ex_d.startswith('[Note]') :
        list_Note.append(split_ex_d)

# # # -- 시간 데이터 리스트, 내용 리스트 확인
# print("time and note print",'\n\n\n')
# for i in list_t:
#     print(i)

# for i in list_Note:
#     print(i)


# print(type(list_t[0])) # str 형식

for i in range(len(list_t)):
    list_d_t.append(list_t[i][11:13]) # 시간만 출력

list_d_t2 = [] # datetime으로 변환된 시간 리스트

for i in range(len(list_d_t)):
    list_d_t2.append(int(list_d_t[i]))

# for i in list_d_t:
#     list_d_t2.append(datetime.datetime.strptime(i, '%H:%M:%S'))

# print(list_d_t2[0])
# print(type(list_d_t2[0]))

# 그래프 그리기
g_00 = 0
g_02 = 0
g_04 = 0 
g_06 = 0 
g_08 = 0 
g_10 = 0 
g_12 = 0 
g_14 = 0 
g_16 = 0 
g_18 = 0 
g_20 = 0 
g_22 = 0 # x축 항목


for i in range(len(list_d_t2)):
    if list_d_t2[i] >= 22:
        g_22 += 1
    elif list_d_t2[i] >= 20:
        g_20 += 1 
    elif list_d_t2[i] >= 18:
        g_18 += 1 
    elif list_d_t2[i] >= 16:
        g_16 += 1 
    elif list_d_t2[i] >= 14:
        g_14 += 1 
    elif list_d_t2[i] >= 12:
        g_12 += 1         
    elif list_d_t2[i] >= 10:
        g_10 += 1 
    elif list_d_t2[i] >= 8:
        g_08 += 1   
    elif list_d_t2[i] >= 6:
        g_06 += 1   
    elif list_d_t2[i] >= 4:
        g_04 += 1   
    elif list_d_t2[i] >= 2:
        g_02 += 1         
    else:
        g_00 += 1

x_values = ['00~02','02~04','04~06','06~08','08~10','10~12','12~14','14~16','16~18','18~20','20~22','22~24']
values = [g_00 , g_02, g_04, g_06, g_08, g_10, g_12, g_14, g_16, g_18, g_20, g_22]

plt.scatter(x_values,values, c = 'b', s = 40)
plt.plot(x_values,values,linestyle='solid',color='green')
plt.title('MYSQL_NOTE_COUNT', fontsize=20)
plt.xlabel('time',fontsize=15)
plt.ylabel('Note_count',fontsize=10)


# 날짜
today = date.today()

now = datetime.datetime.now()
nowDate = str(now.strftime('%Y-%m-%d'))
nowTime = str(now.strftime('%H-%M-%S'))


plt.savefig('C:/Users/dolif/Desktop/프로젝트/{0}-{1}_mysql_graph.png'.format(nowDate,nowTime),dpi=300)

plt.show()
# ----------------------------
# for i in list_Note:
#     print(i)

# for i in list_Warning: # Warning 부분은 따로 시간대별로 짜르지 않고 전체 내용 포함해서 출력함
#     print(i)

# print(len(list_t))
# print(len(list_Note))
# print(len(list_Warning))

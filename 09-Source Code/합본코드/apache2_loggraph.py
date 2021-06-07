import json
import gzip
import os 
import sys
import matplotlib.pyplot as plt
import numpy as np
from datetime import date
import datetime

# -- DATE ------------
# 현재 날짜에 대한 정보를 담은 변수
today = date.today()

today_y = today.year
today_m = today.month
today_d = today.day


# str(today_y) + '/' + str(today_m) + '/' + str(today_d)

f_inputpath1 = "./tmp_web1-apache2-error-log_combine.txt"
f_inputpath2 = "./tmp_web2-apache2-error-log_combine.txt"
f_outpath_combined = "./tmp_weball-apache2-error-log_allcombine.txt"
with open(f_inputpath1, 'r') as f_input1:
    f_read1 = f_input1.readlines()
    with open(f_inputpath2, 'r') as f_input2:
        f_read2 = f_input2.readlines()
        with open(f_outpath_combined, "w+") as f_out_combined:
            for line in f_read1:
                f_out_combined.write(line)
            for line in f_read2:
                f_out_combined.write(line)

f_out_combined.close()
f_input2.close()
f_input1.close()


apache2_path = f_outpath_combined


apache2_r = open(apache2_path,'r')


apache2_data_list = []
for line in apache2_r: 
    apache2_data_list.append(line)

# -------------- log print ------------
# for line in apache2_data_list:
#     print(line)

#  time, client ip, error내용 따로 수집

APACHE2_ERROR_t = [] 
APACHE2_ERROR_ip = [] 
# APACHE2_ERROR_IN = [] 

print('time_LOG START!','\n\n') 

for i in range(len(apache2_data_list)):
    Z_NUM = apache2_data_list[0].find('Z') + 1
    apache2_split_t = apache2_data_list[i][0:Z_NUM] # 시간 부분만 자르기
    if apache2_split_t.endswith('Z') : # 시간만 자른 내용 중에 z로 끝난 것만 추가함, Z로 끝난 데이터는 시간 데이터가 아니기 때문
        APACHE2_ERROR_t.append(apache2_split_t)

# for i in APACHE2_ERROR_t:
#     print(i)
print('TIME_LOG COMPLETE!','\n\n') 

print('IP_LOG START!','\n\n') 
for i in range(len(apache2_data_list)):
    client_NUM = apache2_data_list[i].find('client')-1
    apache2_split_ip = apache2_data_list[i][client_NUM:]
    if apache2_split_ip.startswith('['):
        APACHE2_ERROR_ip.append(apache2_split_ip)
    
# for i in APACHE2_ERROR_ip:
#     print(i)
print('IP_LOG COMPLETE!','\n\n') 


# ----- LOG TIME TO DATETIME --- START! --

# for i in APACHE2_ERROR_t:
#     print(i)
# print('TIME_LOG COMPLETE!','\n\n') 

APACHE_T_1 = [] # 시간 부분만 자르기
APACHE_T_2 = [] # INT로 변환

for i in range(len(APACHE2_ERROR_t)):
    APACHE_T_1.append(APACHE2_ERROR_t[i][11:13]) # 시간만 출력

for i in range(len(APACHE2_ERROR_t)):
    APACHE_T_2.append(int(APACHE_T_1[i])) # 시간만 출력

# print(type(APACHE_T_2[0]))

# 그래프 그리기
ap_00 = 0
ap_02 = 0
ap_04 = 0 
ap_06 = 0 
ap_08 = 0 
ap_10 = 0 
ap_12 = 0 
ap_14 = 0 
ap_16 = 0 
ap_18 = 0 
ap_20 = 0 
ap_22 = 0 

for i in range(len(APACHE_T_2)):
    if APACHE_T_2[i] >= 22:
        ap_22 += 1
    elif APACHE_T_2[i] >= 20:
        ap_20 += 1 
    elif APACHE_T_2[i] >= 18:
        ap_18 += 1 
    elif APACHE_T_2[i] >= 16:
        ap_16 += 1 
    elif APACHE_T_2[i] >= 14:
        ap_14 += 1 
    elif APACHE_T_2[i] >= 12:
        ap_12 += 1         
    elif APACHE_T_2[i] >= 10:
        ap_10 += 1 
    elif APACHE_T_2[i] >= 8:
        ap_08 += 1   
    elif APACHE_T_2[i] >= 6:
        ap_06 += 1   
    elif APACHE_T_2[i] >= 4:
        ap_04 += 1   
    elif APACHE_T_2[i] >= 2:
        ap_02 += 1         
    else:
        ap_00 += 1

ap_x_values = ['00','02','04','06','08','10','12','14','16','18','20','22']
ap_values = [ap_00 , ap_02, ap_04, ap_06, ap_08, ap_10, ap_12, ap_14, ap_16, ap_18, ap_20, ap_22]

plt.scatter(ap_x_values,ap_values, c = 'b', s = 40)
plt.plot(ap_x_values,ap_values,linestyle='solid',color='green')
plt.title('EC2_WEB_NOTE_COUNT', fontsize=20)
plt.xlabel('time',fontsize=15)
plt.ylabel('count',fontsize=10)

# DATE
today = date.today()

now = datetime.datetime.now()
nowDate = str(now.strftime('%Y-%m-%d'))
nowTime = str(now.strftime('%H'))

plt.savefig('./{0}-{1}_apache_web_graph.png'.format(nowDate,nowTime),dpi=300)
# 사진 정하는 경로 ec2내에서 정해줘야함!

# plt.show()

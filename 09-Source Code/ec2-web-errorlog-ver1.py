import json
import gzip
import os 
import sys
import matplotlib.pyplot as plt
import numpy as np
from datetime import date
import datetime

ec2_error_path = 'C:/Users/dolif/Desktop/프로젝트/log/ec2log/2021/5/29/46d4769b089966df22b868/000000.gz'

# -- gzip으로 파일 읽기 -- 일단 절대 경로로 읽어오기!

# -- mysql 로그 읽기 -> json형식으로 안되어 있음
ec2_error_rb = gzip.open(ec2_error_path,'rb')
ec2_error_rb_data = ec2_error_rb.readlines()

ec2_error_split = []
for line in ec2_error_rb_data: # 한줄 한줄 읽어오기 utf-8로 해야 깔끔이 읽어옴
    str_line = str(line, "utf-8")
    ec2_error_split.append(str_line)

# for i in ec2_error_split: # 내용 전체 출력
#     print(i)

ec2_error_time_list = []

for i in range(len(ec2_error_split)):
    Z_NOTE = ec2_error_split[i].find('Z') + 1
    split_ex_t2 = ec2_error_split[i][0:Z_NOTE] # 시간 부분만 자르기
    if split_ex_t2.endswith('Z') : # 시간만 자른 내용 중에 z로 끝난 것만 추가함, Z로 끝난 데이터는 시간 데이터가 아니기 때문
        ec2_error_time_list.append(split_ex_t2)


# -- ec2_error_시간 리스트
# for i in ec2_error_time_list:
#     print(i)

ec2_error_ip_list = []

for i in range(len(ec2_error_split)):
    if 'client' in ec2_error_split[i]:
        client_NOTE = ec2_error_split[i].find('client') -1 # client로 시작하는 부분 위치 찾기
        ec_web_split_t2 = ec2_error_split[i][client_NOTE:]
        ec2_error_ip_list.append(ec_web_split_t2)

# for i in ec2_error_ip_list:
#     print(i)

for i in ec2_error_split:
    print(i)

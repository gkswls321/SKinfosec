import os
import glob
import gzip
from datetime import date

today = date.today()

today_y = today.year
today_m = today.month
today_d = today.day

print(today_d,today_m,today_y)

# ------------------------------
# 최종 가져와야 하는 경로 
# : mysql_path = path + '/' + "mysqllog" + '/' + str(today_y) + '/' + str(today_m) + '/' + str(today_d) + '/' +  파일 경로(이 파일 경로는 아래에서 함수로 찾음) + '/' + '000000.gz'
# ------------------------------

path = 'C:/Users/dolif/Desktop/프로젝트/log'

# -------------
# 리스트 미리 생성 
mysqllog_path_list = []
mysqllog_data_list = [] # mysql 데이터를 담을 리스트 생성

# lambdalog_path_list = []
# lambdalog_data_list = []

def path_m(a): # 경로 생성하는 함수
    path_1 = path + '/' + a + '/' + str(today_y) + '/' + str(today_m) + '/' + str(today_d) + '/'

    path_low_list = os.listdir(path_1) # 하위 폴더 찾기

    for i in range(len(path_low_list)):
        path_2 = path_1 + path_low_list[i] + '/' + '000000.gz'
        globals()['{}_path_list'.format(a)].append(path_2)

# 경로 생성
mysqllog_path = path_m('mysqllog')

# 데이터를 담을 리스트 생성
mysqllog_data_list = [] # mysql 데이터를 담은 리스트 생성

# 경로를 읽고 거기에 해당하는 파일 읽어주는 함수
def read_m(a):
    for i in range(len(globals()['{}_path_list'.format(a)])):
        globals()['{}_rb'.format(a)] = gzip.open(globals()['{}_path_list'.format(a)][i],'rb')
        globals()['{}_rb_data'.format(a)] = globals()['{}_rb'.format(a)].readlines()
        globals()['{}_data_list'.format(a)].append(globals()['{}_rb_data'.format(a)])
    
    for i in range(len(globals()['{}_data_list'.format(a)])):
        print(globals()['{}_data_list'.format(a)][i])

# mysql 로그 읽기
read_m('mysqllog')

# # mysql 로그 읽기
# mysql_data_list = [] # mysql 데이터를 담은 리스트 생성
# for i in range(len(mysqllog_path_list)):
#     mysql_rb = gzip.open(mysqllog_path_list[i],'rb')
#     mysql_rb_data = mysql_rb.readlines()
#     mysql_data_list.append(mysql_rb_data)

# for i in range(len(mysql_data_list)):
#     print(mysql_data_list[i]) # 모든 mysql의 데이터 출력

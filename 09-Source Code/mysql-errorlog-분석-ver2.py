import json
import gzip
import os 
import sys


mysql_path = 'C:/Users/dolif/Desktop/프로젝트/log/mysqllog/2021/5/29/46d4769b089966df22b862/000000.gz'

# -- gzip으로 파일 읽기 -- 일단 절대 경로로 읽어오기!

# with gzip.open(path,'rb') as rb_lambda: # 람다 로그 읽기
#     print(rb_lambda.readlines())

# with gzip.open(ct_path,'rb') as ct_lambda:   # 이거 너무 길어.. 파이썬으로 보기 너무 힘듬
#     print(ct_lambda.readlines())

# -- mysql 로그 읽기 -> json형식으로 안되어 있음
mysql_rb = gzip.open(mysql_path,'rb')
mysql_rb_data = mysql_rb.readlines()

# 로그 내용 ,로 자른 후 리스트로 만들기
mysql_split = str(mysql_rb_data).split(',')

# 시간만 저장되어 있는 리스트, 내용만 저장되어 있는 리스트 만들기

list_ERROR = [] # error로그만 담을 리스트
list_Warning = [] # warning로그만 담을 리스트
list_Note = [] # error로그 중에 내용을 담을 리스트
list_t = [] # error로그 중에 시간만 담을 리스트

# 
for i in range(len(mysql_split)):
    if '[Note]' in mysql_split[i]:
        list_ERROR.append(mysql_split[i])

for i in range(len(mysql_split)):
    if '[Warning]' in mysql_split[i]:
        list_Warning.append(mysql_split[i])

for i in list_ERROR:
    print(i)

# -- 시간 리스트
for i in range(len(list_ERROR)):
    split_ex_t = list_ERROR[i][1:27] # 시간 부분만 자르기
    if split_ex_t.endswith('Z') : # 시간만 자른 내용 중에 z로 끝난 것만 추가함, Z로 끝난 데이터는 시간 데이터가 아니기 때문
        list_t.append(split_ex_t)


# for i in range(len(mysql_split)):
#     split_ex_t = mysql_split[i][1:27] # 시간 부분만 자르기
#     if split_ex_t.endswith('Z') : # 시간만 자른 내용 중에 z로 끝난 것만 추가함, Z로 끝난 데이터는 시간 데이터가 아니기 때문
#         list_t.append(split_ex_t)


# -- 데이터 리스트
S_NOTE = list_ERROR[0].find('[Note]') # 데이터에서 [NOTE인] 위치 찾기

for i in range(len(list_ERROR)):
    split_ex_d = list_ERROR[i][S_NOTE:]
    if split_ex_d.startswith('[Note]') :
        list_Note.append(split_ex_d)

# # -- 시간 데이터 리스트, 내용 리스트 확인
for i in list_t:
    print(i)

for i in list_Note:
    print(i)

for i in list_Warning: # Warning 부분은 따로 시간대별로 짜르지 않고 전체 내용 포함해서 출력함
    print(i)

print(len(list_t))
print(len(list_Note))

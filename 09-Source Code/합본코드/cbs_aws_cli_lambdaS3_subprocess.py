  
import subprocess
import os
import glob
import gzip
from datetime import date


## 리눅스 cmd에서 s3 폴더 다운로드 받는 코드(현재경로)
# subprocess.call("aws s3 cp s3://beom-log-save2/mysql-error.log/ . --recursive", shell=True)

# 현재 날짜에 대한 정보를 담은 변수
today = date.today()

today_y = today.year
today_m = today.month
today_d = today.day

# 변수로 파일 날짜별로 다운받는 code 생성 중


# 람다 실행 aws cli 명령어
# aws lambda invoke --function-name my-function out_log.txt --log-type Tail --query 'LogResult' --output text
# 실행하는 람다 함수: my-function out

awscli_lambdacall = "aws lambda invoke --function-name my-function out_log.txt --log-type Tail --query 'LogResult' --output text"

subprocess.call(awscli_lambdacall, shell=True)


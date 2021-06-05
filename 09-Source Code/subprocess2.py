import subprocess
import os
import glob
import gzip
from datetime import date

## 리눅스 cmd에서 s3 폴더 다운로드 받는 코드(현재경로)
# subprocess.call("aws s3 cp s3://beom-log-save2/mysql-error.log/ . --recursive", shell=True)

today = date.today()

today_y = today.year
today_m = today.month
today_d = today.day

# 변수로 파일 날짜별로 다운받는 code 생성 중

# 최종 가져와야 하는 경로 : aws_cli + str(today_y) + '/' + str(today_m) + '/' + str(today_d) + '/'
path1 = 'aws s3 cp s3://beom-log-save2/web1-mysql-error-log/'
# path_1 = '"' + path1 + str(today_y) + '/' + str(today_m) + '/' + str(today_d) + '/' + ' . --recursive"'

path_1 = '"' + path1 + str(today_y) + '/' + str(today_m) + '/' + '3' + '/' + ' . --recursive"'

print(path_1)
# aws_cli = path
# subprocess.call(aws_cli)

# aws_cli = "aws s3 cp s3://beom-log-save2/web1-mysql-error-log/ . --recursive"
subprocess.call(path_1)


##s3에 파일 업로드 하는 cmd실행하는 코드
## subprocess.call("aws s3 cp [localfilepath] s3://[bucketname]/[filename] --acl public-read")
# subprocess.call("aws s3 cp C:\project_team3\sy_Test s3://beom-log-save2/mysql-error.log/ --recursive")
## subprocess.call("upload: [localfilepath] to s3://[bucketname]/[filename]")

  
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


# 최종 가져와야 하는 경로 : aws_cli + str(today_y) + '/' + str(today_m) + '/' + str(today_d) + '/'
web1_mysql_error_log = 'aws s3 cp s3://beom-log-save2/web1-mysql-error-log/'
web1_apache2_error_log = 'aws s3 cp s3://beom-log-save2/web1-apache2-error-log/'
web2_mysql_error_log = 'aws s3 cp s3://beom-log-save2/web2-mysql-error-log/'
web2_apache2_error_log = 'aws s3 cp s3://beom-log-save2/web2-apache2-error-log/'
# fullpath = '"' + path1 + str(today_y) + '/' + str(today_m) + '/' + str(today_d) + '/' + ' . --recursive"'



today_d = 3     # 테스트용 날짜 설정 teston



inputpath_mysql_error1 = web1_mysql_error_log + str(today_y) +'/'+ str(today_m) +'/'+ str(today_d) +'/'
inputpath_apache2_error1 = web1_apache2_error_log + str(today_y) +'/'+ str(today_m) +'/'+ str(today_d) +'/'
inputpath_mysql_error2 = web2_mysql_error_log + str(today_y) +'/'+ str(today_m) +'/'+ str(today_d) +'/'
inputpath_apache2_error2 = web2_apache2_error_log + str(today_y) +'/'+ str(today_m) +'/'+ str(today_d) +'/'

outputpath_mysql_error1 = './'+'web1-mysql-error-log/'+ str(today_y) +'/'+ str(today_m) +'/'+ str(today_d) +'/'
outputpath_apache2_error1 = './'+'web1-apache2-error-log/'+ str(today_y) +'/'+ str(today_m) +'/'+ str(today_d) +'/'
outputpath_mysql_error2 = './'+'web2-mysql-error-log/'+ str(today_y) +'/'+ str(today_m) +'/'+ str(today_d) +'/'
outputpath_apache2_error2 = './'+'web2-apache2-error-log/'+ str(today_y) +'/'+ str(today_m) +'/'+ str(today_d) +'/'

getS3log_fullpath_mysql_error1 = inputpath_mysql_error1 +' '+ outputpath_mysql_error1 +' --recursive'
getS3log_fullpath_apache2_error1 = inputpath_apache2_error1 +' '+ outputpath_apache2_error1 +' --recursive'
getS3log_fullpath_mysql_error2 = inputpath_mysql_error2 +' '+ outputpath_mysql_error2 +' --recursive'
getS3log_fullpath_apache2_error2 = inputpath_apache2_error2 +' '+ outputpath_apache2_error2 +' --recursive'
# fullpath_apache2_error1 = web1_apache2_error_log + str(today_y) + '/' + str(today_m) + '/' + str(today_d) + '/' + ' ./' + 'web1-apache2-error-log' + ' --recursive'
# fullpath_mysql_error2 = web2_mysql_error_log + str(today_y) + '/' + str(today_m) + '/' + str(today_d) + '/' + ' ./' + 'web2-mysql-error-log' + ' --recursive'
# fullpath_apache2_error2 = web2_apache2_error_log + str(today_y) + '/' + str(today_m) + '/' + str(today_d) + '/' + ' ./' + 'web2-apache2-error-log' + ' --recursive'

print(getS3log_fullpath_mysql_error1)
print(getS3log_fullpath_apache2_error1)
print(getS3log_fullpath_mysql_error2)
print(getS3log_fullpath_apache2_error2)

# aws_cli = path
# subprocess.call(aws_cli)

# aws_cli = "aws s3 cp s3://beom-log-save2/web1-mysql-error-log/ . --recursive"
subprocess.call(getS3log_fullpath_mysql_error1, shell=True)
subprocess.call(getS3log_fullpath_apache2_error1, shell=True)
subprocess.call(getS3log_fullpath_mysql_error2, shell=True)
subprocess.call(getS3log_fullpath_apache2_error2, shell=True)


##s3에 파일 업로드 하는 cmd실행하는 코드
## subprocess.call("aws s3 cp [localfilepath] s3://[bucketname]/[filename] --acl public-read")
# subprocess.call("aws s3 cp C:\project_team3\sy_Test s3://beom-log-save2/mysql-error.log/ --recursive")
## subprocess.call("upload: [localfilepath] to s3://[bucketname]/[filename]")





# EC2 로그 가져오기 명령어1
# aws cloudwatch get-metric-statistics --namespace AWS/EC2 --metric-name CPUUtilization --period 3600 --statistics Maximum --dimensions Name=InstanceId,Value=i-012dcbd703857ccca --start-time 2021-06-04T00:00:00Z --end-time 2021-06-04T23:59:59Z > ./cwEC2logtest_CPUmax_web1.txt  
# Real-Web1(private1) : i-012dcbd703857ccca
# Real-Web2(private3) : i-06d36909db8f6292f




today_d = 4     # 테스트용 날짜 설정 teston



startdate = str(today_y) + '-' + str(today_m) + '-' + str(today_d)
enddate = str(today_y) + '-' + str(today_m) + '-' + str(today_d)


EC2intance = 'i-012dcbd703857ccca'
period = '3600'
EC2log_Web1_CPU = 'aws cloudwatch get-metric-statistics --namespace AWS/EC2 --metric-name CPUUtilization --period '+ period +' --statistics Maximum --dimensions Name=InstanceId,Value='+ EC2intance +' --start-time '+ startdate +'T00:00:00Z --end-time '+ enddate +'T23:59:59Z > ./cwEC2logtest_CPUmax_web1.txt'  
EC2log_Web1_NetworkOut = 'aws cloudwatch get-metric-statistics --namespace AWS/EC2 --metric-name NetworkOut --period '+ period +' --statistics Maximum --dimensions Name=InstanceId,Value='+ EC2intance +' --start-time '+ startdate +'T00:00:00Z --end-time '+ enddate +'T23:59:59Z > ./cwEC2logtest_networkout_web1.txt '


EC2intance = 'i-06d36909db8f6292f'
EC2log_Web2_CPU = 'aws cloudwatch get-metric-statistics --namespace AWS/EC2 --metric-name CPUUtilization --period '+ period +' --statistics Maximum --dimensions Name=InstanceId,Value='+ EC2intance +' --start-time '+ startdate +'T00:00:00Z --end-time '+ enddate + 'T23:59:59Z > ./cwEC2logtest_CPUmax_web2.txt'  
EC2log_Web2_NetworkOut = 'aws cloudwatch get-metric-statistics --namespace AWS/EC2 --metric-name NetworkOut --period '+ period +' --statistics Maximum --dimensions Name=InstanceId,Value='+ EC2intance +' --start-time '+ startdate +'T00:00:00Z --end-time '+ enddate +'T23:59:59Z > ./cwEC2logtest_networkout_web2.txt '


print(EC2log_Web1_CPU)
print(EC2log_Web1_NetworkOut)
print(EC2log_Web2_CPU)
print(EC2log_Web2_NetworkOut)


subprocess.call(EC2log_Web1_CPU, shell=True)
subprocess.call(EC2log_Web1_NetworkOut, shell=True)
subprocess.call(EC2log_Web2_CPU, shell=True)
subprocess.call(EC2log_Web2_NetworkOut, shell=True)



#파이썬 실행

# 'web1_mysql_error_log' = 'web1-mysql-error-log/'
# 'web1_apache2_error_log' = 'web1-apache2-error-log/'
# 'web2_mysql_error_log' = 'web2-mysql-error-log/'
# 'web2_apache2_error_log' = 'web2-apache2-error-log/'


# python ./cbs-log-analysis.py 2021 6 3 web1-mysql-error-log
# python ./cbs-log-analysis.py 2021 6 3 web1-apache2-error-log
# python ./cbs-log-analysis.py 2021 6 3 web2-mysql-error-log
# python ./cbs-log-analysis.py 2021 6 3 web2-apache2-error-log


today_d = 3     # 테스트용 날짜 설정 teston


todaytdate = str(today_y) + ' ' + str(today_m) + ' ' + str(today_d)


pythonpath_web1_mysql_error_log = "python ./cbs-log-analysis.py "+ todaytdate +" "+"web1-mysql-error-log"
pythonpath_web1_apache2_error_log = "python ./cbs-log-analysis.py "+ todaytdate +" "+"web1-apache2-error-log"
pythonpath_web2_mysql_error_log = "python ./cbs-log-analysis.py "+ todaytdate +" "+"web2-mysql-error-log"
pythonpath_web2_apache2_error_log = "python ./cbs-log-analysis.py "+ todaytdate +" "+"web2-apache2-error-log"
print(pythonpath_web1_mysql_error_log)
print(pythonpath_web1_apache2_error_log)
print(pythonpath_web2_mysql_error_log)
print(pythonpath_web2_apache2_error_log)

subprocess.call(pythonpath_web1_mysql_error_log, shell=True)
subprocess.call(pythonpath_web1_apache2_error_log, shell=True)
subprocess.call(pythonpath_web2_mysql_error_log, shell=True)
subprocess.call(pythonpath_web2_apache2_error_log, shell=True)


excelreport_path = "python ./excel_make.py"
print(excelreport_path)

subprocess.call(excelreport_path, shell=True)
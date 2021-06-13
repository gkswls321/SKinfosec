  
import subprocess



# 람다 실행 aws cli 명령어
# aws lambda invoke --function-name my-function out_log.txt --log-type Tail --query 'LogResult' --output text
# 실행하는 람다 함수: my-function out


# 실행되는 aws lambda 함수
# beom-cw-s3-web1-apache2
# beom-cw-s3-web1-mysql
# beom-cw-s3-web2-apache2
# beom-cw-s3-web2-mysql


# 웹로그를 저장하는 람다함수 실행하는 명령어
awscli_lambdacall_web1_apache2 = "aws lambda invoke --function-name beom-cw-s3-web1-apache2 out_log.txt --log-type Tail --query 'LogResult' --output text"
awscli_lambdacall_web1_mysql = "aws lambda invoke --function-name beom-cw-s3-web1-mysql out_log.txt --log-type Tail --query 'LogResult' --output text"
awscli_lambdacall_web2_apache2 = "aws lambda invoke --function-name beom-cw-s3-web2-apache2 out_log.txt --log-type Tail --query 'LogResult' --output text"
awscli_lambdacall_web2_mysql = "aws lambda invoke --function-name beom-cw-s3-web2-mysql out_log.txt --log-type Tail --query 'LogResult' --output text"

# 명령어 실행
subprocess.call(awscli_lambdacall_web1_apache2, shell=True)
subprocess.call(awscli_lambdacall_web1_mysql, shell=True)
subprocess.call(awscli_lambdacall_web2_apache2, shell=True)
subprocess.call(awscli_lambdacall_web2_mysql, shell=True)


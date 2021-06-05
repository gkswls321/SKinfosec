import subprocess

## 리눅스 cmd에서 s3 폴더 다운로드 받는 코드(현재경로)
# subprocess.call("aws s3 cp s3://beom-log-save2/mysql-error.log/ . --recursive", shell=True)


# 변수로 파일 날짜별로 다운받는 code 생성 중
aws_cli = "aws s3 cp s3://beom-log-save2/mysql-error.log/ . --recursive"
subprocess.call(aws_cli)



##s3에 파일 업로드 하는 cmd실행하는 코드
## subprocess.call("aws s3 cp [localfilepath] s3://[bucketname]/[filename] --acl public-read")
# subprocess.call("aws s3 cp C:\project_team3\sy_Test s3://beom-log-save2/mysql-error.log/ --recursive")
## subprocess.call("upload: [localfilepath] to s3://[bucketname]/[filename]")
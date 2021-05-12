import json
import boto3
import datetime


def lambda_handler(event, context):
    bucket = 'cbs-test-bucket01'        #당신의 버킷 이름
    file_name = str(datetime.datetime.now())[:-7]        #이 파이썬 함수 발생 시각을 파일이름으로 정한다.
    file = dict()
    file['customerID'] = 'jinyes'
    file['age'] = '25'
    file['product'] = 'aws_solution'
    
    file_directory = "test-inputfolder/"        #파일이 저장될 경로이다. 공란이면 최상이 경로에 저장된다.
    file_fullpath = file_directory + file_name        #파일 경로와 파일 이름을 합쳐서 최종위치를 만든다.
    result = upload_file_s3(bucket, file_fullpath + '.json', file)

    if result:
        return {
            'statusCode': 200,
            'body': json.dumps("upload success")
        }
    else:
        return {
            'statusCode': 400,
            'body': json.dumps("upload fail")
        }


def upload_file_s3(bucket, file_name, file):
    encode_file = bytes(json.dumps(file).encode('UTF-8'))
    s3 = boto3.client('s3')
    print(s3)
    try:
        s3.put_object(Bucket=bucket, Key=file_name, Body=encode_file)
        return True
    except:
        return False
      
      
      
      

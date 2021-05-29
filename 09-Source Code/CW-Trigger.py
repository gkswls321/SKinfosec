import base64
import json
import boto3
import datetime

'''
람다 트리거로 CloudWatch Logs를 추가해야한다.
'''

# bucket에 로그 파일을 업로드하기 위한 함수
def upload_file_s3(bucket, file_name, file):
    # encode_file = bytes(json.dumps(file).encode('UTF-8'))
    s3 = boto3.client('s3')
    print(s3)
    try:
        s3.put_object(Bucket=bucket, Key=file_name, Body=file)
        return True
    except:
        return False
      
def lambda_handler(event, context):
#----base64 인코딩, 디코딩 테스트-----------------------------------------
    teststring = "base64_test"
    print("teststring: \n", teststring)
    
    
    teststring_bytes = teststring.encode('ascii')
    teststring_base64 = base64.b64encode(teststring_bytes)
    teststring_base64_str = teststring_base64.decode('ascii')
    print("teststring_bytes: \n", teststring_bytes)
    print("teststring_base64: \n", teststring_base64)
    print("teststring_base64_str: \n", teststring_base64_str)
    
    print("\n\n")
    
    teststring_bytes = base64.b64decode(teststring_base64_str)
    teststring_decode = teststring_bytes.decode('ascii')
    print("teststring_bytes: \n", teststring_bytes)
    print("teststring_decode: \n", teststring_decode)
    
# 끝--------------------------------------------------------------------
#----event data의 base64 디코딩 시작--------------------------------------
    
    
    print("Lambda event: \n", event)
    print("Lambda context: \n", context)
    print("event['awslogs']['data']: \n", event['awslogs']['data'], "\n")      
    # 넘겨받은 로그데이터 확인 <- base64로 인코딩 되어있다.
    
    
    data_decode_bytes = base64.b64decode(event['awslogs']['data'])      
    # 넘겨받은 로그데이터를 디코딩 및 확인 
    # <- 파일 자체의 값인 hex값들이 byte 형식으로 변환되어 있는 것을 알 수 있다.
    print("data_decode_bytes: \n", data_decode_bytes, "\n")
# 끝--------------------------------------------------------------------

#----디코딩된 data(data_decode_bytes)를 S3에 쓰기-----------------------------------------
    print("type(data_decode_bytes): ", type(data_decode_bytes))
    
#    data_decode_string = data_decode_bytes.decode()
#    print("type(data_decode_string): ", type(data_decode_string))
#    print("data_decode_string: \n", data_decode_string, "\n\n")

    bucket = 'beom-log-save'        # 버킷 이름
    file_name = str(datetime.datetime.now())[:-7] + "__Lambda1_log"       
    # 파이썬 함수 발생 시각을 파일이름으로 정한다.
    file_content = data_decode_bytes # 데이터 변수 정의 
    file_directory = "test-log-save/"     
    #파일이 저장될 경로이다. 공란이면 최상이 경로에 저장된다.
    file_fullpath = file_directory + file_name        
    #파일 경로와 파일 이름을 합쳐서 최종위치를 만든다.
    result = upload_file_s3(bucket, file_fullpath + '.gz', file_content)       
    #로그를 CloudWatch로 S3에 저장하였을때 .gz로 저장되었기에 .gz로 하였다.
    print(result)       #결과 확인용

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

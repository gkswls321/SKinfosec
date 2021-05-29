import boto3
import json
import datetime

def lambda_handler(event, context):
    s3 = boto3.client("s3")

    if event:
        # 이벤트 내용보기
        print("Event : ", event)
        
        # 무슨 이벤트인지 확인하기
        file_obj = event["Records"][0]
        print("event['Records'][0]: ", file_obj)
        event_name = str(file_obj['eventName'])
        print("Event_name: ", event_name)
        
        # 파일의 이름 가져오기
        file_name = str(file_obj['s3']['object']['key'])
        print('Filename: ', file_name)
        
        # 파일의 size 가져오기
        size_name = event['Records'][0]['s3']['object']['size']
        print('size: ', size_name)
        
        # bucket 이름 찾기 
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        print('bucket_name: ', bucket_name)
        
        # 읽어올 파일(s3.get_object)(bucket이름과 key(파일이름) 필요)
        fileObj = s3.get_object(Bucket=bucket_name, Key=file_name)
        print("fileObj: ", fileObj)
        
        # 읽어올 파일 내용 출
        file_content = fileObj["Body"].read().decode('utf-8')
        print('file_content: ', file_content)
        
        # 가져온 파일을 json 형식으로 변환
        json_data = json.loads(file_content)
        print('json : ',json_data)
        
        
        
        # 읽은 내용을 다른 파일로 S3에 저장
        u_bucket = 'beom-us-east-2' # 파일 저장할 버킷 이름
        datetime_now = str(datetime.datetime.now())[:-7]
        u_file_name = datetime_now
        file = dict()
        file['customerID'] = json_data['customerID']
        file['age'] = json_data['age']
        file['product'] = json_data['product']
        file['timestamp'] = datetime_now
        result = upload_file_s3(u_bucket, u_file_name + '.json', file)
        
        
        
        
    return {
            'age': json_data['age'] , 
            'product': json_data['product'] , 
            'customerID': json_data['customerID'],
            'bucket': bucket_name,
            'file_name': file_name,
            'u_bucket': u_bucket,
            'event_name': event_name,
            'timestamp': datetime_now
        }




# 파일 업로드 함수(같은 지역 s3에만 보낼 수 있는 듯?)
def upload_file_s3(bucket, file_name, file):
    encode_file = bytes(json.dumps(file).encode('UTF-8'))
    s3 = boto3.client('s3')
    try:
        s3.put_object(Bucket=bucket, Key=file_name, Body=encode_file)
        return True
    except:
        return False

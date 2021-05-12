import boto3
import json

def lambda_handler(event, context):
    s3 = boto3.client("s3")

    if event:
        print("Event : ", event)
        # 파일의 이름 가져오기
        file_obj = event["Records"][0]
        filename = str(file_obj['s3']['object']['key'])
        print('Filename: ', filename)
        
        # bucket 이름 찾기 
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        print('bucket_name: ', bucket_name)

        fileObj = s3.get_object(Bucket=bucket_name, Key=filename)
        print("fileObj: ", fileObj)
        # 가져올 파일
        file_content = fileObj["Body"].read().decode('utf-8')
        print('file_content: ', file_content)
        
        # 가져온 파일을 json 형식으로 변환
        json_data = json.loads(file_content)
        print('json : ',json_data)


    return {
            'age': json_data['age'] , 
            'product': json_data['product'] , 
            'customerID': json_data['customerID']
        }

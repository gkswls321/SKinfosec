import json
import gzip
import os 
import sys


print(os.getcwd())
path = './2021-05-29 05_20_05__logfromS3python.gz'


with gzip.open(path, 'rb') as frb:
    print("gzip.open(path) \n\n\n")
    # print(frb.readlines())
    print("\n\n\n")

    with open('./'+'log_test.txt','wb') as f_out:
        f_out.writelines(frb)
        
   
    frb.close()
    f_out.close()


# 궁금증 : json 데이터는 type함수 치면 json으로 뜨나? -> 안 뜨는 걸로 생각됨..

with open('./log_test.txt','r') as j_file : 
    json_data = json.load(j_file)
    print(type(json_data)) ## dic 타입
    print('-----------',json_data,'-----------', sep='\n')
    # print('---------',json_data['logEvents'][1]['message'],'-----------')

    json_data_event = json_data['logEvents'][1]['message']
    print('------------',json_data_event,'-----------', sep='\n')
    print(type(json_data_event)) ##  str 타입

    print(json_data.keys())
    print(json_data.get('logEvents'))
    
    json_data_event2 = json_data.get('logEvents')
    print(type(json_data_event2)) # list 타입

    print(json_data_event2)
    print('--------------',json_data_event2[0],'--------------',sep='\n')
    print(type(json_data_event2[0])) # 이건 또 dic 타입

    print(json_data_event2[0].keys())

    json_data_event3 = json_data_event2[0]
    print('-------------',json_data_event3.get('timestamp'),'----------',sep='\n')
    print(json_data_event3['message'])
    
    # 결론
    json_data.get('logEvents')[0].get('timestamp') # 이런 형태로 출력을 해야할 듯?

    # json_data_event2 = json_data['logEvents'][1]['message'][0]
    # # print(type(json_data_event))
    # print(json_data_event2)
    # # print(json_data_event['Records'])

    j_file.close()


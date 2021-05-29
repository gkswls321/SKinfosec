import boto3
import os
import uuid
import time
import datetime
import asyncio
import json
import logging
from botocore.client import ClientError

# Initialize Logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def set_global_vars(): # 우리 계정에 대한 내용을 적는 부분인듯?
    global_vars = {"status": False}
    
    try:
        global_vars["Owner"]                    = "eventshop" # 그냥 우리 맘대로 이름 쓰는 거 인듯?
        global_vars["Environment"]              = "DevelopTeam" # 이거 그냥 맘대로 이름 쓰는 거 인듯?
        global_vars["aws_region"]               = "ap-northeast-2"
        global_vars["tag_name"]                 = "serverless_cloudwatch_logs_exporter" # 여기도.. tag_name이 뭘까?
        global_vars["retention_days"]           = 0 # 0일전 로그를 긁어오겠다!
        global_vars["cw_logs_to_export"]        = ["mysql-error.log"] # 긁어올 로그 그룹 이름
        global_vars["log_dest_bkt"]             = "beom-log-save2" # 버킷명
        global_vars["time_out"]                 = 300 # 뭔지 모름
        global_vars["tsk_back_off"]             = 2 # 뭔지 모름
        global_vars["status"]                   = True
        
    except Exception as e:
        logger.error("Unable to set Global Environment variables. Exiting")
        global_vars["error_message"]            = str(e)
        
    return global_vars

def gen_uuid():
    """ Generates a uuid string and return it """
    return str( uuid.uuid4() )

def gen_ymd(t,d) -> str:
    """ 주어진 datetime을 바탕으로 "YYYY + d + MM + d + DD" 형식의 문자열을 생성 """
    ymd =  ( str(t.year) + d + str(t.month) + d + str(t.day) )
    return ymd

def does_bucket_exists( bucket_name ):
    """ S3 버켓이 존재하는 지 Check하고 boolean값 반환 """
    
    bucket_exists_status = { 'status':False, 'error_message':'' }

    try:
        s3 = boto3.resource('s3')
        s3.meta.client.head_bucket( Bucket = bucket_name )
        bucket_exists_status['status'] = True

    except ClientError as e:
        if e.response['Error']['Code'] == "404":
            bucket_exists_status['status'] = False
            bucket_exists_status['error_message'] = str(e)
        else:
            # logger.error('ERROR: {0}'.format( str(e) ) )
            bucket_exists_status['status'] = False
            bucket_exists_status['error_message'] = str(e)
    return bucket_exists_status

def get_cloudwatch_log_groups(global_vars):
    """ 클라우드 워치에 있는 로그 그룹의 목록 반환 """
    
    resp_data = {'status': False, 'log_groups':[], 'error_message': ''}
    client = boto3.client('logs')
    
    try:
        resp = client.describe_log_groups( limit = 50 ) # 로그 그룹 목록 수집
        resp_data['log_groups'].extend( resp.get('logGroups') )

        if resp.get('nextToken'):
            while True:
                resp = client.describe_log_groups( nextToken = resp.get('nextToken'), limit = 50 )
                resp_data['log_groups'].extend( resp.get('logGroups') )

                # 더이상 순서 매길 수 없으면 break
                if not resp.get('nextToken'):
                    break
        resp_data['status'] = True
    except Exception as e:
        resp_data['error_message'] = str(e)
    return resp_data

def filter_logs_to_export(global_vars, lgs):
    """  필터를 적용하여 내보낼 로그 그룹 목록 가져오기 """
    
    resp_data = {'status': False, 'log_groups':[], 'error_message': ''}
    
    # 필터링 시작
    for lg in lgs.get('log_groups'):
        if lg.get('logGroupName') in global_vars.get('cw_logs_to_export'): # log_group에서 global 변수에 있는 cw_logs_to_export와 동일한 데이터 출력
            resp_data['log_groups'].append(lg)
            resp_data['status'] = True
    return resp_data

async def export_cw_logs_to_s3(global_vars, log_group_name, retention_days, bucket_name, obj_prefix = None):
    """
    log_group의 로그를 지정된 S3 버킷으로 저장
    하위 디렉터리(prefix)를 만든다. (기본적으로 로그 그룹 이름으로 만듬)
    """
    
    resp_data = {'status': False, 'task_info':{}, 'error_message': ''}
    if not retention_days: retention_days = 0
    if not obj_prefix: obj_prefix = log_group_name.split('/')[-1]
    
    # 로그를 효과적으로 보관하기 위해 설정하는 부분    
    now_time = datetime.datetime.now()
    n1_day = now_time - datetime.timedelta(days = int(retention_days) + 1)
    n_day = now_time - datetime.timedelta(days = int(retention_days))
    f_time = int(n1_day.timestamp() * 1000)
    t_time = int(n_day.timestamp() * 1000)
    
    # '/' 없이 로그 그룹 이름을 구체적으로 처리
    if '/' in log_group_name:
        d_prefix = str( log_group_name.replace("/","-")[1:] ) + "/" + str( gen_ymd(n1_day, '/') )
    else:
        d_prefix = str( log_group_name.replace("/","-") ) + "/" + str( gen_ymd(n1_day, '/') )
    
    # S3 bucket이 존재하는 지 확인
    resp = does_bucket_exists(bucket_name)
    
    if not resp.get('status'):
        resp_data['error_message'] = resp.get('error_message')
        return resp_data
    try:
        client = boto3.client('logs')
        r = client.create_export_task( # 로그 그룹에서 S3 버킷으로 데이터 내보내기 작업 생성
                taskName = gen_uuid(),
                logGroupName = log_group_name,
                fromTime = f_time,
                to = t_time,
                destination = bucket_name,
                destinationPrefix = d_prefix
                )
                
        # Get the status of each of those asynchronous export tasks # 이 부분 무슨 내용인지 모르겟음
        r = get_tsk_status(r.get('taskId'), global_vars.get('time_out'), global_vars.get('tsk_back_off'))
        if resp.get('status'):
            resp_data['task_info'] = r.get('tsk_info')
            resp_data['status'] = True
        else:
            resp_data['error_message'] = r.get('error_message')
    except Exception as e:
        resp_data['error_message'] = str(e)
    return resp_data

def get_tsk_status(tsk_id, time_out, tsk_back_off):
    """`time_out`.까지 내보내기 작업 목록의 상태를 가져오기 """
    
    resp_data = {'status': False, 'tsk_info':{}, 'error_message': ''}
    client = boto3.client('logs')
    if not time_out: time_out = 300
    t = tsk_back_off
    try:
        # Lets get all the logs
        while True:
            time.sleep(t)
            resp = client.describe_export_tasks(taskId = tsk_id)
            tsk_info = resp['exportTasks'][0]
            if t > int(time_out):
                resp_data['error_message'] = f"Task:{tsk_id} is still running. Status:{tsk_info['status']['code']}"
                resp_data['tsk_info'] = tsk_info
                break
            if tsk_info['status']['code'] != "COMPLETED":
                # Crude exponential back off
                t*=2

            else:
                resp_data['tsk_info'] = tsk_info
                resp_data['status'] = True
                break
    except Exception as e:
        resp_data['error_message'] = f"Unable to verify status of task:{tsk_id}. ERROR:{str(e)}"
    resp_data['tsk_info']['time_taken'] = t
    logger.info(f"It took {t} seconds to explort Log Group:'{tsk_info.get('logGroupName')}'")
    return resp_data

def lambda_handler(event, context):

    global_vars = set_global_vars()

    resp_data = {"status": False, "error_message" : '' }

    if not global_vars.get('status'):
        logger.error('ERROR: {0}'.format( global_vars.get('error_message') ) )
        resp_data['error_message'] = global_vars.get('error_message')
        return resp_data

    lgs = get_cloudwatch_log_groups(global_vars) # 클라우드 워치 로그 그룹 목록 가져오기
    if not lgs.get('status'):
        logger.error(f"Unable to get list of cloudwatch Logs.")
        resp_data['error_message'] = lgs.get('error_message')
        return resp_data

    f_lgs = filter_logs_to_export(global_vars, lgs)  # 필터를 적용하여 내보낼 로그 그룹 목록 가져오기
    if not (f_lgs.get('status') or f_lgs.get('log_groups')):
        err = f"There are no log group matching the filter or Unable to get a filtered list of cloudwatch Logs."
        logger.error( err )
        resp_data['error_message'] = f"{err} ERROR:{f_lgs.get('error_message')}"
        resp_data['lgs'] = {'all_logs':lgs, 'cw_logs_to_export':global_vars.get('cw_logs_to_export'), 'filtered_logs':f_lgs}
        return resp_data

    # TODO: This can be a step function (or) async 'ed
    resp_data['export_tasks'] = []
    #loop = asyncio.get_event_loop()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    # Lets being the archving/export process
    for lg in f_lgs.get('log_groups'):
        resp = loop.run_until_complete( export_cw_logs_to_s3( global_vars, lg.get('logGroupName'),global_vars.get('retention_days'), global_vars.get('log_dest_bkt')) )
        print(resp)
        resp_data['export_tasks'].append(resp)
    loop.close()

    resp_data['status'] = True
    return resp_data

if __name__ == '__main__':
    lambda_handler(None, None)

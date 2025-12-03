"""
EmployeeCreate Lambda 최근 로그 확인
"""
import boto3
from datetime import datetime

logs_client = boto3.client('logs', region_name='us-east-2')
log_group = '/aws/lambda/EmployeeCreate'

print("="*60)
print("EmployeeCreate Lambda 최근 로그")
print("="*60)

try:
    streams = logs_client.describe_log_streams(
        logGroupName=log_group,
        orderBy='LastEventTime',
        descending=True,
        limit=2
    )
    
    for stream in streams['logStreams']:
        stream_name = stream['logStreamName']
        print(f"\n{'='*60}")
        print(f"로그 스트림: {stream_name}")
        print(f"{'='*60}")
        
        events = logs_client.get_log_events(
            logGroupName=log_group,
            logStreamName=stream_name,
            limit=100,
            startFromHead=False
        )
        
        for event in events['events'][-30:]:
            timestamp = datetime.fromtimestamp(event['timestamp']/1000)
            message = event['message'].strip()
            print(f"[{timestamp.strftime('%H:%M:%S')}] {message}")
        
except Exception as e:
    print(f"❌ 로그 확인 실패: {str(e)}")
    import traceback
    traceback.print_exc()

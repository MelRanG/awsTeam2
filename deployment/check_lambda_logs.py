import boto3
import time
from datetime import datetime, timedelta

logs_client = boto3.client('logs', region_name='us-east-2')
log_group = '/aws/lambda/DashboardMetrics'

print("=" * 60)
print("Lambda 함수 로그 확인")
print("=" * 60)

try:
    # 최근 5분간의 로그 스트림 가져오기
    response = logs_client.describe_log_streams(
        logGroupName=log_group,
        orderBy='LastEventTime',
        descending=True,
        limit=1
    )
    
    if response['logStreams']:
        stream_name = response['logStreams'][0]['logStreamName']
        print(f"\n최신 로그 스트림: {stream_name}")
        
        # 로그 이벤트 가져오기
        log_response = logs_client.get_log_events(
            logGroupName=log_group,
            logStreamName=stream_name,
            limit=50
        )
        
        print("\n최근 로그:")
        print("-" * 60)
        for event in log_response['events']:
            timestamp = datetime.fromtimestamp(event['timestamp'] / 1000)
            message = event['message']
            print(f"[{timestamp}] {message}")
    else:
        print("\n로그 스트림이 없습니다.")
        
except Exception as e:
    print(f"\n✗ 에러: {str(e)}")

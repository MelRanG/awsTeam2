"""
Lambda 함수 최근 로그 확인
"""
import boto3
from datetime import datetime, timedelta

logs_client = boto3.client('logs', region_name='us-east-2')

log_group = '/aws/lambda/ResumeVerificationQuestions'

print("=" * 60)
print("검증 질문 Lambda 로그 확인")
print("=" * 60)

try:
    # 최근 10분간의 로그 스트림 가져오기
    response = logs_client.describe_log_streams(
        logGroupName=log_group,
        orderBy='LastEventTime',
        descending=True,
        limit=3
    )
    
    if not response['logStreams']:
        print("\n로그 스트림이 없습니다. Lambda가 실행되지 않았을 수 있습니다.")
    else:
        for stream in response['logStreams']:
            stream_name = stream['logStreamName']
            print(f"\n로그 스트림: {stream_name}")
            print("-" * 60)
            
            # 로그 이벤트 가져오기
            events_response = logs_client.get_log_events(
                logGroupName=log_group,
                logStreamName=stream_name,
                limit=50,
                startFromHead=False
            )
            
            for event in events_response['events'][-20:]:  # 최근 20개만
                timestamp = datetime.fromtimestamp(event['timestamp'] / 1000)
                message = event['message'].strip()
                print(f"[{timestamp}] {message}")
            
except logs_client.exceptions.ResourceNotFoundException:
    print(f"\n로그 그룹을 찾을 수 없습니다: {log_group}")
    print("Lambda 함수가 한 번도 실행되지 않았을 수 있습니다.")
except Exception as e:
    print(f"\n오류 발생: {e}")

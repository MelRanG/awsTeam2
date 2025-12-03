"""
Lambda 함수 로그 확인
"""
import boto3
from datetime import datetime, timedelta

logs_client = boto3.client('logs', region_name='us-east-2')

log_group = '/aws/lambda/ResumeVerificationQuestions'

print("="*60)
print("Lambda 함수 최근 로그 확인")
print("="*60)

try:
    # 최근 10분간의 로그 스트림 가져오기
    streams = logs_client.describe_log_streams(
        logGroupName=log_group,
        orderBy='LastEventTime',
        descending=True,
        limit=3
    )
    
    if not streams['logStreams']:
        print("❌ 로그 스트림이 없습니다")
    else:
        print(f"\n✅ 최근 로그 스트림 {len(streams['logStreams'])}개 발견\n")
        
        for stream in streams['logStreams']:
            stream_name = stream['logStreamName']
            print(f"\n{'='*60}")
            print(f"로그 스트림: {stream_name}")
            print(f"{'='*60}")
            
            # 로그 이벤트 가져오기
            events = logs_client.get_log_events(
                logGroupName=log_group,
                logStreamName=stream_name,
                limit=50,
                startFromHead=False
            )
            
            for event in events['events'][-20:]:  # 최근 20개만
                timestamp = datetime.fromtimestamp(event['timestamp']/1000)
                message = event['message'].strip()
                print(f"[{timestamp.strftime('%H:%M:%S')}] {message}")
            
except Exception as e:
    print(f"❌ 로그 확인 실패: {str(e)}")
    import traceback
    traceback.print_exc()

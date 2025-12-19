"""Lambda 타임아웃 설정"""
import boto3
import time

lambda_client = boto3.client('lambda', region_name='us-east-2')

print("Lambda 타임아웃 설정 중...")
time.sleep(10)  # Lambda 업데이트 완료 대기

try:
    lambda_client.update_function_configuration(
        FunctionName='ResumeVerificationQuestions',
        Timeout=90
    )
    print("✓ 타임아웃 90초로 설정 완료")
except Exception as e:
    print(f"✗ 오류: {e}")

"""
Lambda 함수 타임아웃 업데이트
"""
import boto3

lambda_client = boto3.client('lambda', region_name='us-east-2')

print("Lambda 함수 타임아웃 업데이트 중...")

try:
    response = lambda_client.update_function_configuration(
        FunctionName='ResumeVerificationQuestions',
        Timeout=180
    )
    
    print(f"✅ 타임아웃 업데이트 완료: {response['Timeout']}초")
    print(f"   메모리: {response['MemorySize']}MB")
    print(f"   런타임: {response['Runtime']}")
    
except Exception as e:
    print(f"❌ 업데이트 실패: {str(e)}")

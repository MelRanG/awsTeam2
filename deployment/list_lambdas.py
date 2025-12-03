"""Lambda 함수 목록 조회"""
import boto3

lambda_client = boto3.client('lambda', region_name='us-east-2')

response = lambda_client.list_functions()

print("="*60)
print("Lambda 함수 목록")
print("="*60)

for func in response['Functions']:
    name = func['FunctionName']
    runtime = func['Runtime']
    print(f"{name:40} {runtime}")

print(f"\n총 {len(response['Functions'])}개 함수")

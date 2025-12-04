"""
도메인 관련 Lambda 함수 확인
"""
import boto3

lambda_client = boto3.client('lambda', region_name='us-east-2')

print("도메인 관련 Lambda 함수 검색 중...")
response = lambda_client.list_functions()

domain_functions = [
    func for func in response['Functions']
    if 'domain' in func['FunctionName'].lower()
]

if domain_functions:
    print(f"\n찾은 함수: {len(domain_functions)}개")
    for func in domain_functions:
        print(f"  - {func['FunctionName']}")
else:
    print("\n도메인 관련 Lambda 함수를 찾을 수 없습니다.")
    print("\n모든 Lambda 함수 목록:")
    for func in response['Functions'][:20]:
        print(f"  - {func['FunctionName']}")

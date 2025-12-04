"""
모든 Lambda 함수 목록 조회
"""

import boto3

lambda_client = boto3.client('lambda', region_name='us-east-1')

print("Lambda 함수 목록:\n")

try:
    response = lambda_client.list_functions()
    
    functions = response['Functions']
    print(f"총 {len(functions)}개의 함수 발견\n")
    
    for func in sorted(functions, key=lambda x: x['FunctionName']):
        print(f"• {func['FunctionName']}")
        
except Exception as e:
    print(f"오류 발생: {str(e)}")

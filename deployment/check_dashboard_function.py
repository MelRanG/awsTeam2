"""
대시보드 Lambda 함수 확인
"""

import boto3

lambda_client = boto3.client('lambda', region_name='us-east-1')

print("대시보드 관련 Lambda 함수 검색 중...\n")

try:
    response = lambda_client.list_functions()
    
    dashboard_functions = [
        f for f in response['Functions'] 
        if 'dashboard' in f['FunctionName'].lower()
    ]
    
    if dashboard_functions:
        print(f"발견된 함수: {len(dashboard_functions)}개\n")
        for func in dashboard_functions:
            print(f"함수명: {func['FunctionName']}")
            print(f"ARN: {func['FunctionArn']}")
            print(f"런타임: {func['Runtime']}")
            print(f"마지막 수정: {func['LastModified']}")
            print("-" * 60)
    else:
        print("대시보드 관련 Lambda 함수를 찾을 수 없습니다.")
        
except Exception as e:
    print(f"오류 발생: {str(e)}")

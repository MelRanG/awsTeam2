import boto3

lambda_client = boto3.client('lambda', region_name='us-east-2')

print("=" * 60)
print("Lambda 함수 목록")
print("=" * 60)

try:
    response = lambda_client.list_functions()
    
    dashboard_functions = [f for f in response['Functions'] if 'dashboard' in f['FunctionName'].lower()]
    
    if dashboard_functions:
        print("\n대시보드 관련 Lambda 함수:")
        for func in dashboard_functions:
            print(f"  - {func['FunctionName']}")
    else:
        print("\n대시보드 관련 Lambda 함수를 찾을 수 없습니다.")
        print("\n전체 Lambda 함수 목록:")
        for func in response['Functions']:
            print(f"  - {func['FunctionName']}")
            
except Exception as e:
    print(f"\n✗ 에러: {str(e)}")

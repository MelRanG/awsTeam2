"""
직원 프로젝트 이력 데이터 확인
"""
import boto3
import json

dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
employees_table = dynamodb.Table('Employees')

# 한 명의 직원 데이터 조회
response = employees_table.scan(Limit=1)

if response['Items']:
    employee = response['Items'][0]
    print("=" * 60)
    print("직원 데이터 샘플")
    print("=" * 60)
    print(f"\n이름: {employee.get('basic_info', {}).get('name', 'N/A')}")
    print(f"ID: {employee.get('user_id', 'N/A')}")
    
    print("\n프로젝트 이력 (work_experience):")
    work_exp = employee.get('work_experience', [])
    
    if work_exp:
        for i, project in enumerate(work_exp[:3], 1):
            print(f"\n프로젝트 {i}:")
            print(json.dumps(project, indent=2, ensure_ascii=False))
    else:
        print("  프로젝트 이력 없음")

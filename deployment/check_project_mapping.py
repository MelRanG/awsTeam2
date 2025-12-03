"""
프로젝트 ID와 산업 매핑 확인
"""
import boto3
import json

dynamodb = boto3.resource('dynamodb', region_name='us-east-2')

# 직원 데이터 확인
emp_table = dynamodb.Table('Employees')
emp_response = emp_table.scan(Limit=3)
employees = emp_response.get('Items', [])

print("=" * 60)
print("직원의 프로젝트 경험 확인")
print("=" * 60)

for emp in employees[:2]:
    print(f"\n직원: {emp.get('basic_info', {}).get('name', 'N/A')}")
    work_exp = emp.get('work_experience', [])
    print(f"프로젝트 경험 수: {len(work_exp)}")
    for exp in work_exp:
        if isinstance(exp, dict):
            print(f"  - 프로젝트 ID: {exp.get('project_id', 'N/A')}")
            print(f"    프로젝트명: {exp.get('project_name', 'N/A')}")

# 프로젝트 데이터 확인
print("\n" + "=" * 60)
print("프로젝트 데이터 확인")
print("=" * 60)

proj_table = dynamodb.Table('Projects')
proj_response = proj_table.scan(Limit=3)
projects = proj_response.get('Items', [])

for proj in projects[:3]:
    print(f"\n프로젝트 ID: {proj.get('project_id', 'N/A')}")
    print(f"프로젝트명: {proj.get('project_name', 'N/A')}")
    print(f"산업: {proj.get('client_industry', 'N/A')}")

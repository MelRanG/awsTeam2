"""
도메인 전문성 데이터 확인 스크립트
직원의 work_experience와 프로젝트의 client_industry 매핑 확인
"""
import boto3
import json

dynamodb = boto3.resource('dynamodb', region_name='us-east-2')

# 직원 데이터 확인
emp_table = dynamodb.Table('Employees')
emp_response = emp_table.scan(Limit=5)

print("=" * 60)
print("직원 work_experience 샘플:")
print("=" * 60)
for emp in emp_response['Items'][:5]:
    user_id = emp.get('user_id')
    work_exp = emp.get('work_experience', [])
    project_ids = [exp.get('project_id') for exp in work_exp if isinstance(exp, dict)]
    print(f"User: {user_id}, Projects: {project_ids}")

print("\n" + "=" * 60)
print("프로젝트 데이터 샘플:")
print("=" * 60)

# 프로젝트 데이터 확인
proj_table = dynamodb.Table('Projects')
proj_response = proj_table.scan(Limit=5)

for proj in proj_response['Items'][:5]:
    proj_id = proj.get('project_id')
    industry = proj.get('client_industry', '없음')
    print(f"Project: {proj_id}, Industry: {industry}")

print("\n" + "=" * 60)
print("매핑 테스트:")
print("=" * 60)

# 매핑 테스트
all_projects = proj_table.scan()
project_map = {p.get('project_id'): p.get('client_industry', '기타') 
               for p in all_projects['Items']}

print(f"전체 프로젝트 수: {len(project_map)}")

# 직원별 산업 경험 집계
all_employees = emp_table.scan()
matched_count = 0
unmatched_count = 0
industry_counts = {}

for emp in all_employees['Items']:
    work_exp = emp.get('work_experience', [])
    for exp in work_exp:
        if isinstance(exp, dict):
            proj_id = exp.get('project_id')
            if proj_id in project_map:
                matched_count += 1
                industry = project_map[proj_id]
                industry_counts[industry] = industry_counts.get(industry, 0) + 1
            else:
                unmatched_count += 1
                print(f"  ⚠️ 매칭 안됨: {proj_id}")

print(f"\n매칭 성공: {matched_count}개")
print(f"매칭 실패: {unmatched_count}개")
print(f"\n산업별 경험 집계:")
for industry, count in sorted(industry_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"  - {industry}: {count}개")

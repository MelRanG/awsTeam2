"""
프로젝트 ID 형식 확인
"""
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
proj_table = dynamodb.Table('Projects')

response = proj_table.scan()
projects = response['Items']

# 프로젝트 ID 형식별 분류
p_format = []  # P_XXX 형식
prj_format = []  # PRJXXX 형식

for proj in projects:
    proj_id = proj.get('project_id', '')
    if proj_id.startswith('P_'):
        p_format.append(proj_id)
    elif proj_id.startswith('PRJ'):
        prj_format.append(proj_id)

print(f"전체 프로젝트 수: {len(projects)}")
print(f"P_XXX 형식: {len(p_format)}개")
print(f"PRJXXX 형식: {len(prj_format)}개")

if p_format:
    print(f"\nP_XXX 샘플: {p_format[:5]}")
if prj_format:
    print(f"PRJXXX 샘플: {prj_format[:5]}")

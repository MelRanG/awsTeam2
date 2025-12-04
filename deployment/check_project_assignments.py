import boto3
import json
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

dynamodb = boto3.resource('dynamodb', region_name='us-east-2')

print("=" * 60)
print("프로젝트 배정 현황 확인")
print("=" * 60)

# 프로젝트 확인
projects_table = dynamodb.Table('Projects')
projects_response = projects_table.scan()
projects = projects_response.get('Items', [])

print(f"\n총 프로젝트 수: {len(projects)}")

assigned_employees = set()

for project in projects:
    project_id = project.get('project_id')
    status = project.get('status', 'unknown')
    team_members = project.get('team_members', [])
    
    if status == 'in-progress' and team_members:
        print(f"\n프로젝트: {project_id} (상태: {status})")
        print(f"  팀원 수: {len(team_members)}")
        for member in team_members:
            if isinstance(member, dict):
                user_id = member.get('user_id')
                if user_id:
                    assigned_employees.add(user_id)
                    print(f"    - {user_id}: {member.get('name', 'N/A')} ({member.get('role', 'N/A')})")

print(f"\n총 배정된 인원 수: {len(assigned_employees)}")

# 전체 직원 수 확인
employees_table = dynamodb.Table('Employees')
employees_response = employees_table.scan(Select='COUNT')
total_employees = employees_response.get('Count', 0)

print(f"전체 직원 수: {total_employees}")
print(f"투입 대기 인력: {total_employees - len(assigned_employees)}명")

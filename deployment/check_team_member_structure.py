import boto3
import json
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
projects_table = dynamodb.Table('Projects')

print("=" * 60)
print("팀원 데이터 구조 확인")
print("=" * 60)

response = projects_table.scan()
projects = response.get('Items', [])

for project in projects:
    status = project.get('status')
    team_members = project.get('team_members', [])
    
    if status == 'in-progress' and team_members:
        print(f"\n프로젝트: {project.get('project_id')}")
        print(f"팀원 수: {len(team_members)}")
        print(f"팀원 데이터:")
        print(json.dumps(team_members, indent=2, ensure_ascii=False, cls=DecimalEncoder))
        break  # 첫 번째 프로젝트만 확인

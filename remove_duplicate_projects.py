"""프로젝트 중복 제거 스크립트"""
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('Projects')

# 모든 프로젝트 조회
response = table.scan()
items = response.get('Items', [])

print(f"총 프로젝트 수: {len(items)}")

# 프로젝트 이름별로 그룹화
from collections import defaultdict
name_groups = defaultdict(list)

for item in items:
    name = item.get('project_name', '')
    name_groups[name].append(item)

# 중복 제거 (각 이름당 첫 번째 것만 남김)
removed_count = 0
for name, projects in name_groups.items():
    if len(projects) > 1:
        print(f"\n'{name}': {len(projects)}개 중 {len(projects)-1}개 삭제")
        # 첫 번째를 제외한 나머지 삭제
        for proj in projects[1:]:
            project_id = proj.get('project_id')
            try:
                table.delete_item(Key={'project_id': project_id})
                print(f"  삭제: {project_id}")
                removed_count += 1
            except Exception as e:
                print(f"  삭제 실패: {project_id} - {str(e)}")

print(f"\n총 {removed_count}개의 중복 프로젝트가 제거되었습니다.")
print(f"남은 프로젝트 수: {len(items) - removed_count}개")

"""
프로젝트 데이터 및 도메인 확인
"""
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb', region_name='us-east-2')

# 프로젝트 조회
projects_table = dynamodb.Table('Projects')
response = projects_table.scan()
projects = response.get('Items', [])

print(f"총 프로젝트 수: {len(projects)}")
print("\n프로젝트 상세 정보:")
print("=" * 80)

for i, project in enumerate(projects[:10], 1):
    print(f"\n{i}. {project.get('project_name', 'N/A')}")
    print(f"   상태: {project.get('status', 'N/A')}")
    print(f"   산업: {project.get('client_industry', 'N/A')}")
    print(f"   설명: {project.get('description', 'N/A')[:100]}")
    
    tech_stack = project.get('tech_stack', {})
    if tech_stack:
        print(f"   기술 스택:")
        for category, techs in tech_stack.items():
            if isinstance(techs, list):
                print(f"     - {category}: {', '.join(techs[:5])}")

print("\n" + "=" * 80)
print("\nTechTrends 도메인 확인:")
print("=" * 80)

# TechTrends 조회
techtrends_table = dynamodb.Table('TechTrends')
response = techtrends_table.scan()
trends = response.get('Items', [])

# 도메인 수집
all_domains = set()
for trend in trends:
    related_domains = trend.get('related_domains', [])
    category = trend.get('category', '')
    
    if related_domains:
        all_domains.update(related_domains)
    if category:
        all_domains.add(category)

print(f"\nTechTrends에서 발견된 도메인: {len(all_domains)}개")
for domain in sorted(all_domains):
    print(f"  - {domain}")

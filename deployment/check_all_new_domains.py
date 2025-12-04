"""
모든 신규 도메인 확인 (기술 매칭 여부 무관)
"""
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-2')

# TechTrends 조회
techtrends_table = dynamodb.Table('TechTrends')
response = techtrends_table.scan()
trends = response.get('Items', [])

# 프로젝트 조회
projects_table = dynamodb.Table('Projects')
response = projects_table.scan()
projects = response.get('Items', [])

# 현재 프로젝트 도메인 추출
current_domains = set()
for project in projects:
    status = project.get('status', '').lower()
    if status in ['in-progress', 'completed']:
        industry = project.get('client_industry', '')
        if industry:
            current_domains.add(industry.split('/')[0].strip())

print("=" * 80)
print("현재 보유 도메인 vs TechTrends 신규 도메인")
print("=" * 80)

print(f"\n【현재 보유 도메인】 {len(current_domains)}개")
for domain in sorted(current_domains):
    print(f"  - {domain}")

# TechTrends의 모든 도메인 수집
all_trend_domains = set()
for trend in trends:
    related_domains = trend.get('related_domains', [])
    category = trend.get('category', '')
    
    all_trend_domains.update(related_domains)
    if category:
        all_trend_domains.add(category)

print(f"\n【TechTrends 전체 도메인】 {len(all_trend_domains)}개")
for domain in sorted(all_trend_domains):
    print(f"  - {domain}")

# 신규 도메인 (TechTrends에는 있지만 현재 보유하지 않은 도메인)
new_domains = all_trend_domains - current_domains

print(f"\n【신규 진출 가능 도메인】 {len(new_domains)}개")
for domain in sorted(new_domains):
    # 해당 도메인의 기술 수집
    domain_techs = []
    for trend in trends:
        if domain in trend.get('related_domains', []) or domain == trend.get('category', ''):
            domain_techs.append(trend.get('tech_name', ''))
    
    print(f"  - {domain} ({len(domain_techs)}개 기술)")
    if domain_techs:
        print(f"      기술: {', '.join(domain_techs[:5])}")

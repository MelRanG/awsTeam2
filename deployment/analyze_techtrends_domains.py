"""
TechTrends 도메인 상세 분석
"""
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('TechTrends')

response = table.scan()
trends = response.get('Items', [])

print(f"총 TechTrends 데이터: {len(trends)}개\n")

# 카테고리별 분류
categories = {}
for trend in trends:
    category = trend.get('category', 'N/A')
    tech_name = trend.get('tech_name', 'N/A')
    related_domains = trend.get('related_domains', [])
    
    if category not in categories:
        categories[category] = []
    
    categories[category].append({
        'tech': tech_name,
        'domains': related_domains
    })

print("=" * 80)
print("카테고리별 기술 및 관련 도메인")
print("=" * 80)

for category, techs in sorted(categories.items()):
    print(f"\n【{category}】 ({len(techs)}개 기술)")
    for tech_info in techs[:5]:
        domains_str = ', '.join(tech_info['domains']) if tech_info['domains'] else '없음'
        print(f"  - {tech_info['tech']}: {domains_str}")
    if len(techs) > 5:
        print(f"  ... 외 {len(techs) - 5}개")

# related_domains 통계
print("\n" + "=" * 80)
print("related_domains 통계")
print("=" * 80)

all_domains = set()
trends_with_domains = 0

for trend in trends:
    related_domains = trend.get('related_domains', [])
    if related_domains:
        trends_with_domains += 1
        all_domains.update(related_domains)

print(f"\nrelated_domains가 있는 트렌드: {trends_with_domains}/{len(trends)}개")
print(f"발견된 고유 도메인: {len(all_domains)}개")
print("\n도메인 목록:")
for domain in sorted(all_domains):
    print(f"  - {domain}")

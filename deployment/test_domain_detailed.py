"""
도메인 분석 상세 테스트
"""
import boto3
import json

lambda_client = boto3.client('lambda', region_name='us-east-2')

print("=" * 80)
print("도메인 분석 상세 결과")
print("=" * 80)

# Lambda 함수 호출
response = lambda_client.invoke(
    FunctionName='DomainAnalysisEngine',
    InvocationType='RequestResponse',
    Payload=json.dumps({
        'body': json.dumps({
            'analysis_type': 'new_domains'
        })
    })
)

payload = json.loads(response['Payload'].read())
result = json.loads(payload.get('body', '{}'))

print(f"\n【현재 보유 도메인】 {len(result.get('current_domains', []))}개")
for i, domain in enumerate(result.get('current_domains', []), 1):
    print(f"  {i}. {domain}")

print(f"\n【신규 진출 기회】 {len(result.get('identified_domains', []))}개")
print("=" * 80)

for i, domain in enumerate(result.get('identified_domains', [])[:15], 1):
    print(f"\n{i}. {domain.get('domain_name')} (실현가능성: {domain.get('feasibility_score')}점)")
    print(f"   시장 성장률: {domain.get('market_growth_rate', 0)}%")
    print(f"   시장 수요: {domain.get('market_demand_score', 0)}점")
    print(f"   보유 기술: {len(domain.get('matched_skills', []))}개")
    if domain.get('matched_skills'):
        print(f"     - {', '.join(domain.get('matched_skills', [])[:5])}")
    print(f"   필요 기술: {len(domain.get('skill_gap', []))}개")
    if domain.get('skill_gap'):
        print(f"     - {', '.join(domain.get('skill_gap', [])[:5])}")
    print(f"   전환 가능 인력: {domain.get('transferable_employees', 0)}명")
    print(f"   분석 근거: {domain.get('reasoning', '')[:150]}...")

print("\n" + "=" * 80)
print(f"총 분석 프로젝트: {result.get('total_projects_analyzed')}개")
print(f"총 분석 인력: {result.get('total_employees')}명")
print("=" * 80)

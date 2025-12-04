"""
Lambda 함수 직접 호출 테스트
"""
import boto3
import json

lambda_client = boto3.client('lambda', region_name='us-east-2')

print("=" * 80)
print("도메인 분석 Lambda 직접 호출 테스트")
print("=" * 80)

# Lambda 함수 호출
print("\nLambda 함수 호출 중...")
response = lambda_client.invoke(
    FunctionName='DomainAnalysisEngine',
    InvocationType='RequestResponse',
    Payload=json.dumps({
        'body': json.dumps({
            'analysis_type': 'new_domains'
        })
    })
)

# 응답 파싱
payload = json.loads(response['Payload'].read())
print(f"\n상태 코드: {payload.get('statusCode')}")

if payload.get('statusCode') == 200:
    result = json.loads(payload.get('body', '{}'))
    
    print(f"\n✅ 성공!")
    print(f"\n현재 보유 도메인: {len(result.get('current_domains', []))}개")
    for domain in result.get('current_domains', []):
        print(f"  - {domain}")
    
    print(f"\n신규 진출 기회: {len(result.get('identified_domains', []))}개")
    for i, domain in enumerate(result.get('identified_domains', [])[:5], 1):
        print(f"  {i}. {domain.get('domain_name')}: {domain.get('feasibility_score')}점")
        print(f"     보유 기술: {len(domain.get('matched_skills', []))}개")
        print(f"     필요 기술: {len(domain.get('skill_gap', []))}개")
    
    print(f"\n분석 통계:")
    print(f"  - 분석 프로젝트: {result.get('total_projects_analyzed')}개")
    print(f"  - 분석 인력: {result.get('total_employees')}명")
    
else:
    print(f"\n❌ 실패")
    print(payload.get('body'))

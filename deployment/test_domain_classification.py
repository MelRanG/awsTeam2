"""
도메인 분류 테스트
"""
import requests
import json

API_URL = "https://yvbi9c3ik5.execute-api.us-east-2.amazonaws.com/prod"

print("=" * 80)
print("도메인 분석 API 테스트")
print("=" * 80)

# 도메인 분석 요청
print("\n도메인 분석 요청 중...")
response = requests.post(
    f"{API_URL}/domain-analysis",
    json={"analysis_type": "new_domains"},
    headers={"Content-Type": "application/json"}
)

if response.status_code == 200:
    result = response.json()
    
    print(f"\n✅ 성공!")
    print(f"\n현재 보유 도메인: {len(result.get('current_domains', []))}개")
    for domain in result.get('current_domains', []):
        print(f"  - {domain}")
    
    print(f"\n신규 진출 기회: {len(result.get('identified_domains', []))}개")
    for domain in result.get('identified_domains', [])[:5]:
        print(f"  - {domain.get('domain_name')}: {domain.get('feasibility_score')}점")
    
    print(f"\n분석 통계:")
    print(f"  - 분석 프로젝트: {result.get('total_projects_analyzed')}개")
    print(f"  - 분석 인력: {result.get('total_employees')}명")
    
else:
    print(f"\n❌ 실패: {response.status_code}")
    print(response.text)

"""
대기자 생성 API 응답 구조 확인
"""
import requests
import json

API_URL = "https://ifeniowvpb.execute-api.us-east-2.amazonaws.com/prod/pending-candidates"

test_data = {
    "name": "테스트",
    "email": "test@test.com",
    "role": "신규 지원자",
    "years_of_experience": 3,
    "skills": [{"name": "Python", "level": "Intermediate", "years": 3}],
    "status": "pending",
    "evaluation_data": {},
    "verification_questions": []
}

print("=" * 60)
print("대기자 생성 API 테스트")
print("=" * 60)

response = requests.post(API_URL, json=test_data)

print(f"\n상태 코드: {response.status_code}")
print(f"\n응답 본문:")
print(json.dumps(response.json(), indent=2, ensure_ascii=False))

if response.status_code == 201:
    data = response.json()
    print(f"\n✓ candidate_id 추출 테스트:")
    print(f"  - data.get('candidate_id'): {data.get('candidate_id')}")
    print(f"  - data.get('candidate', {{}}).get('candidate_id'): {data.get('candidate', {}).get('candidate_id')}")

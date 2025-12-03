"""
검증 질문 API 빠른 테스트
"""
import requests
import json

# API URL
API_URL = "https://ifeniowvpb.execute-api.us-east-2.amazonaws.com/prod"

# 테스트 데이터
test_data = {
    "resume_data": {
        "name": "김철수",
        "email": "kim.cs@example.com",
        "experience": [
            {
                "company": "네이버",
                "position": "백엔드 개발자",
                "duration": "2018.03 - 2020.12",
                "description": "대규모 트래픽 처리 시스템 개발"
            }
        ],
        "skills": ["Python", "AWS", "Docker"]
    },
    "evaluation": {
        "overall_score": 85,
        "technical_skills": {
            "score": 90,
            "strengths": ["AWS 전문성"],
            "weaknesses": ["프론트엔드 경험 부족"]
        }
    }
}

print("="*60)
print("검증 질문 API 테스트")
print("="*60)
print(f"\n📍 API URL: {API_URL}/resume/verification-questions")
print(f"📤 요청 데이터 크기: {len(json.dumps(test_data))} bytes")

try:
    print("\n⏳ API 호출 중... (Bedrock 호출로 30-60초 소요될 수 있습니다)")
    
    response = requests.post(
        f"{API_URL}/resume/verification-questions",
        json=test_data,
        headers={"Content-Type": "application/json"},
        timeout=90
    )
    
    print(f"\n✅ 응답 상태 코드: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        
        if 'questions' in result:
            questions = result['questions']
            print(f"✅ 생성된 검증 질문: {len(questions)}개")
            
            print("\n" + "="*60)
            print("생성된 검증 질문:")
            print("="*60)
            
            for i, q in enumerate(questions, 1):
                print(f"\n[질문 {i}] {q.get('category', 'N/A')} - {q.get('severity', 'N/A')}")
                print(f"질문: {q.get('question', 'N/A')}")
                print(f"이유: {q.get('reason', 'N/A')}")
        else:
            print(f"⚠️  응답에 questions 필드가 없습니다: {result}")
    else:
        print(f"❌ 오류 응답: {response.text}")
        
except requests.exceptions.Timeout:
    print("❌ 타임아웃: API 응답이 90초를 초과했습니다")
    print("💡 Bedrock 호출이 지연되고 있을 수 있습니다")
except Exception as e:
    print(f"❌ 오류 발생: {str(e)}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("테스트 완료")
print("="*60)

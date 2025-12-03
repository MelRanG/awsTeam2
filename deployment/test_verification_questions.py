"""
검증 질문 생성 API 테스트 스크립트
"""
import boto3
import json
from datetime import datetime

def test_verification_questions():
    """검증 질문 생성 API 테스트"""
    
    # API Gateway 클라이언트 생성
    apigateway = boto3.client('apigateway', region_name='us-east-2')
    
    # API Gateway ID 찾기
    apis = apigateway.get_rest_apis()
    api_id = None
    for api in apis['items']:
        if 'hr-resource-optimization' in api['name'].lower():
            api_id = api['id']
            break
    
    if not api_id:
        print("❌ API Gateway를 찾을 수 없습니다")
        return
    
    print(f"✅ API Gateway ID: {api_id}")
    
    # API URL 구성
    api_url = f"https://{api_id}.execute-api.us-east-2.amazonaws.com/prod"
    print(f"📍 API URL: {api_url}")
    
    # 테스트용 이력서 데이터
    test_resume_data = {
        "name": "김철수",
        "email": "kim.cs@example.com",
        "phone": "010-1234-5678",
        "education": [
            {
                "degree": "학사",
                "major": "컴퓨터공학",
                "school": "서울대학교",
                "graduation_year": "2018"
            }
        ],
        "experience": [
            {
                "company": "네이버",
                "position": "백엔드 개발자",
                "duration": "2018.03 - 2020.12",
                "description": "대규모 트래픽 처리 시스템 개발"
            },
            {
                "company": "카카오",
                "position": "시니어 백엔드 개발자",
                "position": "2021.01 - 현재",
                "description": "MSA 아키텍처 설계 및 구현, 성능 50% 개선"
            }
        ],
        "skills": ["Python", "Java", "AWS", "Docker", "Kubernetes"],
        "certifications": ["AWS Solutions Architect Professional"],
        "projects": [
            {
                "name": "결제 시스템 리팩토링",
                "duration": "2022.01 - 2022.06",
                "description": "레거시 결제 시스템을 MSA로 전환, TPS 3배 향상",
                "role": "Tech Lead"
            }
        ]
    }
    
    test_evaluation = {
        "overall_score": 85,
        "technical_skills": {
            "score": 90,
            "strengths": ["AWS 전문성", "대규모 시스템 경험"],
            "weaknesses": ["프론트엔드 경험 부족"]
        },
        "experience_quality": {
            "score": 85,
            "highlights": ["대기업 경력", "성과 중심 업무"]
        },
        "growth_potential": {
            "score": 80,
            "assessment": "지속적인 기술 학습 의지"
        }
    }
    
    # Lambda 직접 호출 테스트
    lambda_client = boto3.client('lambda', region_name='us-east-2')
    
    print("\n" + "="*60)
    print("Lambda 함수 직접 호출 테스트")
    print("="*60)
    
    payload = {
        "body": json.dumps({
            "resume_data": test_resume_data,
            "evaluation": test_evaluation
        })
    }
    
    try:
        response = lambda_client.invoke(
            FunctionName='ResumeVerificationQuestions',
            InvocationType='RequestResponse',
            Payload=json.dumps(payload)
        )
        
        result = json.loads(response['Payload'].read())
        print(f"\n✅ Lambda 응답 상태: {response['StatusCode']}")
        
        if 'body' in result:
            body = json.loads(result['body'])
            if 'questions' in body:
                questions = body['questions']
                print(f"\n✅ 생성된 검증 질문 수: {len(questions)}개")
                print("\n" + "="*60)
                print("생성된 검증 질문:")
                print("="*60)
                
                for i, q in enumerate(questions, 1):
                    print(f"\n[질문 {i}] {q.get('category', 'N/A')} - {q.get('severity', 'N/A')}")
                    print(f"질문: {q.get('question', 'N/A')}")
                    print(f"이유: {q.get('reason', 'N/A')}")
            else:
                print(f"❌ 질문이 생성되지 않았습니다: {body}")
        else:
            print(f"❌ 예상치 못한 응답 형식: {result}")
            
    except Exception as e:
        print(f"❌ Lambda 호출 실패: {str(e)}")
        import traceback
        traceback.print_exc()
    
    # API Gateway 리소스 확인
    print("\n" + "="*60)
    print("API Gateway 리소스 확인")
    print("="*60)
    
    try:
        resources = apigateway.get_resources(restApiId=api_id, limit=500)
        
        resume_resource = None
        verification_resource = None
        
        for resource in resources['items']:
            if resource['path'] == '/resume':
                resume_resource = resource
            elif resource['path'] == '/resume/verification-questions':
                verification_resource = resource
        
        if resume_resource:
            print(f"✅ /resume 리소스 존재: {resume_resource['id']}")
        else:
            print("❌ /resume 리소스 없음")
        
        if verification_resource:
            print(f"✅ /resume/verification-questions 리소스 존재: {verification_resource['id']}")
            
            # 메서드 확인
            if 'resourceMethods' in verification_resource:
                methods = verification_resource['resourceMethods'].keys()
                print(f"   메서드: {', '.join(methods)}")
                
                # POST 메서드 통합 확인
                if 'POST' in methods:
                    try:
                        integration = apigateway.get_integration(
                            restApiId=api_id,
                            resourceId=verification_resource['id'],
                            httpMethod='POST'
                        )
                        print(f"   ✅ POST 통합 타입: {integration.get('type')}")
                        if 'uri' in integration:
                            print(f"   Lambda URI: {integration['uri']}")
                    except Exception as e:
                        print(f"   ❌ POST 통합 확인 실패: {str(e)}")
        else:
            print("❌ /resume/verification-questions 리소스 없음")
            
    except Exception as e:
        print(f"❌ 리소스 확인 실패: {str(e)}")
    
    print("\n" + "="*60)
    print("테스트 완료")
    print("="*60)
    print(f"\n💡 API 엔드포인트: POST {api_url}/resume/verification-questions")
    print("💡 프론트엔드에서 이력서 업로드 → 승인 버튼 클릭 시 자동 호출됩니다")

if __name__ == "__main__":
    test_verification_questions()

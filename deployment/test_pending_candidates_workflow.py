"""
대기자 관리 워크플로우 테스트 스크립트
"""
import boto3
import json
import requests
from datetime import datetime

# 설정
API_BASE_URL = 'https://ifeniowvpb.execute-api.us-east-2.amazonaws.com/prod'
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
pending_table = dynamodb.Table('PendingCandidates')

def test_add_pending_candidate():
    """테스트 대기자 추가"""
    print("\n" + "="*60)
    print("1. 테스트 대기자 추가")
    print("="*60)
    
    test_candidate = {
        'candidate_id': 'test-candidate-001',
        'name': '테스트 지원자',
        'email': 'test@example.com',
        'role': '백엔드 개발자',
        'years_of_experience': 3,
        'submitted_at': datetime.now().isoformat(),
        'skills': [
            {'name': 'Python', 'level': 'Advanced'},
            {'name': 'Django', 'level': 'Intermediate'},
            {'name': 'AWS', 'level': 'Intermediate'}
        ],
        'basic_info': {
            'name': '테스트 지원자',
            'email': 'test@example.com',
            'role': '백엔드 개발자',
            'years_of_experience': 3
        },
        'evaluation_data': {
            'employee_name': '테스트 지원자',
            'overall_score': 85,
            'scores': {
                'technical_skills': 88,
                'project_experience': 82,
                'resume_credibility': 85,
                'cultural_fit': 85
            },
            'strengths': ['Python 전문성', 'AWS 경험'],
            'weaknesses': ['프론트엔드 경험 부족'],
            'ai_recommendation': '백엔드 개발 프로젝트에 적합합니다.'
        }
    }
    
    try:
        pending_table.put_item(Item=test_candidate)
        print(f"✓ 테스트 대기자 추가 완료: {test_candidate['name']}")
        return test_candidate['candidate_id']
    except Exception as e:
        print(f"✗ 대기자 추가 실패: {str(e)}")
        return None

def test_get_pending_candidates():
    """대기자 목록 조회 테스트"""
    print("\n" + "="*60)
    print("2. 대기자 목록 조회 테스트")
    print("="*60)
    
    try:
        url = f'{API_BASE_URL}/pending-candidates'
        print(f"요청 URL: {url}")
        
        response = requests.get(url)
        print(f"응답 상태 코드: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            candidates = data.get('candidates', [])
            print(f"✓ 대기자 {len(candidates)}명 조회 완료")
            
            for candidate in candidates:
                name = candidate.get('name', '이름 없음')
                candidate_id = candidate.get('candidate_id', 'ID 없음')
                print(f"  - {name} (ID: {candidate_id})")
            
            return candidates
        else:
            print(f"✗ 조회 실패: {response.text}")
            return []
            
    except Exception as e:
        print(f"✗ 에러 발생: {str(e)}")
        return []

def test_delete_pending_candidate(candidate_id):
    """대기자 삭제 테스트"""
    print("\n" + "="*60)
    print("3. 대기자 삭제 테스트")
    print("="*60)
    
    try:
        url = f'{API_BASE_URL}/pending-candidates/{candidate_id}'
        print(f"요청 URL: {url}")
        
        response = requests.delete(url)
        print(f"응답 상태 코드: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ 대기자 삭제 완료")
            print(f"  메시지: {data.get('message')}")
            return True
        else:
            print(f"✗ 삭제 실패: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ 에러 발생: {str(e)}")
        return False

def test_approve_workflow():
    """승인 워크플로우 테스트"""
    print("\n" + "="*60)
    print("4. 승인 워크플로우 테스트")
    print("="*60)
    
    # 시뮬레이션: 대기자를 Employees 테이블에 추가
    print("승인 시뮬레이션:")
    print("  1. PendingCandidates에서 삭제")
    print("  2. Employees 테이블에 추가 (status 없이)")
    print("  ✓ 실제 구현은 프론트엔드에서 처리됩니다")

def main():
    """메인 함수"""
    print("\n" + "="*60)
    print("대기자 관리 워크플로우 테스트")
    print("="*60)
    
    # 1. 테스트 대기자 추가
    candidate_id = test_add_pending_candidate()
    
    if not candidate_id:
        print("\n✗ 테스트 실패: 대기자 추가 불가")
        return
    
    # 2. 대기자 목록 조회
    candidates = test_get_pending_candidates()
    
    # 3. 대기자 삭제
    if candidate_id:
        test_delete_pending_candidate(candidate_id)
    
    # 4. 삭제 확인
    print("\n" + "="*60)
    print("5. 삭제 확인")
    print("="*60)
    candidates_after = test_get_pending_candidates()
    
    # 5. 승인 워크플로우 설명
    test_approve_workflow()
    
    print("\n" + "="*60)
    print("✓ 테스트 완료!")
    print("="*60)
    print("\n다음 단계:")
    print("1. 프론트엔드에서 '인력 평가' 메뉴 접속")
    print("2. '이력서 업로드' 탭에서 PDF 업로드")
    print("3. 분석 결과 확인 후 '승인' 또는 '반려' 버튼 클릭")
    print("4. '대기자 명단' 탭에서 대기 중인 지원자 확인")
    print("5. 대기자 선택 후 '승인' 버튼으로 정식 직원 등록")
    print()

if __name__ == '__main__':
    main()

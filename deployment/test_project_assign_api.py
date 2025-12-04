"""
프로젝트 투입 API 테스트
"""

import requests
import json
from datetime import datetime, timedelta

def test_api():
    """API 테스트"""
    
    print("=" * 60)
    print("프로젝트 투입 API 테스트")
    print("=" * 60)
    
    # API 엔드포인트
    project_id = "PRJ012"
    url = f"https://ifeniowvpb.execute-api.us-east-2.amazonaws.com/prod/projects/{project_id}/assign"
    
    # 테스트 데이터
    start_date = datetime.now().strftime('%Y-%m-%d')
    end_date = (datetime.now() + timedelta(days=180)).strftime('%Y-%m-%d')
    
    payload = {
        "employee_id": "U_003",
        "role": "Backend Developer",
        "start_date": start_date,
        "end_date": end_date,
        "allocation_rate": 100,
        "assignment_reason": "AI 추천 기반 투입 - 기술 매칭 점수 85점, 팀 친밀도 우수"
    }
    
    print(f"\nAPI 엔드포인트: {url}")
    print(f"\n요청 데이터:")
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    
    print("\n요청 전송 중...")
    
    try:
        response = requests.post(url, json=payload)
        
        print(f"\n응답 상태 코드: {response.status_code}")
        print(f"응답 헤더:")
        for key, value in response.headers.items():
            if 'access-control' in key.lower():
                print(f"  {key}: {value}")
        
        if response.status_code == 200:
            data = response.json()
            assignment = data.get('assignment', {})
            
            print("\n" + "=" * 60)
            print("✅ 프로젝트 투입 성공!")
            print("=" * 60)
            
            print(f"\n【투입 정보】")
            print(f"  프로젝트: {assignment.get('project_name', 'N/A')}")
            print(f"  직원: {assignment.get('employee_name', 'N/A')}")
            print(f"  역할: {assignment.get('role', 'N/A')}")
            print(f"  시작일: {assignment.get('start_date', 'N/A')}")
            print(f"  종료일: {assignment.get('end_date', 'N/A')}")
            print(f"  투입률: {assignment.get('allocation_rate', 'N/A')}%")
            
            if assignment.get('assignment_reason'):
                print(f"\n【투입 근거】")
                print(f"  {assignment.get('assignment_reason')}")
        else:
            print(f"\n✗ 투입 실패")
            print(f"응답 내용: {response.text}")
            
    except Exception as e:
        print(f"\n✗ 테스트 실패: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_api()

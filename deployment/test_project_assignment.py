"""
프로젝트 투입 기능 테스트
"""

import boto3
import json
from datetime import datetime, timedelta

def test_project_assignment():
    """프로젝트 투입 기능 테스트"""
    
    lambda_client = boto3.client('lambda', region_name='us-east-2')
    
    print("=" * 60)
    print("프로젝트 투입 기능 테스트")
    print("=" * 60)
    
    # 테스트 데이터
    project_id = "PROJ-001"
    employee_id = "EMP-001"
    
    # 투입 정보
    start_date = datetime.now().strftime('%Y-%m-%d')
    end_date = (datetime.now() + timedelta(days=180)).strftime('%Y-%m-%d')
    
    test_data = {
        'pathParameters': {
            'projectId': project_id
        },
        'httpMethod': 'POST',
        'body': json.dumps({
            'employee_id': employee_id,
            'role': 'Backend Developer',
            'start_date': start_date,
            'end_date': end_date,
            'allocation_rate': 100,
            'assignment_reason': 'AI 추천 기반 투입 - 기술 매칭 점수 85점, 팀 친밀도 우수'
        })
    }
    
    print(f"\n테스트 프로젝트: {project_id}")
    print(f"테스트 직원: {employee_id}")
    print(f"투입 역할: Backend Developer")
    print(f"투입 기간: {start_date} ~ {end_date}")
    print(f"투입률: 100%")
    
    print("\n프로젝트 투입 요청 중...")
    
    try:
        response = lambda_client.invoke(
            FunctionName='ProjectAssignment',
            InvocationType='RequestResponse',
            Payload=json.dumps(test_data)
        )
        
        result = json.loads(response['Payload'].read())
        
        print(f"\n응답 상태 코드: {result['statusCode']}")
        
        if result['statusCode'] == 200:
            body = json.loads(result['body'])
            assignment = body.get('assignment', {})
            
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
            body = json.loads(result['body'])
            print(f"\n✗ 투입 실패: {body.get('error', 'Unknown error')}")
            
            if 'conflict' in body:
                print(f"\n충돌 정보:")
                print(f"  {body['conflict']}")
        
    except Exception as e:
        print(f"\n✗ 테스트 실패: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_project_assignment()

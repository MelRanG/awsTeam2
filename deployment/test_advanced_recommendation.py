"""
고급 알고리즘 기반 추천 근거 테스트
"""

import boto3
import json

def test_recommendation():
    """추천 엔진 테스트"""
    
    lambda_client = boto3.client('lambda', region_name='us-east-2')
    
    print("=" * 60)
    print("고급 알고리즘 기반 추천 근거 테스트")
    print("=" * 60)
    
    # 테스트할 프로젝트 ID (진행 중인 프로젝트)
    test_project_id = "PROJ-001"
    
    print(f"\n테스트 프로젝트: {test_project_id}")
    
    # Lambda 함수 호출
    payload = {
        'httpMethod': 'POST',
        'body': json.dumps({
            'project_id': test_project_id,
            'required_skills': ['Python', 'AWS', 'React'],
            'team_size': 5,
            'priority': 'balanced'
        })
    }
    
    print("\n추천 요청 중...")
    
    try:
        response = lambda_client.invoke(
            FunctionName='ProjectRecommendationEngine',
            InvocationType='RequestResponse',
            Payload=json.dumps(payload)
        )
        
        result = json.loads(response['Payload'].read())
        
        if result['statusCode'] == 200:
            body = json.loads(result['body'])
            recommendations = body.get('recommendations', [])
            
            print(f"\n✓ 추천 결과: {len(recommendations)}명")
            print("\n" + "=" * 60)
            
            # 상위 3명의 추천 근거 출력
            for i, rec in enumerate(recommendations[:3], 1):
                print(f"\n【추천 {i}위】")
                print(f"이름: {rec.get('name', 'N/A')}")
                print(f"역할: {rec.get('role', 'N/A')}")
                print(f"종합 점수: {rec.get('overall_score', 0):.2f}")
                print(f"가용성: {rec.get('availability', 'N/A')}")
                print("\n【추천 근거】")
                print(rec.get('reasoning', '근거 없음'))
                print("\n" + "-" * 60)
            
            print("\n" + "=" * 60)
            print("✅ 테스트 완료!")
            print("=" * 60)
            
        else:
            print(f"\n✗ 오류 발생: {result}")
            
    except Exception as e:
        print(f"\n✗ 테스트 실패: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_recommendation()

import boto3
import json

# Lambda 클라이언트 생성
lambda_client = boto3.client('lambda', region_name='us-east-2')

print("=" * 60)
print("대시보드 메트릭 API 응답 테스트")
print("=" * 60)

try:
    # Lambda 함수 호출
    response = lambda_client.invoke(
        FunctionName='DashboardMetrics',
        InvocationType='RequestResponse'
    )
    
    # 응답 파싱
    payload = json.loads(response['Payload'].read())
    
    print("\n✓ Lambda 함수 호출 성공")
    print(f"Status Code: {payload.get('statusCode')}")
    
    if payload.get('statusCode') == 200:
        body = json.loads(payload.get('body', '{}'))
        
        print("\n응답 데이터 구조:")
        print(json.dumps(body, indent=2, ensure_ascii=False))
        
        # 주요 필드 확인
        print("\n주요 필드 확인:")
        print(f"- employee_distribution: {'있음' if 'employee_distribution' in body else '없음'}")
        print(f"- project_distribution: {'있음' if 'project_distribution' in body else '없음'}")
        print(f"- evaluation_scores: {'있음' if 'evaluation_scores' in body else '없음'}")
        
        if 'employee_distribution' in body:
            print(f"\nemployee_distribution 내용:")
            print(json.dumps(body['employee_distribution'], indent=2, ensure_ascii=False))
            
        if 'evaluation_scores' in body:
            print(f"\nevaluation_scores 내용:")
            print(json.dumps(body['evaluation_scores'], indent=2, ensure_ascii=False))
    else:
        print(f"\n✗ 에러 발생: {payload}")
        
except Exception as e:
    print(f"\n✗ 테스트 실패: {str(e)}")
    import traceback
    traceback.print_exc()

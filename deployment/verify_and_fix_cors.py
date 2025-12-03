"""
CORS 설정 확인 및 수정
"""
import boto3
import json

apigateway = boto3.client('apigateway', region_name='us-east-2')
API_ID = 'ifeniowvpb'

def get_all_resources():
    """모든 리소스 조회"""
    resources = []
    response = apigateway.get_resources(restApiId=API_ID, limit=500)
    resources.extend(response['items'])
    
    while 'position' in response:
        response = apigateway.get_resources(
            restApiId=API_ID,
            limit=500,
            position=response['position']
        )
        resources.extend(response['items'])
    
    return resources

def check_and_fix_cors(resource_id, resource_path, existing_methods):
    """CORS 설정 확인 및 수정"""
    print(f"\n처리 중: {resource_path}")
    print(f"  기존 메서드: {existing_methods}")
    
    if 'OPTIONS' not in existing_methods:
        print(f"  ✗ OPTIONS 메서드 없음")
        return False
    
    try:
        # OPTIONS 메서드의 통합 응답 확인
        try:
            integration_response = apigateway.get_integration_response(
                restApiId=API_ID,
                resourceId=resource_id,
                httpMethod='OPTIONS',
                statusCode='200'
            )
            
            response_params = integration_response.get('responseParameters', {})
            print(f"  현재 CORS 헤더:")
            for key, value in response_params.items():
                print(f"    {key}: {value}")
            
            # CORS 헤더 업데이트
            methods_str = ','.join([m for m in existing_methods if m != 'OPTIONS'])
            
            apigateway.put_integration_response(
                restApiId=API_ID,
                resourceId=resource_id,
                httpMethod='OPTIONS',
                statusCode='200',
                responseParameters={
                    'method.response.header.Access-Control-Allow-Headers': "'Content-Type,Authorization,X-Amz-Date,X-Api-Key,X-Amz-Security-Token'",
                    'method.response.header.Access-Control-Allow-Methods': f"'{methods_str},OPTIONS'",
                    'method.response.header.Access-Control-Allow-Origin': "'*'"
                }
            )
            print(f"  ✓ CORS 헤더 업데이트 완료")
            print(f"    허용 메서드: {methods_str},OPTIONS")
            return True
            
        except apigateway.exceptions.NotFoundException:
            print(f"  ✗ 통합 응답 없음")
            return False
            
    except Exception as e:
        print(f"  ✗ 에러: {str(e)}")
        return False

def check_lambda_cors_headers():
    """Lambda 함수들의 CORS 헤더 확인"""
    print("\n" + "="*60)
    print("Lambda 함수 CORS 헤더 확인")
    print("="*60)
    
    lambda_client = boto3.client('lambda', region_name='us-east-2')
    
    # 주요 Lambda 함수들
    functions = [
        'employees_list',
        'projects_list',
        'dashboard_metrics',
        'pending_candidates_list',
        'pending_candidate_delete',
        'domain_analysis',
        'quantitative_analysis',
        'qualitative_analysis',
        'recommendation_engine'
    ]
    
    for func_name in functions:
        try:
            response = lambda_client.get_function(FunctionName=func_name)
            print(f"\n✓ {func_name} 존재")
            print(f"  Runtime: {response['Configuration']['Runtime']}")
            print(f"  Handler: {response['Configuration']['Handler']}")
        except lambda_client.exceptions.ResourceNotFoundException:
            print(f"\n✗ {func_name} 없음")

def main():
    """메인 함수"""
    print("="*60)
    print("CORS 설정 확인 및 수정")
    print("="*60)
    print(f"API ID: {API_ID}")
    
    # 모든 리소스 조회
    print("\n리소스 조회 중...")
    resources = get_all_resources()
    print(f"✓ {len(resources)}개 리소스 발견")
    
    # 각 리소스의 CORS 확인 및 수정
    fixed = 0
    for resource in resources:
        resource_id = resource['id']
        resource_path = resource['path']
        
        # Root 리소스는 건너뛰기
        if resource_path == '/':
            continue
        
        # 리소스의 메서드 확인
        methods = resource.get('resourceMethods', {})
        if not methods:
            continue
        
        existing_methods = list(methods.keys())
        
        if existing_methods:
            if check_and_fix_cors(resource_id, resource_path, existing_methods):
                fixed += 1
    
    # Lambda 함수 확인
    check_lambda_cors_headers()
    
    # API 배포
    print("\n" + "="*60)
    print("API 배포 중...")
    try:
        apigateway.create_deployment(
            restApiId=API_ID,
            stageName='prod',
            description='CORS 헤더 업데이트'
        )
        print("✓ API 배포 완료")
    except Exception as e:
        print(f"✗ API 배포 실패: {str(e)}")
    
    print("\n" + "="*60)
    print(f"✓ 완료! {fixed}개 리소스 CORS 수정")
    print("="*60)
    print(f"\nAPI URL: https://{API_ID}.execute-api.us-east-2.amazonaws.com/prod")
    print("\n다음 단계:")
    print("1. 브라우저 캐시 완전 삭제")
    print("2. 시크릿 모드로 접속")
    print("3. F12 개발자 도구에서 네트워크 탭 확인")
    print()

if __name__ == '__main__':
    main()

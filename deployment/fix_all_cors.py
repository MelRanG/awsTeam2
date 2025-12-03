"""
모든 API Gateway 엔드포인트에 CORS 설정 추가
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

def add_cors_to_resource(resource_id, resource_path, existing_methods):
    """리소스에 CORS 추가"""
    print(f"\n처리 중: {resource_path}")
    print(f"  기존 메서드: {existing_methods}")
    
    # OPTIONS 메서드가 이미 있는지 확인
    if 'OPTIONS' in existing_methods:
        print(f"  ✓ OPTIONS 메서드 이미 존재")
        return
    
    # OPTIONS 메서드가 없으면 추가
    try:
        # 1. OPTIONS 메서드 생성
        apigateway.put_method(
            restApiId=API_ID,
            resourceId=resource_id,
            httpMethod='OPTIONS',
            authorizationType='NONE'
        )
        print(f"  ✓ OPTIONS 메서드 생성")
        
        # 2. MOCK 통합 설정
        apigateway.put_integration(
            restApiId=API_ID,
            resourceId=resource_id,
            httpMethod='OPTIONS',
            type='MOCK',
            requestTemplates={
                'application/json': '{"statusCode": 200}'
            }
        )
        print(f"  ✓ MOCK 통합 설정")
        
        # 3. 메서드 응답 설정
        apigateway.put_method_response(
            restApiId=API_ID,
            resourceId=resource_id,
            httpMethod='OPTIONS',
            statusCode='200',
            responseParameters={
                'method.response.header.Access-Control-Allow-Headers': True,
                'method.response.header.Access-Control-Allow-Methods': True,
                'method.response.header.Access-Control-Allow-Origin': True
            }
        )
        print(f"  ✓ 메서드 응답 설정")
        
        # 4. 통합 응답 설정
        methods_str = ','.join(existing_methods + ['OPTIONS'])
        apigateway.put_integration_response(
            restApiId=API_ID,
            resourceId=resource_id,
            httpMethod='OPTIONS',
            statusCode='200',
            responseParameters={
                'method.response.header.Access-Control-Allow-Headers': "'Content-Type,Authorization'",
                'method.response.header.Access-Control-Allow-Methods': f"'{methods_str}'",
                'method.response.header.Access-Control-Allow-Origin': "'*'"
            }
        )
        print(f"  ✓ 통합 응답 설정 (허용 메서드: {methods_str})")
        
    except Exception as e:
        print(f"  ✗ CORS 설정 실패: {str(e)}")

def main():
    """메인 함수"""
    print("="*60)
    print("모든 API Gateway 엔드포인트에 CORS 설정 추가")
    print("="*60)
    print(f"API ID: {API_ID}")
    
    # 모든 리소스 조회
    print("\n리소스 조회 중...")
    resources = get_all_resources()
    print(f"✓ {len(resources)}개 리소스 발견")
    
    # 각 리소스에 CORS 추가
    processed = 0
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
        
        existing_methods = [m for m in methods.keys() if m != 'OPTIONS']
        
        if existing_methods:
            add_cors_to_resource(resource_id, resource_path, existing_methods)
            processed += 1
    
    # API 배포
    print("\n" + "="*60)
    print("API 배포 중...")
    try:
        apigateway.create_deployment(
            restApiId=API_ID,
            stageName='prod',
            description='CORS 설정 업데이트'
        )
        print("✓ API 배포 완료")
    except Exception as e:
        print(f"✗ API 배포 실패: {str(e)}")
    
    print("\n" + "="*60)
    print(f"✓ 완료! {processed}개 리소스에 CORS 설정 추가")
    print("="*60)
    print(f"\nAPI URL: https://{API_ID}.execute-api.us-east-2.amazonaws.com/prod")
    print()

if __name__ == '__main__':
    main()

"""
누락된 CORS 통합 응답 추가
"""
import boto3

apigateway = boto3.client('apigateway', region_name='us-east-2')
API_ID = 'ifeniowvpb'

# CORS가 필요한 리소스 경로
PATHS_NEED_CORS = [
    '/quantitative-analysis',
    '/projects',
    '/recommendations',
    '/domain-analysis',
    '/qualitative-analysis'
]

def get_resource_id(path):
    """리소스 ID 조회"""
    resources = apigateway.get_resources(restApiId=API_ID)['items']
    for resource in resources:
        if resource['path'] == path:
            return resource['id'], resource.get('resourceMethods', {})
    return None, {}

def add_cors_integration_response(resource_id, path, methods):
    """CORS 통합 응답 추가"""
    print(f"\n처리 중: {path}")
    print(f"  메서드: {list(methods.keys())}")
    
    if 'OPTIONS' not in methods:
        print(f"  ✗ OPTIONS 메서드 없음")
        return False
    
    try:
        # 메서드 응답 확인/추가
        try:
            apigateway.get_method_response(
                restApiId=API_ID,
                resourceId=resource_id,
                httpMethod='OPTIONS',
                statusCode='200'
            )
            print(f"  ✓ 메서드 응답 존재")
        except:
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
            print(f"  ✓ 메서드 응답 추가")
        
        # 통합 응답 추가
        methods_str = ','.join([m for m in methods.keys() if m != 'OPTIONS'])
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
        print(f"  ✓ 통합 응답 추가 (허용 메서드: {methods_str},OPTIONS)")
        return True
        
    except Exception as e:
        print(f"  ✗ 에러: {str(e)}")
        return False

def main():
    """메인 함수"""
    print("="*60)
    print("누락된 CORS 통합 응답 추가")
    print("="*60)
    
    fixed = 0
    for path in PATHS_NEED_CORS:
        resource_id, methods = get_resource_id(path)
        if resource_id:
            if add_cors_integration_response(resource_id, path, methods):
                fixed += 1
        else:
            print(f"\n✗ 리소스 없음: {path}")
    
    # API 배포
    print("\n" + "="*60)
    print("API 배포 중...")
    try:
        apigateway.create_deployment(
            restApiId=API_ID,
            stageName='prod',
            description='CORS 통합 응답 추가'
        )
        print("✓ API 배포 완료")
    except Exception as e:
        print(f"✗ API 배포 실패: {str(e)}")
    
    print("\n" + "="*60)
    print(f"✓ 완료! {fixed}개 리소스 수정")
    print("="*60)
    print(f"\nAPI URL: https://{API_ID}.execute-api.us-east-2.amazonaws.com/prod")
    print()

if __name__ == '__main__':
    main()

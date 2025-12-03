"""
Lambda 함수들을 API Gateway에 연결
"""
import boto3

apigateway = boto3.client('apigateway', region_name='us-east-2')
lambda_client = boto3.client('lambda', region_name='us-east-2')

API_ID = 'ifeniowvpb'
ACCOUNT_ID = '412677576136'
REGION = 'us-east-2'

# 리소스 경로와 Lambda 함수 매핑
RESOURCE_LAMBDA_MAP = {
    '/employees': {
        'GET': 'EmployeesList',
        'POST': 'EmployeeCreate'
    },
    '/projects': {
        'GET': 'ProjectsList',
        'POST': 'ProjectCreate'
    },
    '/dashboard/metrics': {
        'GET': 'DashboardMetrics'
    },
    '/recommendations': {
        'POST': 'ProjectRecommendationEngine'
    },
    '/domain-analysis': {
        'POST': 'DomainAnalysisEngine'
    },
    '/quantitative-analysis': {
        'POST': 'QuantitativeAnalysis'
    },
    '/qualitative-analysis': {
        'POST': 'QualitativeAnalysis'
    }
}

def get_resource_id(path):
    """리소스 ID 조회"""
    resources = apigateway.get_resources(restApiId=API_ID)['items']
    for resource in resources:
        if resource['path'] == path:
            return resource['id']
    return None

def connect_lambda(resource_id, resource_path, http_method, lambda_name):
    """Lambda 함수를 API Gateway에 연결"""
    print(f"\n{http_method} {resource_path} -> {lambda_name}")
    
    lambda_arn = f'arn:aws:lambda:{REGION}:{ACCOUNT_ID}:function:{lambda_name}'
    
    try:
        # 통합 설정
        apigateway.put_integration(
            restApiId=API_ID,
            resourceId=resource_id,
            httpMethod=http_method,
            type='AWS_PROXY',
            integrationHttpMethod='POST',
            uri=f'arn:aws:apigateway:{REGION}:lambda:path/2015-03-31/functions/{lambda_arn}/invocations'
        )
        print(f"  ✓ Lambda 통합 완료")
        
        # Lambda 권한 추가
        try:
            lambda_client.add_permission(
                FunctionName=lambda_name,
                StatementId=f'AllowAPIGateway{http_method}{resource_path.replace("/", "")}',
                Action='lambda:InvokeFunction',
                Principal='apigateway.amazonaws.com',
                SourceArn=f'arn:aws:execute-api:{REGION}:{ACCOUNT_ID}:{API_ID}/*/*'
            )
            print(f"  ✓ Lambda 권한 추가 완료")
        except lambda_client.exceptions.ResourceConflictException:
            print(f"  ✓ Lambda 권한 이미 존재")
            
    except Exception as e:
        print(f"  ✗ 에러: {str(e)}")

def main():
    """메인 함수"""
    print("="*60)
    print("Lambda 함수들을 API Gateway에 연결")
    print("="*60)
    print(f"API ID: {API_ID}")
    
    connected = 0
    for resource_path, methods in RESOURCE_LAMBDA_MAP.items():
        resource_id = get_resource_id(resource_path)
        
        if not resource_id:
            print(f"\n✗ 리소스 없음: {resource_path}")
            continue
        
        for http_method, lambda_name in methods.items():
            connect_lambda(resource_id, resource_path, http_method, lambda_name)
            connected += 1
    
    # API 배포
    print("\n" + "="*60)
    print("API 배포 중...")
    try:
        apigateway.create_deployment(
            restApiId=API_ID,
            stageName='prod',
            description='Lambda 함수 연결'
        )
        print("✓ API 배포 완료")
    except Exception as e:
        print(f"✗ API 배포 실패: {str(e)}")
    
    print("\n" + "="*60)
    print(f"✓ 완료! {connected}개 연결")
    print("="*60)
    print(f"\nAPI URL: https://{API_ID}.execute-api.us-east-2.amazonaws.com/prod")
    print()

if __name__ == '__main__':
    main()

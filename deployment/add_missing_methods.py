"""
누락된 메서드 및 리소스 추가
"""
import boto3

apigateway = boto3.client('apigateway', region_name='us-east-2')
lambda_client = boto3.client('lambda', region_name='us-east-2')

API_ID = 'ifeniowvpb'
ACCOUNT_ID = '412677576136'
REGION = 'us-east-2'

def get_resource_id(path):
    """리소스 ID 조회"""
    resources = apigateway.get_resources(restApiId=API_ID)['items']
    for resource in resources:
        if resource['path'] == path:
            return resource['id']
    return None

def get_root_id():
    """Root 리소스 ID 조회"""
    resources = apigateway.get_resources(restApiId=API_ID)['items']
    for resource in resources:
        if resource['path'] == '/':
            return resource['id']
    return None

def create_resource(parent_id, path_part):
    """리소스 생성"""
    try:
        response = apigateway.create_resource(
            restApiId=API_ID,
            parentId=parent_id,
            pathPart=path_part
        )
        print(f"  ✓ 리소스 생성: /{path_part}")
        return response['id']
    except apigateway.exceptions.ConflictException:
        print(f"  ✓ 리소스 이미 존재: /{path_part}")
        return get_resource_id(f'/{path_part}')

def add_method(resource_id, http_method, lambda_name):
    """메서드 추가"""
    lambda_arn = f'arn:aws:lambda:{REGION}:{ACCOUNT_ID}:function:{lambda_name}'
    
    try:
        # 메서드 생성
        apigateway.put_method(
            restApiId=API_ID,
            resourceId=resource_id,
            httpMethod=http_method,
            authorizationType='NONE'
        )
        print(f"  ✓ {http_method} 메서드 생성")
    except apigateway.exceptions.ConflictException:
        print(f"  ✓ {http_method} 메서드 이미 존재")
    
    # Lambda 통합
    try:
        apigateway.put_integration(
            restApiId=API_ID,
            resourceId=resource_id,
            httpMethod=http_method,
            type='AWS_PROXY',
            integrationHttpMethod='POST',
            uri=f'arn:aws:apigateway:{REGION}:lambda:path/2015-03-31/functions/{lambda_arn}/invocations'
        )
        print(f"  ✓ Lambda 통합 완료")
    except Exception as e:
        print(f"  ✗ Lambda 통합 실패: {str(e)}")
    
    # Lambda 권한
    try:
        lambda_client.add_permission(
            FunctionName=lambda_name,
            StatementId=f'AllowAPIGateway{http_method}{resource_id}',
            Action='lambda:InvokeFunction',
            Principal='apigateway.amazonaws.com',
            SourceArn=f'arn:aws:execute-api:{REGION}:{ACCOUNT_ID}:{API_ID}/*/*'
        )
        print(f"  ✓ Lambda 권한 추가")
    except lambda_client.exceptions.ResourceConflictException:
        print(f"  ✓ Lambda 권한 이미 존재")

def main():
    """메인 함수"""
    print("="*60)
    print("누락된 메서드 및 리소스 추가")
    print("="*60)
    
    # 1. /employees POST 메서드 추가
    print("\n[1] /employees POST 메서드 추가")
    employees_id = get_resource_id('/employees')
    if employees_id:
        add_method(employees_id, 'POST', 'EmployeeCreate')
    
    # 2. /projects POST 메서드 추가
    print("\n[2] /projects POST 메서드 추가")
    projects_id = get_resource_id('/projects')
    if projects_id:
        add_method(projects_id, 'POST', 'ProjectCreate')
    
    # 3. /dashboard 리소스 생성
    print("\n[3] /dashboard 리소스 생성")
    root_id = get_root_id()
    dashboard_id = create_resource(root_id, 'dashboard')
    
    # 4. /dashboard/metrics 리소스 생성
    print("\n[4] /dashboard/metrics 리소스 생성")
    metrics_id = create_resource(dashboard_id, 'metrics')
    
    # 5. /dashboard/metrics GET 메서드 추가
    print("\n[5] /dashboard/metrics GET 메서드 추가")
    add_method(metrics_id, 'GET', 'DashboardMetrics')
    
    # 6. OPTIONS 메서드 추가 (CORS)
    print("\n[6] CORS OPTIONS 메서드 추가")
    for path, resource_id in [('/dashboard', dashboard_id), ('/dashboard/metrics', metrics_id)]:
        print(f"\n  {path}")
        try:
            apigateway.put_method(
                restApiId=API_ID,
                resourceId=resource_id,
                httpMethod='OPTIONS',
                authorizationType='NONE'
            )
            
            apigateway.put_integration(
                restApiId=API_ID,
                resourceId=resource_id,
                httpMethod='OPTIONS',
                type='MOCK',
                requestTemplates={'application/json': '{"statusCode": 200}'}
            )
            
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
            
            apigateway.put_integration_response(
                restApiId=API_ID,
                resourceId=resource_id,
                httpMethod='OPTIONS',
                statusCode='200',
                responseParameters={
                    'method.response.header.Access-Control-Allow-Headers': "'Content-Type,Authorization,X-Amz-Date,X-Api-Key,X-Amz-Security-Token'",
                    'method.response.header.Access-Control-Allow-Methods': "'GET,POST,OPTIONS'",
                    'method.response.header.Access-Control-Allow-Origin': "'*'"
                }
            )
            print(f"    ✓ OPTIONS 메서드 추가")
        except apigateway.exceptions.ConflictException:
            print(f"    ✓ OPTIONS 메서드 이미 존재")
    
    # API 배포
    print("\n" + "="*60)
    print("API 배포 중...")
    try:
        apigateway.create_deployment(
            restApiId=API_ID,
            stageName='prod',
            description='누락된 메서드 추가'
        )
        print("✓ API 배포 완료")
    except Exception as e:
        print(f"✗ API 배포 실패: {str(e)}")
    
    print("\n" + "="*60)
    print("✓ 완료!")
    print("="*60)
    print(f"\nAPI URL: https://{API_ID}.execute-api.us-east-2.amazonaws.com/prod")
    print()

if __name__ == '__main__':
    main()

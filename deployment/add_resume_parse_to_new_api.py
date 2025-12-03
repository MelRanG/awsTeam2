"""
이력서 파싱 엔드포인트를 새 API Gateway에 추가
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
        return get_resource_id(f'/{path_part}') or get_resource_id(f'/resume/{path_part}')

def add_method_with_lambda(resource_id, http_method, lambda_name):
    """메서드 및 Lambda 통합 추가"""
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
    apigateway.put_integration(
        restApiId=API_ID,
        resourceId=resource_id,
        httpMethod=http_method,
        type='AWS_PROXY',
        integrationHttpMethod='POST',
        uri=f'arn:aws:apigateway:{REGION}:lambda:path/2015-03-31/functions/{lambda_arn}/invocations'
    )
    print(f"  ✓ Lambda 통합 완료: {lambda_name}")
    
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

def add_cors(resource_id, methods):
    """CORS OPTIONS 메서드 추가"""
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
                'method.response.header.Access-Control-Allow-Methods': f"'{','.join(methods)},OPTIONS'",
                'method.response.header.Access-Control-Allow-Origin': "'*'"
            }
        )
        print(f"  ✓ CORS 설정 완료")
    except apigateway.exceptions.ConflictException:
        print(f"  ✓ CORS 이미 존재")

def main():
    """메인 함수"""
    print("="*60)
    print("이력서 파싱 엔드포인트 추가")
    print("="*60)
    
    root_id = get_root_id()
    
    # 1. /resume 리소스 생성
    print("\n[1] /resume 리소스 생성")
    resume_id = get_resource_id('/resume')
    if not resume_id:
        resume_id = create_resource(root_id, 'resume')
    else:
        print("  ✓ /resume 리소스 이미 존재")
    
    # 2. /resume/upload-url 리소스 확인
    print("\n[2] /resume/upload-url 확인")
    upload_url_id = get_resource_id('/resume/upload-url')
    if upload_url_id:
        print("  ✓ /resume/upload-url 이미 존재")
        # POST 메서드 확인 및 Lambda 연결
        add_method_with_lambda(upload_url_id, 'POST', 'ResumeUploadURLGenerator')
        add_cors(upload_url_id, ['POST'])
    
    # 3. /resume/parse 리소스 생성
    print("\n[3] /resume/parse 리소스 생성")
    parse_id = create_resource(resume_id, 'parse')
    
    # 4. POST /resume/parse 메서드 추가
    print("\n[4] POST /resume/parse 메서드 추가")
    add_method_with_lambda(parse_id, 'POST', 'ResumeParser')
    
    # 5. CORS 추가
    print("\n[5] CORS 설정")
    add_cors(parse_id, ['POST'])
    
    # API 배포
    print("\n" + "="*60)
    print("API 배포 중...")
    try:
        apigateway.create_deployment(
            restApiId=API_ID,
            stageName='prod',
            description='이력서 파싱 엔드포인트 추가'
        )
        print("✓ API 배포 완료")
    except Exception as e:
        print(f"✗ API 배포 실패: {str(e)}")
    
    print("\n" + "="*60)
    print("✓ 완료!")
    print("="*60)
    print(f"\nAPI URL: https://{API_ID}.execute-api.us-east-2.amazonaws.com/prod")
    print("엔드포인트:")
    print("  - POST /resume/upload-url")
    print("  - POST /resume/parse")
    print()

if __name__ == '__main__':
    main()

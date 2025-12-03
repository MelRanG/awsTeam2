"""
/resume/upload-url 엔드포인트 추가
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

def create_resource(parent_id, path_part):
    """리소스 생성"""
    try:
        response = apigateway.create_resource(
            restApiId=API_ID,
            parentId=parent_id,
            pathPart=path_part
        )
        print(f"  ✓ 리소스 생성: {path_part}")
        return response['id']
    except apigateway.exceptions.ConflictException:
        print(f"  ✓ 리소스 이미 존재: {path_part}")
        # 기존 리소스 ID 찾기
        resources = apigateway.get_resources(restApiId=API_ID)['items']
        for resource in resources:
            if resource.get('pathPart') == path_part and resource.get('parentId') == parent_id:
                return resource['id']
        return None

def add_method_with_lambda(resource_id, http_method, lambda_name):
    """메서드 및 Lambda 통합 추가"""
    lambda_arn = f'arn:aws:lambda:{REGION}:{ACCOUNT_ID}:function:{lambda_name}'
    
    try:
        apigateway.put_method(
            restApiId=API_ID,
            resourceId=resource_id,
            httpMethod=http_method,
            authorizationType='NONE'
        )
        print(f"  ✓ {http_method} 메서드 생성")
    except apigateway.exceptions.ConflictException:
        print(f"  ✓ {http_method} 메서드 이미 존재")
    
    apigateway.put_integration(
        restApiId=API_ID,
        resourceId=resource_id,
        httpMethod=http_method,
        type='AWS_PROXY',
        integrationHttpMethod='POST',
        uri=f'arn:aws:apigateway:{REGION}:lambda:path/2015-03-31/functions/{lambda_arn}/invocations'
    )
    print(f"  ✓ Lambda 통합 완료: {lambda_name}")
    
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
    print("/resume/upload-url 엔드포인트 추가")
    print("="*60)
    
    # /resume 리소스 ID 가져오기
    resume_id = get_resource_id('/resume')
    if not resume_id:
        print("✗ /resume 리소스가 없습니다")
        return
    
    print(f"✓ /resume 리소스 ID: {resume_id}")
    
    # /resume/upload-url 리소스 생성
    print("\n[1] /resume/upload-url 리소스 생성")
    upload_url_id = create_resource(resume_id, 'upload-url')
    
    if not upload_url_id:
        print("✗ 리소스 생성 실패")
        return
    
    # POST 메서드 추가
    print("\n[2] POST /resume/upload-url 메서드 추가")
    add_method_with_lambda(upload_url_id, 'POST', 'ResumeUploadURLGenerator')
    
    # CORS 추가
    print("\n[3] CORS 설정")
    add_cors(upload_url_id, ['POST'])
    
    # API 배포
    print("\n" + "="*60)
    print("API 배포 중...")
    try:
        apigateway.create_deployment(
            restApiId=API_ID,
            stageName='prod',
            description='/resume/upload-url 추가'
        )
        print("✓ API 배포 완료")
    except Exception as e:
        print(f"✗ API 배포 실패: {str(e)}")
    
    print("\n" + "="*60)
    print("✓ 완료!")
    print("="*60)
    print(f"\nAPI URL: https://{API_ID}.execute-api.us-east-2.amazonaws.com/prod")
    print("  - POST /resume/upload-url")
    print("  - POST /resume/parse")
    print()

if __name__ == '__main__':
    main()

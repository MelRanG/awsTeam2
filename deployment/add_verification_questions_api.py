"""
이력서 검증 질문 API 추가
"""
import boto3
import zipfile
import os
from pathlib import Path

lambda_client = boto3.client('lambda', region_name='us-east-2')
apigateway = boto3.client('apigateway', region_name='us-east-2')
iam = boto3.client('iam', region_name='us-east-2')

API_ID = 'ifeniowvpb'
ACCOUNT_ID = '412677576136'
REGION = 'us-east-2'
LAMBDA_ROLE_ARN = 'arn:aws:iam::412677576136:role/LambdaExecutionRole-Team2'

def create_lambda_zip():
    """Lambda 함수 ZIP 파일 생성"""
    zip_path = 'resume_verification_questions.zip'
    lambda_dir = Path('lambda_functions/resume_verification_questions')
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        index_file = lambda_dir / 'index.py'
        if index_file.exists():
            zipf.write(index_file, 'index.py')
    
    return zip_path

def create_or_update_lambda():
    """Lambda 함수 생성 또는 업데이트"""
    print("\n[1] Lambda 함수 생성/업데이트")
    
    zip_path = create_lambda_zip()
    
    with open(zip_path, 'rb') as f:
        zip_content = f.read()
    
    function_name = 'ResumeVerificationQuestions'
    
    try:
        # 기존 함수 확인
        lambda_client.get_function(FunctionName=function_name)
        print(f"  ✓ 기존 함수 발견, 코드 업데이트 중...")
        
        lambda_client.update_function_code(
            FunctionName=function_name,
            ZipFile=zip_content
        )
        print(f"  ✓ 함수 코드 업데이트 완료")
        
    except lambda_client.exceptions.ResourceNotFoundException:
        print(f"  ✓ 새 함수 생성 중...")
        
        lambda_client.create_function(
            FunctionName=function_name,
            Runtime='python3.11',
            Role=LAMBDA_ROLE_ARN,
            Handler='index.lambda_handler',
            Code={'ZipFile': zip_content},
            Timeout=60,
            MemorySize=512,
            Tags={
                'Team': 'Team2',
                'EmployeeID': '524956',
                'Project': 'HR-Resource-Optimization'
            }
        )
        print(f"  ✓ 함수 생성 완료")
    
    # ZIP 파일 삭제
    os.remove(zip_path)
    
    return f'arn:aws:lambda:{REGION}:{ACCOUNT_ID}:function:{function_name}'

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
        resources = apigateway.get_resources(restApiId=API_ID)['items']
        for resource in resources:
            if resource.get('pathPart') == path_part and resource.get('parentId') == parent_id:
                return resource['id']
        return None

def add_method_with_lambda(resource_id, http_method, lambda_arn):
    """메서드 및 Lambda 통합 추가"""
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
    print(f"  ✓ Lambda 통합 완료")
    
    try:
        lambda_client.add_permission(
            FunctionName='ResumeVerificationQuestions',
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
    print("이력서 검증 질문 API 추가")
    print("="*60)
    
    # 1. Lambda 함수 생성
    lambda_arn = create_or_update_lambda()
    
    # 2. /resume 리소스 ID 가져오기
    print("\n[2] API Gateway 리소스 설정")
    resume_id = get_resource_id('/resume')
    if not resume_id:
        print("  ✗ /resume 리소스가 없습니다")
        return
    
    print(f"  ✓ /resume 리소스 ID: {resume_id}")
    
    # 3. /resume/verification-questions 리소스 생성
    print("\n[3] /resume/verification-questions 리소스 생성")
    verification_id = create_resource(resume_id, 'verification-questions')
    
    if not verification_id:
        print("  ✗ 리소스 생성 실패")
        return
    
    # 4. POST 메서드 추가
    print("\n[4] POST /resume/verification-questions 메서드 추가")
    add_method_with_lambda(verification_id, 'POST', lambda_arn)
    
    # 5. CORS 추가
    print("\n[5] CORS 설정")
    add_cors(verification_id, ['POST'])
    
    # 6. API 배포
    print("\n[6] API 배포")
    try:
        apigateway.create_deployment(
            restApiId=API_ID,
            stageName='prod',
            description='이력서 검증 질문 API 추가'
        )
        print("  ✓ API 배포 완료")
    except Exception as e:
        print(f"  ✗ API 배포 실패: {str(e)}")
    
    print("\n" + "="*60)
    print("✓ 완료!")
    print("="*60)
    print(f"\nAPI URL: https://{API_ID}.execute-api.us-east-2.amazonaws.com/prod")
    print("  - POST /resume/verification-questions")
    print()

if __name__ == '__main__':
    main()

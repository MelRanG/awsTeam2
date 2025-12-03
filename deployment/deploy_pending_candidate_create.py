"""
대기자 생성 Lambda 배포 및 API Gateway 연결
"""
import boto3
import zipfile
import os
import json

lambda_client = boto3.client('lambda', region_name='us-east-2')
apigateway = boto3.client('apigateway', region_name='us-east-2')
iam = boto3.client('iam')

print("="*60)
print("대기자 생성 Lambda 배포")
print("="*60)

# 1. Lambda 함수 패키징
print("\n1. Lambda 함수 패키징...")
zip_path = 'pending_candidate_create.zip'

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipf.write(
        'lambda_functions/pending_candidate_create/index.py',
        'index.py'
    )

print(f"✅ 패키징 완료: {zip_path}")

# 2. Lambda 함수 생성 또는 업데이트
print("\n2. Lambda 함수 배포...")
function_name = 'PendingCandidateCreate'

with open(zip_path, 'rb') as f:
    zip_content = f.read()

try:
    # 기존 함수 업데이트
    lambda_client.update_function_code(
        FunctionName=function_name,
        ZipFile=zip_content
    )
    print(f"✅ Lambda 함수 업데이트 완료: {function_name}")
except lambda_client.exceptions.ResourceNotFoundException:
    # 새 함수 생성
    lambda_client.create_function(
        FunctionName=function_name,
        Runtime='python3.11',
        Role='arn:aws:iam::412677576136:role/LabRole',
        Handler='index.lambda_handler',
        Code={'ZipFile': zip_content},
        Timeout=30,
        MemorySize=256,
        Environment={
            'Variables': {}
        }
    )
    print(f"✅ Lambda 함수 생성 완료: {function_name}")

# 3. API Gateway 연결
print("\n3. API Gateway 연결...")

# API Gateway ID 찾기
apis = apigateway.get_rest_apis()
api_id = None
for api in apis['items']:
    if 'hr-resource-optimization' in api['name'].lower():
        api_id = api['id']
        break

if not api_id:
    print("❌ API Gateway를 찾을 수 없습니다")
    exit(1)

print(f"✅ API Gateway ID: {api_id}")

# /pending-candidates 리소스 찾기 또는 생성
resources = apigateway.get_resources(restApiId=api_id, limit=500)
root_id = None
pending_resource = None

for resource in resources['items']:
    if resource['path'] == '/':
        root_id = resource['id']
    elif resource['path'] == '/pending-candidates':
        pending_resource = resource

if not pending_resource:
    print("\n/pending-candidates 리소스 생성...")
    pending_resource = apigateway.create_resource(
        restApiId=api_id,
        parentId=root_id,
        pathPart='pending-candidates'
    )
    print(f"✅ 리소스 생성 완료: {pending_resource['id']}")
else:
    print(f"✅ 기존 리소스 사용: {pending_resource['id']}")

resource_id = pending_resource['id']

# POST 메서드 생성 또는 업데이트
try:
    apigateway.put_method(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod='POST',
        authorizationType='NONE'
    )
    print("✅ POST 메서드 생성")
except:
    print("✅ POST 메서드 이미 존재")

# Lambda 통합 설정
lambda_arn = f"arn:aws:lambda:us-east-2:412677576136:function:{function_name}"

apigateway.put_integration(
    restApiId=api_id,
    resourceId=resource_id,
    httpMethod='POST',
    type='AWS_PROXY',
    integrationHttpMethod='POST',
    uri=f"arn:aws:apigateway:us-east-2:lambda:path/2015-03-31/functions/{lambda_arn}/invocations"
)
print("✅ Lambda 통합 완료")

# Lambda 권한 추가
try:
    lambda_client.add_permission(
        FunctionName=function_name,
        StatementId=f'apigateway-{api_id}-POST',
        Action='lambda:InvokeFunction',
        Principal='apigateway.amazonaws.com',
        SourceArn=f"arn:aws:execute-api:us-east-2:412677576136:{api_id}/*/*"
    )
    print("✅ Lambda 권한 추가")
except lambda_client.exceptions.ResourceConflictException:
    print("✅ Lambda 권한 이미 존재")

# OPTIONS 메서드 (CORS)
try:
    apigateway.put_method(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod='OPTIONS',
        authorizationType='NONE'
    )
except:
    pass

apigateway.put_integration(
    restApiId=api_id,
    resourceId=resource_id,
    httpMethod='OPTIONS',
    type='MOCK',
    requestTemplates={'application/json': '{"statusCode": 200}'}
)

apigateway.put_method_response(
    restApiId=api_id,
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
    restApiId=api_id,
    resourceId=resource_id,
    httpMethod='OPTIONS',
    statusCode='200',
    responseParameters={
        'method.response.header.Access-Control-Allow-Headers': "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'",
        'method.response.header.Access-Control-Allow-Methods': "'GET,POST,OPTIONS,DELETE'",
        'method.response.header.Access-Control-Allow-Origin': "'*'"
    }
)

print("✅ CORS 설정 완료")

# 4. API 배포
print("\n4. API 배포...")
apigateway.create_deployment(
    restApiId=api_id,
    stageName='prod'
)
print("✅ API 배포 완료")

# 정리
os.remove(zip_path)

print("\n" + "="*60)
print("배포 완료!")
print("="*60)
print(f"\nAPI 엔드포인트: POST https://{api_id}.execute-api.us-east-2.amazonaws.com/prod/pending-candidates")

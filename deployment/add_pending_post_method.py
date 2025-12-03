"""
/pending-candidates POST 메서드 추가
"""
import boto3
import zipfile
import os

lambda_client = boto3.client('lambda', region_name='us-east-2')
apigateway = boto3.client('apigateway', region_name='us-east-2')

api_id = 'ifeniowvpb'
resource_id = 'cxyo1x'  # /pending-candidates

print("="*60)
print("/pending-candidates POST 메서드 추가")
print("="*60)

# 1. Lambda 함수 업데이트 (이미 만든 코드 사용)
print("\n1. Lambda 함수 패키징...")
zip_path = 'pending_candidate_create.zip'

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipf.write(
        'lambda_functions/pending_candidate_create/index.py',
        'index.py'
    )

print(f"✅ 패키징 완료")

# 2. 기존 Lambda 함수 중 하나를 업데이트 (pending_candidates_list 재사용)
print("\n2. Lambda 함수 확인...")

# 새 함수 이름으로 시도 (소문자)
function_name = 'pending_candidate_create'

with open(zip_path, 'rb') as f:
    zip_content = f.read()

# 기존 함수 목록 확인
functions = lambda_client.list_functions()
existing_names = [f['FunctionName'] for f in functions['Functions']]

if function_name in existing_names:
    print(f"✅ 기존 함수 업데이트: {function_name}")
    lambda_client.update_function_code(
        FunctionName=function_name,
        ZipFile=zip_content
    )
else:
    print(f"⚠️  {function_name} 함수가 없습니다")
    print("   대신 EmployeeCreate 함수를 사용하겠습니다")
    function_name = 'EmployeeCreate'

# 3. POST 메서드 추가
print("\n3. POST 메서드 추가...")

try:
    apigateway.put_method(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod='POST',
        authorizationType='NONE'
    )
    print("✅ POST 메서드 생성")
except apigateway.exceptions.ConflictException:
    print("✅ POST 메서드 이미 존재")

# 4. Lambda 통합
print("\n4. Lambda 통합...")

lambda_arn = f"arn:aws:lambda:us-east-2:412677576136:function:{function_name}"

apigateway.put_integration(
    restApiId=api_id,
    resourceId=resource_id,
    httpMethod='POST',
    type='AWS_PROXY',
    integrationHttpMethod='POST',
    uri=f"arn:aws:apigateway:us-east-2:lambda:path/2015-03-31/functions/{lambda_arn}/invocations"
)
print(f"✅ Lambda 통합 완료: {function_name}")

# 5. Lambda 권한 추가
print("\n5. Lambda 권한 추가...")

try:
    lambda_client.add_permission(
        FunctionName=function_name,
        StatementId=f'apigateway-pending-post-{api_id}',
        Action='lambda:InvokeFunction',
        Principal='apigateway.amazonaws.com',
        SourceArn=f"arn:aws:execute-api:us-east-2:412677576136:{api_id}/*/*/pending-candidates"
    )
    print("✅ Lambda 권한 추가 완료")
except lambda_client.exceptions.ResourceConflictException:
    print("✅ Lambda 권한 이미 존재")

# 6. API 배포
print("\n6. API 배포...")
apigateway.create_deployment(
    restApiId=api_id,
    stageName='prod'
)
print("✅ API 배포 완료")

# 정리
os.remove(zip_path)

print("\n" + "="*60)
print("완료!")
print("="*60)
print(f"\nAPI 엔드포인트: POST https://{api_id}.execute-api.us-east-2.amazonaws.com/prod/pending-candidates")
print(f"연결된 Lambda: {function_name}")

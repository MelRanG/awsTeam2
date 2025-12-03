"""
/employee-evaluation API 추가
"""
import boto3

lambda_client = boto3.client('lambda', region_name='us-east-2')
apigateway = boto3.client('apigateway', region_name='us-east-2')

api_id = 'ifeniowvpb'
function_name = 'EmployeeEvaluation'

print("="*60)
print("/employee-evaluation API 추가")
print("="*60)

# 1. 루트 리소스 찾기
resources = apigateway.get_resources(restApiId=api_id, limit=500)
root_id = None

for resource in resources['items']:
    if resource['path'] == '/':
        root_id = resource['id']
        break

print(f"✅ 루트 리소스 ID: {root_id}")

# 2. /employee-evaluation 리소스 생성
print("\n/employee-evaluation 리소스 생성...")

eval_resource = apigateway.create_resource(
    restApiId=api_id,
    parentId=root_id,
    pathPart='employee-evaluation'
)

resource_id = eval_resource['id']
print(f"✅ 리소스 생성 완료: {resource_id}")

# 3. POST 메서드 추가
print("\nPOST 메서드 추가...")

apigateway.put_method(
    restApiId=api_id,
    resourceId=resource_id,
    httpMethod='POST',
    authorizationType='NONE'
)
print("✅ POST 메서드 생성")

# 4. Lambda 통합
print("\nLambda 통합...")

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
print("\nLambda 권한 추가...")

try:
    lambda_client.add_permission(
        FunctionName=function_name,
        StatementId=f'apigateway-{api_id}-employee-eval',
        Action='lambda:InvokeFunction',
        Principal='apigateway.amazonaws.com',
        SourceArn=f"arn:aws:execute-api:us-east-2:412677576136:{api_id}/*/*/employee-evaluation"
    )
    print("✅ Lambda 권한 추가 완료")
except lambda_client.exceptions.ResourceConflictException:
    print("✅ Lambda 권한 이미 존재")

# 6. OPTIONS 메서드 (CORS)
print("\nCORS 설정...")

apigateway.put_method(
    restApiId=api_id,
    resourceId=resource_id,
    httpMethod='OPTIONS',
    authorizationType='NONE'
)

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
        'method.response.header.Access-Control-Allow-Methods': "'GET,POST,PUT,DELETE,OPTIONS'",
        'method.response.header.Access-Control-Allow-Origin': "'*'"
    }
)
print("✅ CORS 설정 완료")

# 7. API 배포
print("\nAPI 배포...")
apigateway.create_deployment(
    restApiId=api_id,
    stageName='prod'
)
print("✅ API 배포 완료")

print("\n" + "="*60)
print("완료!")
print("="*60)
print(f"\nAPI 엔드포인트: POST https://{api_id}.execute-api.us-east-2.amazonaws.com/prod/employee-evaluation")

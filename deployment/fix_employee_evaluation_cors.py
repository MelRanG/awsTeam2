"""
employee-evaluation API CORS 수정
"""
import boto3

apigateway = boto3.client('apigateway', region_name='us-east-2')
api_id = 'ifeniowvpb'

print("="*60)
print("/employee-evaluation CORS 수정")
print("="*60)

# 리소스 찾기
resources = apigateway.get_resources(restApiId=api_id, limit=500)

eval_resource = None
for resource in resources['items']:
    if resource['path'] == '/employee-evaluation':
        eval_resource = resource
        break

if not eval_resource:
    print("❌ /employee-evaluation 리소스를 찾을 수 없습니다")
    exit(1)

resource_id = eval_resource['id']
print(f"✅ 리소스 ID: {resource_id}")

# OPTIONS 메서드 추가/업데이트
print("\nOPTIONS 메서드 설정...")

try:
    apigateway.put_method(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod='OPTIONS',
        authorizationType='NONE'
    )
    print("✅ OPTIONS 메서드 생성")
except:
    print("✅ OPTIONS 메서드 이미 존재")

# MOCK 통합
apigateway.put_integration(
    restApiId=api_id,
    resourceId=resource_id,
    httpMethod='OPTIONS',
    type='MOCK',
    requestTemplates={'application/json': '{"statusCode": 200}'}
)
print("✅ MOCK 통합 설정")

# 메서드 응답
try:
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
    print("✅ 메서드 응답 설정")
except:
    print("✅ 메서드 응답 이미 존재")

# 통합 응답
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
print("✅ 통합 응답 설정")

# API 배포
print("\nAPI 배포 중...")
apigateway.create_deployment(
    restApiId=api_id,
    stageName='prod'
)
print("✅ API 배포 완료")

print("\n" + "="*60)
print("CORS 설정 완료!")
print("="*60)

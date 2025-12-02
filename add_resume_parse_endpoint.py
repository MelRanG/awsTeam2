#!/usr/bin/env python3
"""API Gateway에 /resume/parse 엔드포인트 추가"""

import boto3
import json

apigateway = boto3.client('apigateway', region_name='us-east-2')
lambda_client = boto3.client('lambda', region_name='us-east-2')

# API Gateway ID
api_id = 'xoc7x1m6p8'
region = 'us-east-2'
account_id = '412677576136'

# Lambda 함수 - ResumeParser 사용
lambda_function_name = 'ResumeParser'
lambda_arn = f'arn:aws:lambda:{region}:{account_id}:function:{lambda_function_name}'

print("=" * 60)
print("API Gateway 엔드포인트 추가")
print("=" * 60)

try:
    # 1. /resume 리소스 찾기
    print("\n1. /resume 리소스 찾기...")
    resources = apigateway.get_resources(restApiId=api_id)
    
    resume_resource_id = None
    for resource in resources['items']:
        if resource['path'] == '/resume':
            resume_resource_id = resource['id']
            print(f"✓ /resume 리소스 찾음: {resume_resource_id}")
            break
    
    if not resume_resource_id:
        print("✗ /resume 리소스를 찾을 수 없습니다")
        exit(1)
    
    # 2. /resume/parse 리소스 생성 또는 찾기
    print("\n2. /resume/parse 리소스 확인...")
    parse_resource_id = None
    
    for resource in resources['items']:
        if resource['path'] == '/resume/parse':
            parse_resource_id = resource['id']
            print(f"✓ /resume/parse 리소스 이미 존재: {parse_resource_id}")
            break
    
    if not parse_resource_id:
        print("새 리소스 생성 중...")
        response = apigateway.create_resource(
            restApiId=api_id,
            parentId=resume_resource_id,
            pathPart='parse'
        )
        parse_resource_id = response['id']
        print(f"✓ /resume/parse 리소스 생성 완료: {parse_resource_id}")
    
    # 3. POST 메서드 추가
    print("\n3. POST 메서드 추가...")
    try:
        apigateway.put_method(
            restApiId=api_id,
            resourceId=parse_resource_id,
            httpMethod='POST',
            authorizationType='NONE'
        )
        print("✓ POST 메서드 추가 완료")
    except apigateway.exceptions.ConflictException:
        print("✓ POST 메서드 이미 존재")
    
    # 4. Lambda 통합 설정
    print("\n4. Lambda 통합 설정...")
    integration_uri = f'arn:aws:apigateway:{region}:lambda:path/2015-03-31/functions/{lambda_arn}/invocations'
    
    apigateway.put_integration(
        restApiId=api_id,
        resourceId=parse_resource_id,
        httpMethod='POST',
        type='AWS_PROXY',
        integrationHttpMethod='POST',
        uri=integration_uri
    )
    print("✓ Lambda 통합 완료")
    
    # 5. Lambda 권한 추가
    print("\n5. Lambda 실행 권한 추가...")
    statement_id = f'apigateway-{api_id}-resume-parse'
    
    try:
        lambda_client.add_permission(
            FunctionName=lambda_function_name,
            StatementId=statement_id,
            Action='lambda:InvokeFunction',
            Principal='apigateway.amazonaws.com',
            SourceArn=f'arn:aws:execute-api:{region}:{account_id}:{api_id}/*/POST/resume/parse'
        )
        print("✓ Lambda 권한 추가 완료")
    except lambda_client.exceptions.ResourceConflictException:
        print("✓ Lambda 권한 이미 존재")
    
    # 6. OPTIONS 메서드 추가 (CORS)
    print("\n6. OPTIONS 메서드 추가 (CORS)...")
    try:
        apigateway.put_method(
            restApiId=api_id,
            resourceId=parse_resource_id,
            httpMethod='OPTIONS',
            authorizationType='NONE'
        )
        
        apigateway.put_integration(
            restApiId=api_id,
            resourceId=parse_resource_id,
            httpMethod='OPTIONS',
            type='MOCK',
            requestTemplates={
                'application/json': '{"statusCode": 200}'
            }
        )
        
        apigateway.put_method_response(
            restApiId=api_id,
            resourceId=parse_resource_id,
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
            resourceId=parse_resource_id,
            httpMethod='OPTIONS',
            statusCode='200',
            responseParameters={
                'method.response.header.Access-Control-Allow-Headers': "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'",
                'method.response.header.Access-Control-Allow-Methods': "'POST,OPTIONS'",
                'method.response.header.Access-Control-Allow-Origin': "'*'"
            }
        )
        print("✓ CORS 설정 완료")
    except Exception as e:
        print(f"CORS 설정: {str(e)}")
    
    # 7. 배포
    print("\n7. API 배포 중...")
    apigateway.create_deployment(
        restApiId=api_id,
        stageName='prod'
    )
    print("✓ 배포 완료")
    
    print("\n" + "=" * 60)
    print("✅ 엔드포인트 추가 완료!")
    print("=" * 60)
    print(f"\nURL: https://{api_id}.execute-api.{region}.amazonaws.com/prod/resume/parse")
    
except Exception as e:
    print(f"\n✗ 에러: {str(e)}")
    import traceback
    traceback.print_exc()

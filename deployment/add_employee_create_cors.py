#!/usr/bin/env python3
"""
employee-create API에 CORS 설정 추가
"""
import boto3
import json

def add_cors_to_employee_create():
    """employee-create API에 CORS 설정 추가"""
    client = boto3.client('apigateway', region_name='us-east-2')
    
    # API Gateway ID
    api_id = 'xoc7x1m6p8'
    
    print("=" * 60)
    print("employee-create API에 CORS 설정 추가")
    print("=" * 60)
    
    try:
        # 1. /employee-create 리소스 찾기
        print("\n1. 리소스 검색 중...")
        resources = client.get_resources(restApiId=api_id)
        
        employee_create_resource = None
        for resource in resources['items']:
            if resource['path'] == '/employee-create':
                employee_create_resource = resource
                print(f"  ✓ /employee-create 리소스 발견: {resource['id']}")
                break
        
        if not employee_create_resource:
            print("  ✗ /employee-create 리소스를 찾을 수 없습니다")
            return False
        
        resource_id = employee_create_resource['id']
        
        # 2. OPTIONS 메서드 추가 (이미 있으면 스킵)
        print("\n2. OPTIONS 메서드 확인 중...")
        try:
            client.get_method(
                restApiId=api_id,
                resourceId=resource_id,
                httpMethod='OPTIONS'
            )
            print("  ✓ OPTIONS 메서드가 이미 존재합니다")
        except client.exceptions.NotFoundException:
            print("  → OPTIONS 메서드 생성 중...")
            client.put_method(
                restApiId=api_id,
                resourceId=resource_id,
                httpMethod='OPTIONS',
                authorizationType='NONE'
            )
            print("  ✓ OPTIONS 메서드 생성 완료")
        
        # 3. OPTIONS 메서드 응답 설정
        print("\n3. OPTIONS 메서드 응답 설정 중...")
        
        # Method Response 설정
        try:
            client.put_method_response(
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
            print("  ✓ Method Response 설정 완료")
        except Exception as e:
            print(f"  → Method Response 이미 존재: {str(e)}")
        
        # Integration 설정 (MOCK)
        try:
            client.put_integration(
                restApiId=api_id,
                resourceId=resource_id,
                httpMethod='OPTIONS',
                type='MOCK',
                requestTemplates={
                    'application/json': '{"statusCode": 200}'
                }
            )
            print("  ✓ Integration 설정 완료")
        except Exception as e:
            print(f"  → Integration 이미 존재: {str(e)}")
        
        # Integration Response 설정
        try:
            client.put_integration_response(
                restApiId=api_id,
                resourceId=resource_id,
                httpMethod='OPTIONS',
                statusCode='200',
                responseParameters={
                    'method.response.header.Access-Control-Allow-Headers': "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'",
                    'method.response.header.Access-Control-Allow-Methods': "'POST,OPTIONS'",
                    'method.response.header.Access-Control-Allow-Origin': "'*'"
                },
                responseTemplates={
                    'application/json': ''
                }
            )
            print("  ✓ Integration Response 설정 완료")
        except Exception as e:
            print(f"  → Integration Response 이미 존재: {str(e)}")
        
        # 4. POST 메서드에도 CORS 헤더 추가
        print("\n4. POST 메서드 응답에 CORS 헤더 추가 중...")
        try:
            # 200 응답
            client.put_method_response(
                restApiId=api_id,
                resourceId=resource_id,
                httpMethod='POST',
                statusCode='200',
                responseParameters={
                    'method.response.header.Access-Control-Allow-Origin': True
                }
            )
            print("  ✓ POST 200 응답 헤더 추가")
        except Exception as e:
            print(f"  → POST 200 응답 헤더 이미 존재")
        
        try:
            # 201 응답
            client.put_method_response(
                restApiId=api_id,
                resourceId=resource_id,
                httpMethod='POST',
                statusCode='201',
                responseParameters={
                    'method.response.header.Access-Control-Allow-Origin': True
                }
            )
            print("  ✓ POST 201 응답 헤더 추가")
        except Exception as e:
            print(f"  → POST 201 응답 헤더 이미 존재")
        
        # Integration Response에도 CORS 헤더 추가
        try:
            client.put_integration_response(
                restApiId=api_id,
                resourceId=resource_id,
                httpMethod='POST',
                statusCode='200',
                responseParameters={
                    'method.response.header.Access-Control-Allow-Origin': "'*'"
                }
            )
            print("  ✓ POST Integration Response 200 헤더 추가")
        except Exception as e:
            print(f"  → POST Integration Response 200 헤더 설정 중 에러: {str(e)}")
        
        try:
            client.put_integration_response(
                restApiId=api_id,
                resourceId=resource_id,
                httpMethod='POST',
                statusCode='201',
                responseParameters={
                    'method.response.header.Access-Control-Allow-Origin': "'*'"
                }
            )
            print("  ✓ POST Integration Response 201 헤더 추가")
        except Exception as e:
            print(f"  → POST Integration Response 201 헤더 설정 중 에러: {str(e)}")
        
        # 5. API 배포
        print("\n5. API 배포 중...")
        client.create_deployment(
            restApiId=api_id,
            stageName='prod',
            description='employee-create CORS 설정 추가'
        )
        print("  ✓ API 배포 완료")
        
        print("\n" + "=" * 60)
        print("✅ CORS 설정이 완료되었습니다!")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n❌ 에러 발생: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    add_cors_to_employee_create()

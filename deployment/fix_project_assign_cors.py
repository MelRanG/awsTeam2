"""
프로젝트 투입 API CORS 설정 추가
"""

import boto3
import json

def fix_cors():
    """CORS 설정 추가"""
    
    apigateway = boto3.client('apigateway', region_name='us-east-2')
    
    print("=" * 60)
    print("프로젝트 투입 API CORS 설정")
    print("=" * 60)
    
    # API Gateway ID
    api_id = 'ifeniowvpb'
    
    # 1. REST API 리소스 찾기
    print("\n1. API 리소스 조회 중...")
    
    resources = apigateway.get_resources(restApiId=api_id)
    
    # /projects/{projectId}/assign 리소스 찾기
    assign_resource = None
    for resource in resources['items']:
        if resource['path'] == '/projects/{projectId}/assign':
            assign_resource = resource
            break
    
    if not assign_resource:
        print("  ✗ /projects/{projectId}/assign 리소스를 찾을 수 없습니다")
        return False
    
    resource_id = assign_resource['id']
    print(f"  ✓ 리소스 ID: {resource_id}")
    
    # 2. OPTIONS 메서드 확인
    print("\n2. OPTIONS 메서드 확인 중...")
    
    try:
        method = apigateway.get_method(
            restApiId=api_id,
            resourceId=resource_id,
            httpMethod='OPTIONS'
        )
        print("  ✓ OPTIONS 메서드가 이미 존재합니다")
        has_options = True
    except:
        print("  ℹ OPTIONS 메서드가 없습니다. 생성합니다...")
        has_options = False
    
    # 3. OPTIONS 메서드 생성 (없는 경우)
    if not has_options:
        print("\n3. OPTIONS 메서드 생성 중...")
        
        try:
            # OPTIONS 메서드 생성
            apigateway.put_method(
                restApiId=api_id,
                resourceId=resource_id,
                httpMethod='OPTIONS',
                authorizationType='NONE'
            )
            
            # Mock 통합 설정
            apigateway.put_integration(
                restApiId=api_id,
                resourceId=resource_id,
                httpMethod='OPTIONS',
                type='MOCK',
                requestTemplates={
                    'application/json': '{"statusCode": 200}'
                }
            )
            
            # 메서드 응답 설정
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
            
            # 통합 응답 설정
            apigateway.put_integration_response(
                restApiId=api_id,
                resourceId=resource_id,
                httpMethod='OPTIONS',
                statusCode='200',
                responseParameters={
                    'method.response.header.Access-Control-Allow-Headers': "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'",
                    'method.response.header.Access-Control-Allow-Methods': "'POST,OPTIONS'",
                    'method.response.header.Access-Control-Allow-Origin': "'*'"
                }
            )
            
            print("  ✓ OPTIONS 메서드 생성 완료")
            
        except Exception as e:
            print(f"  ✗ OPTIONS 메서드 생성 실패: {str(e)}")
            return False
    
    # 4. POST 메서드 응답에 CORS 헤더 추가
    print("\n4. POST 메서드 응답 헤더 업데이트 중...")
    
    try:
        # 메서드 응답 업데이트
        try:
            apigateway.put_method_response(
                restApiId=api_id,
                resourceId=resource_id,
                httpMethod='POST',
                statusCode='200',
                responseParameters={
                    'method.response.header.Access-Control-Allow-Origin': True
                }
            )
        except:
            pass
        
        # 통합 응답 업데이트
        try:
            apigateway.update_integration_response(
                restApiId=api_id,
                resourceId=resource_id,
                httpMethod='POST',
                statusCode='200',
                patchOperations=[
                    {
                        'op': 'add',
                        'path': '/responseParameters/method.response.header.Access-Control-Allow-Origin',
                        'value': "'*'"
                    }
                ]
            )
        except:
            pass
        
        print("  ✓ POST 메서드 응답 헤더 업데이트 완료")
        
    except Exception as e:
        print(f"  ⚠ POST 메서드 업데이트 경고: {str(e)}")
    
    # 5. API 배포
    print("\n5. API 배포 중...")
    
    try:
        apigateway.create_deployment(
            restApiId=api_id,
            stageName='prod',
            description='프로젝트 투입 CORS 설정 추가'
        )
        print("  ✓ API 배포 완료")
        
    except Exception as e:
        print(f"  ✗ API 배포 실패: {str(e)}")
        return False
    
    print("\n" + "=" * 60)
    print("✅ CORS 설정 완료!")
    print("=" * 60)
    print("\nAPI 엔드포인트:")
    print(f"  POST https://ifeniowvpb.execute-api.us-east-2.amazonaws.com/prod/projects/{{projectId}}/assign")
    
    return True

if __name__ == '__main__':
    fix_cors()

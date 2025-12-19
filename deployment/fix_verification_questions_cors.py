import boto3
import json

# API Gateway 클라이언트 생성
client = boto3.client('apigateway', region_name='us-east-2')

# API Gateway ID
api_id = 'ifeniowvpb'

def add_cors_to_verification_questions():
    """검증 질문 API에 CORS 설정 추가"""
    
    print("=" * 60)
    print("검증 질문 API CORS 설정 추가")
    print("=" * 60)
    
    # 1. 리소스 찾기
    print("\n1. 리소스 찾기...")
    resources = client.get_resources(restApiId=api_id, limit=500)
    
    verification_resource = None
    for resource in resources['items']:
        if resource['path'] == '/resume/verification-questions':
            verification_resource = resource
            print(f"  ✓ 검증 질문 리소스 발견: {resource['id']}")
            break
    
    if not verification_resource:
        print("  ✗ 검증 질문 리소스를 찾을 수 없습니다!")
        return
    
    resource_id = verification_resource['id']
    
    # 2. OPTIONS 메서드 확인
    print("\n2. OPTIONS 메서드 확인...")
    try:
        client.get_method(
            restApiId=api_id,
            resourceId=resource_id,
            httpMethod='OPTIONS'
        )
        print("  ✓ OPTIONS 메서드가 이미 존재합니다")
    except client.exceptions.NotFoundException:
        print("  → OPTIONS 메서드 생성 중...")
        
        # OPTIONS 메서드 생성
        client.put_method(
            restApiId=api_id,
            resourceId=resource_id,
            httpMethod='OPTIONS',
            authorizationType='NONE'
        )
        
        # MOCK 통합 설정
        client.put_integration(
            restApiId=api_id,
            resourceId=resource_id,
            httpMethod='OPTIONS',
            type='MOCK',
            requestTemplates={
                'application/json': '{"statusCode": 200}'
            }
        )
        
        # 200 응답 설정
        client.put_method_response(
            restApiId=api_id,
            resourceId=resource_id,
            httpMethod='OPTIONS',
            statusCode='200',
            responseParameters={
                'method.response.header.Access-Control-Allow-Headers': False,
                'method.response.header.Access-Control-Allow-Methods': False,
                'method.response.header.Access-Control-Allow-Origin': False
            }
        )
        
        # 통합 응답 설정
        client.put_integration_response(
            restApiId=api_id,
            resourceId=resource_id,
            httpMethod='OPTIONS',
            statusCode='200',
            responseParameters={
                'method.response.header.Access-Control-Allow-Headers': "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'",
                'method.response.header.Access-Control-Allow-Methods': "'GET,POST,OPTIONS'",
                'method.response.header.Access-Control-Allow-Origin': "'*'"
            }
        )
        print("  ✓ OPTIONS 메서드 생성 완료")
    
    # 3. POST 메서드에 CORS 헤더 추가
    print("\n3. POST 메서드 CORS 헤더 추가...")
    try:
        # 먼저 기존 통합 응답 확인
        try:
            existing_response = client.get_integration_response(
                restApiId=api_id,
                resourceId=resource_id,
                httpMethod='POST',
                statusCode='200'
            )
            print(f"  → 기존 통합 응답 발견")
            
            # 기존 응답 삭제
            client.delete_integration_response(
                restApiId=api_id,
                resourceId=resource_id,
                httpMethod='POST',
                statusCode='200'
            )
            print(f"  → 기존 통합 응답 삭제")
        except:
            print(f"  → 기존 통합 응답 없음")
        
        # 메서드 응답 업데이트 (CORS 헤더 추가)
        try:
            # 기존 메서드 응답 삭제
            try:
                client.delete_method_response(
                    restApiId=api_id,
                    resourceId=resource_id,
                    httpMethod='POST',
                    statusCode='200'
                )
                print("  → 기존 메서드 응답 삭제")
            except:
                pass
            
            # 새 메서드 응답 생성
            client.put_method_response(
                restApiId=api_id,
                resourceId=resource_id,
                httpMethod='POST',
                statusCode='200',
                responseParameters={
                    'method.response.header.Access-Control-Allow-Origin': False
                }
            )
            print("  ✓ 메서드 응답 CORS 헤더 추가")
        except Exception as e:
            print(f"  → 메서드 응답 설정 중 오류: {e}")
        
        # 새로운 통합 응답 생성 (CORS 헤더 포함)
        client.put_integration_response(
            restApiId=api_id,
            resourceId=resource_id,
            httpMethod='POST',
            statusCode='200',
            responseParameters={
                'method.response.header.Access-Control-Allow-Origin': "'*'"
            },
            responseTemplates={
                'application/json': ''
            }
        )
        print("  ✓ POST 메서드 CORS 헤더 추가 완료")
    except Exception as e:
        print(f"  ⚠ POST 메서드 CORS 설정 중 오류: {e}")
    
    # 4. 배포
    print("\n4. API 배포 중...")
    client.create_deployment(
        restApiId=api_id,
        stageName='prod',
        description='검증 질문 API CORS 설정 추가'
    )
    print("  ✓ 배포 완료")
    
    print("\n" + "=" * 60)
    print("✅ CORS 설정 완료!")
    print("=" * 60)

if __name__ == '__main__':
    add_cors_to_verification_questions()

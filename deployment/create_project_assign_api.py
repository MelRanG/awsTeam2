"""
프로젝트 투입 API 생성
"""

import boto3
import json

def create_api():
    """프로젝트 투입 API 생성"""
    
    apigateway = boto3.client('apigateway', region_name='us-east-2')
    lambda_client = boto3.client('lambda', region_name='us-east-2')
    
    print("=" * 60)
    print("프로젝트 투입 API 생성")
    print("=" * 60)
    
    api_id = 'ifeniowvpb'
    region = 'us-east-2'
    account_id = '412677576136'
    
    # 1. 리소스 조회
    print("\n1. API 리소스 조회 중...")
    
    resources = apigateway.get_resources(restApiId=api_id)
    
    # /projects 리소스 찾기
    projects_resource = None
    for resource in resources['items']:
        if resource['path'] == '/projects':
            projects_resource = resource
            break
    
    if not projects_resource:
        print("  ✗ /projects 리소스를 찾을 수 없습니다")
        return False
    
    print(f"  ✓ /projects 리소스 ID: {projects_resource['id']}")
    
    # 2. {projectId} 리소스 확인/생성
    print("\n2. {projectId} 리소스 확인 중...")
    
    projectId_resource = None
    for resource in resources['items']:
        if resource['path'] == '/projects/{projectId}':
            projectId_resource = resource
            break
    
    if not projectId_resource:
        print("  ℹ {projectId} 리소스가 없습니다. 생성합니다...")
        
        try:
            projectId_resource = apigateway.create_resource(
                restApiId=api_id,
                parentId=projects_resource['id'],
                pathPart='{projectId}'
            )
            print(f"  ✓ {{projectId}} 리소스 생성 완료: {projectId_resource['id']}")
        except Exception as e:
            print(f"  ✗ {{projectId}} 리소스 생성 실패: {str(e)}")
            return False
    else:
        print(f"  ✓ {{projectId}} 리소스 ID: {projectId_resource['id']}")
    
    # 3. /assign 리소스 확인/생성
    print("\n3. /assign 리소스 확인 중...")
    
    assign_resource = None
    for resource in resources['items']:
        if resource['path'] == '/projects/{projectId}/assign':
            assign_resource = resource
            break
    
    if not assign_resource:
        print("  ℹ /assign 리소스가 없습니다. 생성합니다...")
        
        try:
            assign_resource = apigateway.create_resource(
                restApiId=api_id,
                parentId=projectId_resource['id'],
                pathPart='assign'
            )
            print(f"  ✓ /assign 리소스 생성 완료: {assign_resource['id']}")
        except Exception as e:
            print(f"  ✗ /assign 리소스 생성 실패: {str(e)}")
            return False
    else:
        print(f"  ✓ /assign 리소스 ID: {assign_resource['id']}")
    
    resource_id = assign_resource['id']
    
    # 4. POST 메서드 생성
    print("\n4. POST 메서드 생성 중...")
    
    try:
        # POST 메서드 생성
        apigateway.put_method(
            restApiId=api_id,
            resourceId=resource_id,
            httpMethod='POST',
            authorizationType='NONE'
        )
        print("  ✓ POST 메서드 생성 완료")
        
    except Exception as e:
        if 'ConflictException' in str(e):
            print("  ℹ POST 메서드가 이미 존재합니다")
        else:
            print(f"  ✗ POST 메서드 생성 실패: {str(e)}")
            return False
    
    # 5. Lambda 통합 설정
    print("\n5. Lambda 통합 설정 중...")
    
    lambda_arn = f'arn:aws:lambda:{region}:{account_id}:function:ProjectAssignment'
    
    try:
        apigateway.put_integration(
            restApiId=api_id,
            resourceId=resource_id,
            httpMethod='POST',
            type='AWS_PROXY',
            integrationHttpMethod='POST',
            uri=f'arn:aws:apigateway:{region}:lambda:path/2015-03-31/functions/{lambda_arn}/invocations'
        )
        print("  ✓ Lambda 통합 설정 완료")
        
    except Exception as e:
        print(f"  ✗ Lambda 통합 설정 실패: {str(e)}")
        return False
    
    # 6. Lambda 권한 추가
    print("\n6. Lambda 권한 추가 중...")
    
    try:
        lambda_client.add_permission(
            FunctionName='ProjectAssignment',
            StatementId=f'apigateway-project-assign-{resource_id}',
            Action='lambda:InvokeFunction',
            Principal='apigateway.amazonaws.com',
            SourceArn=f'arn:aws:execute-api:{region}:{account_id}:{api_id}/*/POST/projects/*/assign'
        )
        print("  ✓ Lambda 권한 추가 완료")
        
    except Exception as e:
        if 'ResourceConflictException' in str(e):
            print("  ℹ Lambda 권한이 이미 존재합니다")
        else:
            print(f"  ⚠ Lambda 권한 추가 경고: {str(e)}")
    
    # 7. OPTIONS 메서드 생성 (CORS)
    print("\n7. OPTIONS 메서드 생성 중...")
    
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
        if 'ConflictException' in str(e):
            print("  ℹ OPTIONS 메서드가 이미 존재합니다")
        else:
            print(f"  ⚠ OPTIONS 메서드 생성 경고: {str(e)}")
    
    # 8. API 배포
    print("\n8. API 배포 중...")
    
    try:
        apigateway.create_deployment(
            restApiId=api_id,
            stageName='prod',
            description='프로젝트 투입 API 생성'
        )
        print("  ✓ API 배포 완료")
        
    except Exception as e:
        print(f"  ✗ API 배포 실패: {str(e)}")
        return False
    
    print("\n" + "=" * 60)
    print("✅ 프로젝트 투입 API 생성 완료!")
    print("=" * 60)
    print("\nAPI 엔드포인트:")
    print(f"  POST https://{api_id}.execute-api.{region}.amazonaws.com/prod/projects/{{projectId}}/assign")
    print("\n요청 예시:")
    print("""  {
    "employee_id": "EMP-001",
    "role": "Backend Developer",
    "start_date": "2025-12-04",
    "end_date": "2026-06-02",
    "allocation_rate": 100,
    "assignment_reason": "AI 추천 기반"
  }""")
    
    return True

if __name__ == '__main__':
    create_api()

"""
pending-candidates API 엔드포인트 추가 스크립트
"""
import boto3
import json
import zipfile
import os
from pathlib import Path

# AWS 클라이언트 초기화
lambda_client = boto3.client('lambda', region_name='us-east-2')
apigateway = boto3.client('apigateway', region_name='us-east-2')
iam = boto3.client('iam', region_name='us-east-2')

# 설정
LAMBDA_ROLE_ARN = 'arn:aws:iam::412677576136:role/LambdaExecutionRole-Team2'
API_NAME = 'HR-Resource-Optimization-API'

def create_lambda_zip(function_name):
    """Lambda 함수 ZIP 파일 생성"""
    zip_path = f'{function_name}.zip'
    lambda_dir = Path(f'lambda_functions/{function_name}')
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        index_file = lambda_dir / 'index.py'
        if index_file.exists():
            zipf.write(index_file, 'index.py')
    
    return zip_path

def create_or_update_lambda(function_name, handler='index.lambda_handler'):
    """Lambda 함수 생성 또는 업데이트"""
    print(f"\n{'='*60}")
    print(f"Lambda 함수 처리: {function_name}")
    print(f"{'='*60}")
    
    zip_path = create_lambda_zip(function_name)
    
    with open(zip_path, 'rb') as f:
        zip_content = f.read()
    
    try:
        # 기존 함수 확인
        lambda_client.get_function(FunctionName=function_name)
        print(f"✓ 기존 함수 발견, 코드 업데이트 중...")
        
        response = lambda_client.update_function_code(
            FunctionName=function_name,
            ZipFile=zip_content
        )
        print(f"✓ 함수 코드 업데이트 완료")
        
    except lambda_client.exceptions.ResourceNotFoundException:
        print(f"✓ 새 함수 생성 중...")
        
        response = lambda_client.create_function(
            FunctionName=function_name,
            Runtime='python3.11',
            Role=LAMBDA_ROLE_ARN,
            Handler=handler,
            Code={'ZipFile': zip_content},
            Timeout=30,
            MemorySize=256,
            Tags={
                'Team': 'Team2',
                'EmployeeID': '524956',
                'Project': 'HR-Resource-Optimization'
            }
        )
        print(f"✓ 함수 생성 완료")
    
    # ZIP 파일 삭제
    os.remove(zip_path)
    
    return response['FunctionArn']

def get_api_id():
    """API Gateway ID 조회"""
    response = apigateway.get_rest_apis()
    for api in response['items']:
        if api['name'] == API_NAME:
            return api['id']
    raise Exception(f"API {API_NAME}를 찾을 수 없습니다")

def get_root_resource_id(api_id):
    """Root 리소스 ID 조회"""
    response = apigateway.get_resources(restApiId=api_id)
    for resource in response['items']:
        if resource['path'] == '/':
            return resource['id']
    raise Exception("Root 리소스를 찾을 수 없습니다")

def create_api_resource(api_id, parent_id, path_part):
    """API Gateway 리소스 생성"""
    try:
        # 기존 리소스 확인
        resources = apigateway.get_resources(restApiId=api_id)
        for resource in resources['items']:
            if resource.get('pathPart') == path_part and resource.get('parentId') == parent_id:
                print(f"✓ 기존 리소스 발견: /{path_part}")
                return resource['id']
        
        # 새 리소스 생성
        response = apigateway.create_resource(
            restApiId=api_id,
            parentId=parent_id,
            pathPart=path_part
        )
        print(f"✓ 리소스 생성 완료: /{path_part}")
        return response['id']
        
    except Exception as e:
        print(f"✗ 리소스 생성 실패: {str(e)}")
        raise

def create_api_method(api_id, resource_id, http_method, lambda_arn=None):
    """API Gateway 메서드 생성"""
    try:
        # 메서드 생성
        try:
            apigateway.put_method(
                restApiId=api_id,
                resourceId=resource_id,
                httpMethod=http_method,
                authorizationType='NONE'
            )
            print(f"✓ 메서드 생성: {http_method}")
        except apigateway.exceptions.ConflictException:
            print(f"✓ 메서드 이미 존재: {http_method}")
        
        if http_method == 'OPTIONS':
            # CORS OPTIONS 메서드 설정
            apigateway.put_integration(
                restApiId=api_id,
                resourceId=resource_id,
                httpMethod='OPTIONS',
                type='MOCK',
                requestTemplates={
                    'application/json': '{"statusCode": 200}'
                }
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
                    'method.response.header.Access-Control-Allow-Headers': "'Content-Type,Authorization'",
                    'method.response.header.Access-Control-Allow-Methods': "'GET,DELETE,OPTIONS'",
                    'method.response.header.Access-Control-Allow-Origin': "'*'"
                }
            )
            print(f"✓ CORS 설정 완료")
            
        elif lambda_arn:
            # Lambda 통합 설정
            apigateway.put_integration(
                restApiId=api_id,
                resourceId=resource_id,
                httpMethod=http_method,
                type='AWS_PROXY',
                integrationHttpMethod='POST',
                uri=f'arn:aws:apigateway:us-east-2:lambda:path/2015-03-31/functions/{lambda_arn}/invocations'
            )
            print(f"✓ Lambda 통합 완료")
            
            # Lambda 권한 추가
            function_name = lambda_arn.split(':')[-1]
            try:
                lambda_client.add_permission(
                    FunctionName=function_name,
                    StatementId=f'AllowAPIGateway{http_method}',
                    Action='lambda:InvokeFunction',
                    Principal='apigateway.amazonaws.com',
                    SourceArn=f'arn:aws:execute-api:us-east-2:412677576136:{api_id}/*/*'
                )
                print(f"✓ Lambda 권한 추가 완료")
            except lambda_client.exceptions.ResourceConflictException:
                print(f"✓ Lambda 권한 이미 존재")
                
    except Exception as e:
        print(f"✗ 메서드 생성 실패: {str(e)}")
        raise

def deploy_api(api_id):
    """API 배포"""
    try:
        apigateway.create_deployment(
            restApiId=api_id,
            stageName='prod',
            description='pending-candidates API 추가'
        )
        print(f"✓ API 배포 완료")
    except Exception as e:
        print(f"✗ API 배포 실패: {str(e)}")
        raise

def main():
    """메인 함수"""
    print("\n" + "="*60)
    print("pending-candidates API 엔드포인트 추가")
    print("="*60)
    
    # 1. Lambda 함수 생성
    print("\n[1단계] Lambda 함수 생성")
    list_lambda_arn = create_or_update_lambda('pending_candidates_list')
    delete_lambda_arn = create_or_update_lambda('pending_candidate_delete')
    
    # 2. API Gateway 설정
    print("\n[2단계] API Gateway 설정")
    api_id = get_api_id()
    print(f"✓ API ID: {api_id}")
    
    root_id = get_root_resource_id(api_id)
    print(f"✓ Root Resource ID: {root_id}")
    
    # 3. /pending-candidates 리소스 생성
    print("\n[3단계] /pending-candidates 리소스 생성")
    pending_candidates_id = create_api_resource(api_id, root_id, 'pending-candidates')
    
    # 4. GET /pending-candidates 메서드 생성
    print("\n[4단계] GET /pending-candidates 메서드 생성")
    create_api_method(api_id, pending_candidates_id, 'GET', list_lambda_arn)
    
    # 5. OPTIONS /pending-candidates 메서드 생성 (CORS)
    print("\n[5단계] OPTIONS /pending-candidates 메서드 생성")
    create_api_method(api_id, pending_candidates_id, 'OPTIONS')
    
    # 6. /pending-candidates/{candidateId} 리소스 생성
    print("\n[6단계] /pending-candidates/{candidateId} 리소스 생성")
    candidate_id_resource = create_api_resource(api_id, pending_candidates_id, '{candidateId}')
    
    # 7. DELETE /pending-candidates/{candidateId} 메서드 생성
    print("\n[7단계] DELETE /pending-candidates/{candidateId} 메서드 생성")
    create_api_method(api_id, candidate_id_resource, 'DELETE', delete_lambda_arn)
    
    # 8. OPTIONS /pending-candidates/{candidateId} 메서드 생성 (CORS)
    print("\n[8단계] OPTIONS /pending-candidates/{candidateId} 메서드 생성")
    create_api_method(api_id, candidate_id_resource, 'OPTIONS')
    
    # 9. API 배포
    print("\n[9단계] API 배포")
    deploy_api(api_id)
    
    print("\n" + "="*60)
    print("✓ pending-candidates API 엔드포인트 추가 완료!")
    print("="*60)
    print(f"\nAPI URL: https://{api_id}.execute-api.us-east-2.amazonaws.com/prod")
    print(f"  - GET    /pending-candidates")
    print(f"  - DELETE /pending-candidates/{{candidateId}}")
    print()

if __name__ == '__main__':
    main()

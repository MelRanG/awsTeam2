#!/usr/bin/env python3
"""
직원 삭제 API 생성 및 배포
"""
import boto3
import zipfile
import io
import os
import time

def create_employee_delete_api():
    """직원 삭제 Lambda 함수 생성 및 API Gateway 연결"""
    
    lambda_client = boto3.client('lambda', region_name='us-east-2')
    apigateway = boto3.client('apigateway', region_name='us-east-2')
    iam = boto3.client('iam')
    
    api_id = 'xoc7x1m6p8'
    function_name = 'EmployeeDelete'
    
    print("=" * 60)
    print("직원 삭제 API 생성")
    print("=" * 60)
    
    # 1. Lambda 함수 코드 압축
    print("\n1. Lambda 함수 코드 압축 중...")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        lambda_file = os.path.join(project_root, 'lambda_functions', 'employee_delete', 'index.py')
        if os.path.exists(lambda_file):
            zip_file.write(lambda_file, 'index.py')
            print(f"  ✓ index.py 추가됨")
        else:
            print(f"  ✗ index.py 파일을 찾을 수 없습니다")
            return False
    
    zip_buffer.seek(0)
    zip_content = zip_buffer.read()
    
    # 2. Lambda 함수 생성 또는 업데이트
    print(f"\n2. Lambda 함수 '{function_name}' 생성/업데이트 중...")
    try:
        # 함수가 이미 존재하는지 확인
        try:
            lambda_client.get_function(FunctionName=function_name)
            # 존재하면 코드 업데이트
            lambda_client.update_function_code(
                FunctionName=function_name,
                ZipFile=zip_content
            )
            print(f"  ✓ Lambda 함수 코드 업데이트 완료")
            function_arn = lambda_client.get_function(FunctionName=function_name)['Configuration']['FunctionArn']
        except lambda_client.exceptions.ResourceNotFoundException:
            # 존재하지 않으면 새로 생성
            response = lambda_client.create_function(
                FunctionName=function_name,
                Runtime='python3.13',
                Role='arn:aws:iam::412677576136:role/LabRole',
                Handler='index.lambda_handler',
                Code={'ZipFile': zip_content},
                Environment={
                    'Variables': {
                        'EMPLOYEES_TABLE': 'Employees'
                    }
                },
                Timeout=30,
                MemorySize=256
            )
            function_arn = response['FunctionArn']
            print(f"  ✓ Lambda 함수 생성 완료")
            time.sleep(2)
    except Exception as e:
        print(f"  ✗ Lambda 함수 생성/업데이트 실패: {str(e)}")
        return False
    
    # 3. /employees/{employeeId} 리소스 생성
    print("\n3. API Gateway 리소스 생성 중...")
    try:
        resources = apigateway.get_resources(restApiId=api_id)
        
        # /employees 리소스 찾기
        employees_resource = None
        for resource in resources['items']:
            if resource['path'] == '/employees':
                employees_resource = resource
                break
        
        if not employees_resource:
            print("  ✗ /employees 리소스를 찾을 수 없습니다")
            return False
        
        employees_resource_id = employees_resource['id']
        
        # /employees/{employeeId} 리소스 찾기 또는 생성
        employee_id_resource = None
        for resource in resources['items']:
            if resource['path'] == '/employees/{employeeId}':
                employee_id_resource = resource
                break
        
        if employee_id_resource:
            print(f"  ✓ /employees/{{employeeId}} 리소스가 이미 존재합니다")
            employee_id_resource_id = employee_id_resource['id']
        else:
            response = apigateway.create_resource(
                restApiId=api_id,
                parentId=employees_resource_id,
                pathPart='{employeeId}'
            )
            employee_id_resource_id = response['id']
            print(f"  ✓ /employees/{{employeeId}} 리소스 생성 완료")
    except Exception as e:
        print(f"  ✗ 리소스 생성 실패: {str(e)}")
        return False
    
    # 4. DELETE 메서드 생성
    print("\n4. DELETE 메서드 생성 중...")
    try:
        try:
            apigateway.get_method(
                restApiId=api_id,
                resourceId=employee_id_resource_id,
                httpMethod='DELETE'
            )
            print("  ✓ DELETE 메서드가 이미 존재합니다")
        except apigateway.exceptions.NotFoundException:
            apigateway.put_method(
                restApiId=api_id,
                resourceId=employee_id_resource_id,
                httpMethod='DELETE',
                authorizationType='NONE'
            )
            print("  ✓ DELETE 메서드 생성 완료")
    except Exception as e:
        print(f"  ✗ DELETE 메서드 생성 실패: {str(e)}")
        return False
    
    # 5. Lambda 통합 설정
    print("\n5. Lambda 통합 설정 중...")
    try:
        uri = f"arn:aws:apigateway:us-east-2:lambda:path/2015-03-31/functions/{function_arn}/invocations"
        
        apigateway.put_integration(
            restApiId=api_id,
            resourceId=employee_id_resource_id,
            httpMethod='DELETE',
            type='AWS_PROXY',
            integrationHttpMethod='POST',
            uri=uri
        )
        print("  ✓ Lambda 통합 설정 완료")
    except Exception as e:
        print(f"  ✗ Lambda 통합 설정 실패: {str(e)}")
        return False
    
    # 6. Lambda 권한 추가
    print("\n6. Lambda 실행 권한 추가 중...")
    try:
        statement_id = f"apigateway-delete-{int(time.time())}"
        source_arn = f"arn:aws:execute-api:us-east-2:412677576136:{api_id}/*/DELETE/employees/*"
        
        lambda_client.add_permission(
            FunctionName=function_name,
            StatementId=statement_id,
            Action='lambda:InvokeFunction',
            Principal='apigateway.amazonaws.com',
            SourceArn=source_arn
        )
        print("  ✓ Lambda 실행 권한 추가 완료")
    except lambda_client.exceptions.ResourceConflictException:
        print("  ✓ Lambda 실행 권한이 이미 존재합니다")
    except Exception as e:
        print(f"  ✗ Lambda 실행 권한 추가 실패: {str(e)}")
    
    # 7. OPTIONS 메서드 추가 (CORS)
    print("\n7. CORS 설정 중...")
    try:
        try:
            apigateway.put_method(
                restApiId=api_id,
                resourceId=employee_id_resource_id,
                httpMethod='OPTIONS',
                authorizationType='NONE'
            )
        except:
            pass
        
        apigateway.put_method_response(
            restApiId=api_id,
            resourceId=employee_id_resource_id,
            httpMethod='OPTIONS',
            statusCode='200',
            responseParameters={
                'method.response.header.Access-Control-Allow-Headers': True,
                'method.response.header.Access-Control-Allow-Methods': True,
                'method.response.header.Access-Control-Allow-Origin': True
            }
        )
        
        apigateway.put_integration(
            restApiId=api_id,
            resourceId=employee_id_resource_id,
            httpMethod='OPTIONS',
            type='MOCK',
            requestTemplates={'application/json': '{"statusCode": 200}'}
        )
        
        apigateway.put_integration_response(
            restApiId=api_id,
            resourceId=employee_id_resource_id,
            httpMethod='OPTIONS',
            statusCode='200',
            responseParameters={
                'method.response.header.Access-Control-Allow-Headers': "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'",
                'method.response.header.Access-Control-Allow-Methods': "'DELETE,OPTIONS'",
                'method.response.header.Access-Control-Allow-Origin': "'*'"
            },
            responseTemplates={'application/json': ''}
        )
        print("  ✓ CORS 설정 완료")
    except Exception as e:
        print(f"  → CORS 설정 중 에러: {str(e)}")
    
    # 8. API 배포
    print("\n8. API 배포 중...")
    try:
        apigateway.create_deployment(
            restApiId=api_id,
            stageName='prod',
            description='직원 삭제 API 추가'
        )
        print("  ✓ API 배포 완료")
    except Exception as e:
        print(f"  ✗ API 배포 실패: {str(e)}")
        return False
    
    print("\n" + "=" * 60)
    print("✅ 직원 삭제 API가 성공적으로 생성되었습니다!")
    print("=" * 60)
    print(f"\nAPI 엔드포인트: DELETE /employees/{{employeeId}}")
    return True

if __name__ == '__main__':
    create_employee_delete_api()

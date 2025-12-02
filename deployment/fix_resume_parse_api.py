#!/usr/bin/env python3
"""
/resume/parse API Gateway 엔드포인트 CORS 및 통합 수정
"""
import boto3
import json

def fix_resume_parse_endpoint():
    """resume/parse 엔드포인트 수정"""
    apigateway = boto3.client('apigateway', region_name='us-east-2')
    lambda_client = boto3.client('lambda', region_name='us-east-2')
    
    api_id = 'xoc7x1m6p8'
    resource_id = '1777mr'  # /resume/parse
    
    print("=" * 60)
    print("/resume/parse 엔드포인트 수정")
    print("=" * 60)
    
    # 1. Lambda 함수 ARN 가져오기
    try:
        lambda_response = lambda_client.get_function(FunctionName='ResumeParser')
        lambda_arn = lambda_response['Configuration']['FunctionArn']
        print(f"\n✓ Lambda ARN: {lambda_arn}")
    except Exception as e:
        print(f"✗ Lambda 함수를 찾을 수 없습니다: {e}")
        return False
    
    # 2. POST 메서드 확인 및 생성
    try:
        method = apigateway.get_method(
            restApiId=api_id,
            resourceId=resource_id,
            httpMethod='POST'
        )
        print("\n✓ POST 메서드가 이미 존재합니다")
    except:
        print("\n✗ POST 메서드가 없습니다. 생성 중...")
        try:
            apigateway.put_method(
                restApiId=api_id,
                resourceId=resource_id,
                httpMethod='POST',
                authorizationType='NONE'
            )
            print("✓ POST 메서드 생성 완료")
        except Exception as e:
            print(f"✗ POST 메서드 생성 실패: {e}")
            return False
    
    # 3. Lambda 통합 설정
    try:
        integration_uri = f"arn:aws:apigateway:us-east-2:lambda:path/2015-03-31/functions/{lambda_arn}/invocations"
        
        apigateway.put_integration(
            restApiId=api_id,
            resourceId=resource_id,
            httpMethod='POST',
            type='AWS_PROXY',
            integrationHttpMethod='POST',
            uri=integration_uri
        )
        print("✓ Lambda 통합 설정 완료")
    except Exception as e:
        print(f"✗ Lambda 통합 설정 실패: {e}")
        return False
    
    # 4. Lambda 권한 추가
    try:
        lambda_client.add_permission(
            FunctionName='ResumeParser',
            StatementId=f'apigateway-resume-parse-{api_id}',
            Action='lambda:InvokeFunction',
            Principal='apigateway.amazonaws.com',
            SourceArn=f'arn:aws:execute-api:us-east-2:412677576136:{api_id}/*/*'
        )
        print("✓ Lambda 권한 추가 완료")
    except lambda_client.exceptions.ResourceConflictException:
        print("✓ Lambda 권한이 이미 존재합니다")
    except Exception as e:
        print(f"✗ Lambda 권한 추가 실패: {e}")
    
    # 5. OPTIONS 메서드 추가 (CORS)
    try:
        apigateway.put_method(
            restApiId=api_id,
            resourceId=resource_id,
            httpMethod='OPTIONS',
            authorizationType='NONE'
        )
        print("✓ OPTIONS 메서드 생성 완료")
    except:
        print("✓ OPTIONS 메서드가 이미 존재합니다")
    
    # 6. OPTIONS MOCK 통합
    try:
        apigateway.put_integration(
            restApiId=api_id,
            resourceId=resource_id,
            httpMethod='OPTIONS',
            type='MOCK',
            requestTemplates={
                'application/json': '{"statusCode": 200}'
            }
        )
        print("✓ OPTIONS MOCK 통합 완료")
    except Exception as e:
        print(f"✗ OPTIONS 통합 실패: {e}")
    
    # 7. OPTIONS 응답 설정
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
        print("✓ OPTIONS 메서드 응답 설정 완료")
    except:
        print("✓ OPTIONS 메서드 응답이 이미 설정되어 있습니다")
    
    # 8. OPTIONS 통합 응답 설정
    try:
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
        print("✓ OPTIONS 통합 응답 설정 완료")
    except:
        print("✓ OPTIONS 통합 응답이 이미 설정되어 있습니다")
    
    # 9. API 배포
    try:
        apigateway.create_deployment(
            restApiId=api_id,
            stageName='prod',
            description='Resume parse endpoint CORS fix'
        )
        print("\n✅ API Gateway 배포 완료!")
        print(f"\n엔드포인트: https://{api_id}.execute-api.us-east-2.amazonaws.com/prod/resume/parse")
    except Exception as e:
        print(f"\n✗ API 배포 실패: {e}")
        return False
    
    return True

if __name__ == '__main__':
    fix_resume_parse_endpoint()

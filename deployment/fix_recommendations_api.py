"""
Recommendations API 엔드포인트 수정
"""
import boto3

def fix_recommendations_api():
    """Recommendations API 수정"""
    api_gateway = boto3.client('apigateway', region_name='us-east-2')
    lambda_client = boto3.client('lambda', region_name='us-east-2')
    
    api_id = 'ifeniowvpb'
    resource_id = 'gaa5o6'  # /recommendations
    
    print("=== Recommendations API 수정 ===\n")
    
    # 1. POST 메서드 확인 및 생성
    try:
        method = api_gateway.get_method(
            restApiId=api_id,
            resourceId=resource_id,
            httpMethod='POST'
        )
        print("✓ POST 메서드 존재")
    except:
        print("✗ POST 메서드 없음 - 생성 중...")
        api_gateway.put_method(
            restApiId=api_id,
            resourceId=resource_id,
            httpMethod='POST',
            authorizationType='NONE'
        )
        print("✓ POST 메서드 생성 완료")
    
    # 2. Lambda 통합 설정
    lambda_arn = 'arn:aws:lambda:us-east-2:412677576136:function:ProjectRecommendationEngine'
    
    try:
        api_gateway.put_integration(
            restApiId=api_id,
            resourceId=resource_id,
            httpMethod='POST',
            type='AWS_PROXY',
            integrationHttpMethod='POST',
            uri=f'arn:aws:apigateway:us-east-2:lambda:path/2015-03-31/functions/{lambda_arn}/invocations'
        )
        print("✓ Lambda 통합 설정 완료")
    except Exception as e:
        print(f"✗ Lambda 통합 실패: {str(e)}")
    
    # 3. Lambda 권한 추가
    try:
        lambda_client.add_permission(
            FunctionName='ProjectRecommendationEngine',
            StatementId='apigateway-recommendations-post',
            Action='lambda:InvokeFunction',
            Principal='apigateway.amazonaws.com',
            SourceArn=f'arn:aws:execute-api:us-east-2:412677576136:{api_id}/*/POST/recommendations'
        )
        print("✓ Lambda 권한 추가 완료")
    except lambda_client.exceptions.ResourceConflictException:
        print("✓ Lambda 권한 이미 존재")
    except Exception as e:
        print(f"✗ Lambda 권한 추가 실패: {str(e)}")
    
    # 4. CORS 설정 (OPTIONS 메서드)
    try:
        api_gateway.put_method(
            restApiId=api_id,
            resourceId=resource_id,
            httpMethod='OPTIONS',
            authorizationType='NONE'
        )
        print("✓ OPTIONS 메서드 생성 완료")
    except:
        print("✓ OPTIONS 메서드 이미 존재")
    
    # CORS 응답 설정
    try:
        api_gateway.put_integration(
            restApiId=api_id,
            resourceId=resource_id,
            httpMethod='OPTIONS',
            type='MOCK',
            requestTemplates={
                'application/json': '{"statusCode": 200}'
            }
        )
        
        api_gateway.put_integration_response(
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
        
        api_gateway.put_method_response(
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
        print("✓ CORS 설정 완료")
    except Exception as e:
        print(f"CORS 설정 중 오류 (무시 가능): {str(e)}")
    
    # 5. API 배포
    try:
        api_gateway.create_deployment(
            restApiId=api_id,
            stageName='prod',
            description='Recommendations API 수정'
        )
        print("✓ API 배포 완료")
    except Exception as e:
        print(f"✗ API 배포 실패: {str(e)}")
    
    print("\n=== 완료 ===")
    print(f"URL: https://{api_id}.execute-api.us-east-2.amazonaws.com/prod/recommendations")

if __name__ == '__main__':
    fix_recommendations_api()

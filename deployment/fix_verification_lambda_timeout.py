import boto3

lambda_client = boto3.client('lambda', region_name='us-east-2')
apigateway = boto3.client('apigateway', region_name='us-east-2')

def update_lambda_timeout():
    """Lambda 타임아웃 설정 업데이트"""
    print("=" * 60)
    print("검증 질문 Lambda 타임아웃 설정 업데이트")
    print("=" * 60)
    
    function_name = 'ResumeVerificationQuestions'
    
    try:
        # 현재 설정 확인
        response = lambda_client.get_function_configuration(
            FunctionName=function_name
        )
        current_timeout = response['Timeout']
        print(f"\n현재 타임아웃: {current_timeout}초")
        
        # 타임아웃을 90초로 증가
        lambda_client.update_function_configuration(
            FunctionName=function_name,
            Timeout=90
        )
        print(f"✓ 타임아웃을 90초로 업데이트 완료")
        
        # API Gateway 통합 타임아웃도 확인
        print("\nAPI Gateway 통합 타임아웃 확인 중...")
        api_id = 'ifeniowvpb'
        
        # 리소스 찾기
        resources = apigateway.get_resources(restApiId=api_id, limit=500)
        verification_resource = None
        
        for resource in resources['items']:
            if resource['path'] == '/resume/verification-questions':
                verification_resource = resource
                break
        
        if verification_resource:
            resource_id = verification_resource['id']
            
            # 통합 설정 확인
            integration = apigateway.get_integration(
                restApiId=api_id,
                resourceId=resource_id,
                httpMethod='POST'
            )
            
            print(f"✓ API Gateway 통합 타입: {integration['type']}")
            print(f"✓ API Gateway 통합 타임아웃: {integration.get('timeoutInMillis', 29000)}ms")
            
            # 통합 타임아웃 업데이트 (최대 29초)
            apigateway.update_integration(
                restApiId=api_id,
                resourceId=resource_id,
                httpMethod='POST',
                patchOperations=[
                    {
                        'op': 'replace',
                        'path': '/timeoutInMillis',
                        'value': '29000'
                    }
                ]
            )
            print(f"✓ API Gateway 통합 타임아웃을 29초로 업데이트")
            
            # 배포
            apigateway.create_deployment(
                restApiId=api_id,
                stageName='prod',
                description='검증 질문 API 타임아웃 설정 업데이트'
            )
            print(f"✓ API 배포 완료")
        
        print("\n" + "=" * 60)
        print("✅ 타임아웃 설정 완료!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 에러 발생: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    update_lambda_timeout()

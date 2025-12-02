#!/usr/bin/env python3
"""API Gateway 설정 확인"""

import boto3
import json

apigateway = boto3.client('apigateway', region_name='us-east-2')

print("=" * 60)
print("API Gateway 설정 확인")
print("=" * 60)

try:
    # API 목록 조회
    apis = apigateway.get_rest_apis()
    
    for api in apis['items']:
        print(f"\nAPI 이름: {api['name']}")
        print(f"API ID: {api['id']}")
        
        # 리소스 조회
        resources = apigateway.get_resources(restApiId=api['id'])
        
        print("\n리소스 목록:")
        for resource in resources['items']:
            path = resource.get('path', '/')
            print(f"  - {path}")
            
            # 메서드 확인
            if 'resourceMethods' in resource:
                for method in resource['resourceMethods'].keys():
                    print(f"    └─ {method}")
                    
                    # 통합 정보 확인
                    try:
                        integration = apigateway.get_integration(
                            restApiId=api['id'],
                            resourceId=resource['id'],
                            httpMethod=method
                        )
                        
                        if 'uri' in integration:
                            # Lambda 함수 이름 추출
                            uri = integration['uri']
                            if 'function:' in uri:
                                func_name = uri.split('function:')[1].split('/')[0]
                                print(f"       → Lambda: {func_name}")
                    except:
                        pass
        
        print("-" * 60)

except Exception as e:
    print(f"에러: {str(e)}")

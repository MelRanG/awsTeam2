"""
/pending-candidates API 확인
"""
import boto3

apigateway = boto3.client('apigateway', region_name='us-east-2')
api_id = 'ifeniowvpb'

print("="*60)
print("/pending-candidates API 확인")
print("="*60)

# 리소스 찾기
resources = apigateway.get_resources(restApiId=api_id, limit=500)

for resource in resources['items']:
    if resource['path'] == '/pending-candidates':
        print(f"\n✅ 리소스 ID: {resource['id']}")
        print(f"   경로: {resource['path']}")
        
        if 'resourceMethods' in resource:
            methods = resource['resourceMethods'].keys()
            print(f"   메서드: {', '.join(methods)}")
            
            # POST 메서드 통합 확인
            if 'POST' in methods:
                try:
                    integration = apigateway.get_integration(
                        restApiId=api_id,
                        resourceId=resource['id'],
                        httpMethod='POST'
                    )
                    print(f"\n   POST 통합:")
                    print(f"   - 타입: {integration.get('type')}")
                    if 'uri' in integration:
                        print(f"   - URI: {integration['uri']}")
                except Exception as e:
                    print(f"   ❌ POST 통합 없음: {str(e)}")
            else:
                print("\n   ⚠️  POST 메서드 없음")
        else:
            print("   ⚠️  메서드 없음")
        break
else:
    print("\n❌ /pending-candidates 리소스를 찾을 수 없습니다")

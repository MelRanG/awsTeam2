"""
모든 API Gateway 리소스 확인
"""
import boto3

apigateway = boto3.client('apigateway', region_name='us-east-2')
api_id = 'ifeniowvpb'

print("="*60)
print("API Gateway 리소스 목록")
print("="*60)

resources = apigateway.get_resources(restApiId=api_id, limit=500)

print(f"\n총 {len(resources['items'])}개 리소스\n")

for resource in sorted(resources['items'], key=lambda x: x['path']):
    path = resource['path']
    resource_id = resource['id']
    methods = resource.get('resourceMethods', {}).keys() if 'resourceMethods' in resource else []
    
    print(f"{path}")
    print(f"  ID: {resource_id}")
    if methods:
        print(f"  메서드: {', '.join(methods)}")
    print()

#!/usr/bin/env python3
"""
API Gateway 리소스 목록 조회
"""
import boto3
import json

client = boto3.client('apigateway', region_name='us-east-2')
api_id = 'xoc7x1m6p8'

print("API Gateway 리소스 목록:")
print("=" * 60)

resources = client.get_resources(restApiId=api_id, limit=500)

for resource in resources['items']:
    path = resource.get('path', '/')
    resource_id = resource['id']
    methods = resource.get('resourceMethods', {})
    method_list = ', '.join(methods.keys()) if methods else 'None'
    
    print(f"Path: {path}")
    print(f"  ID: {resource_id}")
    print(f"  Methods: {method_list}")
    print()

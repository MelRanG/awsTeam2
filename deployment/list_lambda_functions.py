#!/usr/bin/env python3
"""
Lambda 함수 목록 조회
"""
import boto3

lambda_client = boto3.client('lambda', region_name='us-east-2')

print("Lambda 함수 목록:")
print("=" * 60)

response = lambda_client.list_functions()

for func in response['Functions']:
    name = func['FunctionName']
    runtime = func['Runtime']
    handler = func['Handler']
    
    if 'employee' in name.lower() or 'Employee' in name:
        print(f"이름: {name}")
        print(f"  Runtime: {runtime}")
        print(f"  Handler: {handler}")
        print()

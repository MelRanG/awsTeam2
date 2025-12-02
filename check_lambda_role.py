#!/usr/bin/env python3
"""Lambda 실행 역할 권한 확인"""

import boto3
import json

lambda_client = boto3.client('lambda', region_name='us-east-2')
iam_client = boto3.client('iam')

function_name = 'ResumeUploadURLGenerator'

try:
    # Lambda 함수 정보 조회
    response = lambda_client.get_function(FunctionName=function_name)
    role_arn = response['Configuration']['Role']
    role_name = role_arn.split('/')[-1]
    
    print(f"Lambda 함수: {function_name}")
    print(f"실행 역할: {role_name}")
    print(f"역할 ARN: {role_arn}")
    
    # 역할에 연결된 정책 조회
    print("\n연결된 정책:")
    
    # 관리형 정책
    attached_policies = iam_client.list_attached_role_policies(RoleName=role_name)
    for policy in attached_policies['AttachedPolicies']:
        print(f"  - {policy['PolicyName']}")
    
    # 인라인 정책
    inline_policies = iam_client.list_role_policies(RoleName=role_name)
    for policy_name in inline_policies['PolicyNames']:
        print(f"  - {policy_name} (인라인)")
        
        # 인라인 정책 내용 확인
        policy_doc = iam_client.get_role_policy(
            RoleName=role_name,
            PolicyName=policy_name
        )
        print(f"\n{policy_name} 정책 내용:")
        print(json.dumps(policy_doc['PolicyDocument'], indent=2, ensure_ascii=False))
    
    print("\n" + "=" * 60)
    print("권한 확인 사항:")
    print("- s3:PutObject 권한이 있어야 Presigned URL 생성 가능")
    print("- s3:GetObject 권한도 있으면 다운로드도 가능")
    
except Exception as e:
    print(f"✗ 에러: {str(e)}")

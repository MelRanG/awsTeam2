#!/usr/bin/env python3
"""Lambda 역할에 S3 권한 추가 (조건 없이)"""

import boto3
import json

iam_client = boto3.client('iam')
role_name = 'LambdaExecutionRole-Team2'
policy_name = 'ResumeUploadS3Access'

# 조건 없는 S3 권한 정책
policy_document = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObject"
            ],
            "Resource": "arn:aws:s3:::hr-resource-optimization-resumes-prod/uploads/*"
        }
    ]
}

try:
    print(f"Lambda 역할에 S3 권한 추가 중...")
    print(f"역할: {role_name}")
    print(f"정책: {policy_name}")
    
    # 인라인 정책 추가
    iam_client.put_role_policy(
        RoleName=role_name,
        PolicyName=policy_name,
        PolicyDocument=json.dumps(policy_document)
    )
    
    print(f"✓ 권한 추가 완료!")
    
    # 확인
    response = iam_client.get_role_policy(
        RoleName=role_name,
        PolicyName=policy_name
    )
    
    print(f"\n추가된 정책:")
    print(json.dumps(response['PolicyDocument'], indent=2, ensure_ascii=False))
    
    print("\n" + "=" * 60)
    print("✅ 이제 Presigned URL로 업로드할 수 있습니다!")
    print("=" * 60)
    
except Exception as e:
    print(f"✗ 에러: {str(e)}")
    exit(1)

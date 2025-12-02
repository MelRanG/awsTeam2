#!/usr/bin/env python3
"""S3 버킷 정책 수정 - Presigned URL 업로드 허용"""

import boto3
import json

s3_client = boto3.client('s3', region_name='us-east-2')
bucket_name = 'hr-resource-optimization-resumes-prod'

# 버킷 정책 - Presigned URL 업로드 허용
bucket_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowPresignedURLUpload",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:PutObject",
            "Resource": f"arn:aws:s3:::{bucket_name}/uploads/*"
        }
    ]
}

try:
    print(f"S3 버킷 정책 업데이트 중: {bucket_name}")
    
    # 기존 정책 확인
    try:
        response = s3_client.get_bucket_policy(Bucket=bucket_name)
        print("\n기존 버킷 정책:")
        print(json.dumps(json.loads(response['Policy']), indent=2, ensure_ascii=False))
    except Exception as e:
        if 'NoSuchBucketPolicy' in str(e):
            print("\n기존 버킷 정책 없음")
        else:
            print(f"\n기존 정책 확인 실패: {str(e)}")
    
    # 새 정책 적용
    s3_client.put_bucket_policy(
        Bucket=bucket_name,
        Policy=json.dumps(bucket_policy)
    )
    print("\n✓ 버킷 정책 업데이트 완료!")
    
    # 확인
    response = s3_client.get_bucket_policy(Bucket=bucket_name)
    print("\n새 버킷 정책:")
    print(json.dumps(json.loads(response['Policy']), indent=2, ensure_ascii=False))
    
except Exception as e:
    print(f"✗ 에러 발생: {str(e)}")
    exit(1)

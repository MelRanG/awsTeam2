#!/usr/bin/env python3
"""S3 CORS 설정 업데이트"""

import boto3
import json

s3_client = boto3.client('s3', region_name='us-east-2')
bucket_name = 'hr-resource-optimization-resumes-prod'

cors_configuration = {
    'CORSRules': [
        {
            'AllowedHeaders': ['*'],
            'AllowedMethods': ['GET', 'PUT', 'POST', 'DELETE', 'HEAD'],
            'AllowedOrigins': ['*'],
            'ExposeHeaders': [
                'ETag',
                'x-amz-server-side-encryption',
                'x-amz-request-id',
                'x-amz-id-2'
            ],
            'MaxAgeSeconds': 3000
        }
    ]
}

try:
    print(f"S3 버킷 CORS 설정 업데이트 중: {bucket_name}")
    s3_client.put_bucket_cors(
        Bucket=bucket_name,
        CORSConfiguration=cors_configuration
    )
    print("✓ CORS 설정 완료!")
    
    # 확인
    response = s3_client.get_bucket_cors(Bucket=bucket_name)
    print("\n현재 CORS 설정:")
    print(json.dumps(response['CORSRules'], indent=2, ensure_ascii=False))
    
except Exception as e:
    print(f"✗ 에러 발생: {str(e)}")
    exit(1)

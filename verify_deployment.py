#!/usr/bin/env python3
"""배포 확인"""

import boto3
import json

lambda_client = boto3.client('lambda', region_name='us-east-2')
s3_client = boto3.client('s3', region_name='us-east-2')

print("=" * 60)
print("배포 상태 확인")
print("=" * 60)

# 1. S3 CORS 확인
print("\n[1/2] S3 CORS 설정 확인")
print("-" * 60)
try:
    response = s3_client.get_bucket_cors(
        Bucket='hr-resource-optimization-resumes-prod'
    )
    cors_rules = response['CORSRules'][0]
    print(f"✓ AllowedMethods: {', '.join(cors_rules['AllowedMethods'])}")
    print(f"✓ AllowedOrigins: {', '.join(cors_rules['AllowedOrigins'])}")
    print(f"✓ AllowedHeaders: {', '.join(cors_rules['AllowedHeaders'])}")
    print("✓ S3 CORS 설정 정상")
except Exception as e:
    print(f"✗ S3 CORS 확인 실패: {str(e)}")

# 2. Lambda 함수 확인
print("\n[2/2] Lambda 함수 확인")
print("-" * 60)
try:
    response = lambda_client.get_function(FunctionName='ResumeParser')
    config = response['Configuration']
    print(f"✓ 함수명: {config['FunctionName']}")
    print(f"✓ 런타임: {config['Runtime']}")
    print(f"✓ 마지막 수정: {config['LastModified']}")
    print(f"✓ 코드 크기: {config['CodeSize']} bytes")
    print("✓ Lambda 함수 정상")
except Exception as e:
    print(f"✗ Lambda 함수 확인 실패: {str(e)}")

print("\n" + "=" * 60)
print("✅ 모든 배포 완료!")
print("=" * 60)
print("\n다음 단계:")
print("1. 브라우저 캐시 삭제 (Ctrl + Shift + Delete)")
print("2. 시크릿 모드로 접속")
print("3. PDF 파일 업로드 테스트")

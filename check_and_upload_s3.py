#!/usr/bin/env python3
"""S3 버킷 확인 및 파일 업로드"""

import boto3
import os
from pathlib import Path

s3_client = boto3.client('s3', region_name='us-east-2')
bucket_name = 'hr-resource-optimization-frontend-hosting-prod'

print("=" * 60)
print("S3 버킷 확인 및 업로드")
print("=" * 60)

# 1. 버킷 내용 확인
print("\n1. 현재 S3 버킷 내용:")
try:
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    if 'Contents' in response:
        for obj in response['Contents']:
            print(f"  - {obj['Key']} ({obj['Size']} bytes)")
    else:
        print("  버킷이 비어있습니다!")
except Exception as e:
    print(f"  에러: {str(e)}")

# 2. 로컬 빌드 폴더 확인
print("\n2. 로컬 빌드 폴더 확인:")
build_dir = Path('frontend/build')
if not build_dir.exists():
    print("  ✗ 빌드 폴더가 없습니다!")
    exit(1)

files_to_upload = []
for file_path in build_dir.rglob('*'):
    if file_path.is_file():
        relative_path = file_path.relative_to(build_dir)
        files_to_upload.append((file_path, str(relative_path).replace('\\', '/')))
        print(f"  - {relative_path}")

print(f"\n  총 {len(files_to_upload)}개 파일")

# 3. 파일 업로드
print("\n3. S3에 파일 업로드 중...")
for local_path, s3_key in files_to_upload:
    try:
        # Content-Type 설정
        content_type = 'text/html' if s3_key.endswith('.html') else \
                      'text/css' if s3_key.endswith('.css') else \
                      'application/javascript' if s3_key.endswith('.js') else \
                      'application/octet-stream'
        
        s3_client.upload_file(
            str(local_path),
            bucket_name,
            s3_key,
            ExtraArgs={
                'ContentType': content_type,
                'CacheControl': 'no-cache, no-store, must-revalidate, max-age=0'
            }
        )
        print(f"  ✓ {s3_key}")
    except Exception as e:
        print(f"  ✗ {s3_key}: {str(e)}")

# 4. 업로드 확인
print("\n4. 업로드 후 S3 버킷 내용:")
try:
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    if 'Contents' in response:
        for obj in response['Contents']:
            print(f"  - {obj['Key']} ({obj['Size']} bytes)")
    else:
        print("  버킷이 비어있습니다!")
except Exception as e:
    print(f"  에러: {str(e)}")

print("\n" + "=" * 60)
print("✅ 완료!")
print("=" * 60)
print(f"\nURL: http://{bucket_name}.s3-website.us-east-2.amazonaws.com/")

#!/usr/bin/env python3
"""프론트엔드 S3 배포 (boto3 사용)"""

import boto3
import os
from pathlib import Path
import mimetypes

s3_client = boto3.client('s3', region_name='us-east-2')
bucket_name = 'hr-resource-optimization-frontend-hosting-prod'

print("=" * 60)
print("프론트엔드 S3 배포")
print("=" * 60)

# 1. 빌드 폴더 확인
print("\n1. 빌드 폴더 확인...")
# 현재 디렉토리 확인
current_dir = Path.cwd()
if current_dir.name == 'frontend':
    build_dir = Path('build')
else:
    build_dir = Path('frontend/build')

if not build_dir.exists():
    print(f"  ✗ 빌드 폴더가 없습니다! (찾는 경로: {build_dir.absolute()})")
    print("  먼저 'cd frontend && npm run build'를 실행하세요.")
    exit(1)

# 2. 업로드할 파일 목록
files_to_upload = []
for file_path in build_dir.rglob('*'):
    if file_path.is_file():
        relative_path = file_path.relative_to(build_dir)
        s3_key = str(relative_path).replace('\\', '/')
        files_to_upload.append((file_path, s3_key))

print(f"  ✓ {len(files_to_upload)}개 파일 발견")

# 3. S3 버킷 비우기
print("\n2. S3 버킷 기존 파일 삭제 중...")
try:
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    if 'Contents' in response:
        objects_to_delete = [{'Key': obj['Key']} for obj in response['Contents']]
        s3_client.delete_objects(
            Bucket=bucket_name,
            Delete={'Objects': objects_to_delete}
        )
        print(f"  ✓ {len(objects_to_delete)}개 파일 삭제 완료")
    else:
        print("  ✓ 버킷이 이미 비어있음")
except Exception as e:
    print(f"  ✗ 삭제 실패: {str(e)}")

# 4. 파일 업로드
print("\n3. S3에 파일 업로드 중...")
uploaded_count = 0
for local_path, s3_key in files_to_upload:
    try:
        # Content-Type 자동 감지
        content_type, _ = mimetypes.guess_type(str(local_path))
        if not content_type:
            content_type = 'application/octet-stream'
        
        # 업로드
        s3_client.upload_file(
            str(local_path),
            bucket_name,
            s3_key,
            ExtraArgs={
                'ContentType': content_type,
                'CacheControl': 'no-cache, no-store, must-revalidate, max-age=0'
            }
        )
        uploaded_count += 1
        print(f"  ✓ {s3_key}")
    except Exception as e:
        print(f"  ✗ {s3_key}: {str(e)}")

print(f"\n  총 {uploaded_count}/{len(files_to_upload)}개 파일 업로드 완료")

# 5. 확인
print("\n4. 업로드 확인...")
try:
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    if 'Contents' in response:
        print(f"  ✓ S3 버킷에 {len(response['Contents'])}개 파일 존재")
        for obj in response['Contents']:
            print(f"    - {obj['Key']}")
    else:
        print("  ✗ 버킷이 비어있습니다!")
except Exception as e:
    print(f"  ✗ 확인 실패: {str(e)}")

print("\n" + "=" * 60)
print("✅ 배포 완료!")
print("=" * 60)
print(f"\nURL: http://{bucket_name}.s3-website.us-east-2.amazonaws.com/")
print("\n⚠️  브라우저 캐시 삭제 또는 시크릿 모드로 접속하세요!")

#!/usr/bin/env python3
"""Presigned URL 생성 테스트"""

import boto3
import requests
from datetime import datetime

s3_client = boto3.client('s3', region_name='us-east-2')
bucket_name = 'hr-resource-optimization-resumes-prod'

# 테스트 파일 키
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
file_key = f"uploads/test_{timestamp}.txt"

print("=" * 60)
print("Presigned URL 생성 및 테스트")
print("=" * 60)

try:
    # Presigned URL 생성
    print(f"\n1. Presigned URL 생성 중...")
    print(f"   버킷: {bucket_name}")
    print(f"   키: {file_key}")
    
    presigned_url = s3_client.generate_presigned_url(
        'put_object',
        Params={
            'Bucket': bucket_name,
            'Key': file_key,
            'ContentType': 'text/plain',
        },
        ExpiresIn=3600,
        HttpMethod='PUT'
    )
    
    print(f"✓ URL 생성 완료")
    print(f"   URL: {presigned_url[:100]}...")
    
    # 테스트 업로드
    print(f"\n2. 테스트 파일 업로드 중...")
    test_content = b"Test content for presigned URL"
    
    response = requests.put(
        presigned_url,
        data=test_content,
        headers={'Content-Type': 'text/plain'}
    )
    
    print(f"   상태 코드: {response.status_code}")
    
    if response.status_code in [200, 204]:
        print(f"✓ 업로드 성공!")
        
        # 파일 확인
        print(f"\n3. 업로드된 파일 확인 중...")
        obj = s3_client.head_object(Bucket=bucket_name, Key=file_key)
        print(f"✓ 파일 존재 확인")
        print(f"   크기: {obj['ContentLength']} bytes")
        print(f"   Content-Type: {obj['ContentType']}")
        
        # 정리
        print(f"\n4. 테스트 파일 삭제 중...")
        s3_client.delete_object(Bucket=bucket_name, Key=file_key)
        print(f"✓ 정리 완료")
        
        print("\n" + "=" * 60)
        print("✅ Presigned URL이 정상 작동합니다!")
        print("=" * 60)
    else:
        print(f"✗ 업로드 실패")
        print(f"   응답: {response.text}")
        print(f"   헤더: {dict(response.headers)}")
        
except Exception as e:
    print(f"✗ 에러: {str(e)}")
    import traceback
    traceback.print_exc()

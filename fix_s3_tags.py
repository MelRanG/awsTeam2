#!/usr/bin/env python3
"""S3 버킷 태그 확인 및 추가"""

import boto3

s3_client = boto3.client('s3', region_name='us-east-2')
bucket_name = 'hr-resource-optimization-resumes-prod'

try:
    # 기존 태그 확인
    print(f"S3 버킷 태그 확인: {bucket_name}")
    try:
        response = s3_client.get_bucket_tagging(Bucket=bucket_name)
        print("\n기존 태그:")
        for tag in response['TagSet']:
            print(f"  - {tag['Key']}: {tag['Value']}")
    except Exception as e:
        if 'NoSuchTagSet' in str(e):
            print("\n기존 태그 없음")
        else:
            print(f"\n태그 확인 실패: {str(e)}")
    
    # Team2 태그 추가
    print(f"\nTeam2 태그 추가 중...")
    s3_client.put_bucket_tagging(
        Bucket=bucket_name,
        Tagging={
            'TagSet': [
                {
                    'Key': 'Team',
                    'Value': 'Team2'
                },
                {
                    'Key': 'Project',
                    'Value': 'HR-Resource-Optimization'
                }
            ]
        }
    )
    print("✓ 태그 추가 완료!")
    
    # 확인
    response = s3_client.get_bucket_tagging(Bucket=bucket_name)
    print("\n새 태그:")
    for tag in response['TagSet']:
        print(f"  - {tag['Key']}: {tag['Value']}")
    
    print("\n" + "=" * 60)
    print("✅ 이제 Lambda 함수가 S3에 접근할 수 있습니다!")
    print("=" * 60)
    
except Exception as e:
    print(f"✗ 에러: {str(e)}")
    exit(1)

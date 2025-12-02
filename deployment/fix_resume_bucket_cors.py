"""
이력서 업로드 S3 버킷 CORS 설정 수정
403 Forbidden 에러 해결을 위한 스크립트
"""

import boto3
import json

s3_client = boto3.client('s3', region_name='us-east-2')

BUCKET_NAME = 'hr-resource-optimization-resumes-prod'

def fix_cors_configuration():
    """S3 버킷 CORS 설정 수정"""
    
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
        # CORS 설정 적용
        s3_client.put_bucket_cors(
            Bucket=BUCKET_NAME,
            CORSConfiguration=cors_configuration
        )
        print(f"✓ {BUCKET_NAME} CORS 설정 완료")
        
        # 설정 확인
        response = s3_client.get_bucket_cors(Bucket=BUCKET_NAME)
        print("\n현재 CORS 설정:")
        print(json.dumps(response['CORSRules'], indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(f"✗ CORS 설정 실패: {str(e)}")
        return False
    
    return True

def check_bucket_policy():
    """버킷 정책 확인"""
    try:
        response = s3_client.get_bucket_policy(Bucket=BUCKET_NAME)
        policy = json.loads(response['Policy'])
        print("\n현재 버킷 정책:")
        print(json.dumps(policy, indent=2, ensure_ascii=False))
    except s3_client.exceptions.NoSuchBucketPolicy:
        print("\n버킷 정책이 설정되지 않았습니다.")
    except Exception as e:
        print(f"\n버킷 정책 확인 실패: {str(e)}")

def check_public_access_block():
    """퍼블릭 액세스 차단 설정 확인"""
    try:
        response = s3_client.get_public_access_block(Bucket=BUCKET_NAME)
        config = response['PublicAccessBlockConfiguration']
        print("\n퍼블릭 액세스 차단 설정:")
        print(json.dumps(config, indent=2, ensure_ascii=False))
        
        # 업로드를 위해서는 일부 설정이 False여야 함
        if config.get('BlockPublicAcls') or config.get('IgnorePublicAcls'):
            print("\n⚠️  경고: 퍼블릭 ACL이 차단되어 있습니다.")
            print("   Presigned URL 업로드에는 영향이 없지만, 다운로드 시 문제가 될 수 있습니다.")
            
    except Exception as e:
        print(f"\n퍼블릭 액세스 차단 설정 확인 실패: {str(e)}")

if __name__ == '__main__':
    print("=" * 60)
    print("이력서 업로드 S3 버킷 CORS 설정 수정")
    print("=" * 60)
    
    # CORS 설정
    if fix_cors_configuration():
        print("\n✓ CORS 설정이 완료되었습니다.")
    else:
        print("\n✗ CORS 설정에 실패했습니다.")
    
    # 버킷 정책 확인
    check_bucket_policy()
    
    # 퍼블릭 액세스 차단 설정 확인
    check_public_access_block()
    
    print("\n" + "=" * 60)
    print("완료!")
    print("=" * 60)

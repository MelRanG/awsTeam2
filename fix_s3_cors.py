import boto3
import json

# S3 클라이언트 생성
s3_client = boto3.client('s3', region_name='us-east-2')

# 이력서 버킷 이름
bucket_name = 'hr-resource-optimization-resumes-prod'

# CORS 설정
cors_configuration = {
    'CORSRules': [
        {
            'AllowedHeaders': ['*'],
            'AllowedMethods': ['GET', 'PUT', 'POST', 'DELETE', 'HEAD'],
            'AllowedOrigins': [
                'http://hr-resource-optimization-frontend-hosting-prod.s3-website.us-east-2.amazonaws.com',
                'http://localhost:3000',
                'http://localhost:5173'
            ],
            'ExposeHeaders': ['ETag', 'x-amz-request-id'],
            'MaxAgeSeconds': 3000
        }
    ]
}

try:
    # CORS 설정 적용
    s3_client.put_bucket_cors(
        Bucket=bucket_name,
        CORSConfiguration=cors_configuration
    )
    print(f"✅ S3 버킷 '{bucket_name}'에 CORS 설정이 적용되었습니다!")
    print("\n적용된 CORS 설정:")
    print(json.dumps(cors_configuration, indent=2, ensure_ascii=False))
    
    # 설정 확인
    response = s3_client.get_bucket_cors(Bucket=bucket_name)
    print("\n현재 CORS 설정:")
    print(json.dumps(response['CORSRules'], indent=2, ensure_ascii=False))
    
except Exception as e:
    print(f"❌ 오류 발생: {str(e)}")

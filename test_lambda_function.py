#!/usr/bin/env python3
"""Lambda 함수 직접 테스트"""

import boto3
import json
import requests

lambda_client = boto3.client('lambda', region_name='us-east-2')

# Lambda 함수 호출
event = {
    "httpMethod": "POST",
    "body": json.dumps({
        "file_name": "test_resume.pdf",
        "content_type": "application/pdf"
    })
}

print("=" * 60)
print("Lambda 함수 테스트")
print("=" * 60)

try:
    print("\n1. Lambda 함수 호출 중...")
    response = lambda_client.invoke(
        FunctionName='ResumeUploadURLGenerator',
        InvocationType='RequestResponse',
        Payload=json.dumps(event)
    )
    
    # 응답 파싱
    payload = json.loads(response['Payload'].read())
    print(f"✓ Lambda 응답 받음")
    print(f"   상태 코드: {payload.get('statusCode')}")
    
    if payload.get('statusCode') == 200:
        body = json.loads(payload['body'])
        print(f"✓ 성공 응답")
        print(f"   upload_url: {body['upload_url'][:100]}...")
        print(f"   file_key: {body['file_key']}")
        print(f"   expires_in: {body['expires_in']}")
        
        # 실제 업로드 테스트
        print(f"\n2. Presigned URL로 업로드 테스트 중...")
        test_content = b"Test PDF content"
        
        upload_response = requests.put(
            body['upload_url'],
            data=test_content,
            headers={'Content-Type': 'application/pdf'}
        )
        
        print(f"   상태 코드: {upload_response.status_code}")
        
        if upload_response.status_code in [200, 204]:
            print(f"✓ 업로드 성공!")
            print("\n" + "=" * 60)
            print("✅ Lambda 함수가 정상 작동합니다!")
            print("=" * 60)
        else:
            print(f"✗ 업로드 실패")
            print(f"   응답: {upload_response.text}")
            print(f"   헤더: {dict(upload_response.headers)}")
    else:
        print(f"✗ Lambda 함수 에러")
        print(f"   응답: {json.dumps(payload, indent=2, ensure_ascii=False)}")
        
except Exception as e:
    print(f"✗ 에러: {str(e)}")
    import traceback
    traceback.print_exc()

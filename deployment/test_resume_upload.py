"""
이력서 업로드 기능 테스트
Presigned URL 생성 및 업로드 테스트
"""

import requests
import json
import os

# API Gateway URL
API_BASE_URL = "https://your-api-gateway-url"  # 실제 URL로 변경 필요

def test_presigned_url_generation():
    """Presigned URL 생성 테스트"""
    print("\n1. Presigned URL 생성 테스트")
    print("-" * 60)
    
    url = f"{API_BASE_URL}/resume/upload-url"
    payload = {
        "file_name": "test_resume.pdf",
        "content_type": "application/pdf"
    }
    
    try:
        response = requests.post(url, json=payload)
        print(f"상태 코드: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✓ Presigned URL 생성 성공")
            print(f"  - Upload URL: {data['upload_url'][:100]}...")
            print(f"  - File Key: {data['file_key']}")
            print(f"  - Expires In: {data['expires_in']}초")
            return data
        else:
            print(f"✗ 실패: {response.text}")
            return None
            
    except Exception as e:
        print(f"✗ 에러: {str(e)}")
        return None

def test_file_upload(upload_data, test_file_path):
    """실제 파일 업로드 테스트"""
    print("\n2. 파일 업로드 테스트")
    print("-" * 60)
    
    if not upload_data:
        print("✗ Upload URL이 없습니다.")
        return False
    
    if not os.path.exists(test_file_path):
        print(f"✗ 테스트 파일이 없습니다: {test_file_path}")
        return False
    
    try:
        with open(test_file_path, 'rb') as f:
            file_content = f.read()
        
        headers = {
            'Content-Type': 'application/pdf'
        }
        
        response = requests.put(
            upload_data['upload_url'],
            data=file_content,
            headers=headers
        )
        
        print(f"상태 코드: {response.status_code}")
        
        if response.status_code in [200, 204]:
            print("✓ 파일 업로드 성공")
            print(f"  - 파일 크기: {len(file_content)} bytes")
            print(f"  - S3 Key: {upload_data['file_key']}")
            return True
        else:
            print(f"✗ 업로드 실패")
            print(f"  - 응답: {response.text}")
            print(f"  - 헤더: {dict(response.headers)}")
            return False
            
    except Exception as e:
        print(f"✗ 에러: {str(e)}")
        return False

def check_cors_headers(upload_url):
    """CORS 헤더 확인"""
    print("\n3. CORS 헤더 확인")
    print("-" * 60)
    
    try:
        # OPTIONS 요청
        response = requests.options(upload_url)
        print(f"OPTIONS 상태 코드: {response.status_code}")
        print("CORS 헤더:")
        
        cors_headers = {
            'Access-Control-Allow-Origin',
            'Access-Control-Allow-Methods',
            'Access-Control-Allow-Headers',
            'Access-Control-Max-Age'
        }
        
        for header in cors_headers:
            value = response.headers.get(header, '없음')
            print(f"  - {header}: {value}")
            
    except Exception as e:
        print(f"✗ 에러: {str(e)}")

if __name__ == '__main__':
    print("=" * 60)
    print("이력서 업로드 기능 테스트")
    print("=" * 60)
    
    # 1. Presigned URL 생성
    upload_data = test_presigned_url_generation()
    
    # 2. CORS 헤더 확인
    if upload_data:
        check_cors_headers(upload_data['upload_url'])
    
    # 3. 실제 파일 업로드 (테스트 파일 경로 지정)
    test_file = "../test_data/sample_resume.pdf"  # 실제 테스트 파일 경로로 변경
    if os.path.exists(test_file):
        test_file_upload(upload_data, test_file)
    else:
        print(f"\n⚠️  테스트 파일이 없습니다: {test_file}")
        print("   실제 PDF 파일을 준비하여 테스트하세요.")
    
    print("\n" + "=" * 60)
    print("테스트 완료!")
    print("=" * 60)

"""
이력서 관련 API 테스트
"""
import requests
import json

API_BASE_URL = 'https://ifeniowvpb.execute-api.us-east-2.amazonaws.com/prod'

def test_resume_upload_url():
    """이력서 업로드 URL 생성 테스트"""
    print("\n" + "="*60)
    print("POST /resume/upload-url 테스트")
    print("="*60)
    
    url = f'{API_BASE_URL}/resume/upload-url'
    print(f"URL: {url}")
    
    try:
        response = requests.post(
            url,
            json={
                'file_name': 'test_resume.pdf',
                'content_type': 'application/pdf'
            },
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"상태 코드: {response.status_code}")
        print(f"CORS 헤더:")
        for key, value in response.headers.items():
            if 'Access-Control' in key:
                print(f"  {key}: {value}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ 성공!")
            print(f"  upload_url: {data.get('upload_url', '')[:80]}...")
            print(f"  file_key: {data.get('file_key', '')}")
            return True, data.get('file_key')
        else:
            print(f"✗ 실패: {response.text[:200]}")
            return False, None
            
    except Exception as e:
        print(f"✗ 에러: {str(e)}")
        return False, None

def test_resume_parse(file_key):
    """이력서 파싱 테스트"""
    print("\n" + "="*60)
    print("POST /resume/parse 테스트")
    print("="*60)
    
    if not file_key:
        print("✗ file_key가 없습니다")
        return False
    
    url = f'{API_BASE_URL}/resume/parse'
    print(f"URL: {url}")
    print(f"file_key: {file_key}")
    
    try:
        response = requests.post(
            url,
            json={'file_key': file_key},
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"상태 코드: {response.status_code}")
        print(f"CORS 헤더:")
        for key, value in response.headers.items():
            if 'Access-Control' in key:
                print(f"  {key}: {value}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ 성공!")
            print(f"  employee_name: {data.get('employee_name', 'N/A')}")
            print(f"  overall_score: {data.get('overall_score', 'N/A')}")
            return True
        else:
            print(f"✗ 실패: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"✗ 에러: {str(e)}")
        return False

def main():
    """메인 함수"""
    print("="*60)
    print("이력서 API 테스트")
    print("="*60)
    
    # 1. 업로드 URL 생성 테스트
    success1, file_key = test_resume_upload_url()
    
    # 2. 이력서 파싱 테스트 (실제 파일이 없으므로 에러 예상)
    # success2 = test_resume_parse(file_key)
    
    print("\n" + "="*60)
    print("테스트 결과")
    print("="*60)
    print(f"POST /resume/upload-url: {'✓ 성공' if success1 else '✗ 실패'}")
    # print(f"POST /resume/parse: {'✓ 성공' if success2 else '✗ 실패'}")
    
    print("\n다음 단계:")
    print("1. 브라우저 캐시 완전 삭제 (Ctrl+Shift+Delete)")
    print("2. 시크릿 모드로 프론트엔드 접속")
    print("3. 인력 평가 → 이력서 업로드 탭")
    print("4. PDF 파일 업로드 테스트")
    print(f"\n프론트엔드 URL: http://hr-resource-optimization-frontend-hosting-prod.s3-website.us-east-2.amazonaws.com/")
    print()

if __name__ == '__main__':
    main()

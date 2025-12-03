"""
모든 API 엔드포인트 테스트
"""
import requests
import json

API_BASE_URL = 'https://ifeniowvpb.execute-api.us-east-2.amazonaws.com/prod'

def test_endpoint(method, path, data=None):
    """API 엔드포인트 테스트"""
    url = f'{API_BASE_URL}{path}'
    print(f"\n{'='*60}")
    print(f"{method} {path}")
    print(f"{'='*60}")
    print(f"URL: {url}")
    
    try:
        if method == 'GET':
            response = requests.get(url)
        elif method == 'POST':
            response = requests.post(url, json=data, headers={'Content-Type': 'application/json'})
        elif method == 'DELETE':
            response = requests.delete(url)
        
        print(f"상태 코드: {response.status_code}")
        print(f"응답 헤더:")
        for key, value in response.headers.items():
            if 'Access-Control' in key:
                print(f"  {key}: {value}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"✓ 성공!")
                if isinstance(data, dict):
                    for key in list(data.keys())[:5]:  # 처음 5개 키만 표시
                        print(f"  {key}: {str(data[key])[:100]}")
                return True
            except:
                print(f"✓ 성공! (JSON 아님)")
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
    print("모든 API 엔드포인트 테스트")
    print("="*60)
    
    results = {}
    
    # 1. Dashboard Metrics
    results['dashboard_metrics'] = test_endpoint('GET', '/dashboard/metrics')
    
    # 2. Employees List
    results['employees_list'] = test_endpoint('GET', '/employees')
    
    # 3. Projects List
    results['projects_list'] = test_endpoint('GET', '/projects')
    
    # 4. Pending Candidates List
    results['pending_candidates'] = test_endpoint('GET', '/pending-candidates')
    
    # 5. Domain Analysis
    results['domain_analysis'] = test_endpoint('POST', '/domain-analysis', {
        'analysis_type': 'current'
    })
    
    # 6. Quantitative Analysis (테스트 user_id 필요)
    # results['quantitative'] = test_endpoint('POST', '/quantitative-analysis', {
    #     'user_id': 'test-user-id'
    # })
    
    # 7. Recommendations (테스트 project_id 필요)
    # results['recommendations'] = test_endpoint('POST', '/recommendations', {
    #     'project_id': 'test-project-id'
    # })
    
    # 결과 요약
    print("\n" + "="*60)
    print("테스트 결과 요약")
    print("="*60)
    
    success = sum(1 for v in results.values() if v)
    total = len(results)
    
    for name, result in results.items():
        status = "✓ 성공" if result else "✗ 실패"
        print(f"{name:30} {status}")
    
    print(f"\n총 {success}/{total}개 성공")
    
    if success == total:
        print("\n🎉 모든 API가 정상 작동합니다!")
    else:
        print(f"\n⚠️  {total - success}개 API에 문제가 있습니다.")
    
    print("\n다음 단계:")
    print("1. 브라우저 캐시 완전 삭제 (Ctrl+Shift+Delete)")
    print("2. 시크릿 모드로 프론트엔드 접속")
    print("3. F12 개발자 도구 열기")
    print("4. Network 탭에서 API 호출 확인")
    print(f"\n프론트엔드 URL: http://hr-resource-optimization-frontend-hosting-prod.s3-website.us-east-2.amazonaws.com/")
    print()

if __name__ == '__main__':
    main()

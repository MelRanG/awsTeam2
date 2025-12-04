"""
추천 엔진 Lambda 함수 업데이트 - 고급 알고리즘 기반 추천 근거
"""

import boto3
import zipfile
import os
import io

def update_recommendation_engine():
    """추천 엔진 Lambda 함수 업데이트"""
    
    lambda_client = boto3.client('lambda', region_name='us-east-2')
    
    print("=" * 60)
    print("추천 엔진 Lambda 함수 업데이트")
    print("=" * 60)
    
    # 1. Lambda 함수 코드 압축
    print("\n1. Lambda 함수 코드 압축 중...")
    
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        lambda_path = 'lambda_functions/recommendation_engine/index.py'
        zip_file.write(lambda_path, 'index.py')
    
    zip_buffer.seek(0)
    print("  ✓ 코드 압축 완료")
    
    # 2. Lambda 함수 업데이트
    print("\n2. Lambda 함수 업데이트 중...")
    
    try:
        response = lambda_client.update_function_code(
            FunctionName='ProjectRecommendationEngine',
            ZipFile=zip_buffer.read()
        )
        
        print(f"  ✓ 함수 업데이트 완료")
        print(f"  - 함수명: {response['FunctionName']}")
        print(f"  - 버전: {response['Version']}")
        print(f"  - 상태: {response['State']}")
        
    except Exception as e:
        print(f"  ✗ 업데이트 실패: {str(e)}")
        return False
    
    print("\n" + "=" * 60)
    print("✅ 추천 엔진 업데이트 완료!")
    print("=" * 60)
    print("\n고급 알고리즘 기반 추천 근거:")
    print("  1. 적합도 점수 산정 (Feature Engineering)")
    print("     - Score(P,E) = Σ(Smatch × Wlevel × Wrecency) + (Expdomain × Wdomain)")
    print("  2. 추천 알고리즘 (Content-based Filtering)")
    print("     - 기술 매칭 및 벡터 유사도")
    print("  3. 하이브리드 점수 (벡터 + 필터링)")
    print("     - 팀 친밀도 및 가용성 반영")
    print("  4. 최종 추천 근거 생성")
    
    return True

if __name__ == '__main__':
    update_recommendation_engine()

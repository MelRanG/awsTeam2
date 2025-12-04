"""
TechTrends 테이블 확인
"""

import boto3
import json

def check_techtrends():
    """TechTrends 테이블 확인"""
    
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    
    print("=" * 60)
    print("TechTrends 테이블 확인")
    print("=" * 60)
    
    try:
        table = dynamodb.Table('TechTrends')
        
        # 테이블 정보 확인
        print("\n1. 테이블 정보:")
        print(f"  테이블명: {table.table_name}")
        print(f"  상태: {table.table_status}")
        
        # 데이터 조회
        print("\n2. 데이터 조회 중...")
        response = table.scan(Limit=10)
        
        items = response.get('Items', [])
        print(f"  ✓ {len(items)}개 데이터 발견")
        
        if items:
            print("\n【TechTrends 데이터 샘플】")
            for i, item in enumerate(items[:5], 1):
                print(f"\n  {i}. {item.get('trend_name', 'N/A')}")
                print(f"     - 카테고리: {item.get('category', 'N/A')}")
                print(f"     - 성장률: {item.get('growth_rate', 'N/A')}")
                print(f"     - 관련 기술: {item.get('related_skills', [])}")
                print(f"     - 시장 규모: {item.get('market_size', 'N/A')}")
        
        # 전체 데이터 수 확인
        print("\n3. 전체 데이터 수 확인 중...")
        response = table.scan(Select='COUNT')
        total_count = response.get('Count', 0)
        print(f"  ✓ 전체 {total_count}개 트렌드 데이터")
        
    except Exception as e:
        print(f"\n✗ 테이블 확인 실패: {str(e)}")
        print("\nTechTrends 테이블이 존재하지 않거나 접근 권한이 없습니다.")
    
    print("\n" + "=" * 60)

if __name__ == '__main__':
    check_techtrends()

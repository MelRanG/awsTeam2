"""
TechTrends 테이블 상세 확인
"""

import boto3
import json

def view_techtrends():
    """TechTrends 테이블 상세 확인"""
    
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    
    print("=" * 60)
    print("TechTrends 테이블 상세 확인")
    print("=" * 60)
    
    try:
        table = dynamodb.Table('TechTrends')
        
        # 전체 데이터 조회
        response = table.scan()
        items = response.get('Items', [])
        
        print(f"\n전체 {len(items)}개 트렌드 데이터")
        
        if items:
            # 첫 번째 아이템의 전체 구조 확인
            print("\n【첫 번째 아이템 전체 구조】")
            print(json.dumps(items[0], indent=2, default=str, ensure_ascii=False))
            
            # 모든 필드 이름 수집
            all_fields = set()
            for item in items:
                all_fields.update(item.keys())
            
            print(f"\n【사용 가능한 필드 목록】")
            for field in sorted(all_fields):
                print(f"  - {field}")
            
            # 카테고리별 그룹화
            print("\n【카테고리별 트렌드】")
            categories = {}
            for item in items:
                category = item.get('category', 'Unknown')
                if category not in categories:
                    categories[category] = []
                categories[category].append(item)
            
            for category, trends in sorted(categories.items()):
                print(f"\n  {category} ({len(trends)}개)")
                for trend in trends[:3]:
                    # 가능한 이름 필드 찾기
                    name = trend.get('trend_name') or trend.get('name') or trend.get('technology') or trend.get('skill_name') or 'N/A'
                    growth = trend.get('growth_rate', 'N/A')
                    print(f"    - {name}: 성장률 {growth}%")
        
    except Exception as e:
        print(f"\n✗ 오류: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)

if __name__ == '__main__':
    view_techtrends()

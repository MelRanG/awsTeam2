"""
대기자 명단에서 중복 데이터 정리
"""
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('Employees')

print("="*60)
print("대기자 명단 조회 및 중복 정리")
print("="*60)

# 1. 현재 대기자 목록 조회
print("\n1. 현재 대기자 목록 조회 중...")
response = table.scan(
    FilterExpression='attribute_exists(#status) AND #status = :status',
    ExpressionAttributeNames={'#status': 'status'},
    ExpressionAttributeValues={':status': 'pending'}
)

candidates = response['Items']
print(f"✅ 총 {len(candidates)}명의 대기자 발견\n")

# 2. 이름별로 그룹화
from collections import defaultdict
name_groups = defaultdict(list)

for candidate in candidates:
    name = candidate.get('name', '이름없음')
    name_groups[name].append(candidate)

# 3. 중복 확인 및 표시
print("="*60)
print("대기자 목록:")
print("="*60)

duplicates = []
for name, items in name_groups.items():
    print(f"\n👤 {name} ({len(items)}명)")
    for idx, item in enumerate(items, 1):
        user_id = item.get('user_id', 'N/A')
        email = item.get('email', 'N/A')
        created = item.get('created_at', 'N/A')
        has_questions = 'verification_questions' in item
        questions_count = len(item.get('verification_questions', [])) if has_questions else 0
        
        print(f"  [{idx}] ID: {user_id}")
        print(f"      이메일: {email}")
        print(f"      생성일: {created}")
        print(f"      검증질문: {questions_count}개")
        
        if len(items) > 1:
            duplicates.append({
                'name': name,
                'user_id': user_id,
                'email': email,
                'created_at': created,
                'questions_count': questions_count
            })

# 4. 최정우 중복 데이터 삭제
print("\n" + "="*60)
print("최정우 중복 데이터 삭제")
print("="*60)

choi_items = name_groups.get('최정우', [])
if len(choi_items) > 1:
    print(f"\n최정우 {len(choi_items)}명 발견")
    
    # 생성일 기준으로 정렬 (오래된 것부터)
    choi_items_sorted = sorted(choi_items, key=lambda x: x.get('created_at', ''))
    
    # 가장 최근 것만 남기고 나머지 삭제
    to_keep = choi_items_sorted[-1]
    to_delete = choi_items_sorted[:-1]
    
    print(f"\n✅ 유지할 데이터:")
    print(f"   ID: {to_keep.get('user_id')}")
    print(f"   생성일: {to_keep.get('created_at')}")
    print(f"   검증질문: {len(to_keep.get('verification_questions', []))}개")
    
    print(f"\n🗑️  삭제할 데이터 ({len(to_delete)}개):")
    for item in to_delete:
        user_id = item.get('user_id')
        created = item.get('created_at')
        print(f"   - ID: {user_id}, 생성일: {created}")
        
        try:
            table.delete_item(Key={'user_id': user_id})
            print(f"     ✅ 삭제 완료")
        except Exception as e:
            print(f"     ❌ 삭제 실패: {str(e)}")
    
    print(f"\n✅ 최정우 중복 데이터 정리 완료!")
else:
    print(f"\n최정우는 {len(choi_items)}명만 있습니다 (중복 없음)")

# 5. 최종 확인
print("\n" + "="*60)
print("정리 후 대기자 목록")
print("="*60)

response = table.scan(
    FilterExpression='attribute_exists(#status) AND #status = :status',
    ExpressionAttributeNames={'#status': 'status'},
    ExpressionAttributeValues={':status': 'pending'}
)

final_candidates = response['Items']
print(f"\n✅ 총 {len(final_candidates)}명의 대기자")

final_name_groups = defaultdict(list)
for candidate in final_candidates:
    name = candidate.get('name', '이름없음')
    final_name_groups[name].append(candidate)

for name, items in sorted(final_name_groups.items()):
    print(f"  - {name}: {len(items)}명")

print("\n" + "="*60)
print("정리 완료!")
print("="*60)

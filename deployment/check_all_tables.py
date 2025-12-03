"""
모든 테이블에서 최정우 데이터 확인 및 삭제
"""
import boto3
from collections import defaultdict

dynamodb = boto3.resource('dynamodb', region_name='us-east-2')

print("="*60)
print("DynamoDB 테이블 확인")
print("="*60)

# 1. Employees 테이블 확인
print("\n[1] Employees 테이블")
print("-"*60)
employees_table = dynamodb.Table('Employees')

try:
    # status='pending'인 항목 조회
    response = employees_table.scan(
        FilterExpression='attribute_exists(#status) AND #status = :status',
        ExpressionAttributeNames={'#status': 'status'},
        ExpressionAttributeValues={':status': 'pending'}
    )
    pending_employees = response['Items']
    print(f"✅ status='pending'인 직원: {len(pending_employees)}명")
    
    for emp in pending_employees:
        name = emp.get('name', 'N/A')
        user_id = emp.get('user_id', 'N/A')
        email = emp.get('email', 'N/A')
        print(f"  - {name} (ID: {user_id}, Email: {email})")
    
    # 최정우 검색
    choi_in_employees = [e for e in pending_employees if e.get('name') == '최정우']
    if choi_in_employees:
        print(f"\n🔍 최정우 발견: {len(choi_in_employees)}명")
        for idx, emp in enumerate(choi_in_employees, 1):
            print(f"  [{idx}] ID: {emp.get('user_id')}, Email: {emp.get('email')}")
    
except Exception as e:
    print(f"❌ Employees 테이블 조회 실패: {str(e)}")

# 2. PendingCandidates 테이블 확인
print("\n[2] PendingCandidates 테이블")
print("-"*60)

try:
    pending_table = dynamodb.Table('PendingCandidates')
    response = pending_table.scan()
    pending_candidates = response['Items']
    print(f"✅ 대기자: {len(pending_candidates)}명")
    
    name_groups = defaultdict(list)
    for candidate in pending_candidates:
        name = candidate.get('name', 'N/A')
        name_groups[name].append(candidate)
    
    for name, items in sorted(name_groups.items()):
        print(f"  - {name}: {len(items)}명")
        for item in items:
            candidate_id = item.get('candidate_id', 'N/A')
            email = item.get('email', 'N/A')
            created = item.get('created_at', 'N/A')
            print(f"    · ID: {candidate_id}, Email: {email}, 생성: {created}")
    
    # 최정우 검색 및 삭제
    choi_items = name_groups.get('최정우', [])
    if len(choi_items) > 1:
        print(f"\n🗑️  최정우 중복 데이터 삭제 ({len(choi_items)}명)")
        
        # 생성일 기준 정렬 (최신 것만 유지)
        choi_sorted = sorted(choi_items, key=lambda x: x.get('created_at', ''))
        to_keep = choi_sorted[-1]
        to_delete = choi_sorted[:-1]
        
        print(f"\n✅ 유지: ID={to_keep.get('candidate_id')}, 생성={to_keep.get('created_at')}")
        
        for item in to_delete:
            candidate_id = item.get('candidate_id')
            created = item.get('created_at')
            print(f"\n🗑️  삭제 중: ID={candidate_id}, 생성={created}")
            
            try:
                pending_table.delete_item(Key={'candidate_id': candidate_id})
                print(f"   ✅ 삭제 완료")
            except Exception as e:
                print(f"   ❌ 삭제 실패: {str(e)}")
        
        print(f"\n✅ 최정우 중복 데이터 정리 완료!")
    elif len(choi_items) == 1:
        print(f"\n✅ 최정우는 1명만 있습니다 (중복 없음)")
    else:
        print(f"\n⚠️  최정우를 찾을 수 없습니다")
        
except Exception as e:
    print(f"❌ PendingCandidates 테이블 조회 실패: {str(e)}")

# 3. 최종 확인
print("\n" + "="*60)
print("최종 대기자 목록")
print("="*60)

try:
    pending_table = dynamodb.Table('PendingCandidates')
    response = pending_table.scan()
    final_candidates = response['Items']
    
    print(f"\n✅ 총 {len(final_candidates)}명의 대기자")
    
    final_name_groups = defaultdict(list)
    for candidate in final_candidates:
        name = candidate.get('name', 'N/A')
        final_name_groups[name].append(candidate)
    
    for name, items in sorted(final_name_groups.items()):
        print(f"  - {name}: {len(items)}명")
        
except Exception as e:
    print(f"❌ 최종 확인 실패: {str(e)}")

print("\n" + "="*60)
print("완료!")
print("="*60)

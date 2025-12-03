"""
PendingCandidates 상세 정보 확인
"""
import boto3
import json

dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
pending_table = dynamodb.Table('PendingCandidates')

print("="*60)
print("PendingCandidates 상세 정보")
print("="*60)

response = pending_table.scan()
candidates = response['Items']

print(f"\n총 {len(candidates)}명의 대기자\n")

for idx, candidate in enumerate(candidates, 1):
    print(f"\n{'='*60}")
    print(f"[{idx}] 대기자 정보")
    print(f"{'='*60}")
    
    # 기본 정보
    candidate_id = candidate.get('candidate_id', 'N/A')
    print(f"Candidate ID: {candidate_id}")
    
    # 모든 키 출력
    for key, value in sorted(candidate.items()):
        if key == 'evaluation_data':
            print(f"\n{key}:")
            if isinstance(value, dict):
                # 이름 찾기
                name = value.get('employee_name') or value.get('name') or 'N/A'
                print(f"  - employee_name: {name}")
                print(f"  - overall_score: {value.get('overall_score', 'N/A')}")
                print(f"  - experience_years: {value.get('experience_years', 'N/A')}")
            else:
                print(f"  {value}")
        elif key == 'verification_questions':
            questions = value if isinstance(value, list) else []
            print(f"\n{key}: {len(questions)}개")
        elif key == 'basic_info':
            print(f"\n{key}:")
            if isinstance(value, dict):
                for k, v in value.items():
                    print(f"  - {k}: {v}")
        else:
            # 값이 너무 길면 축약
            str_value = str(value)
            if len(str_value) > 100:
                str_value = str_value[:100] + "..."
            print(f"{key}: {str_value}")

print("\n" + "="*60)
print("이름 추출 시도")
print("="*60)

for idx, candidate in enumerate(candidates, 1):
    candidate_id = candidate.get('candidate_id', 'N/A')
    
    # 여러 위치에서 이름 찾기
    name = None
    
    # 1. 직접 name 필드
    if 'name' in candidate:
        name = candidate['name']
    
    # 2. basic_info.name
    elif 'basic_info' in candidate and isinstance(candidate['basic_info'], dict):
        name = candidate['basic_info'].get('name')
    
    # 3. evaluation_data.employee_name
    elif 'evaluation_data' in candidate and isinstance(candidate['evaluation_data'], dict):
        name = candidate['evaluation_data'].get('employee_name')
    
    print(f"[{idx}] ID: {candidate_id} → 이름: {name or 'N/A'}")

print("\n" + "="*60)
print("최정우 검색 및 삭제")
print("="*60)

choi_items = []
for candidate in candidates:
    candidate_id = candidate.get('candidate_id')
    
    # 이름 찾기
    name = (
        candidate.get('name') or
        (candidate.get('basic_info', {}).get('name') if isinstance(candidate.get('basic_info'), dict) else None) or
        (candidate.get('evaluation_data', {}).get('employee_name') if isinstance(candidate.get('evaluation_data'), dict) else None)
    )
    
    if name and '최정우' in name:
        choi_items.append({
            'candidate_id': candidate_id,
            'name': name,
            'data': candidate
        })

if choi_items:
    print(f"\n🔍 최정우 발견: {len(choi_items)}명")
    
    for idx, item in enumerate(choi_items, 1):
        print(f"\n[{idx}] ID: {item['candidate_id']}")
        print(f"    이름: {item['name']}")
        
        # 생성일 확인
        created = item['data'].get('created_at', 'N/A')
        print(f"    생성일: {created}")
    
    if len(choi_items) > 1:
        print(f"\n🗑️  중복 데이터 삭제 시작...")
        
        # 생성일 기준 정렬
        choi_sorted = sorted(choi_items, key=lambda x: x['data'].get('created_at', ''))
        to_keep = choi_sorted[-1]
        to_delete = choi_sorted[:-1]
        
        print(f"\n✅ 유지: {to_keep['candidate_id']}")
        
        for item in to_delete:
            candidate_id = item['candidate_id']
            print(f"\n🗑️  삭제: {candidate_id}")
            
            try:
                pending_table.delete_item(Key={'candidate_id': candidate_id})
                print(f"   ✅ 삭제 완료")
            except Exception as e:
                print(f"   ❌ 삭제 실패: {str(e)}")
        
        print(f"\n✅ 최정우 중복 데이터 정리 완료!")
    else:
        print(f"\n✅ 최정우는 1명만 있습니다")
else:
    print("\n⚠️  최정우를 찾을 수 없습니다")
    print("\n모든 대기자 삭제를 원하시면 별도로 요청해주세요.")

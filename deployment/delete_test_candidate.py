"""
테스트 대기자 삭제
"""
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('PendingCandidates')

print("=" * 60)
print("테스트 대기자 삭제")
print("=" * 60)

# 모든 대기자 조회
response = table.scan()
candidates = response.get('Items', [])

print(f"\n총 {len(candidates)}명의 대기자")

# 테스트 데이터 찾기 (이름이 "테스트"인 것)
for candidate in candidates:
    name = candidate.get('basic_info', {}).get('name', candidate.get('name', 'N/A'))
    candidate_id = candidate.get('candidate_id', 'N/A')
    
    if name == '테스트' or name == 'N/A':
        print(f"\n삭제 대상: {name} (ID: {candidate_id})")
        try:
            table.delete_item(Key={'candidate_id': candidate_id})
            print(f"  ✓ 삭제 완료")
        except Exception as e:
            print(f"  ✗ 삭제 실패: {e}")

print("\n완료!")

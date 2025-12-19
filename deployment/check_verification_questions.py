"""
대기자 명단의 검증 질문 확인
"""
import boto3
import json

dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('PendingCandidates')

print("=" * 60)
print("대기자 명단 검증 질문 확인")
print("=" * 60)

response = table.scan()
candidates = response.get('Items', [])

print(f"\n총 {len(candidates)}명의 대기자")

for candidate in candidates:
    name = candidate.get('name', 'N/A')
    candidate_id = candidate.get('candidate_id', 'N/A')
    questions = candidate.get('verification_questions', [])
    questions_time = candidate.get('questions_generated_at', 'N/A')
    
    print(f"\n이름: {name}")
    print(f"  - ID: {candidate_id}")
    print(f"  - 검증 질문: {len(questions)}개")
    print(f"  - 생성 시간: {questions_time}")
    
    if questions:
        print(f"  - 첫 번째 질문: {questions[0].get('question', 'N/A')[:50]}...")

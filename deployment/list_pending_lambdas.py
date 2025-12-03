"""
Pending 관련 Lambda 함수 목록 확인
"""
import boto3

lambda_client = boto3.client('lambda', region_name='us-east-2')

print("="*60)
print("Pending 관련 Lambda 함수 목록")
print("="*60)

response = lambda_client.list_functions()

pending_functions = []
for func in response['Functions']:
    name = func['FunctionName']
    if 'pending' in name.lower() or 'candidate' in name.lower():
        pending_functions.append(func)

if pending_functions:
    print(f"\n✅ {len(pending_functions)}개 발견:\n")
    for func in pending_functions:
        print(f"  - {func['FunctionName']}")
        print(f"    런타임: {func['Runtime']}")
        print(f"    핸들러: {func['Handler']}")
        print()
else:
    print("\n⚠️  Pending 관련 Lambda 함수를 찾을 수 없습니다")

print("\n모든 Lambda 함수 목록:")
print("-"*60)
for func in response['Functions']:
    print(f"  - {func['FunctionName']}")

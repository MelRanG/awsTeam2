import json
import boto3
from decimal import Decimal

def convert_to_decimal(obj):
    if isinstance(obj, list):
        return [convert_to_decimal(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: convert_to_decimal(v) for k, v in obj.items()}
    elif isinstance(obj, float):
        return Decimal(str(obj))
    return obj

dynamodb = boto3.resource('dynamodb', region_name='us-east-2')

# 1. Company Events
print("=== 회사 이벤트 데이터 로드 ===")
try:
    with open('../test_data/company_events.json', 'r', encoding='utf-8') as f:
        events = json.load(f)
    table = dynamodb.Table('CompanyEvents')
    for event in events:
        table.put_item(Item=convert_to_decimal(event))
    print(f"✓ {len(events)}개 이벤트 로드 완료")
except Exception as e:
    print(f"✗ 이벤트 로드 실패: {e}")

# 2. Employee Affinity
print("\n=== 직원 친밀도 데이터 로드 ===")
try:
    with open('../test_data/employee_affinity_data.json', 'r', encoding='utf-8') as f:
        affinity = json.load(f)
    table = dynamodb.Table('EmployeeAffinity')
    for aff in affinity:
        table.put_item(Item=convert_to_decimal(aff))
    print(f"✓ {len(affinity)}개 친밀도 데이터 로드 완료")
except Exception as e:
    print(f"✗ 친밀도 로드 실패: {e}")

# 3. Messenger Logs
print("\n=== 메신저 로그 데이터 로드 ===")
try:
    with open('../test_data/messenger_logs_anonymized.json', 'r', encoding='utf-8') as f:
        logs = json.load(f)
    table = dynamodb.Table('MessengerLogs')
    count = 0
    for log in logs[:100]:  # 처음 100개만
        table.put_item(Item=convert_to_decimal(log))
        count += 1
    print(f"✓ {count}개 메신저 로그 로드 완료")
except Exception as e:
    print(f"✗ 메신저 로그 로드 실패: {e}")

print("\n=== 모든 데이터 로드 완료! ===")

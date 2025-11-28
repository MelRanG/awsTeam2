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

# DynamoDB 연결
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('Employees')

# 데이터 로드
with open('../test_data/employees_extended.json', 'r', encoding='utf-8') as f:
    employees = json.load(f)

# 데이터 삽입
count = 0
for emp in employees:
    emp_converted = convert_to_decimal(emp)
    table.put_item(Item=emp_converted)
    count += 1
    print(f"Loaded employee {count}: {emp.get('basic_info', {}).get('name', 'Unknown')}")

print(f"\n총 {count}명의 직원 데이터 로드 완료!")

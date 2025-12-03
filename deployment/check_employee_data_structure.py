"""
Employees 테이블 데이터 구조 확인
"""
import boto3
import json
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('Employees')

print("=" * 60)
print("Employees 테이블 데이터 구조 확인")
print("=" * 60)

# 첫 번째 직원 데이터 가져오기
response = table.scan(Limit=1)
items = response.get('Items', [])

if items:
    employee = items[0]
    print("\n첫 번째 직원 데이터 구조:")
    print(json.dumps(employee, indent=2, cls=DecimalEncoder, ensure_ascii=False))
    
    print("\n\n사용 가능한 필드:")
    for key in employee.keys():
        print(f"  - {key}: {type(employee[key]).__name__}")
else:
    print("데이터가 없습니다.")

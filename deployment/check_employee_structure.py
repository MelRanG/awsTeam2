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
print("직원 데이터 구조 확인")
print("=" * 60)

try:
    response = table.scan(Limit=3)
    items = response.get('Items', [])
    
    if items:
        print(f"\n총 {len(items)}개 샘플 데이터:")
        for i, item in enumerate(items, 1):
            print(f"\n직원 {i}:")
            print(json.dumps(item, indent=2, ensure_ascii=False, cls=DecimalEncoder))
            print("\n주요 필드:")
            print(f"  - employeeId: {item.get('employeeId')}")
            print(f"  - name: {item.get('name')}")
            print(f"  - role: {item.get('role')}")
            print(f"  - yearsOfExperience: {item.get('yearsOfExperience')}")
            print(f"  - department: {item.get('department')}")
            print(f"  - basic_info: {item.get('basic_info')}")
    else:
        print("\n데이터가 없습니다.")
        
except Exception as e:
    print(f"\n✗ 에러: {str(e)}")
    import traceback
    traceback.print_exc()

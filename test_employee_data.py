import boto3
import json

dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('Employees')

response = table.scan(Limit=2)

print('직원 데이터 샘플 (전체 구조):')
for item in response.get('Items', []):
    print(json.dumps(item, indent=2, ensure_ascii=False, default=str))

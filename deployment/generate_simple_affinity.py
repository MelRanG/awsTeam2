"""
간단한 친밀도 데이터 생성
"""
import boto3
import random
from decimal import Decimal

dynamodb = boto3.resource('dynamodb', region_name='us-east-2')

def generate_affinity_data():
    """모든 직원에 대한 친밀도 데이터 생성"""
    print("=" * 60)
    print("친밀도 데이터 생성")
    print("=" * 60)
    
    # 1. 직원 목록 조회
    print("\n1. 직원 목록 조회 중...")
    employees_table = dynamodb.Table('Employees')
    response = employees_table.scan(ProjectionExpression='user_id')
    
    employee_ids = [item['user_id'] for item in response.get('Items', [])]
    
    while 'LastEvaluatedKey' in response:
        response = employees_table.scan(
            ProjectionExpression='user_id',
            ExclusiveStartKey=response['LastEvaluatedKey']
        )
        employee_ids.extend([item['user_id'] for item in response.get('Items', [])])
    
    print(f"  ✓ 총 {len(employee_ids)}명의 직원 발견")
    
    # 2. EmployeeAffinity 테이블 생성 또는 확인
    print("\n2. EmployeeAffinity 테이블 확인 중...")
    try:
        affinity_table = dynamodb.Table('EmployeeAffinity')
        affinity_table.load()
        print("  ✓ 테이블 존재")
    except:
        print("  → 테이블이 없습니다. 생성 중...")
        dynamodb_client = boto3.client('dynamodb', region_name='us-east-2')
        dynamodb_client.create_table(
            TableName='EmployeeAffinity',
            KeySchema=[
                {'AttributeName': 'affinity_id', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'affinity_id', 'AttributeType': 'S'}
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        print("  ✓ 테이블 생성 완료")
        
        # 테이블 활성화 대기
        import time
        time.sleep(10)
        affinity_table = dynamodb.Table('EmployeeAffinity')
    
    # 3. 친밀도 데이터 생성
    print("\n3. 친밀도 데이터 생성 중...")
    records = []
    
    for i, emp1_id in enumerate(employee_ids):
        # 각 직원당 10-15명과 친밀도 생성
        num_connections = min(random.randint(10, 15), len(employee_ids) - 1)
        other_employees = [e for e in employee_ids if e != emp1_id]
        selected = random.sample(other_employees, min(num_connections, len(other_employees)))
        
        for emp2_id in selected:
            # 중복 방지 (emp1 < emp2)
            if emp1_id > emp2_id:
                continue
            
            # 친밀도 점수 생성 (50-85점)
            score = Decimal(str(round(random.uniform(50, 85), 2)))
            
            record = {
                'affinity_id': f"AFF_{emp1_id}_{emp2_id}",
                'employee_pair': {
                    'employee_1': emp1_id,
                    'employee_2': emp2_id
                },
                'overall_affinity_score': score,
                'project_collaboration': {
                    'collaboration_score': Decimal(str(round(random.uniform(40, 80), 2)))
                },
                'messenger_communication': {
                    'communication_score': Decimal(str(round(random.uniform(50, 90), 2)))
                },
                'company_events': {
                    'social_score': Decimal(str(round(random.uniform(30, 70), 2)))
                },
                'personal_closeness': {
                    'personal_score': Decimal(str(round(random.uniform(20, 60), 2)))
                }
            }
            records.append(record)
        
        if (i + 1) % 50 == 0:
            print(f"  → {i + 1}/{len(employee_ids)} 직원 처리 완료")
    
    print(f"  ✓ 총 {len(records)}개의 친밀도 데이터 생성")
    
    # 4. DynamoDB에 저장
    print("\n4. DynamoDB에 저장 중...")
    saved_count = 0
    batch_size = 25
    
    for i in range(0, len(records), batch_size):
        batch = records[i:i + batch_size]
        
        with affinity_table.batch_writer() as writer:
            for record in batch:
                writer.put_item(Item=record)
                saved_count += 1
        
        if saved_count % 100 == 0:
            print(f"  → {saved_count}/{len(records)} 저장 완료")
    
    print(f"  ✓ 총 {saved_count}개 저장 완료")
    
    print("\n" + "=" * 60)
    print("✅ 친밀도 데이터 생성 완료!")
    print("=" * 60)
    print(f"\n통계:")
    print(f"  - 전체 직원 수: {len(employee_ids)}명")
    print(f"  - 생성된 친밀도 데이터: {len(records)}개")
    print(f"  - 직원당 평균 연결: {len(records) * 2 / len(employee_ids):.1f}명")

if __name__ == '__main__':
    generate_affinity_data()

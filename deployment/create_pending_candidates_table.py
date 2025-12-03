#!/usr/bin/env python3
"""
대기자 명단 DynamoDB 테이블 생성
"""
import boto3

def create_pending_candidates_table():
    """PendingCandidates 테이블 생성"""
    dynamodb = boto3.client('dynamodb', region_name='us-east-2')
    
    table_name = 'PendingCandidates'
    
    print("=" * 60)
    print(f"{table_name} 테이블 생성")
    print("=" * 60)
    
    try:
        # 테이블이 이미 존재하는지 확인
        try:
            dynamodb.describe_table(TableName=table_name)
            print(f"✓ {table_name} 테이블이 이미 존재합니다")
            return True
        except dynamodb.exceptions.ResourceNotFoundException:
            pass
        
        # 테이블 생성
        print(f"\n{table_name} 테이블 생성 중...")
        response = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'candidate_id',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'candidate_id',
                    'AttributeType': 'S'
                }
            ],
            BillingMode='PAY_PER_REQUEST',
            Tags=[
                {
                    'Key': 'Environment',
                    'Value': 'Production'
                },
                {
                    'Key': 'Project',
                    'Value': 'HR-Resource-Optimization'
                }
            ]
        )
        
        print(f"✓ {table_name} 테이블 생성 요청 완료")
        print(f"  상태: {response['TableDescription']['TableStatus']}")
        
        # 테이블이 활성화될 때까지 대기
        print("\n테이블 활성화 대기 중...")
        waiter = dynamodb.get_waiter('table_exists')
        waiter.wait(TableName=table_name)
        
        print(f"✅ {table_name} 테이블이 성공적으로 생성되었습니다!")
        return True
        
    except Exception as e:
        print(f"❌ 테이블 생성 실패: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    create_pending_candidates_table()

#!/usr/bin/env python3
"""
Employees 테이블에서 status='pending'인 데이터 삭제
"""
import boto3

def cleanup_pending_employees():
    """status='pending'인 직원 삭제"""
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    employees_table = dynamodb.Table('Employees')
    
    print("=" * 60)
    print("Employees 테이블에서 대기자 데이터 삭제")
    print("=" * 60)
    
    try:
        # 전체 직원 스캔
        print("\n1. 전체 직원 조회 중...")
        response = employees_table.scan()
        all_employees = response['Items']
        
        # status='pending'인 직원 필터링
        pending_employees = [emp for emp in all_employees if emp.get('status') == 'pending']
        
        print(f"  ✓ 전체 직원: {len(all_employees)}명")
        print(f"  ✓ 대기자: {len(pending_employees)}명")
        
        if len(pending_employees) == 0:
            print("\n삭제할 대기자가 없습니다.")
            return True
        
        # 대기자 삭제
        print(f"\n2. {len(pending_employees)}명의 대기자 삭제 중...")
        for emp in pending_employees:
            user_id = emp['user_id']
            name = emp.get('basic_info', {}).get('name', 'Unknown')
            
            employees_table.delete_item(Key={'user_id': user_id})
            print(f"  ✓ 삭제: {name} ({user_id})")
        
        print(f"\n✅ {len(pending_employees)}명의 대기자가 삭제되었습니다!")
        return True
        
    except Exception as e:
        print(f"\n❌ 에러 발생: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    cleanup_pending_employees()

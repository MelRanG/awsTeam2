"""
가용한 직원 찾기
"""

import boto3

def find_available():
    """가용한 직원 찾기"""
    
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    table = dynamodb.Table('Employees')
    
    print("=" * 60)
    print("가용한 직원 찾기")
    print("=" * 60)
    
    # 모든 직원 조회
    response = table.scan()
    employees = response.get('Items', [])
    
    print(f"\n전체 직원 수: {len(employees)}명")
    
    # 가용한 직원 찾기
    available_employees = []
    
    for emp in employees:
        user_id = emp.get('user_id')
        name = emp.get('basic_info', {}).get('name', 'N/A')
        role = emp.get('basic_info', {}).get('role', 'N/A')
        current_project = emp.get('current_project')
        
        if not current_project:
            available_employees.append({
                'user_id': user_id,
                'name': name,
                'role': role
            })
    
    print(f"가용한 직원 수: {len(available_employees)}명")
    
    if available_employees:
        print("\n【가용한 직원 목록】")
        for i, emp in enumerate(available_employees[:10], 1):
            print(f"{i}. {emp['name']} ({emp['user_id']}) - {emp['role']}")
        
        if len(available_employees) > 10:
            print(f"... 외 {len(available_employees) - 10}명")
    else:
        print("\n⚠ 가용한 직원이 없습니다")

if __name__ == '__main__':
    find_available()

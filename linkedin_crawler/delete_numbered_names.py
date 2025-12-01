"""
이름에 숫자가 포함된 직원 데이터 삭제
예: 김민준1, 이서준2 등
"""
import boto3
import re

def delete_numbered_names():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    table = dynamodb.Table('Employees')
    
    print("Employees 테이블에서 데이터 조회 중...")
    
    # 모든 직원 조회
    response = table.scan()
    employees = response.get('Items', [])
    
    # 페이지네이션 처리
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        employees.extend(response.get('Items', []))
    
    print(f"총 {len(employees)}명 조회 완료\n")
    
    # 이름에 숫자가 포함된 직원 찾기
    to_delete = []
    for emp in employees:
        name = emp.get('basic_info', {}).get('name', '')
        # 이름에 숫자가 있는지 확인
        if re.search(r'\d', name):
            to_delete.append({
                'user_id': emp.get('user_id'),
                'name': name
            })
    
    if not to_delete:
        print("삭제할 데이터가 없습니다.")
        return
    
    print(f"이름에 숫자가 포함된 직원: {len(to_delete)}명")
    print("\n삭제 시작...")
    deleted = 0
    failed = 0
    
    for emp in to_delete:
        try:
            table.delete_item(Key={'user_id': emp['user_id']})
            deleted += 1
            print(f"✓ {emp['name']} 삭제 완료")
        except Exception as e:
            failed += 1
            print(f"✗ {emp['name']} 삭제 실패: {e}")
    
    print(f"\n완료: 삭제 {deleted}개, 실패 {failed}개")

if __name__ == '__main__':
    delete_numbered_names()

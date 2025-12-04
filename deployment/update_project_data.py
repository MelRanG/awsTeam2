"""
프로젝트 데이터 업데이트 스크립트
- 진행 중인 프로젝트: 기간 업데이트 (2025 ~ 2026)
- 완료된 프로젝트: 투입 인력 배정
"""
import boto3
import random
from datetime import datetime, timedelta

dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
projects_table = dynamodb.Table('Projects')
employees_table = dynamodb.Table('Employees')

# 직원 목록 조회
def get_all_employees():
    """모든 직원 조회"""
    response = employees_table.scan()
    return response.get('Items', [])

# 프로젝트 상태 결정
def determine_project_status(project_name):
    """프로젝트 이름 기반으로 상태 결정"""
    # 일부는 완료, 일부는 진행 중으로 설정
    completed_keywords = ['EMR', '환자 관리', '품질 관리', '예지 보전', '의료 데이터']
    
    for keyword in completed_keywords:
        if keyword in project_name:
            return 'completed'
    
    return 'in-progress'

# 날짜 생성
def generate_dates(status):
    """상태에 따라 날짜 생성"""
    if status == 'completed':
        # 완료된 프로젝트: 2024년 시작 ~ 2024년 종료
        start_month = random.randint(1, 6)
        end_month = random.randint(start_month + 3, 12)
        start_date = f"2024-{start_month:02d}-{random.randint(1, 28):02d}"
        end_date = f"2024-{end_month:02d}-{random.randint(1, 28):02d}"
    else:
        # 진행 중인 프로젝트: 2025년 시작 ~ 2026년 종료
        start_month = random.randint(1, 12)
        end_month = random.randint(1, 12)
        start_date = f"2025-{start_month:02d}-{random.randint(1, 28):02d}"
        end_date = f"2026-{end_month:02d}-{random.randint(1, 28):02d}"
    
    return start_date, end_date

# 프로젝트에 인력 배정
def assign_employees_to_project(project_id, project_name, employees, num_members):
    """프로젝트에 직원 배정"""
    # 랜덤하게 직원 선택
    selected_employees = random.sample(employees, min(num_members, len(employees)))
    
    assigned_members = []
    for emp in selected_employees:
        # 직원 데이터 구조에 맞게 추출
        employee_id = emp.get('user_id', '')
        basic_info = emp.get('basic_info', {})
        name = basic_info.get('name', '이름 없음') if isinstance(basic_info, dict) else '이름 없음'
        
        assigned_members.append({
            'employee_id': employee_id,
            'name': name,
            'role': random.choice(['개발자', '시니어 개발자', '리드 개발자', 'PM'])
        })
    
    return assigned_members

# 메인 업데이트 함수
def update_projects():
    """모든 프로젝트 업데이트"""
    # 프로젝트 조회
    response = projects_table.scan()
    projects = response.get('Items', [])
    
    # 직원 조회
    employees = get_all_employees()
    
    print(f"총 {len(projects)}개 프로젝트 업데이트 시작...")
    print(f"사용 가능한 직원 수: {len(employees)}명\n")
    
    updated_count = 0
    
    for project in projects:
        project_id = project.get('project_id')
        project_name = project.get('project_name', '')
        
        # 상태 결정
        status = determine_project_status(project_name)
        
        # 날짜 생성
        start_date, end_date = generate_dates(status)
        
        # 업데이트할 데이터
        update_data = {
            'project_id': project_id,
            'project_name': project_name,
            'status': status,
            'period': {
                'start': start_date,
                'end': end_date
            }
        }
        
        # 완료된 프로젝트에만 인력 배정
        if status == 'completed' and employees:
            num_members = random.randint(3, 7)
            assigned_members = assign_employees_to_project(
                project_id, project_name, employees, num_members
            )
            update_data['assigned_members'] = assigned_members
            update_data['required_members'] = num_members
            
            print(f"✓ {project_name}")
            print(f"  상태: {status}")
            print(f"  기간: {start_date} ~ {end_date}")
            print(f"  투입 인력: {len(assigned_members)}명")
        else:
            # 진행 중인 프로젝트
            update_data['assigned_members'] = []
            update_data['required_members'] = random.randint(5, 10)
            
            print(f"✓ {project_name}")
            print(f"  상태: {status}")
            print(f"  기간: {start_date} ~ {end_date}")
            print(f"  필요 인력: {update_data['required_members']}명")
        
        # 기존 데이터 유지
        if 'tech_stack' in project:
            update_data['tech_stack'] = project['tech_stack']
        if 'description' in project:
            update_data['description'] = project['description']
        if 'client_industry' in project:
            update_data['client_industry'] = project['client_industry']
        
        # DynamoDB 업데이트
        try:
            projects_table.put_item(Item=update_data)
            updated_count += 1
        except Exception as e:
            print(f"  ✗ 업데이트 실패: {str(e)}")
        
        print()
    
    print(f"\n총 {updated_count}개 프로젝트가 업데이트되었습니다.")

if __name__ == '__main__':
    update_projects()

"""
프로젝트 중복 확인 및 제거 스크립트
"""
import boto3
from collections import Counter
import json

def check_and_remove_duplicates():
    """프로젝트 중복 확인 및 제거"""
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    table = dynamodb.Table('Projects')
    
    # 모든 프로젝트 조회
    response = table.scan()
    items = response.get('Items', [])
    
    print(f"\n=== 프로젝트 중복 분석 ===")
    print(f"총 프로젝트 수: {len(items)}")
    
    # project_id 중복 확인
    project_ids = [item.get('project_id') for item in items]
    id_counter = Counter(project_ids)
    duplicates = {k: v for k, v in id_counter.items() if v > 1}
    
    print(f"고유 프로젝트 ID 수: {len(set(project_ids))}")
    print(f"중복된 프로젝트 ID: {duplicates}")
    
    # project_name으로 중복 확인
    project_names = [item.get('project_name', '') for item in items]
    name_counter = Counter(project_names)
    name_duplicates = {k: v for k, v in name_counter.items() if v > 1}
    
    print(f"\n중복된 프로젝트 이름:")
    for name, count in name_duplicates.items():
        print(f"  - '{name}': {count}개")
        
        # 해당 이름을 가진 프로젝트들 찾기
        matching_projects = [item for item in items if item.get('project_name') == name]
        print(f"    프로젝트 ID들:")
        for proj in matching_projects:
            print(f"      * {proj.get('project_id')} (생성일: {proj.get('created_at', 'N/A')})")
    
    # 중복 제거 여부 확인
    if name_duplicates:
        print(f"\n총 {sum(name_duplicates.values()) - len(name_duplicates)}개의 중복 프로젝트 발견")
        
        # 자동으로 중복 제거 실행
        remove_duplicates(table, items, name_duplicates)
    else:
        print("\n중복된 프로젝트가 없습니다.")

def remove_duplicates(table, items, name_duplicates):
    """중복 프로젝트 제거 (가장 최근 것만 남김)"""
    removed_count = 0
    
    for name in name_duplicates.keys():
        # 해당 이름을 가진 모든 프로젝트 찾기
        matching_projects = [item for item in items if item.get('project_name') == name]
        
        # created_at 기준으로 정렬 (최신 것이 마지막)
        sorted_projects = sorted(
            matching_projects, 
            key=lambda x: x.get('created_at', ''), 
            reverse=False
        )
        
        # 가장 최근 것을 제외한 나머지 삭제
        for proj in sorted_projects[:-1]:
            project_id = proj.get('project_id')
            try:
                table.delete_item(Key={'project_id': project_id})
                print(f"삭제됨: {name} (ID: {project_id})")
                removed_count += 1
            except Exception as e:
                print(f"삭제 실패: {project_id} - {str(e)}")
    
    print(f"\n총 {removed_count}개의 중복 프로젝트가 제거되었습니다.")

if __name__ == '__main__':
    check_and_remove_duplicates()

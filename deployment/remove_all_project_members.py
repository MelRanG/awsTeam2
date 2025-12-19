"""
모든 프로젝트에서 팀원 제거
"""
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
projects_table = dynamodb.Table('Projects')

def remove_all_team_members():
    """모든 프로젝트의 팀원 제거"""
    print("=" * 60)
    print("프로젝트 팀원 제거")
    print("=" * 60)
    
    # 1. 모든 프로젝트 조회
    print("\n1. 프로젝트 목록 조회 중...")
    response = projects_table.scan()
    projects = response['Items']
    
    while 'LastEvaluatedKey' in response:
        response = projects_table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        projects.extend(response['Items'])
    
    print(f"  ✓ 총 {len(projects)}개 프로젝트 발견")
    
    # 2. 팀원이 있는 프로젝트 확인
    projects_with_members = []
    total_members = 0
    
    for project in projects:
        team_members = project.get('team_members', [])
        if team_members:
            projects_with_members.append(project)
            total_members += len(team_members)
    
    print(f"  ✓ 팀원이 있는 프로젝트: {len(projects_with_members)}개")
    print(f"  ✓ 총 팀원 수: {total_members}명")
    
    if not projects_with_members:
        print("\n✅ 제거할 팀원이 없습니다.")
        return
    
    # 3. 팀원 제거
    print("\n2. 팀원 제거 중...")
    removed_count = 0
    
    for project in projects_with_members:
        project_id = project['project_id']
        project_name = project.get('project_name', 'Unknown')
        member_count = len(project.get('team_members', []))
        
        # team_members를 빈 리스트로 업데이트
        projects_table.update_item(
            Key={'project_id': project_id},
            UpdateExpression='SET team_members = :empty_list',
            ExpressionAttributeValues={
                ':empty_list': []
            }
        )
        
        removed_count += member_count
        print(f"  ✓ {project_name}: {member_count}명 제거")
    
    print(f"\n  ✓ 총 {removed_count}명 제거 완료")
    
    # 4. 확인
    print("\n3. 제거 확인 중...")
    response = projects_table.scan()
    projects = response['Items']
    
    remaining_members = 0
    for project in projects:
        remaining_members += len(project.get('team_members', []))
    
    print(f"  ✓ 남은 팀원 수: {remaining_members}명")
    
    print("\n" + "=" * 60)
    print("✅ 팀원 제거 완료!")
    print("=" * 60)

if __name__ == '__main__':
    remove_all_team_members()

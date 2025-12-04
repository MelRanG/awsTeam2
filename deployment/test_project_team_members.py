"""
프로젝트 팀 멤버 표시 테스트
"""

import boto3
import json

def test_team_members():
    """프로젝트 팀 멤버 확인"""
    
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    lambda_client = boto3.client('lambda', region_name='us-east-2')
    
    print("=" * 60)
    print("프로젝트 팀 멤버 표시 테스트")
    print("=" * 60)
    
    # 1. DynamoDB에서 직접 확인
    print("\n1. DynamoDB에서 프로젝트 확인...")
    
    table = dynamodb.Table('Projects')
    response = table.scan()
    
    projects_with_members = []
    for project in response.get('Items', []):
        team_members = project.get('team_members', [])
        if team_members:
            projects_with_members.append({
                'project_id': project.get('project_id'),
                'project_name': project.get('project_name'),
                'team_members_count': len(team_members),
                'team_members': team_members
            })
    
    print(f"  ✓ 팀 멤버가 있는 프로젝트: {len(projects_with_members)}개")
    
    if projects_with_members:
        print("\n【팀 멤버가 있는 프로젝트】")
        for proj in projects_with_members[:5]:
            print(f"\n  프로젝트: {proj['project_name']} ({proj['project_id']})")
            print(f"  팀 멤버 수: {proj['team_members_count']}명")
            for member in proj['team_members']:
                print(f"    - {member.get('employee_id')}: {member.get('role')} (투입률: {member.get('allocation_rate', 0)}%)")
    
    # 2. Lambda 함수 호출 테스트
    print("\n2. Lambda 함수 호출 테스트...")
    
    try:
        response = lambda_client.invoke(
            FunctionName='ProjectsList',
            InvocationType='RequestResponse',
            Payload=json.dumps({
                'httpMethod': 'GET'
            })
        )
        
        result = json.loads(response['Payload'].read())
        
        if result['statusCode'] == 200:
            body = json.loads(result['body'])
            projects = body.get('projects', [])
            
            print(f"  ✓ 전체 프로젝트 수: {len(projects)}개")
            
            # assigned_members가 있는 프로젝트 확인
            projects_with_assigned = [p for p in projects if p.get('assigned_members')]
            
            print(f"  ✓ 배정된 멤버가 있는 프로젝트: {len(projects_with_assigned)}개")
            
            if projects_with_assigned:
                print("\n【Lambda 응답 - 배정된 멤버가 있는 프로젝트】")
                for proj in projects_with_assigned[:5]:
                    print(f"\n  프로젝트: {proj['project_name']} ({proj['project_id']})")
                    print(f"  배정된 멤버 수: {len(proj['assigned_members'])}명")
                    print(f"  필요 인력: {proj.get('required_members', 0)}명")
        else:
            print(f"  ✗ Lambda 호출 실패: {result}")
            
    except Exception as e:
        print(f"  ✗ 테스트 실패: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("✅ 테스트 완료!")
    print("=" * 60)

if __name__ == '__main__':
    test_team_members()

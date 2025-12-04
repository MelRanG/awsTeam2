"""
직원들에게 신규 도메인 관련 기술 추가
30-40명에게 게임, 핀테크, AI/ML, 자동차, 에너지, 보험, 부동산 등의 기술 추가
"""
import boto3
import random

dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('Employees')

# 신규 도메인 기술 정의
new_domain_skills = {
    '게임/엔터테인먼트': [
        {'name': 'Unity', 'level': 'Advanced'},
        {'name': 'Unreal Engine', 'level': 'Intermediate'},
        {'name': 'C#', 'level': 'Advanced'},
        {'name': 'C++', 'level': 'Intermediate'},
    ],
    '핀테크': [
        {'name': 'Stripe', 'level': 'Intermediate'},
        {'name': 'Plaid', 'level': 'Intermediate'},
        {'name': 'Solidity', 'level': 'Beginner'},
        {'name': 'Blockchain', 'level': 'Intermediate'},
    ],
    'AI/ML': [
        {'name': 'ChatGPT API', 'level': 'Intermediate'},
        {'name': 'LangChain', 'level': 'Advanced'},
        {'name': 'Stable Diffusion', 'level': 'Beginner'},
        {'name': 'TensorFlow', 'level': 'Advanced'},
        {'name': 'PyTorch', 'level': 'Advanced'},
    ],
    '자동차/모빌리티': [
        {'name': 'AUTOSAR', 'level': 'Intermediate'},
        {'name': 'ROS', 'level': 'Advanced'},
        {'name': 'C++', 'level': 'Advanced'},
        {'name': 'Embedded Systems', 'level': 'Intermediate'},
    ],
    '에너지': [
        {'name': 'Smart Grid', 'level': 'Intermediate'},
        {'name': 'Battery Management System', 'level': 'Advanced'},
        {'name': 'IoT', 'level': 'Advanced'},
        {'name': 'Python', 'level': 'Advanced'},
    ],
    '보험': [
        {'name': 'Actuarial Analytics', 'level': 'Advanced'},
        {'name': 'Telematics', 'level': 'Intermediate'},
        {'name': 'Python', 'level': 'Advanced'},
        {'name': 'R', 'level': 'Intermediate'},
    ],
    '부동산': [
        {'name': 'GIS', 'level': 'Advanced'},
        {'name': 'BIM', 'level': 'Intermediate'},
        {'name': 'Python', 'level': 'Advanced'},
        {'name': 'PostgreSQL', 'level': 'Intermediate'},
    ],
    '미디어': [
        {'name': 'Next.js', 'level': 'Advanced'},
        {'name': 'GraphQL', 'level': 'Advanced'},
        {'name': 'IPFS', 'level': 'Beginner'},
        {'name': 'FFmpeg', 'level': 'Intermediate'},
    ],
}

# 모든 직원 조회
response = table.scan()
employees = response.get('Items', [])

print(f"총 직원 수: {len(employees)}명")
print("\n신규 도메인 기술 추가 중...")
print("=" * 80)

# 랜덤하게 35명 선택
selected_employees = random.sample(employees, min(35, len(employees)))

updated_count = 0
domain_distribution = {domain: 0 for domain in new_domain_skills.keys()}

for i, employee in enumerate(selected_employees):
    user_id = employee.get('user_id')
    current_skills = employee.get('skills', [])
    
    # 각 직원에게 1-2개 도메인의 기술 추가
    num_domains = random.randint(1, 2)
    selected_domains = random.sample(list(new_domain_skills.keys()), num_domains)
    
    new_skills = []
    for domain in selected_domains:
        # 해당 도메인에서 2-3개 기술 선택
        num_skills = random.randint(2, 3)
        domain_skills = random.sample(new_domain_skills[domain], min(num_skills, len(new_domain_skills[domain])))
        new_skills.extend(domain_skills)
        domain_distribution[domain] += 1
    
    # 기존 기술과 중복 제거
    existing_skill_names = {skill.get('name') for skill in current_skills if isinstance(skill, dict)}
    unique_new_skills = [skill for skill in new_skills if skill['name'] not in existing_skill_names]
    
    if unique_new_skills:
        updated_skills = current_skills + unique_new_skills
        
        try:
            table.update_item(
                Key={'user_id': user_id},
                UpdateExpression='SET skills = :skills',
                ExpressionAttributeValues={':skills': updated_skills}
            )
            updated_count += 1
            print(f"✓ {user_id}: {', '.join([s['name'] for s in unique_new_skills])}")
        except Exception as e:
            print(f"✗ {user_id} 업데이트 실패: {str(e)}")

print("\n" + "=" * 80)
print(f"업데이트 완료: {updated_count}명")
print("\n도메인별 인력 분포:")
for domain, count in sorted(domain_distribution.items(), key=lambda x: x[1], reverse=True):
    print(f"  - {domain}: {count}명")

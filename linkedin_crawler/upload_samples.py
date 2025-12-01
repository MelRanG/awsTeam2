"""
미리 생성된 샘플 데이터를 DynamoDB에 업로드
"""
import boto3
import json
import uuid
from decimal import Decimal

# 샘플 데이터 생성
def generate_sample_data():
    samples = []
    
    names = ["김민준", "이서준", "박도윤", "최시우", "정주원", "강하준", "조지호", "윤지후", "임준서", "한건우"]
    companies = ["네이버", "카카오", "쿠팡", "토스", "배달의민족", "라인", "당근마켓", "야놀자", "직방", "무신사"]
    
    for i in range(100):
        user_id = f"EMP_{uuid.uuid4().hex[:8].upper()}"
        name = names[i % len(names)] + str(i // len(names) + 1)
        years = (i % 10) + 1
        
        if years <= 3:
            role = "Backend Developer"
        elif years <= 5:
            role = "Senior Backend Developer"
        else:
            role = "Lead Backend Developer"
        
        sample = {
            "user_id": user_id,
            "basic_info": {
                "name": name,
                "role": role,
                "years_of_experience": years,
                "email": f"{user_id.lower()}@example.com"
            },
            "self_introduction": f"{years}년차 개발자입니다.",
            "skills": [
                {"name": "Java", "level": "Advanced", "years": min(years, 5)},
                {"name": "Spring", "level": "Advanced", "years": min(years, 4)},
                {"name": "Docker", "level": "Intermediate", "years": min(years, 3)}
            ],
            "work_experience": [{
                "project_id": f"PROJ_{uuid.uuid4().hex[:8].upper()}",
                "project_name": f"{companies[i % len(companies)]} - 프로젝트",
                "role": role,
                "duration": f"2020-01 ~ 2024-12",
                "main_tasks": ["백엔드 개발"],
                "performance_result": "성공적으로 완료"
            }],
            "education": {
                "degree": "Computer Science, BS",
                "university": "서울대학교"
            },
            "certifications": [],
            "source": "sample",
            "location": "Seoul, South Korea"
        }
        
        samples.append(sample)
    
    return samples

# DynamoDB 업로드
def upload_to_dynamodb(samples):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    table = dynamodb.Table('Employees')
    
    success = 0
    failed = 0
    
    for sample in samples:
        try:
            # Decimal 변환
            sample_decimal = json.loads(json.dumps(sample), parse_float=Decimal)
            table.put_item(Item=sample_decimal)
            success += 1
            print(f"✓ {sample['basic_info']['name']} 업로드 성공")
        except Exception as e:
            failed += 1
            print(f"✗ {sample['basic_info']['name']} 실패: {e}")
    
    print(f"\n완료: 성공 {success}개, 실패 {failed}개")

if __name__ == '__main__':
    print("샘플 데이터 생성 중...")
    samples = generate_sample_data()
    print(f"{len(samples)}개 생성 완료\n")
    
    print("DynamoDB 업로드 시작...")
    upload_to_dynamodb(samples)

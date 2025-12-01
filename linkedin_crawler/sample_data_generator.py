"""
샘플 데이터 생성기
LinkedIn 계정 없이 테스트용 프로필 데이터 생성
"""

import random
import json
from typing import List, Dict, Any
from dynamodb_uploader import DynamoDBUploader
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SampleDataGenerator:
    """샘플 프로필 데이터 생성기"""
    
    def __init__(self):
        # 성씨 50개 + 이름 100개 조합 = 5000개 가능
        self.last_names = [
            "김", "이", "박", "최", "정", "강", "조", "윤", "장", "임",
            "한", "오", "서", "신", "권", "황", "안", "송", "류", "전",
            "홍", "고", "문", "양", "손", "배", "백", "허", "남", "심",
            "노", "하", "곽", "성", "차", "주", "우", "구", "신", "라",
            "전", "민", "유", "진", "지", "엄", "채", "원", "천", "방"
        ]
        
        self.first_names = [
            "민준", "서준", "예준", "도윤", "시우", "주원", "하준", "지호", "지후", "준서",
            "건우", "우진", "선우", "연우", "유준", "정우", "승우", "승현", "시윤", "준혁",
            "은우", "지환", "승민", "지훈", "현우", "예성", "민재", "현준", "인우", "시후",
            "서연", "서윤", "지우", "서현", "민서", "하은", "하윤", "윤서", "지유", "채원",
            "지민", "수아", "지아", "다은", "예은", "소율", "수빈", "예린", "지안", "채은",
            "수현", "민지", "지원", "예나", "하린", "유나", "서아", "은서", "가은", "나은",
            "소연", "지수", "예지", "수진", "민경", "혜진", "은지", "지영", "수영", "미영",
            "동현", "상현", "재현", "태현", "민호", "준호", "진호", "성호", "영호", "철수",
            "영수", "광수", "명수", "성수", "태수", "진수", "동수", "상수", "재수", "준수",
            "영희", "순희", "미희", "정희", "선희", "경희", "은희", "지희", "수희", "혜원"
        ]
        
        self.companies = [
            # IT 대기업
            "네이버", "카카오", "라인", "쿠팡", "배달의민족", "토스", "당근마켓",
            "야놀자", "직방", "무신사", "마켓컬리", "컬리", "오늘의집", "번개장터",
            "29CM", "지그재그", "에이블리", "크림", "발란", "W컨셉",
            
            # 대기업
            "삼성전자", "삼성SDS", "삼성물산", "LG전자", "LG CNS", "LG유플러스",
            "SK텔레콤", "SK하이닉스", "SK C&C", "KT", "KT DS", "현대자동차",
            "현대모비스", "기아", "포스코", "롯데정보통신", "신세계I&C", "CJ올리브네트웍스",
            
            # 금융
            "KB국민은행", "신한은행", "하나은행", "우리은행", "NH농협은행",
            "카카오뱅크", "토스뱅크", "케이뱅크", "삼성증권", "미래에셋증권",
            
            # 게임
            "넷마블", "엔씨소프트", "넥슨", "넥슨코리아", "크래프톤", "펄어비스",
            "컴투스", "스마일게이트", "게임빌", "카카오게임즈",
            
            # 스타트업
            "두나무", "비바리퍼블리카", "센드버드", "하이퍼커넥트", "리디",
            "왓챠", "플렉스", "뱅크샐러드", "핀다", "어니스트펀드",
            "8퍼센트", "렌딧", "피플펀드", "테라펀딩", "와디즈",
            "텀블벅", "오픈서베이", "리멤버", "원티드", "로켓펀치",
            
            # 외국계
            "구글코리아", "마이크로소프트", "아마존웹서비스", "메타", "애플코리아",
            "오라클", "SAP코리아", "IBM", "시스코", "VM웨어"
        ]
        
        self.roles = {
            'junior': [
                'Junior Backend Developer',
                'Junior Frontend Developer',
                'Backend Developer',
                'Frontend Developer'
            ],
            'mid': [
                'Backend Developer',
                'Senior Backend Developer',
                'Frontend Developer',
                'Senior Frontend Developer',
                'Full Stack Developer'
            ],
            'senior': [
                'Senior Backend Developer',
                'Senior Frontend Developer',
                'Lead Backend Developer',
                'Lead Frontend Developer',
                'Software Architect',
                'DevOps Engineer'
            ]
        }
        
        self.backend_skills = [
            # 언어
            'Java', 'Python', 'Go', 'Kotlin', 'Scala', 'C++', 'C#', 'Ruby', 'PHP', 'Rust',
            # 프레임워크
            'Spring', 'Spring Boot', 'Spring Cloud', 'Django', 'Flask', 'FastAPI',
            'Node.js', 'Express', 'NestJS', 'Koa', 'Ruby on Rails', 'Laravel', 'ASP.NET',
            # 데이터베이스
            'PostgreSQL', 'MySQL', 'MariaDB', 'Oracle', 'MS SQL Server',
            'MongoDB', 'Cassandra', 'DynamoDB', 'Redis', 'Memcached', 'Elasticsearch',
            # 메시징
            'Kafka', 'RabbitMQ', 'ActiveMQ', 'AWS SQS', 'AWS SNS', 'Google Pub/Sub',
            # 컨테이너/오케스트레이션
            'Docker', 'Kubernetes', 'Docker Compose', 'Helm', 'Istio',
            # 클라우드
            'AWS', 'GCP', 'Azure', 'AWS Lambda', 'AWS ECS', 'AWS EKS', 'AWS RDS',
            'AWS S3', 'AWS CloudFront', 'AWS API Gateway', 'AWS DynamoDB',
            # 아키텍처
            'Microservices', 'REST API', 'GraphQL', 'gRPC', 'WebSocket',
            'Event-Driven Architecture', 'CQRS', 'DDD', 'Hexagonal Architecture',
            # 기타
            'JPA', 'Hibernate', 'MyBatis', 'SQLAlchemy', 'Prisma', 'TypeORM'
        ]
        
        self.frontend_skills = [
            # 프레임워크/라이브러리
            'React', 'Vue.js', 'Angular', 'Svelte', 'Next.js', 'Nuxt.js', 'Gatsby',
            'React Native', 'Flutter', 'Ionic', 'Electron',
            # 언어
            'TypeScript', 'JavaScript', 'HTML5', 'CSS3', 'Sass', 'SCSS', 'Less',
            # 상태관리
            'Redux', 'Redux Toolkit', 'MobX', 'Recoil', 'Zustand', 'Jotai',
            'Vuex', 'Pinia', 'NgRx', 'Context API',
            # 빌드/번들러
            'Webpack', 'Vite', 'Rollup', 'Parcel', 'esbuild', 'Turbopack',
            # UI 라이브러리
            'Tailwind CSS', 'Material-UI', 'Ant Design', 'Chakra UI', 'Bootstrap',
            'Styled Components', 'Emotion', 'CSS Modules',
            # 테스팅
            'Jest', 'React Testing Library', 'Cypress', 'Playwright', 'Vitest',
            'Storybook', 'Chromatic',
            # 기타
            'GraphQL', 'Apollo Client', 'React Query', 'SWR', 'Axios',
            'Webpack Module Federation', 'Micro Frontends', 'PWA', 'SEO'
        ]
        
        self.common_skills = [
            'Git', 'GitHub', 'GitLab', 'Bitbucket', 'SVN',
            'Jira', 'Confluence', 'Notion', 'Slack', 'Teams',
            'Agile', 'Scrum', 'Kanban', 'XP',
            'CI/CD', 'Jenkins', 'GitHub Actions', 'GitLab CI', 'CircleCI', 'Travis CI',
            'Linux', 'Ubuntu', 'CentOS', 'Shell Script', 'Bash',
            'Nginx', 'Apache', 'Tomcat',
            'Monitoring', 'Prometheus', 'Grafana', 'ELK Stack', 'Datadog', 'New Relic',
            'Terraform', 'Ansible', 'CloudFormation',
            'TDD', 'BDD', 'Code Review', 'Pair Programming',
            'RESTful API', 'API Design', 'Swagger', 'OpenAPI'
        ]
        
        self.universities = [
            '서울대학교', '연세대학교', '고려대학교', 'KAIST',
            '성균관대학교', '한양대학교', '중앙대학교', '경희대학교',
            '이화여자대학교', '서강대학교', '부산대학교', '전남대학교'
        ]
        
        self.degrees = [
            'Computer Science, BS',
            'Computer Engineering, BS',
            'Software Engineering, BS',
            'Information Systems, BS',
            'Computer Science, MS'
        ]
    
    def generate_profiles(self, count: int = 100) -> List[Dict[str, Any]]:
        """
        샘플 프로필 생성
        
        Args:
            count: 생성할 프로필 수
            
        Returns:
            프로필 리스트
        """
        profiles = []
        
        # 연차별 분포 (1-3년: 40%, 3-5년: 30%, 5-10년: 20%, 10년+: 10%)
        junior_count = int(count * 0.4)
        mid_count = int(count * 0.3)
        senior_count = int(count * 0.2)
        lead_count = count - junior_count - mid_count - senior_count
        
        logger.info(f"샘플 데이터 생성 시작: 총 {count}개")
        logger.info(f"  - 1-3년: {junior_count}명")
        logger.info(f"  - 3-5년: {mid_count}명")
        logger.info(f"  - 5-10년: {senior_count}명")
        logger.info(f"  - 10년+: {lead_count}명")
        
        # 주니어 (1-3년)
        for i in range(junior_count):
            years = random.randint(1, 3)
            profiles.append(self._generate_profile(years, 'junior'))
        
        # 미들 (3-5년)
        for i in range(mid_count):
            years = random.randint(3, 5)
            profiles.append(self._generate_profile(years, 'mid'))
        
        # 시니어 (5-10년)
        for i in range(senior_count):
            years = random.randint(5, 10)
            profiles.append(self._generate_profile(years, 'senior'))
        
        # 리드 (10년+)
        for i in range(lead_count):
            years = random.randint(10, 15)
            profiles.append(self._generate_profile(years, 'senior'))
        
        logger.info(f"샘플 데이터 생성 완료: {len(profiles)}개")
        return profiles
    
    def _generate_profile(self, years: int, level: str) -> Dict[str, Any]:
        """개별 프로필 생성"""
        # 이름 생성 (성 + 이름)
        name = random.choice(self.last_names) + random.choice(self.first_names)
        role = random.choice(self.roles[level])
        
        # 백엔드 vs 프론트엔드 결정
        is_backend = 'Backend' in role or 'Full Stack' in role or 'DevOps' in role
        is_frontend = 'Frontend' in role or 'Full Stack' in role
        
        # 기술 스택 생성
        skills = self.common_skills.copy()
        
        if is_backend:
            # 백엔드 기술 5-10개 추가
            backend_count = random.randint(5, 10)
            skills.extend(random.sample(self.backend_skills, backend_count))
        
        if is_frontend:
            # 프론트엔드 기술 5-8개 추가
            frontend_count = random.randint(5, 8)
            skills.extend(random.sample(self.frontend_skills, frontend_count))
        
        # 중복 제거
        skills = list(set(skills))
        
        # 경력 사항 생성
        experience = self._generate_experience(years, role)
        
        # 학력 생성
        education = [{
            'school': random.choice(self.universities),
            'degree': random.choice(self.degrees)
        }]
        
        # 자기소개 생성
        about = self._generate_about(years, role, skills[:5])
        
        profile = {
            'profile_url': f'https://linkedin.com/in/{name.lower().replace(" ", "-")}',
            'name': name,
            'headline': f'{role} at {random.choice(self.companies)}',
            'location': random.choice(['Seoul, South Korea', 'Gyeonggi, South Korea', 'Busan, South Korea']),
            'about': about,
            'years_of_experience': years,
            'current_role': role,
            'experience': experience,
            'education': education,
            'skills': skills
        }
        
        return profile
    
    def _generate_experience(self, total_years: int, role: str) -> List[Dict[str, Any]]:
        """경력 사항 생성"""
        experiences = []
        remaining_years = total_years
        current_year = 2024
        
        # 평균 2-3년마다 이직
        while remaining_years > 0:
            years_at_company = min(random.randint(2, 4), remaining_years)
            
            company = random.choice(self.companies)
            start_year = current_year - remaining_years
            end_year = start_year + years_at_company
            
            # 직책 결정
            if remaining_years == total_years:
                # 현재 직장
                job_role = role
                duration = f'{start_year}-01 ~ Present'
            else:
                # 이전 직장
                if years_at_company >= 3:
                    job_role = role
                else:
                    job_role = role.replace('Senior ', '').replace('Lead ', '')
                duration = f'{start_year}-01 ~ {end_year}-12'
            
            description = self._generate_job_description(job_role)
            
            experiences.append({
                'title': job_role,
                'company': company,
                'duration': f'{years_at_company} yrs',
                'description': description
            })
            
            remaining_years -= years_at_company
        
        return experiences
    
    def _generate_job_description(self, role: str) -> str:
        """직무 설명 생성"""
        descriptions = {
            'Backend': [
                'RESTful API 설계 및 개발',
                '마이크로서비스 아키텍처 구축',
                '데이터베이스 설계 및 최적화',
                '대용량 트래픽 처리 시스템 개발',
                '레거시 시스템 리팩토링'
            ],
            'Frontend': [
                '사용자 인터페이스 개발',
                '반응형 웹 애플리케이션 구축',
                '성능 최적화 및 번들 사이즈 개선',
                '컴포넌트 라이브러리 개발',
                '크로스 브라우저 호환성 확보'
            ],
            'Full Stack': [
                '풀스택 웹 애플리케이션 개발',
                '프론트엔드 및 백엔드 통합',
                'API 설계 및 구현',
                '데이터베이스 설계',
                '배포 자동화'
            ],
            'DevOps': [
                'CI/CD 파이프라인 구축',
                '인프라 자동화',
                '모니터링 시스템 구축',
                '컨테이너 오케스트레이션',
                '클라우드 인프라 관리'
            ]
        }
        
        for key, desc_list in descriptions.items():
            if key in role:
                return ' / '.join(random.sample(desc_list, min(3, len(desc_list))))
        
        return '소프트웨어 개발 및 유지보수'
    
    def _generate_about(self, years: int, role: str, top_skills: List[str]) -> str:
        """자기소개 생성"""
        skills_str = ', '.join(top_skills)
        
        templates = [
            f'{years}년차 {role}입니다. {skills_str} 등의 기술을 활용하여 다양한 프로젝트를 수행했습니다.',
            f'{skills_str}에 능숙한 {years}년 경력의 개발자입니다. 사용자 중심의 서비스 개발에 관심이 많습니다.',
            f'{role}로 {years}년간 근무하며 {skills_str} 기술 스택을 활용한 프로젝트를 진행했습니다.',
        ]
        
        return random.choice(templates)


def main():
    """메인 함수"""
    import argparse
    
    parser = argparse.ArgumentParser(description='샘플 프로필 데이터 생성 및 DynamoDB 업로드')
    parser.add_argument('--count', type=int, default=100, help='생성할 프로필 수')
    parser.add_argument('--output', default='sample_profiles.json', help='출력 파일명')
    parser.add_argument('--upload', action='store_true', help='DynamoDB에 업로드')
    parser.add_argument('--region', default='us-east-2', help='AWS 리전')
    
    args = parser.parse_args()
    
    # 샘플 데이터 생성
    generator = SampleDataGenerator()
    profiles = generator.generate_profiles(count=args.count)
    
    # JSON 파일로 저장
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(profiles, f, ensure_ascii=False, indent=2)
    logger.info(f"샘플 데이터 저장: {args.output}")
    
    # DynamoDB 업로드
    if args.upload:
        logger.info("\nDynamoDB 업로드 시작...")
        uploader = DynamoDBUploader(region=args.region)
        result = uploader.upload_profiles(profiles)
        
        logger.info("\n업로드 결과:")
        logger.info(f"  성공: {result['success']}개")
        logger.info(f"  실패: {result['failed']}개")
    
    logger.info("\n완료!")


if __name__ == '__main__':
    main()

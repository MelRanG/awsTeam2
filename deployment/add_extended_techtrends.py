"""
TechTrends 테이블에 확장 데이터 추가
2024-2025 최신 기술 트렌드 및 신규 산업 도메인
"""
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('TechTrends')

# 2024-2025 최신 기술 트렌드 데이터
extended_trends = [
    # === 신규 산업 도메인 ===
    
    # 게임/엔터테인먼트
    {
        'tech_name': 'Unity',
        'category': 'Gaming',
        'growth_rate': Decimal('18.5'),
        'demand_score': Decimal('82'),
        'trend_score': Decimal('88'),
        'related_domains': ['게임', '엔터테인먼트', '교육'],
        'description': '게임 엔진 및 실시간 3D 개발 플랫폼'
    },
    {
        'tech_name': 'Unreal Engine',
        'category': 'Gaming',
        'growth_rate': Decimal('22.3'),
        'demand_score': Decimal('85'),
        'trend_score': Decimal('90'),
        'related_domains': ['게임', '엔터테인먼트', '미디어'],
        'description': '고성능 게임 및 시각화 엔진'
    },
    
    # 핀테크/금융기술
    {
        'tech_name': 'Stripe',
        'category': 'FinTech',
        'growth_rate': Decimal('25.7'),
        'demand_score': Decimal('88'),
        'trend_score': Decimal('92'),
        'related_domains': ['핀테크', '전자상거래', '금융'],
        'description': '온라인 결제 플랫폼'
    },
    {
        'tech_name': 'Plaid',
        'category': 'FinTech',
        'growth_rate': Decimal('28.4'),
        'demand_score': Decimal('86'),
        'trend_score': Decimal('89'),
        'related_domains': ['핀테크', '금융'],
        'description': '금융 데이터 연동 API'
    },
    
    # 에너지/스마트그리드
    {
        'tech_name': 'Smart Grid',
        'category': 'Energy',
        'growth_rate': Decimal('15.8'),
        'demand_score': Decimal('78'),
        'trend_score': Decimal('82'),
        'related_domains': ['에너지', 'IoT', '제조'],
        'description': '스마트 전력망 관리 시스템'
    },
    {
        'tech_name': 'Battery Management System',
        'category': 'Energy',
        'growth_rate': Decimal('19.2'),
        'demand_score': Decimal('81'),
        'trend_score': Decimal('85'),
        'related_domains': ['에너지', '자동차', 'IoT'],
        'description': '배터리 관리 및 최적화 시스템'
    },
    
    # 자동차/모빌리티
    {
        'tech_name': 'AUTOSAR',
        'category': 'Automotive',
        'growth_rate': Decimal('16.5'),
        'demand_score': Decimal('79'),
        'trend_score': Decimal('83'),
        'related_domains': ['자동차', '제조', 'IoT'],
        'description': '자동차 소프트웨어 표준 플랫폼'
    },
    {
        'tech_name': 'ROS',
        'category': 'Automotive',
        'growth_rate': Decimal('21.8'),
        'demand_score': Decimal('84'),
        'trend_score': Decimal('87'),
        'related_domains': ['자동차', '로봇', 'IoT'],
        'description': '로봇 운영 체제'
    },
    
    # 부동산/프롭테크
    {
        'tech_name': 'GIS',
        'category': 'PropTech',
        'growth_rate': Decimal('14.2'),
        'demand_score': Decimal('76'),
        'trend_score': Decimal('80'),
        'related_domains': ['부동산', '물류', '공공'],
        'description': '지리정보시스템'
    },
    {
        'tech_name': 'BIM',
        'category': 'PropTech',
        'growth_rate': Decimal('17.6'),
        'demand_score': Decimal('80'),
        'trend_score': Decimal('84'),
        'related_domains': ['부동산', '건설', '제조'],
        'description': '건축정보모델링'
    },
    
    # 보험/인슈어테크
    {
        'tech_name': 'Actuarial Analytics',
        'category': 'InsurTech',
        'growth_rate': Decimal('13.8'),
        'demand_score': Decimal('75'),
        'trend_score': Decimal('78'),
        'related_domains': ['보험', '금융', 'AI/ML'],
        'description': '보험계리 분석'
    },
    {
        'tech_name': 'Telematics',
        'category': 'InsurTech',
        'growth_rate': Decimal('18.9'),
        'demand_score': Decimal('82'),
        'trend_score': Decimal('86'),
        'related_domains': ['보험', '자동차', 'IoT'],
        'description': '텔레매틱스 기반 보험'
    },
    
    # === 최신 기술 트렌드 ===
    
    # 생성형 AI
    {
        'tech_name': 'ChatGPT API',
        'category': 'AI_ML',
        'growth_rate': Decimal('45.2'),
        'demand_score': Decimal('95'),
        'trend_score': Decimal('98'),
        'related_domains': ['AI/ML', '교육', '전자상거래', '의료'],
        'description': '대화형 AI 서비스'
    },
    {
        'tech_name': 'Stable Diffusion',
        'category': 'AI_ML',
        'growth_rate': Decimal('38.7'),
        'demand_score': Decimal('91'),
        'trend_score': Decimal('94'),
        'related_domains': ['AI/ML', '미디어', '게임', '엔터테인먼트'],
        'description': '이미지 생성 AI'
    },
    {
        'tech_name': 'LangChain',
        'category': 'AI_ML',
        'growth_rate': Decimal('52.3'),
        'demand_score': Decimal('93'),
        'trend_score': Decimal('96'),
        'related_domains': ['AI/ML', '전자상거래', '금융', '의료'],
        'description': 'LLM 애플리케이션 프레임워크'
    },
    
    # 웹3/블록체인
    {
        'tech_name': 'Solidity',
        'category': 'Blockchain',
        'growth_rate': Decimal('24.5'),
        'demand_score': Decimal('79'),
        'trend_score': Decimal('85'),
        'related_domains': ['블록체인', '핀테크', '금융'],
        'description': '스마트 컨트랙트 개발 언어'
    },
    {
        'tech_name': 'IPFS',
        'category': 'Blockchain',
        'growth_rate': Decimal('19.8'),
        'demand_score': Decimal('76'),
        'trend_score': Decimal('81'),
        'related_domains': ['블록체인', '클라우드', '미디어'],
        'description': '분산 파일 시스템'
    },
    
    # 엣지 컴퓨팅
    {
        'tech_name': 'Edge Computing',
        'category': 'Cloud',
        'growth_rate': Decimal('26.4'),
        'demand_score': Decimal('87'),
        'trend_score': Decimal('90'),
        'related_domains': ['클라우드', 'IoT', '제조', '통신'],
        'description': '엣지 컴퓨팅 플랫폼'
    },
    {
        'tech_name': 'AWS IoT Greengrass',
        'category': 'Cloud',
        'growth_rate': Decimal('23.1'),
        'demand_score': Decimal('84'),
        'trend_score': Decimal('87'),
        'related_domains': ['클라우드', 'IoT', '제조'],
        'description': 'AWS 엣지 컴퓨팅 서비스'
    },
    
    # 데이터 엔지니어링
    {
        'tech_name': 'Apache Spark',
        'category': 'Data_Engineering',
        'growth_rate': Decimal('20.3'),
        'demand_score': Decimal('86'),
        'trend_score': Decimal('89'),
        'related_domains': ['데이터 엔지니어링', '금융', '전자상거래', '의료'],
        'description': '대규모 데이터 처리 프레임워크'
    },
    {
        'tech_name': 'Apache Kafka',
        'category': 'Data_Engineering',
        'growth_rate': Decimal('22.7'),
        'demand_score': Decimal('88'),
        'trend_score': Decimal('91'),
        'related_domains': ['데이터 엔지니어링', '금융', '전자상거래', '통신'],
        'description': '실시간 데이터 스트리밍 플랫폼'
    },
    {
        'tech_name': 'Snowflake',
        'category': 'Data_Engineering',
        'growth_rate': Decimal('31.5'),
        'demand_score': Decimal('90'),
        'trend_score': Decimal('93'),
        'related_domains': ['데이터 엔지니어링', '금융', '의료', '전자상거래'],
        'description': '클라우드 데이터 웨어하우스'
    },
    
    # 사이버보안
    {
        'tech_name': 'Zero Trust',
        'category': 'Security',
        'growth_rate': Decimal('27.8'),
        'demand_score': Decimal('89'),
        'trend_score': Decimal('92'),
        'related_domains': ['보안', '금융', '의료', '공공'],
        'description': '제로 트러스트 보안 아키텍처'
    },
    {
        'tech_name': 'SIEM',
        'category': 'Security',
        'growth_rate': Decimal('18.6'),
        'demand_score': Decimal('83'),
        'trend_score': Decimal('86'),
        'related_domains': ['보안', '금융', '의료', '통신'],
        'description': '보안 정보 및 이벤트 관리'
    },
    
    # 최신 프론트엔드
    {
        'tech_name': 'Next.js',
        'category': 'Frontend',
        'growth_rate': Decimal('35.2'),
        'demand_score': Decimal('92'),
        'trend_score': Decimal('95'),
        'related_domains': ['프론트엔드', '전자상거래', '교육', '미디어'],
        'description': 'React 기반 풀스택 프레임워크'
    },
    {
        'tech_name': 'Svelte',
        'category': 'Frontend',
        'growth_rate': Decimal('29.4'),
        'demand_score': Decimal('85'),
        'trend_score': Decimal('88'),
        'related_domains': ['프론트엔드', '전자상거래', '게임'],
        'description': '컴파일 기반 프론트엔드 프레임워크'
    },
    
    # 최신 백엔드
    {
        'tech_name': 'Rust',
        'category': 'Backend',
        'growth_rate': Decimal('33.8'),
        'demand_score': Decimal('87'),
        'trend_score': Decimal('90'),
        'related_domains': ['백엔드', '블록체인', '게임', '시스템'],
        'description': '고성능 시스템 프로그래밍 언어'
    },
    {
        'tech_name': 'GraphQL',
        'category': 'Backend',
        'growth_rate': Decimal('28.9'),
        'demand_score': Decimal('86'),
        'trend_score': Decimal('89'),
        'related_domains': ['백엔드', '전자상거래', '모바일', '미디어'],
        'description': 'API 쿼리 언어'
    },
]

print("=" * 80)
print("TechTrends 확장 데이터 추가")
print("=" * 80)

added_count = 0
failed_count = 0

for trend in extended_trends:
    try:
        table.put_item(Item=trend)
        added_count += 1
        print(f"✓ {trend['tech_name']} ({trend['category']}) - {', '.join(trend['related_domains'])}")
    except Exception as e:
        failed_count += 1
        print(f"✗ {trend['tech_name']} 실패: {str(e)}")

print("\n" + "=" * 80)
print(f"추가 완료: {added_count}개")
print(f"실패: {failed_count}개")
print("=" * 80)

# 추가된 도메인 요약
all_domains = set()
for trend in extended_trends:
    all_domains.update(trend['related_domains'])

print(f"\n신규 도메인: {len(all_domains)}개")
for domain in sorted(all_domains):
    print(f"  - {domain}")

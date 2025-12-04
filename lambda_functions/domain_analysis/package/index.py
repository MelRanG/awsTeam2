"""
Domain Analysis Engine Lambda Function
신규 도메인 확장 분석

Requirements: 4.1, 4.2, 4.3, 4.4
"""

import json
import logging
import os
from typing import Dict, Any, List, Set
from decimal import Decimal
import boto3

# 로깅 설정
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# AWS 클라이언트 초기화
dynamodb = boto3.resource('dynamodb', region_name=os.environ.get('AWS_REGION', 'us-east-2'))
bedrock_runtime = boto3.client('bedrock-runtime', region_name=os.environ.get('AWS_REGION', 'us-east-2'))


def handler(event, context):
    """
    Lambda handler for API Gateway
    
    Requirements: 4.1 - 도메인 분석 수행
    
    Args:
        event: API Gateway 이벤트
        context: Lambda 컨텍스트
        
    Returns:
        dict: API Gateway 응답
    """
    try:
        logger.info(f"도메인 분석 요청 수신: {json.dumps(event)}")
        
        # 요청 본문 파싱
        body = json.loads(event.get('body', '{}'))
        analysis_type = body.get('analysis_type', 'new_domains')
        
        # 전체 프로젝트 이력 수집
        projects = fetch_all_projects()
        employees = fetch_all_employees()
        tech_trends = fetch_tech_trends()
        
        logger.info(f"프로젝트 {len(projects)}개, 직원 {len(employees)}명, 트렌드 {len(tech_trends)}개 조회")
        
        # 도메인 분석 수행
        if analysis_type == 'new_domains':
            result = analyze_new_domains(projects, employees, tech_trends)
        elif analysis_type == 'expansion_strategy':
            result = analyze_expansion_strategy(projects, employees, tech_trends)
        else:
            result = analyze_new_domains(projects, employees, tech_trends)
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,Authorization',
                'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
            },
            'body': json.dumps(result, default=decimal_default)
        }
        
    except Exception as e:
        logger.error(f"도메인 분석 중 오류 발생: {str(e)}", exc_info=True)
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,Authorization',
                'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
            },
            'body': json.dumps({'error': str(e)})
        }


def fetch_all_projects() -> List[Dict[str, Any]]:
    """
    모든 프로젝트 조회
    
    Returns:
        list: 프로젝트 목록
    """
    try:
        table = dynamodb.Table('Projects')
        response = table.scan()
        
        projects = response.get('Items', [])
        
        # 페이지네이션 처리
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            projects.extend(response.get('Items', []))
        
        return projects
        
    except Exception as e:
        logger.error(f"프로젝트 조회 실패: {str(e)}")
        return []


def fetch_all_employees() -> List[Dict[str, Any]]:
    """
    모든 직원 조회
    
    Returns:
        list: 직원 목록
    """
    try:
        table = dynamodb.Table('Employees')
        response = table.scan()
        
        employees = response.get('Items', [])
        
        # 페이지네이션 처리
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            employees.extend(response.get('Items', []))
        
        return employees
        
    except Exception as e:
        logger.error(f"직원 조회 실패: {str(e)}")
        return []


def fetch_tech_trends() -> List[Dict[str, Any]]:
    """
    TechTrends 테이블에서 기술 트렌드 조회
    
    Returns:
        list: 기술 트렌드 목록
    """
    try:
        table = dynamodb.Table('TechTrends')
        response = table.scan()
        
        trends = response.get('Items', [])
        
        # 페이지네이션 처리
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            trends.extend(response.get('Items', []))
        
        logger.info(f"TechTrends에서 {len(trends)}개 트렌드 조회")
        return trends
        
    except Exception as e:
        logger.error(f"TechTrends 조회 실패: {str(e)}")
        return []


def analyze_new_domains(
    projects: List[Dict[str, Any]],
    employees: List[Dict[str, Any]],
    tech_trends: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    신규 도메인 분석 (TechTrends 기반)
    
    Requirements: 4.1, 4.2, 4.3
    
    Args:
        projects: 프로젝트 목록
        employees: 직원 목록
        tech_trends: 기술 트렌드 목록
        
    Returns:
        dict: 도메인 분석 결과
    """
    # 1. 프로젝트 도메인 분류 (Requirements: 4.1)
    domain_classification = classify_project_domains(projects)
    
    # 2. 인력 기술 기반 TechTrends 도메인 식별 (Requirements: 4.2)
    potential_domains = identify_potential_domains_from_trends(
        domain_classification,
        tech_trends,
        employees
    )
    
    # 3. 도메인 진입 분석 (Requirements: 4.3)
    domain_analysis = []
    for domain_info in potential_domains:
        analysis = analyze_domain_entry_with_trends(
            domain_info,
            employees,
            tech_trends
        )
        domain_analysis.append(analysis)
    
    return {
        'current_domains': domain_classification['current_domains'],
        'identified_domains': domain_analysis,
        'total_projects_analyzed': len(projects),
        'total_employees': len(employees)
    }


def classify_project_domains(projects: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    프로젝트 도메인 분류 - 실제 프로젝트 데이터에서 도메인 추출
    
    Requirements: 4.1 - 진행 중이거나 완료된 프로젝트의 도메인 분류
    
    Args:
        projects: 프로젝트 목록
        
    Returns:
        dict: 도메인 분류 결과
    """
    try:
        # 프로젝트에서 실제 도메인 추출
        current_domains = set()
        domain_projects = {}
        
        for project in projects:
            status = project.get('status', '')
            # 진행 중(In Progress) 또는 완료(Completed) 프로젝트만 포함
            if status not in ['In Progress', 'Completed']:
                continue
            
            # client_industry 필드에서 도메인 추출
            industry = project.get('client_industry', '')
            if industry and industry.strip():
                domain = industry.strip()
                current_domains.add(domain)
                
                if domain not in domain_projects:
                    domain_projects[domain] = []
                domain_projects[domain].append(project.get('project_name', ''))
        
        # 도메인이 없으면 프로젝트 이름이나 설명에서 추출 시도
        if not current_domains:
            for project in projects:
                status = project.get('status', '')
                if status not in ['In Progress', 'Completed']:
                    continue
                    
                project_name = project.get('project_name', '').lower()
                description = project.get('description', '').lower()
                
                # 일반적인 도메인 키워드 매칭
                domain_keywords = {
                    'Finance': ['finance', 'banking', 'payment', 'fintech'],
                    'Healthcare': ['health', 'medical', 'hospital', 'patient'],
                    'E-commerce': ['ecommerce', 'e-commerce', 'shopping', 'retail'],
                    'Manufacturing': ['manufacturing', 'factory', 'production'],
                    'Logistics': ['logistics', 'delivery', 'shipping', 'warehouse'],
                    'Education': ['education', 'learning', 'school', 'university'],
                    'Government': ['government', 'public', 'civic'],
                    'Telecommunications': ['telecom', 'network', 'communication'],
                    'Insurance': ['insurance', 'policy', 'claim'],
                    'Real Estate': ['real estate', 'property', 'housing']
                }
                
                for domain, keywords in domain_keywords.items():
                    if any(keyword in project_name or keyword in description for keyword in keywords):
                        current_domains.add(domain)
                        if domain not in domain_projects:
                            domain_projects[domain] = []
                        domain_projects[domain].append(project.get('project_name', ''))
                        break
        
        # 도메인 목록 정렬
        sorted_domains = sorted(list(current_domains))
        
        logger.info(f"프로젝트에서 추출한 도메인: {sorted_domains}")
        logger.info(f"도메인별 프로젝트 수: {[(d, len(domain_projects.get(d, []))) for d in sorted_domains]}")
        
        return {
            'current_domains': sorted_domains if sorted_domains else ['General'],
            'domain_projects': domain_projects,
            'classification_text': f"진행 중/완료 프로젝트에서 {len(sorted_domains)}개 도메인 식별"
        }
        
    except Exception as e:
        logger.error(f"도메인 분류 실패: {str(e)}")
        # 기본 도메인 반환
        return {
            'current_domains': ['General'],
            'domain_projects': {},
            'classification_text': ''
        }


def extract_domains_from_text(text: str) -> List[str]:
    """
    텍스트에서 도메인 추출
    
    Args:
        text: 분류 텍스트
        
    Returns:
        list: 도메인 목록
    """
    # 간단한 구현: 일반적인 도메인 키워드 찾기
    common_domains = [
        'Finance', 'Banking', 'Healthcare', 'E-commerce', 'Retail',
        'Manufacturing', 'Logistics', 'Education', 'Government',
        'Telecommunications', 'Media', 'Entertainment', 'Insurance'
    ]
    
    found_domains = []
    for domain in common_domains:
        if domain.lower() in text.lower():
            found_domains.append(domain)
    
    return found_domains if found_domains else ['General']


def identify_potential_domains(classification: Dict[str, Any]) -> List[str]:
    """
    잠재적 신규 도메인 식별
    
    Requirements: 4.2 - 현재 보유하지 않은 도메인 식별
    
    Args:
        classification: 도메인 분류 결과
        
    Returns:
        list: 잠재적 신규 도메인 목록
    """
    current_domains = set(classification.get('current_domains', []))
    
    # 모든 가능한 도메인
    all_domains = {
        'Finance', 'Banking', 'Healthcare', 'E-commerce', 'Retail',
        'Manufacturing', 'Logistics', 'Education', 'Government',
        'Telecommunications', 'Media', 'Entertainment', 'Insurance',
        'Real Estate', 'Energy', 'Transportation', 'Hospitality'
    }
    
    # 현재 보유하지 않은 도메인
    potential_domains = list(all_domains - current_domains)
    
    # 상위 5개만 반환
    return potential_domains[:5]


def identify_potential_domains_from_trends(
    classification: Dict[str, Any],
    tech_trends: List[Dict[str, Any]],
    employees: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    인력 기술 기반 TechTrends 도메인 식별
    
    Requirements: 4.2 - 보유 인력의 기술로 진출 가능한 도메인 분석
    
    Args:
        classification: 도메인 분류 결과
        tech_trends: 기술 트렌드 목록
        employees: 직원 목록
        
    Returns:
        list: 진출 가능 도메인 정보 (도메인명, 성장률, 관련 기술, 보유 기술 포함)
    """
    current_domains = set(classification.get('current_domains', []))
    
    # 1. 인력이 보유한 모든 기술 수집
    employee_skills = set()
    for employee in employees:
        skills = employee.get('skills', [])
        for skill in skills:
            if isinstance(skill, dict):
                skill_name = skill.get('name', '')
                if skill_name:
                    employee_skills.add(skill_name)
    
    logger.info(f"보유 인력 기술: {len(employee_skills)}개 - {list(employee_skills)[:10]}")
    
    # 2. TechTrends에서 보유 기술과 연관된 도메인 찾기
    domain_trends = {}
    
    for trend in tech_trends:
        related_domains = trend.get('related_domains', [])
        category = trend.get('category', '')
        tech_name = trend.get('tech_name', '')
        growth_rate = float(trend.get('growth_rate', 0))
        demand_score = float(trend.get('demand_score', 0))
        trend_score = float(trend.get('trend_score', 0))
        
        # related_domains가 있으면 사용, 없으면 category 사용
        domains_to_check = related_domains if related_domains else [category]
        
        for domain in domains_to_check:
            if not domain or domain == '':
                continue
                
            if domain not in domain_trends:
                domain_trends[domain] = {
                    'domain_name': domain,
                    'technologies': [],
                    'matched_technologies': [],  # 보유 기술과 매칭되는 기술
                    'avg_growth_rate': 0,
                    'avg_demand_score': 0,
                    'avg_trend_score': 0,
                    'count': 0
                }
            
            domain_trends[domain]['technologies'].append(tech_name)
            
            # 보유 기술과 매칭되는지 확인
            if tech_name in employee_skills:
                domain_trends[domain]['matched_technologies'].append(tech_name)
            
            domain_trends[domain]['avg_growth_rate'] += growth_rate
            domain_trends[domain]['avg_demand_score'] += demand_score
            domain_trends[domain]['avg_trend_score'] += trend_score
            domain_trends[domain]['count'] += 1
    
    # 3. 평균 계산 및 매칭률 계산
    for domain_info in domain_trends.values():
        count = domain_info['count']
        if count > 0:
            domain_info['avg_growth_rate'] /= count
            domain_info['avg_demand_score'] /= count
            domain_info['avg_trend_score'] /= count
        
        # 기술 매칭률 계산
        total_techs = len(domain_info['technologies'])
        matched_techs = len(domain_info['matched_technologies'])
        domain_info['skill_match_rate'] = (matched_techs / total_techs * 100) if total_techs > 0 else 0
    
    # 4. 보유 기술이 있는 도메인만 필터링 (현재 도메인 제외)
    potential_domains = [
        info for domain, info in domain_trends.items()
        if len(info['matched_technologies']) > 0 and domain not in current_domains
    ]
    
    # 5. 기술 매칭률과 성장률을 종합하여 정렬
    # 점수 = 기술매칭률(60%) + 성장률(20%) + 수요점수(20%)
    for domain in potential_domains:
        domain['opportunity_score'] = (
            domain['skill_match_rate'] * 0.6 +
            (domain['avg_growth_rate'] / 100 * 100) * 0.2 +
            (domain['avg_demand_score'] / 100 * 100) * 0.2
        )
    
    potential_domains.sort(key=lambda x: x['opportunity_score'], reverse=True)
    
    logger.info(f"진출 가능 도메인: {len(potential_domains)}개 발견")
    
    # 상위 8개 반환
    return potential_domains[:8]


def analyze_domain_entry_with_trends(
    domain_info: Dict[str, Any],
    employees: List[Dict[str, Any]],
    tech_trends: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    TechTrends 기반 도메인 진입 분석
    
    Requirements: 4.3 - 시장 트렌드 반영 도메인 분석
    
    Args:
        domain_info: 도메인 정보 (이름, 성장률, 관련 기술 포함)
        employees: 직원 목록
        tech_trends: 기술 트렌드 목록
        
    Returns:
        dict: 도메인 진입 분석 결과
    """
    try:
        domain_name = domain_info['domain_name']
        required_skills = domain_info['technologies']
        
        # 현재 보유 기술 분석
        current_skills = set()
        skill_proficiency = {}
        
        for employee in employees:
            skills = employee.get('skills', [])
            for skill in skills:
                if isinstance(skill, dict):
                    skill_name = skill.get('name', '')
                    skill_level = skill.get('level', 'Intermediate')
                    current_skills.add(skill_name)
                    
                    if skill_name not in skill_proficiency or \
                       get_level_score(skill_level) > get_level_score(skill_proficiency[skill_name]):
                        skill_proficiency[skill_name] = skill_level
        
        # 기술 갭 계산
        skill_gap = list(set(required_skills) - current_skills)
        matched_skills = list(current_skills.intersection(set(required_skills)))
        
        # 전환 가능한 직원 찾기
        transferable_employees = find_transferable_employees(
            employees,
            required_skills
        )
        
        # TechTrends 기반 실현 가능성 점수 계산
        feasibility_score = calculate_feasibility_score_with_trends(
            required_skills=required_skills,
            current_skills=current_skills,
            transferable_employees=transferable_employees,
            growth_rate=domain_info['avg_growth_rate'],
            demand_score=domain_info['avg_demand_score'],
            trend_score=domain_info['avg_trend_score']
        )
        
        # 상세 분석 및 근거 생성
        reasoning = generate_domain_reasoning_with_trends(
            domain=domain_name,
            feasibility_score=feasibility_score,
            matched_skills=matched_skills,
            skill_gap=skill_gap,
            skill_proficiency=skill_proficiency,
            transferable_count=len(transferable_employees),
            growth_rate=domain_info['avg_growth_rate'],
            demand_score=domain_info['avg_demand_score']
        )
        
        return {
            'domain_name': domain_name,
            'feasibility_score': feasibility_score,
            'required_skills': required_skills,
            'matched_skills': matched_skills,
            'skill_gap': skill_gap,
            'skill_proficiency': {skill: skill_proficiency.get(skill, 'N/A') for skill in matched_skills},
            'transferable_employees': len(transferable_employees),
            'recommended_team': [
                {
                    'user_id': emp.get('user_id'),
                    'name': emp.get('basic_info', {}).get('name', emp.get('user_id'))
                }
                for emp in transferable_employees[:5]
            ],
            'reasoning': reasoning,
            'market_growth_rate': round(domain_info['avg_growth_rate'], 1),
            'market_demand_score': round(domain_info['avg_demand_score'], 1)
        }
        
    except Exception as e:
        logger.error(f"도메인 진입 분석 실패: {str(e)}")
        return {
            'domain_name': domain_info.get('domain_name', 'Unknown'),
            'feasibility_score': 0,
            'required_skills': [],
            'matched_skills': [],
            'skill_gap': [],
            'skill_proficiency': {},
            'transferable_employees': 0,
            'recommended_team': [],
            'reasoning': '분석 실패',
            'market_growth_rate': 0,
            'market_demand_score': 0
        }


def analyze_domain_entry(
    domain: str,
    employees: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    도메인 진입 분석 (근거 기반)
    
    Requirements: 4.3 - 기술 갭 및 전환 가능성 분석
    
    Args:
        domain: 도메인 이름
        employees: 직원 목록
        
    Returns:
        dict: 도메인 진입 분석 결과
    """
    try:
        # 도메인별 필요 기술 정의
        required_skills = get_required_skills_for_domain(domain)
        
        # 현재 보유 기술 분석
        current_skills = set()
        skill_proficiency = {}  # 기술별 숙련도 추적
        
        for employee in employees:
            skills = employee.get('skills', [])
            for skill in skills:
                if isinstance(skill, dict):
                    skill_name = skill.get('name', '')
                    skill_level = skill.get('level', 'Intermediate')
                    current_skills.add(skill_name)
                    
                    # 최고 숙련도 추적
                    if skill_name not in skill_proficiency or \
                       get_level_score(skill_level) > get_level_score(skill_proficiency[skill_name]):
                        skill_proficiency[skill_name] = skill_level
        
        # 기술 갭 계산
        skill_gap = list(set(required_skills) - current_skills)
        matched_skills = list(current_skills.intersection(set(required_skills)))
        
        # 전환 가능한 직원 찾기
        transferable_employees = find_transferable_employees(
            employees,
            required_skills
        )
        
        # 실현 가능성 점수 계산
        feasibility_score = calculate_feasibility_score(
            required_skills,
            current_skills,
            transferable_employees
        )
        
        # Claude를 사용한 상세 분석 및 근거 생성
        reasoning = generate_domain_reasoning(
            domain=domain,
            feasibility_score=feasibility_score,
            matched_skills=matched_skills,
            skill_gap=skill_gap,
            skill_proficiency=skill_proficiency,
            transferable_count=len(transferable_employees)
        )
        
        return {
            'domain_name': domain,
            'feasibility_score': feasibility_score,
            'required_skills': required_skills,
            'matched_skills': matched_skills,
            'skill_gap': skill_gap,
            'skill_proficiency': {skill: skill_proficiency.get(skill, 'N/A') for skill in matched_skills},
            'transferable_employees': len(transferable_employees),
            'recommended_team': [
                {
                    'user_id': emp.get('user_id'),
                    'name': emp.get('basic_info', {}).get('name', emp.get('user_id'))
                }
                for emp in transferable_employees[:5]
            ],
            'reasoning': reasoning
        }
        
    except Exception as e:
        logger.error(f"도메인 진입 분석 실패: {str(e)}")
        return {
            'domain_name': domain,
            'feasibility_score': 0,
            'required_skills': [],
            'matched_skills': [],
            'skill_gap': [],
            'skill_proficiency': {},
            'transferable_employees': 0,
            'recommended_team': [],
            'reasoning': '분석 실패'
        }


def get_level_score(level: str) -> int:
    """기술 레벨을 점수로 변환"""
    level_scores = {
        'Beginner': 1,
        'Intermediate': 2,
        'Advanced': 3,
        'Expert': 4
    }
    return level_scores.get(level, 2)


def generate_domain_reasoning(
    domain: str,
    feasibility_score: float,
    matched_skills: List[str],
    skill_gap: List[str],
    skill_proficiency: Dict[str, str],
    transferable_count: int
) -> str:
    """
    도메인 진입 근거 생성
    
    Args:
        domain: 도메인 이름
        feasibility_score: 실현 가능성 점수
        matched_skills: 보유 기술
        skill_gap: 부족한 기술
        skill_proficiency: 기술별 숙련도
        transferable_count: 전환 가능 인력 수
        
    Returns:
        str: 도메인 진입 근거
    """
    try:
        # 숙련도 정보 포맷팅
        proficiency_info = "\n".join([
            f"  - {skill}: {level}"
            for skill, level in skill_proficiency.items()
        ]) if skill_proficiency else "없음"
        
        prompt = f"""다음 신규 도메인 진입 가능성을 분석하고 근거를 제시해주세요:

## 도메인 정보
- 도메인: {domain}
- 실현 가능성 점수: {feasibility_score:.1f}/100

## 현재 역량
- 보유 기술: {', '.join(matched_skills) if matched_skills else '없음'}
- 기술별 숙련도:
{proficiency_info}
- 전환 가능 인력: {transferable_count}명

## 기술 갭
- 부족한 기술: {', '.join(skill_gap) if skill_gap else '없음'}

위 정보를 바탕으로 다음 형식으로 분석 근거를 작성해주세요:
1. 현재 강점 (보유 기술 및 인력)
2. 진입 장벽 (부족한 기술 및 리스크)
3. 추천 전략 (채용, 교육, 파트너십 등)

총 3-4문장으로 간결하게 작성해주세요."""

        response = bedrock_runtime.invoke_model(
            modelId='anthropic.claude-v2',
            body=json.dumps({
                'prompt': f"\n\nHuman: {prompt}\n\nAssistant:",
                'max_tokens_to_sample': 300,
                'temperature': 0.7
            })
        )
        
        response_body = json.loads(response['body'].read())
        reasoning = response_body.get('completion', '').strip()
        
        return reasoning
        
    except Exception as e:
        logger.error(f"도메인 근거 생성 실패: {str(e)}")
        
        # 폴백: 구조화된 근거 생성
        if feasibility_score >= 70:
            level = "높음"
            recommendation = "즉시 진입 가능"
        elif feasibility_score >= 40:
            level = "중간"
            recommendation = "단기 교육 후 진입 가능"
        else:
            level = "낮음"
            recommendation = "장기 준비 필요"
        
        reasoning = f"[실현가능성: {level}] "
        
        if matched_skills:
            reasoning += f"{', '.join(matched_skills[:3])} 등 {len(matched_skills)}개 기술을 보유하고 있으며, {transferable_count}명의 전환 가능 인력이 있습니다. "
        
        if skill_gap:
            reasoning += f"다만 {', '.join(skill_gap[:3])} 등 {len(skill_gap)}개 기술이 부족합니다. "
        
        reasoning += f"[전략] {recommendation}."
        
        return reasoning


def get_required_skills_for_domain(domain: str) -> List[str]:
    """
    도메인별 필요 기술 반환
    
    Args:
        domain: 도메인 이름
        
    Returns:
        list: 필요 기술 목록
    """
    domain_skills = {
        'Finance': ['Java', 'Spring', 'Oracle', 'Security', 'Compliance'],
        'Healthcare': ['Python', 'HIPAA', 'HL7', 'FHIR', 'Data Privacy'],
        'E-commerce': ['Node.js', 'React', 'MongoDB', 'Payment Gateway', 'AWS'],
        'Manufacturing': ['IoT', 'Python', 'Data Analytics', 'ERP', 'MES'],
        'Logistics': ['GPS', 'Route Optimization', 'Mobile', 'Real-time Tracking'],
        'Education': ['LMS', 'Video Streaming', 'Mobile', 'Gamification'],
        'Government': ['Security', 'Compliance', 'Java', 'Legacy Systems'],
        'Telecommunications': ['5G', 'Network', 'Real-time', 'High Availability'],
        'Insurance': ['Actuarial', 'Risk Assessment', 'Java', 'Compliance'],
        'Real Estate': ['GIS', 'Mobile', 'Payment', 'CRM'],
        'Energy': ['IoT', 'SCADA', 'Real-time Monitoring', 'Data Analytics'],
        'Transportation': ['GPS', 'Route Planning', 'Mobile', 'Real-time'],
        'Hospitality': ['Booking System', 'Payment', 'Mobile', 'CRM']
    }
    
    return domain_skills.get(domain, ['General Programming', 'Database', 'Web Development'])


def find_transferable_employees(
    employees: List[Dict[str, Any]],
    required_skills: List[str]
) -> List[Dict[str, Any]]:
    """
    전환 가능한 직원 찾기
    
    Args:
        employees: 직원 목록
        required_skills: 필요 기술 목록
        
    Returns:
        list: 전환 가능한 직원 목록
    """
    transferable = []
    
    for employee in employees:
        employee_skills = set()
        skills = employee.get('skills', [])
        for skill in skills:
            if isinstance(skill, dict):
                employee_skills.add(skill.get('name', ''))
        
        # 필요 기술 중 일부를 보유한 직원
        matched_skills = employee_skills.intersection(set(required_skills))
        if len(matched_skills) >= len(required_skills) * 0.3:  # 30% 이상 매칭
            transferable.append(employee)
    
    return transferable


def calculate_feasibility_score(
    required_skills: List[str],
    current_skills: Set[str],
    transferable_employees: List[Dict[str, Any]]
) -> float:
    """
    실현 가능성 점수 계산 (근거 기반)
    
    공식: Score(D) = (Trend_growth × W_market) - (Gap_skill × W_risk)
    
    실제 구현:
    - 기술 보유율 (Skill Coverage): 현재 보유 기술 / 필요 기술
    - 인력 가용성 (Employee Availability): 전환 가능 인력 / 최소 필요 인력
    - 기술 갭 페널티 (Skill Gap Penalty): 부족한 핵심 기술에 대한 감점
    
    Args:
        required_skills: 필요 기술 목록
        current_skills: 현재 보유 기술
        transferable_employees: 전환 가능한 직원 목록
        
    Returns:
        float: 실현 가능성 점수 (0-100)
    """
    # 1. 기술 보유율 계산
    matched_skills = current_skills.intersection(set(required_skills))
    skill_coverage = len(matched_skills) / len(required_skills) if required_skills else 0
    
    # 2. 인력 가용성 계산
    min_team_size = 5  # 최소 팀 크기
    employee_availability = min(1.0, len(transferable_employees) / min_team_size)
    
    # 3. 기술 갭 분석
    skill_gap = set(required_skills) - current_skills
    gap_penalty = len(skill_gap) / len(required_skills) if required_skills else 0
    
    # 4. 핵심 기술 가중치
    # 특정 핵심 기술이 없으면 추가 페널티
    core_skills = ['AWS', 'Python', 'Java', 'React', 'Database']
    missing_core_skills = [skill for skill in core_skills if skill in skill_gap]
    core_penalty = len(missing_core_skills) * 0.05  # 핵심 기술 하나당 5% 감점
    
    # 5. 시장 수요 가중치 (W_market)
    # 실제로는 TechTrends 테이블에서 가져와야 하지만, 여기서는 기본값 사용
    market_weight = 1.2  # 시장 수요가 높다고 가정
    
    # 6. 리스크 가중치 (W_risk)
    risk_weight = 1.0
    
    # 7. 종합 점수 계산
    # Score = (기술보유율 × 시장가중치 + 인력가용성) - (기술갭 × 리스크가중치 + 핵심기술페널티)
    positive_score = (skill_coverage * market_weight * 0.5 + employee_availability * 0.3) * 100
    negative_score = (gap_penalty * risk_weight * 0.2 + core_penalty) * 100
    
    feasibility = max(0, positive_score - negative_score)
    
    logger.info(f"실현가능성 계산: 기술보유율={skill_coverage:.2f}, 인력가용성={employee_availability:.2f}, 기술갭={gap_penalty:.2f}, 최종점수={feasibility:.2f}")
    
    return round(feasibility, 2)


def calculate_feasibility_score_with_trends(
    required_skills: List[str],
    current_skills: Set[str],
    transferable_employees: List[Dict[str, Any]],
    growth_rate: float,
    demand_score: float,
    trend_score: float
) -> float:
    """
    TechTrends 기반 실현 가능성 점수 계산
    
    공식: Score(D) = (Trend_growth × W_market) - (Gap_skill × W_risk)
    
    Args:
        required_skills: 필요 기술 목록
        current_skills: 현재 보유 기술
        transferable_employees: 전환 가능한 직원 목록
        growth_rate: 시장 성장률 (%)
        demand_score: 수요 점수 (0-100)
        trend_score: 트렌드 점수 (0-100)
        
    Returns:
        float: 실현 가능성 점수 (0-100)
    """
    # 1. 기술 보유율 계산
    matched_skills = current_skills.intersection(set(required_skills))
    skill_coverage = len(matched_skills) / len(required_skills) if required_skills else 0
    
    # 2. 인력 가용성 계산
    min_team_size = 5
    employee_availability = min(1.0, len(transferable_employees) / min_team_size)
    
    # 3. 기술 갭 분석
    skill_gap = set(required_skills) - current_skills
    gap_penalty = len(skill_gap) / len(required_skills) if required_skills else 0
    
    # 4. 시장 트렌드 가중치 (W_market)
    # 성장률, 수요 점수, 트렌드 점수를 종합
    market_weight = (
        (growth_rate / 100) * 0.4 +  # 성장률 (정규화)
        (demand_score / 100) * 0.4 +  # 수요 점수
        (trend_score / 100) * 0.2      # 트렌드 점수
    )
    market_weight = max(0.5, min(2.0, market_weight * 2))  # 0.5 ~ 2.0 범위로 제한
    
    # 5. 리스크 가중치 (W_risk)
    # 기술 갭이 클수록 리스크 증가
    risk_weight = 1.0 + (gap_penalty * 0.5)
    
    # 6. 종합 점수 계산
    # Score = (기술보유율 × 시장가중치 + 인력가용성 + 트렌드보너스) - (기술갭 × 리스크가중치)
    positive_score = (
        skill_coverage * market_weight * 50 +  # 기술 보유율 (최대 50점)
        employee_availability * 30 +            # 인력 가용성 (최대 30점)
        (trend_score / 100) * 20                # 트렌드 보너스 (최대 20점)
    )
    
    negative_score = gap_penalty * risk_weight * 30  # 기술 갭 페널티 (최대 30점)
    
    feasibility = max(0, min(100, positive_score - negative_score))
    
    logger.info(f"TechTrends 기반 실현가능성: 기술보유율={skill_coverage:.2f}, 시장가중치={market_weight:.2f}, 성장률={growth_rate:.1f}%, 최종점수={feasibility:.2f}")
    
    return round(feasibility, 2)


def generate_domain_reasoning_with_trends(
    domain: str,
    feasibility_score: float,
    matched_skills: List[str],
    skill_gap: List[str],
    skill_proficiency: Dict[str, str],
    transferable_count: int,
    growth_rate: float,
    demand_score: float
) -> str:
    """
    TechTrends 기반 도메인 진입 근거 생성
    
    Args:
        domain: 도메인 이름
        feasibility_score: 실현 가능성 점수
        matched_skills: 보유 기술
        skill_gap: 부족한 기술
        skill_proficiency: 기술별 숙련도
        transferable_count: 전환 가능 인력 수
        growth_rate: 시장 성장률
        demand_score: 수요 점수
        
    Returns:
        str: 도메인 진입 근거
    """
    # 구조화된 근거 생성
    if feasibility_score >= 70:
        level = "높음"
        recommendation = "즉시 진입 가능"
    elif feasibility_score >= 40:
        level = "중간"
        recommendation = "단기 교육 후 진입 가능"
    else:
        level = "낮음"
        recommendation = "장기 준비 필요"
    
    reasoning = f"[시장 분석] {domain} 도메인은 연평균 {growth_rate:.1f}% 성장률과 {demand_score:.0f}점의 높은 수요를 보이고 있습니다. "
    
    reasoning += f"[실현가능성: {level}] "
    
    if matched_skills:
        top_skills = ', '.join(matched_skills[:3])
        reasoning += f"{top_skills} 등 {len(matched_skills)}개 핵심 기술을 보유하고 있으며, {transferable_count}명의 전환 가능 인력이 있습니다. "
    else:
        reasoning += f"현재 관련 기술을 보유한 인력이 부족하지만, {transferable_count}명이 교육을 통해 전환 가능합니다. "
    
    if skill_gap:
        top_gaps = ', '.join(skill_gap[:3])
        reasoning += f"다만 {top_gaps} 등 {len(skill_gap)}개 기술 확보가 필요합니다. "
    
    reasoning += f"[전략] {recommendation}."
    
    return reasoning


def analyze_expansion_strategy(
    projects: List[Dict[str, Any]],
    employees: List[Dict[str, Any]],
    tech_trends: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    확장 전략 분석 (TechTrends 기반)
    
    Args:
        projects: 프로젝트 목록
        employees: 직원 목록
        tech_trends: 기술 트렌드 목록
        
    Returns:
        dict: 확장 전략 분석 결과
    """
    # 신규 도메인 분석 재사용
    new_domains_result = analyze_new_domains(projects, employees, tech_trends)
    
    # 우선순위 정렬 (실현 가능성 기준)
    sorted_domains = sorted(
        new_domains_result['identified_domains'],
        key=lambda x: x['feasibility_score'],
        reverse=True
    )
    
    return {
        'recommended_domains': sorted_domains[:3],
        'expansion_strategy': 'Focus on high-feasibility and high-growth domains first',
        'total_analysis': new_domains_result
    }


def update_domain_portfolio_on_new_hire(employee_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    신규 채용 시 도메인 포트폴리오 업데이트
    
    Requirements: 4.4 - 신규 직원의 기술로 진입 가능한 도메인 추가
    
    Args:
        employee_data: 신규 직원 데이터
        
    Returns:
        dict: 업데이트된 도메인 포트폴리오
    """
    try:
        # 신규 직원의 기술 추출
        employee_skills = set()
        skills = employee_data.get('skills', [])
        for skill in skills:
            if isinstance(skill, dict):
                employee_skills.add(skill.get('name', ''))
        
        logger.info(f"신규 직원 기술: {employee_skills}")
        
        # 모든 도메인에 대해 진입 가능성 확인
        all_domains = [
            'Finance', 'Banking', 'Healthcare', 'E-commerce', 'Retail',
            'Manufacturing', 'Logistics', 'Education', 'Government',
            'Telecommunications', 'Media', 'Entertainment', 'Insurance',
            'Real Estate', 'Energy', 'Transportation', 'Hospitality'
        ]
        
        new_accessible_domains = []
        
        for domain in all_domains:
            required_skills = set(get_required_skills_for_domain(domain))
            
            # 신규 직원의 기술이 도메인 필요 기술의 30% 이상을 충족하는지 확인
            matched_skills = employee_skills.intersection(required_skills)
            match_rate = len(matched_skills) / len(required_skills) if required_skills else 0
            
            if match_rate >= 0.3:
                new_accessible_domains.append({
                    'domain': domain,
                    'match_rate': round(match_rate * 100, 2),
                    'matched_skills': list(matched_skills)
                })
        
        # DomainPortfolio 테이블에 저장 (테이블이 있다면)
        if new_accessible_domains:
            try:
                table = dynamodb.Table('DomainPortfolio')
                for domain_info in new_accessible_domains:
                    table.put_item(Item={
                        'domain_name': domain_info['domain'],
                        'employee_id': employee_data.get('user_id'),
                        'match_rate': Decimal(str(domain_info['match_rate'])),
                        'matched_skills': domain_info['matched_skills'],
                        'added_date': employee_data.get('hire_date', 'unknown')
                    })
                logger.info(f"도메인 포트폴리오 업데이트 완료: {len(new_accessible_domains)}개 도메인")
            except Exception as e:
                logger.warning(f"DomainPortfolio 테이블 업데이트 실패 (테이블이 없을 수 있음): {str(e)}")
        
        return {
            'employee_id': employee_data.get('user_id'),
            'new_accessible_domains': new_accessible_domains,
            'total_domains_added': len(new_accessible_domains)
        }
        
    except Exception as e:
        logger.error(f"도메인 포트폴리오 업데이트 실패: {str(e)}")
        return {
            'employee_id': employee_data.get('user_id'),
            'new_accessible_domains': [],
            'total_domains_added': 0,
            'error': str(e)
        }


def decimal_default(obj):
    """Decimal을 float로 변환"""
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

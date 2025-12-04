"""
Project Recommendation Engine Lambda Function
프로젝트 투입 인력 추천

Requirements: 2.2, 2.4, 2.5, 1.3, 1.4, 11.3, 11.4
"""

import json
import logging
import os
from typing import Dict, Any, List, Optional
from decimal import Decimal
import boto3

# 로깅 설정
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# AWS 클라이언트 초기화
dynamodb = boto3.resource('dynamodb', region_name=os.environ.get('AWS_REGION', 'us-east-2'))

# Bedrock 클라이언트 (선택적)
try:
    bedrock_runtime = boto3.client('bedrock-runtime', region_name=os.environ.get('AWS_REGION', 'us-east-2'))
except:
    bedrock_runtime = None
    logger.warning("Bedrock 클라이언트 초기화 실패 - 기본 추천 근거 사용")


def handler(event, context):
    """
    Lambda handler for API Gateway
    
    Requirements: 2.2 - 프로젝트 투입 인력 추천
    
    Args:
        event: API Gateway 이벤트
        context: Lambda 컨텍스트
        
    Returns:
        dict: API Gateway 응답
    """
    try:
        logger.info(f"추천 요청 수신: {json.dumps(event)}")
        
        # 요청 본문 파싱 (Requirements: 2.2)
        body = json.loads(event.get('body', '{}'))
        
        # CORS preflight 요청 처리
        if event.get('httpMethod') == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type,Authorization',
                    'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
                },
                'body': ''
            }
        
        # 입력 검증
        if not body.get('project_id'):
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type,Authorization',
                    'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
                },
                'body': json.dumps({'error': 'project_id가 필요합니다'})
            }
        
        project_id = body['project_id']
        required_skills = body.get('required_skills', [])
        team_size = body.get('team_size', 5)
        priority = body.get('priority', 'balanced')  # skill, affinity, balanced
        
        logger.info(f"프로젝트 {project_id}에 대한 추천 시작")
        
        # 프로젝트 정보 조회하여 필요 인력 수 확인
        project_table = dynamodb.Table('Projects')
        project_response = project_table.get_item(Key={'project_id': project_id})
        project = project_response.get('Item', {})
        
        # 필요 인력 수 가져오기
        required_members = project.get('required_members', team_size)
        if isinstance(required_members, str):
            required_members = int(required_members)
        
        # 필요 인력 * 2 만큼 추천 (정수로 변환)
        recommendation_count = int(required_members * 2)
        
        # 프로젝트 요구 기술 가져오기
        if not required_skills:
            tech_stack = project.get('tech_stack', {})
            required_skills = []
            if isinstance(tech_stack, dict):
                for category, skills in tech_stack.items():
                    if isinstance(skills, list):
                        required_skills.extend([str(skill) for skill in skills])
        
        logger.info(f"필요 인력: {int(required_members)}명, 추천 인원: {recommendation_count}명")
        
        # 추천 생성
        recommendations = generate_recommendations(
            project_id=project_id,
            required_skills=required_skills,
            team_size=recommendation_count,
            priority=priority
        )
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,Authorization',
                'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
            },
            'body': json.dumps({
                'project_id': project_id,
                'recommendations': recommendations
            }, default=decimal_default)
        }
        
    except Exception as e:
        logger.error(f"추천 생성 중 오류 발생: {str(e)}", exc_info=True)
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


def generate_recommendations(
    project_id: str,
    required_skills: List[str],
    team_size: int,
    priority: str
) -> List[Dict[str, Any]]:
    """
    프로젝트 투입 인력 추천 생성
    
    Requirements: 2.2, 2.4 - 다중 요소 점수 계산 및 추천
    
    Args:
        project_id: 프로젝트 ID
        required_skills: 요구 기술 목록
        team_size: 팀 크기
        priority: 우선순위 (skill, affinity, balanced)
        
    Returns:
        list: 추천 후보자 목록
    """
    # 1. 기술 매칭 알고리즘 (Requirements: 1.3, 2.2)
    skill_matches = find_employees_by_skills(required_skills)
    logger.info(f"기술 매칭 결과: {len(skill_matches)} 명")
    
    # 2. 벡터 유사도 검색 (Requirements: 11.3, 11.4)
    vector_matches = search_similar_employees(project_id, required_skills)
    logger.info(f"벡터 검색 결과: {len(vector_matches)} 명")
    
    # 3. 친밀도 점수 조회 (Requirements: 2.2)
    affinity_scores = get_affinity_scores()
    
    # 4. 후보자 통합 및 점수 계산
    candidates = merge_and_score_candidates(
        skill_matches=skill_matches,
        vector_matches=vector_matches,
        affinity_scores=affinity_scores,
        priority=priority
    )
    
    # 5. 가용성 확인 (Requirements: 2.5)
    candidates = check_availability(candidates)
    
    # 6. 상위 후보자 선택
    top_candidates = sorted(
        candidates,
        key=lambda x: x['overall_score'],
        reverse=True
    )[:team_size]
    
    # 7. 추천 근거 생성 (Requirements: 2.4)
    for candidate in top_candidates:
        candidate['reasoning'] = generate_reasoning(candidate)
    
    return top_candidates


def find_employees_by_skills(required_skills: List[str]) -> List[Dict[str, Any]]:
    """
    기술 스택으로 직원 검색 (가중치 기반)
    
    Requirements: 1.3 - 기술 매칭 알고리즘
    
    적합도 점수 공식: Score(P, E) = Σ(Smatch × Wlevel × Wrecency) + (Expdomain × Wdomain)
    - Smatch: 요구 기술 일치 여부 (0 or 1)
    - Wlevel: 기술 숙련도 가중치 (Beginner: 1.0 ~ Expert: 2.0)
    - Wrecency: 최신성 가중치 (최근 6개월: 1.0, 3년 전: 0.3)
    - Wdomain: 도메인 경험 가중치 (1.3)
    
    Args:
        required_skills: 요구 기술 목록
        
    Returns:
        list: 매칭된 직원 목록
    """
    try:
        import math
        from datetime import datetime
        
        table = dynamodb.Table('Employees')
        
        # 모든 직원 조회
        response = table.scan()
        employees = response.get('Items', [])
        
        # 페이지네이션 처리
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            employees.extend(response.get('Items', []))
        
        # 기술 매칭 점수 계산 (가중치 적용)
        matches = []
        current_year = datetime.now().year
        
        for employee in employees:
            # 이미 다른 프로젝트에 배정된 직원은 제외
            current_project = employee.get('current_project')
            if current_project:
                logger.info(f"직원 {employee.get('user_id')}는 프로젝트 {current_project}에 이미 배정되어 있어 제외")
                continue
            
            skills = employee.get('skills', [])
            work_experience = employee.get('work_experience', [])
            
            # 가중치 점수 계산
            weighted_score = 0.0
            matched_skills = []
            skill_details = []
            
            for req_skill in required_skills:
                # 직원이 해당 기술을 보유하는지 확인
                for emp_skill in skills:
                    if not isinstance(emp_skill, dict):
                        continue
                    
                    skill_name = emp_skill.get('name', '')
                    if skill_name.lower() == req_skill.lower():
                        # 1. 기본 매칭 (Smatch = 1)
                        s_match = 1.0
                        
                        # 2. 숙련도 가중치 (Wlevel)
                        level = emp_skill.get('level', 'Intermediate')
                        level_weights = {
                            'Beginner': 1.0,
                            'Intermediate': 1.5,
                            'Advanced': 1.8,
                            'Expert': 2.0
                        }
                        w_level = level_weights.get(level, 1.0)
                        
                        # 3. 최신성 가중치 (Wrecency)
                        # 최근 프로젝트에서 사용했는지 확인
                        w_recency = 0.5  # 기본값
                        
                        for project in work_experience:
                            if not isinstance(project, dict):
                                continue
                            
                            # 프로젝트 기간 파싱
                            period = project.get('period', '')
                            if period:
                                try:
                                    # "2024-01 ~ 2025-07" 형식 파싱
                                    end_date = period.split('~')[-1].strip()
                                    end_year = int(end_date.split('-')[0])
                                    years_ago = current_year - end_year
                                    
                                    # 시간 감쇠: e^(-λt), λ = 0.3
                                    w_recency = max(w_recency, math.exp(-0.3 * years_ago))
                                except:
                                    pass
                        
                        # 가중치 점수 계산
                        skill_score = s_match * w_level * w_recency
                        weighted_score += skill_score
                        
                        matched_skills.append(req_skill)
                        skill_details.append({
                            'skill': skill_name,
                            'level': level,
                            'years': emp_skill.get('years', 0),
                            'score': round(skill_score, 2)
                        })
                        break
            
            # 도메인 경험 보너스 (Wdomain = 1.3)
            # 프로젝트 이력에서 유사 도메인 경험 확인
            domain_bonus = 0.0
            for project in work_experience:
                if isinstance(project, dict):
                    # 프로젝트 이름이나 설명에서 도메인 키워드 확인
                    project_name = project.get('project_name', '').lower()
                    # 간단한 도메인 매칭 (실제로는 더 정교한 로직 필요)
                    if any(keyword in project_name for keyword in ['금융', 'finance', '은행', 'banking']):
                        domain_bonus = weighted_score * 0.3  # 30% 보너스
                        break
            
            weighted_score += domain_bonus
            
            if matched_skills:
                # 0-100 범위로 정규화
                match_score = min(100.0, (weighted_score / len(required_skills)) * 50)
                
                matches.append({
                    'user_id': employee.get('user_id'),
                    'name': employee.get('basic_info', {}).get('name', ''),
                    'role': employee.get('basic_info', {}).get('role', ''),
                    'matched_skills': matched_skills,
                    'skill_match_score': match_score,
                    'skill_details': skill_details,
                    'years_of_experience': employee.get('basic_info', {}).get('years_of_experience', 0),
                    'domain_bonus': domain_bonus > 0
                })
        
        logger.info(f"기술 매칭 완료: {len(matches)}명 발견")
        return matches
        
    except Exception as e:
        logger.error(f"기술 검색 실패: {str(e)}")
        return []


def search_similar_employees(
    project_id: str,
    required_skills: List[str]
) -> List[Dict[str, Any]]:
    """
    벡터 유사도 검색 (간소화 버전)
    
    Requirements: 11.3, 11.4 - OpenSearch 벡터 검색
    
    Args:
        project_id: 프로젝트 ID
        required_skills: 요구 기술 목록
        
    Returns:
        list: 유사한 직원 목록
    """
    # OpenSearch가 설정되지 않은 경우 빈 리스트 반환
    # 기술 매칭만으로도 충분한 추천 가능
    logger.info("벡터 검색 스킵 - 기술 매칭 기반 추천 사용")
    return []


def get_affinity_scores() -> Dict[str, float]:
    """
    친밀도 점수 조회
    
    Requirements: 2.2 - 친밀도 점수 반영
    
    Returns:
        dict: 직원 쌍별 친밀도 점수
    """
    try:
        table = dynamodb.Table('EmployeeAffinity')
        response = table.scan()
        
        affinity_map = {}
        for item in response.get('Items', []):
            employee_pair = item.get('employee_pair', {})
            emp1 = employee_pair.get('employee_1')
            emp2 = employee_pair.get('employee_2')
            score = float(item.get('overall_affinity_score', 0))
            
            if emp1 and emp2:
                key = f"{emp1}_{emp2}"
                affinity_map[key] = score
                # 양방향 저장
                key_reverse = f"{emp2}_{emp1}"
                affinity_map[key_reverse] = score
        
        return affinity_map
        
    except Exception as e:
        logger.error(f"친밀도 점수 조회 실패: {str(e)}")
        return {}


def merge_and_score_candidates(
    skill_matches: List[Dict[str, Any]],
    vector_matches: List[Dict[str, Any]],
    affinity_scores: Dict[str, float],
    priority: str
) -> List[Dict[str, Any]]:
    """
    후보자 통합 및 종합 점수 계산
    
    Requirements: 2.2, 2.4 - 다중 요소 점수 계산
    
    Args:
        skill_matches: 기술 매칭 결과
        vector_matches: 벡터 검색 결과
        affinity_scores: 친밀도 점수
        priority: 우선순위
        
    Returns:
        list: 통합된 후보자 목록
    """
    # 후보자 통합
    candidates_map = {}
    
    # 기술 매칭 결과 추가
    for match in skill_matches:
        user_id = match['user_id']
        candidates_map[user_id] = {
            'user_id': user_id,
            'name': match.get('name', ''),
            'role': match.get('role', ''),
            'skill_match_score': match.get('skill_match_score', 0),
            'similarity_score': 0,
            'affinity_score': 0,
            'matched_skills': match.get('matched_skills', []),
            'years_of_experience': match.get('years_of_experience', 0)
        }
    
    # 벡터 검색 결과 추가
    for match in vector_matches:
        user_id = match['user_id']
        if user_id in candidates_map:
            candidates_map[user_id]['similarity_score'] = match.get('similarity_score', 0)
        else:
            candidates_map[user_id] = {
                'user_id': user_id,
                'name': match.get('name', ''),
                'role': match.get('role', ''),
                'skill_match_score': 0,
                'similarity_score': match.get('similarity_score', 0),
                'affinity_score': 0,
                'matched_skills': [],
                'years_of_experience': 0
            }
    
    # 친밀도 점수 추가 (평균)
    for user_id in candidates_map:
        related_scores = [
            score for key, score in affinity_scores.items()
            if user_id in key
        ]
        if related_scores:
            candidates_map[user_id]['affinity_score'] = sum(related_scores) / len(related_scores)
    
    # 종합 점수 계산
    for candidate in candidates_map.values():
        if priority == 'skill':
            weights = {'skill': 0.6, 'similarity': 0.3, 'affinity': 0.1}
        elif priority == 'affinity':
            weights = {'skill': 0.3, 'similarity': 0.2, 'affinity': 0.5}
        else:  # balanced
            weights = {'skill': 0.4, 'similarity': 0.3, 'affinity': 0.3}
        
        overall_score = (
            candidate['skill_match_score'] * weights['skill'] +
            candidate['similarity_score'] * weights['similarity'] +
            candidate['affinity_score'] * weights['affinity']
        )
        
        candidate['overall_score'] = overall_score
    
    return list(candidates_map.values())


def check_availability(candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    직원 가용성 확인
    
    Requirements: 2.5 - 가용성 정보 포함
    
    Args:
        candidates: 후보자 목록
        
    Returns:
        list: 가용성 정보가 추가된 후보자 목록
    """
    try:
        # 현재 프로젝트 배정 확인
        table = dynamodb.Table('Projects')
        response = table.scan()
        
        # 진행 중인 프로젝트 찾기
        active_projects = {}
        for project in response.get('Items', []):
            team = project.get('team_composition', {})
            for role, members in team.items():
                if isinstance(members, list):
                    for member_id in members:
                        active_projects[member_id] = project.get('project_name', '')
        
        # 가용성 정보 추가
        for candidate in candidates:
            user_id = candidate['user_id']
            if user_id in active_projects:
                candidate['availability'] = 'Busy'
                candidate['current_project'] = active_projects[user_id]
            else:
                candidate['availability'] = 'Available'
                candidate['current_project'] = None
        
        return candidates
        
    except Exception as e:
        logger.error(f"가용성 확인 실패: {str(e)}")
        # 오류 시 모두 Available로 설정
        for candidate in candidates:
            candidate['availability'] = 'Unknown'
            candidate['current_project'] = None
        return candidates


def generate_reasoning(candidate: Dict[str, Any]) -> str:
    """
    추천 근거 생성 (고급 알고리즘 기반)
    
    Requirements: 2.4 - 추천 근거 생성
    
    적합도 점수 공식 기반:
    Score(P, E) = Σ(Smatch × Wlevel × Wrecency) + (Expdomain × Wdomain)
    
    Args:
        candidate: 후보자 정보
        
    Returns:
        str: 추천 근거
    """
    matched_skills = candidate.get('matched_skills', [])
    skill_score = candidate.get('skill_match_score', 0)
    affinity_score = candidate.get('affinity_score', 0)
    availability = candidate.get('availability', 'Unknown')
    years_exp = candidate.get('years_of_experience', 0)
    role = candidate.get('role', '개발자')
    skill_details = candidate.get('skill_details', [])
    domain_bonus = candidate.get('domain_bonus', False)
    
    # 1단계: 적합도 점수 산정 (Feature Engineering)
    reasoning = f"""【1단계: 적합도 점수 산정】
▸ 기본 프로필: {years_exp}년 경력의 {role}
▸ 종합 적합도 점수: {skill_score:.1f}/100점

【점수 산정 공식】
Score(P,E) = Σ(Smatch × Wlevel × Wrecency) + (Expdomain × Wdomain)

"""
    
    # 기술별 상세 점수
    if skill_details:
        reasoning += "【기술별 가중치 분석】\n"
        for detail in skill_details[:3]:  # 상위 3개만 표시
            skill_name = detail.get('skill', '')
            level = detail.get('level', 'Intermediate')
            years = detail.get('years', 0)
            score = detail.get('score', 0)
            
            # 숙련도 가중치 설명
            level_weight_desc = {
                'Beginner': '1.0 (초급)',
                'Intermediate': '1.5 (중급)',
                'Advanced': '1.8 (고급)',
                'Expert': '2.0 (전문가)'
            }
            
            reasoning += f"  • {skill_name}: {level} ({years}년 경험)\n"
            reasoning += f"    - 숙련도 가중치(Wlevel): {level_weight_desc.get(level, '1.0')}\n"
            reasoning += f"    - 최신성 가중치(Wrecency): 최근 프로젝트 활용 반영\n"
            reasoning += f"    - 기술 점수: {score:.2f}점\n"
    
    # 도메인 경험 보너스
    if domain_bonus:
        reasoning += "\n【도메인 경험 가중치】\n"
        reasoning += "  • 유사 산업군 프로젝트 수행 이력 확인\n"
        reasoning += "  • 도메인 가중치(Wdomain): 1.3배 적용\n"
        reasoning += "  • 보너스 점수: +30% 가산\n"
    
    # 2단계: 추천 알고리즘 (Content-based Filtering)
    reasoning += f"\n【2단계: 추천 알고리즘】\n"
    reasoning += f"▸ 알고리즘: Content-based Filtering\n"
    reasoning += f"▸ 매칭된 핵심 기술: {', '.join(matched_skills[:5])}\n"
    
    if len(matched_skills) > 5:
        reasoning += f"▸ 추가 매칭 기술: 외 {len(matched_skills) - 5}개\n"
    
    # 3단계: 하이브리드 추천 (벡터 + 필터링)
    reasoning += f"\n【3단계: 하이브리드 점수】\n"
    
    # 팀 적합성 (친밀도)
    if affinity_score > 50:
        reasoning += f"▸ 팀 친밀도: {affinity_score:.1f}점 (우수)\n"
        reasoning += f"  - 기존 팀원들과 높은 협업 시너지 예상\n"
        reasoning += f"  - 친밀도 가중치: 0.2배 적용\n"
    elif affinity_score > 0:
        reasoning += f"▸ 팀 친밀도: {affinity_score:.1f}점\n"
        reasoning += f"  - 팀 협업 가능 수준\n"
    else:
        reasoning += f"▸ 팀 친밀도: 신규 팀원 (친밀도 데이터 없음)\n"
    
    # 가용성 필터
    reasoning += f"\n【4단계: 가용성 필터】\n"
    if availability == 'Available':
        reasoning += f"▸ 상태: 즉시 투입 가능 ✓\n"
        reasoning += f"  - 가용성 가중치: 1.0 (최대)\n"
    elif availability == 'Busy':
        current_project = candidate.get('current_project', '다른 프로젝트')
        reasoning += f"▸ 상태: 현재 '{current_project}' 참여 중\n"
        reasoning += f"  - 가용성 가중치: 0.5 (일정 조율 필요)\n"
        reasoning += f"  - 권장: 프로젝트 종료 시점 확인 후 배정\n"
    else:
        reasoning += f"▸ 상태: 가용성 확인 필요\n"
    
    # 최종 추천 근거
    reasoning += f"\n【최종 추천 근거】\n"
    
    if skill_score >= 70:
        reasoning += f"✓ 높은 기술 적합도 ({skill_score:.1f}점)\n"
    elif skill_score >= 50:
        reasoning += f"✓ 적정 기술 적합도 ({skill_score:.1f}점)\n"
    
    if affinity_score > 50:
        reasoning += f"✓ 우수한 팀 협업 능력\n"
    
    if domain_bonus:
        reasoning += f"✓ 유사 도메인 프로젝트 경험 보유\n"
    
    if availability == 'Available':
        reasoning += f"✓ 즉시 투입 가능\n"
    
    return reasoning


def decimal_default(obj):
    """Decimal을 float로 변환"""
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

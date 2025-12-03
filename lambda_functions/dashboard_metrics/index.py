"""
대시보드 메트릭 집계 Lambda 함수
전체 직원 수, 활성 프로젝트 수, 대기 중인 평가 등의 통계를 집계하여 반환
"""

import json
import os
import boto3
from decimal import Decimal
from boto3.dynamodb.conditions import Attr
from typing import Dict, List, Any

# DynamoDB 클라이언트 초기화
dynamodb = boto3.resource('dynamodb')

# 테이블 이름 환경 변수에서 가져오기
EMPLOYEES_TABLE = os.environ.get('EMPLOYEES_TABLE', 'Employees')
PROJECTS_TABLE = os.environ.get('PROJECTS_TABLE', 'Projects')
EVALUATIONS_TABLE = os.environ.get('EVALUATIONS_TABLE', 'EmployeeEvaluations')


class DecimalEncoder(json.JSONEncoder):
    """DynamoDB Decimal 타입을 JSON으로 변환하기 위한 인코더"""
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)


def get_total_employees() -> int:
    """전체 직원 수 조회"""
    try:
        table = dynamodb.Table(EMPLOYEES_TABLE)
        response = table.scan(Select='COUNT')
        return response.get('Count', 0)
    except Exception as e:
        print(f"Error getting total employees: {str(e)}")
        return 0


def get_active_projects() -> int:
    """진행 중인 프로젝트 수 조회"""
    try:
        table = dynamodb.Table(PROJECTS_TABLE)
        # 프로젝트 상태가 'in-progress'인 것만 카운트
        response = table.scan(
            FilterExpression=Attr('status').eq('in-progress'),
            Select='COUNT'
        )
        return response.get('Count', 0)
    except Exception as e:
        print(f"Error getting active projects: {str(e)}")
        # 상태 필드가 없는 경우 전체 프로젝트 수 반환
        try:
            response = table.scan(Select='COUNT')
            return response.get('Count', 0)
        except:
            return 0


def get_available_employees() -> int:
    """투입 대기 인력 수 조회 (현재 프로젝트에 배정되지 않은 직원)"""
    try:
        table = dynamodb.Table(EMPLOYEES_TABLE)
        # currentProject가 없거나 None인 직원 카운트
        response = table.scan()
        items = response.get('Items', [])
        
        # currentProject가 없거나 None인 직원 필터링
        available_count = 0
        for item in items:
            current_project = item.get('currentProject')
            if current_project is None or current_project == '':
                available_count += 1
        
        return available_count
    except Exception as e:
        print(f"Error getting available employees: {str(e)}")
        return 0


def get_pending_candidates() -> int:
    """대기자명단 수 조회"""
    try:
        table = dynamodb.Table('PendingCandidates')
        response = table.scan(Select='COUNT')
        return response.get('Count', 0)
    except Exception as e:
        print(f"Error getting pending candidates: {str(e)}")
        return 0


def get_employee_distribution() -> Dict[str, Any]:
    """인력 현황 상세 분포"""
    try:
        table = dynamodb.Table(EMPLOYEES_TABLE)
        response = table.scan()
        items = response.get('Items', [])
        
        # 부서별 분포
        department_dist = {}
        # 경력 분포
        experience_dist = {'신입': 0, '주니어': 0, '시니어': 0, '리드': 0}
        # 역할별 분포
        role_dist = {}
        
        for employee in items:
            # 부서별
            dept = employee.get('department', '미지정')
            department_dist[dept] = department_dist.get(dept, 0) + 1
            
            # 경력별
            years = employee.get('basic_info', {}).get('years_of_experience', 0)
            if isinstance(years, Decimal):
                years = float(years)
            if years < 3:
                experience_dist['신입'] += 1
            elif years < 6:
                experience_dist['주니어'] += 1
            elif years < 11:
                experience_dist['시니어'] += 1
            else:
                experience_dist['리드'] += 1
            
            # 역할별
            role = employee.get('basic_info', {}).get('role', '미지정')
            role_dist[role] = role_dist.get(role, 0) + 1
        
        return {
            'by_department': [{'name': k, 'count': v} for k, v in department_dist.items()],
            'by_experience': [{'name': k, 'count': v} for k, v in experience_dist.items()],
            'by_role': [{'name': k, 'count': v} for k, v in role_dist.items()]
        }
    except Exception as e:
        print(f"Error getting employee distribution: {str(e)}")
        return {'by_department': [], 'by_experience': [], 'by_role': []}


def get_project_distribution() -> Dict[str, Any]:
    """프로젝트 현황 분포"""
    try:
        table = dynamodb.Table(PROJECTS_TABLE)
        response = table.scan()
        items = response.get('Items', [])
        
        # 상태별 분포
        status_dist = {'planning': 0, 'in-progress': 0, 'completed': 0}
        # 산업별 분포
        industry_dist = {}
        # 예산 규모별 분포
        budget_dist = {'소형': 0, '중형': 0, '대형': 0}
        
        for project in items:
            # 상태별
            status = project.get('status', 'in-progress')
            if status in status_dist:
                status_dist[status] += 1
            
            # 산업별
            industry = project.get('client_industry', '기타')
            industry_dist[industry] = industry_dist.get(industry, 0) + 1
            
            # 예산 규모별
            budget = project.get('budget_scale', '중형')
            if budget in budget_dist:
                budget_dist[budget] += 1
        
        return {
            'by_status': [{'name': k, 'count': v} for k, v in status_dist.items()],
            'by_industry': [{'name': k, 'count': v} for k, v in industry_dist.items()],
            'by_budget': [{'name': k, 'count': v} for k, v in budget_dist.items()]
        }
    except Exception as e:
        print(f"Error getting project distribution: {str(e)}")
        return {'by_status': [], 'by_industry': [], 'by_budget': []}


def get_evaluation_stats() -> Dict[str, Any]:
    """평가 현황 통계"""
    try:
        table = dynamodb.Table(EVALUATIONS_TABLE)
        response = table.scan()
        items = response.get('Items', [])
        
        # 상태별 건수
        status_dist = {'pending': 0, 'approved': 0, 'rejected': 0, 'review': 0}
        # 유형별 건수
        type_dist = {'career': 0, 'freelancer': 0}
        # 평균 점수
        total_score = 0
        score_count = 0
        
        for evaluation in items:
            # 상태별
            status = evaluation.get('status', 'pending')
            if status in status_dist:
                status_dist[status] += 1
            
            # 유형별
            eval_type = evaluation.get('type', 'career')
            if eval_type in type_dist:
                type_dist[eval_type] += 1
            
            # 평균 점수 계산
            score = evaluation.get('overall_score')
            if score is not None:
                if isinstance(score, Decimal):
                    score = float(score)
                total_score += score
                score_count += 1
        
        avg_score = round(total_score / score_count, 1) if score_count > 0 else 0
        
        # 승인율 계산
        total_processed = status_dist['approved'] + status_dist['rejected']
        approval_rate = round((status_dist['approved'] / total_processed * 100), 1) if total_processed > 0 else 0
        
        return {
            'by_status': [{'name': k, 'count': v} for k, v in status_dist.items()],
            'by_type': [{'name': k, 'count': v} for k, v in type_dist.items()],
            'average_score': avg_score,
            'approval_rate': approval_rate,
            'total_evaluations': len(items)
        }
    except Exception as e:
        print(f"Error getting evaluation stats: {str(e)}")
        return {
            'by_status': [],
            'by_type': [],
            'average_score': 0,
            'approval_rate': 0,
            'total_evaluations': 0
        }


def get_pending_candidates_detail() -> Dict[str, Any]:
    """대기자명단 상세 정보"""
    try:
        table = dynamodb.Table('PendingCandidates')
        response = table.scan()
        items = response.get('Items', [])
        
        from datetime import datetime, timedelta
        
        # 대기 기간별 분포
        wait_dist = {'1주 이내': 0, '1-2주': 0, '2주 이상': 0}
        total_wait_days = 0
        
        for candidate in items:
            created_at = candidate.get('created_at', '')
            if created_at:
                try:
                    created_date = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                    wait_days = (datetime.now(created_date.tzinfo) - created_date).days
                    total_wait_days += wait_days
                    
                    if wait_days <= 7:
                        wait_dist['1주 이내'] += 1
                    elif wait_days <= 14:
                        wait_dist['1-2주'] += 1
                    else:
                        wait_dist['2주 이상'] += 1
                except:
                    wait_dist['1주 이내'] += 1
        
        avg_wait_days = round(total_wait_days / len(items)) if len(items) > 0 else 0
        
        return {
            'total': len(items),
            'by_wait_period': [{'name': k, 'count': v} for k, v in wait_dist.items()],
            'average_wait_days': avg_wait_days
        }
    except Exception as e:
        print(f"Error getting pending candidates detail: {str(e)}")
        return {'total': 0, 'by_wait_period': [], 'average_wait_days': 0}


def get_action_required_items() -> Dict[str, Any]:
    """알림/액션 필요 항목"""
    try:
        from datetime import datetime, timedelta
        
        # 장기 대기 인력 (3개월 이상 프로젝트 미배정)
        emp_table = dynamodb.Table(EMPLOYEES_TABLE)
        emp_response = emp_table.scan()
        employees = emp_response.get('Items', [])
        
        long_waiting = 0
        for emp in employees:
            if not emp.get('currentProject'):
                # 실제로는 마지막 프로젝트 종료일을 확인해야 하지만, 
                # 현재는 currentProject가 없는 경우로 판단
                long_waiting += 1
        
        # 평가 지연 건 (제출 후 7일 이상 pending)
        eval_table = dynamodb.Table(EVALUATIONS_TABLE)
        eval_response = eval_table.scan()
        evaluations = eval_response.get('Items', [])
        
        delayed_evaluations = 0
        for evaluation in evaluations:
            if evaluation.get('status') == 'pending':
                submitted_at = evaluation.get('submitted_at', '')
                if submitted_at:
                    try:
                        submitted_date = datetime.fromisoformat(submitted_at.replace('Z', '+00:00'))
                        days_pending = (datetime.now(submitted_date.tzinfo) - submitted_date).days
                        if days_pending >= 7:
                            delayed_evaluations += 1
                    except:
                        pass
        
        # 검증 필요 이력서 (verification_questions 미완료)
        # PendingCandidates 테이블에서 확인
        pending_table = dynamodb.Table('PendingCandidates')
        pending_response = pending_table.scan()
        pending_items = pending_response.get('Items', [])
        
        verification_needed = 0
        for item in pending_items:
            if not item.get('verification_completed'):
                verification_needed += 1
        
        return {
            'long_waiting_employees': long_waiting,
            'delayed_evaluations': delayed_evaluations,
            'verification_needed': verification_needed
        }
    except Exception as e:
        print(f"Error getting action required items: {str(e)}")
        return {
            'long_waiting_employees': 0,
            'delayed_evaluations': 0,
            'verification_needed': 0
        }


def get_skill_competency_analysis() -> Dict[str, Any]:
    """기술 역량 분석"""
    try:
        table = dynamodb.Table(EMPLOYEES_TABLE)
        response = table.scan()
        items = response.get('Items', [])
        
        skill_levels = {}  # 기술별 숙련도 집계
        skill_counts = {}  # 기술별 보유 인력 수
        multi_skilled = 0  # 5개 이상 기술 보유
        
        for employee in items:
            skills = employee.get('skills', [])
            if len(skills) >= 5:
                multi_skilled += 1
            
            for skill in skills:
                if isinstance(skill, dict):
                    skill_name = skill.get('name', '')
                    skill_level = skill.get('level', 'Beginner')
                    
                    if skill_name:
                        skill_counts[skill_name] = skill_counts.get(skill_name, 0) + 1
                        
                        if skill_name not in skill_levels:
                            skill_levels[skill_name] = {'Beginner': 0, 'Intermediate': 0, 'Advanced': 0, 'Expert': 0}
                        skill_levels[skill_name][skill_level] = skill_levels[skill_name].get(skill_level, 0) + 1
        
        # 희소 기술 (3명 이하)
        rare_skills = [{'name': k, 'count': v} for k, v in skill_counts.items() if v <= 3]
        
        # 기술별 평균 숙련도
        skill_proficiency = []
        for skill_name, levels in skill_levels.items():
            total = sum(levels.values())
            if total > 0:
                # 숙련도 점수 계산 (Beginner=1, Intermediate=2, Advanced=3, Expert=4)
                score = (levels.get('Beginner', 0) * 1 + levels.get('Intermediate', 0) * 2 + 
                        levels.get('Advanced', 0) * 3 + levels.get('Expert', 0) * 4) / total
                skill_proficiency.append({'name': skill_name, 'avg_level': round(score, 2), 'count': total})
        
        skill_proficiency.sort(key=lambda x: x['avg_level'], reverse=True)
        
        return {
            'rare_skills': rare_skills[:10],
            'multi_skilled_count': multi_skilled,
            'top_proficiency_skills': skill_proficiency[:10],
            'total_unique_skills': len(skill_counts)
        }
    except Exception as e:
        print(f"Error in skill competency analysis: {str(e)}")
        return {'rare_skills': [], 'multi_skilled_count': 0, 'top_proficiency_skills': [], 'total_unique_skills': 0}


def get_career_growth_analysis() -> Dict[str, Any]:
    """경력 & 성장 분석"""
    try:
        table = dynamodb.Table(EMPLOYEES_TABLE)
        response = table.scan()
        items = response.get('Items', [])
        
        total_years = 0
        senior_count = 0  # 10년 이상
        skill_per_year = []
        
        for employee in items:
            years = employee.get('basic_info', {}).get('years_of_experience', 0)
            if isinstance(years, Decimal):
                years = float(years)
            
            total_years += years
            
            if years >= 10:
                senior_count += 1
            
            # 경력 대비 기술 수
            skills_count = len(employee.get('skills', []))
            if years > 0:
                skill_per_year.append(skills_count / years)
        
        avg_years = round(total_years / len(items), 1) if len(items) > 0 else 0
        avg_skill_growth = round(sum(skill_per_year) / len(skill_per_year), 2) if skill_per_year else 0
        senior_ratio = round((senior_count / len(items)) * 100, 1) if len(items) > 0 else 0
        
        return {
            'average_years': avg_years,
            'senior_count': senior_count,
            'senior_ratio': senior_ratio,
            'skill_growth_rate': avg_skill_growth
        }
    except Exception as e:
        print(f"Error in career growth analysis: {str(e)}")
        return {'average_years': 0, 'senior_count': 0, 'senior_ratio': 0, 'skill_growth_rate': 0}


def get_project_experience_analysis() -> Dict[str, Any]:
    """프로젝트 참여 이력 분석"""
    try:
        table = dynamodb.Table(EMPLOYEES_TABLE)
        response = table.scan()
        items = response.get('Items', [])
        
        total_projects = 0
        no_experience = 0
        multi_industry = 0
        leader_count = 0
        
        for employee in items:
            work_exp = employee.get('work_experience', [])
            project_count = len(work_exp)
            total_projects += project_count
            
            if project_count == 0:
                no_experience += 1
            
            # 다양한 산업 경험 (3개 이상 다른 산업)
            industries = set()
            has_leader_role = False
            
            for exp in work_exp:
                if isinstance(exp, dict):
                    # 산업 정보는 프로젝트 테이블과 조인 필요하지만, 간단히 프로젝트 수로 판단
                    role = exp.get('role', '').lower()
                    if 'lead' in role or 'manager' in role or 'architect' in role:
                        has_leader_role = True
            
            if project_count >= 3:
                multi_industry += 1
            
            if has_leader_role:
                leader_count += 1
        
        avg_projects = round(total_projects / len(items), 1) if len(items) > 0 else 0
        
        return {
            'average_projects': avg_projects,
            'no_experience_count': no_experience,
            'multi_industry_count': multi_industry,
            'leader_experience_count': leader_count
        }
    except Exception as e:
        print(f"Error in project experience analysis: {str(e)}")
        return {'average_projects': 0, 'no_experience_count': 0, 'multi_industry_count': 0, 'leader_experience_count': 0}


def get_utilization_analysis() -> Dict[str, Any]:
    """인력 활용도 분석"""
    try:
        table = dynamodb.Table(EMPLOYEES_TABLE)
        response = table.scan()
        items = response.get('Items', [])
        
        assigned = 0
        available = 0
        
        for employee in items:
            if employee.get('currentProject'):
                assigned += 1
            else:
                available += 1
        
        utilization_rate = round((assigned / len(items)) * 100, 1) if len(items) > 0 else 0
        
        return {
            'assigned_count': assigned,
            'available_count': available,
            'utilization_rate': utilization_rate
        }
    except Exception as e:
        print(f"Error in utilization analysis: {str(e)}")
        return {'assigned_count': 0, 'available_count': 0, 'utilization_rate': 0}


def get_education_certification_analysis() -> Dict[str, Any]:
    """학력 & 자격증 분석"""
    try:
        table = dynamodb.Table(EMPLOYEES_TABLE)
        response = table.scan()
        items = response.get('Items', [])
        
        education_dist = {}
        total_certs = 0
        no_cert_count = 0
        
        for employee in items:
            # 학력
            education = employee.get('education', {})
            if isinstance(education, dict):
                degree = education.get('degree', '미지정')
                education_dist[degree] = education_dist.get(degree, 0) + 1
            
            # 자격증
            certs = employee.get('certifications', [])
            cert_count = len(certs) if isinstance(certs, list) else 0
            total_certs += cert_count
            
            if cert_count == 0:
                no_cert_count += 1
        
        avg_certs = round(total_certs / len(items), 1) if len(items) > 0 else 0
        
        return {
            'education_distribution': [{'name': k, 'count': v} for k, v in education_dist.items()],
            'average_certifications': avg_certs,
            'no_certification_count': no_cert_count
        }
    except Exception as e:
        print(f"Error in education certification analysis: {str(e)}")
        return {'education_distribution': [], 'average_certifications': 0, 'no_certification_count': 0}


def get_portfolio_health_analysis() -> Dict[str, Any]:
    """인력 포트폴리오 건강도 분석"""
    try:
        table = dynamodb.Table(EMPLOYEES_TABLE)
        response = table.scan()
        items = response.get('Items', [])
        
        role_categories = {'Backend': 0, 'Frontend': 0, 'Fullstack': 0, 'DevOps': 0, 'Other': 0}
        
        for employee in items:
            role = employee.get('basic_info', {}).get('role', '').lower()
            
            if 'backend' in role:
                role_categories['Backend'] += 1
            elif 'frontend' in role:
                role_categories['Frontend'] += 1
            elif 'full' in role or 'fullstack' in role:
                role_categories['Fullstack'] += 1
            elif 'devops' in role or 'infra' in role:
                role_categories['DevOps'] += 1
            else:
                role_categories['Other'] += 1
        
        # 기술 다양성 지수 (보유 기술 종류 / 전체 인력)
        all_skills = set()
        for employee in items:
            for skill in employee.get('skills', []):
                if isinstance(skill, dict):
                    skill_name = skill.get('name', '')
                    if skill_name:
                        all_skills.add(skill_name)
        
        diversity_index = round(len(all_skills) / len(items), 2) if len(items) > 0 else 0
        
        return {
            'role_distribution': [{'name': k, 'count': v} for k, v in role_categories.items()],
            'skill_diversity_index': diversity_index,
            'unique_skills_count': len(all_skills)
        }
    except Exception as e:
        print(f"Error in portfolio health analysis: {str(e)}")
        return {'role_distribution': [], 'skill_diversity_index': 0, 'unique_skills_count': 0}


def get_employee_quality_analysis() -> Dict[str, Any]:
    """직원 품질 분석 (평가 기반)"""
    try:
        table = dynamodb.Table(EMPLOYEES_TABLE)
        response = table.scan()
        items = response.get('Items', [])
        
        # 고급 기술 보유자 (난이도 높은 기술)
        advanced_tech_keywords = ['kubernetes', 'k8s', 'msa', 'microservices', 'aws', 'azure', 'gcp', 'ai', 'ml', 'machine learning']
        advanced_tech_count = 0
        
        # 역량 레벨 분포 (직원별 최고 레벨만 카운트)
        skill_level_dist = {'Expert': 0, 'Advanced': 0, 'Intermediate': 0, 'Beginner': 0}
        level_priority = {'Expert': 4, 'Advanced': 3, 'Intermediate': 2, 'Beginner': 1}
        
        # 성과 기록 보유자
        performance_record_count = 0
        
        # 다중 역할 경험자
        multi_role_count = 0
        
        for employee in items:
            # 고급 기술 체크
            skills = employee.get('skills', [])
            has_advanced_tech = False
            
            # 직원의 최고 역량 레벨 찾기
            highest_level = 'Beginner'
            highest_priority = 0
            
            for skill in skills:
                if isinstance(skill, dict):
                    skill_name = skill.get('name', '').lower()
                    if any(keyword in skill_name for keyword in advanced_tech_keywords):
                        has_advanced_tech = True
                    
                    # 최고 레벨 찾기
                    level = skill.get('level', 'Beginner')
                    priority = level_priority.get(level, 0)
                    if priority > highest_priority:
                        highest_priority = priority
                        highest_level = level
            
            # 직원별 최고 레벨만 카운트
            if highest_level in skill_level_dist:
                skill_level_dist[highest_level] += 1
            
            if has_advanced_tech:
                advanced_tech_count += 1
            
            # 성과 기록 체크
            work_exp = employee.get('work_experience', [])
            for exp in work_exp:
                if isinstance(exp, dict) and exp.get('performance_result'):
                    performance_record_count += 1
                    break
            
            # 다중 역할 경험 체크
            roles = set()
            for exp in work_exp:
                if isinstance(exp, dict):
                    role = exp.get('role', '')
                    if role:
                        roles.add(role)
            if len(roles) >= 3:
                multi_role_count += 1
        
        # 비율 계산
        total = len(items)
        advanced_tech_ratio = round((advanced_tech_count / total) * 100, 1) if total > 0 else 0
        performance_ratio = round((performance_record_count / total) * 100, 1) if total > 0 else 0
        
        return {
            'advanced_tech_count': advanced_tech_count,
            'advanced_tech_ratio': advanced_tech_ratio,
            'skill_level_distribution': [{'name': k, 'count': v} for k, v in skill_level_dist.items()],
            'performance_record_count': performance_record_count,
            'performance_ratio': performance_ratio,
            'multi_role_count': multi_role_count
        }
    except Exception as e:
        print(f"Error in employee quality analysis: {str(e)}")
        return {
            'advanced_tech_count': 0,
            'advanced_tech_ratio': 0,
            'skill_level_distribution': [],
            'performance_record_count': 0,
            'performance_ratio': 0,
            'multi_role_count': 0
        }


def get_domain_expertise_analysis() -> Dict[str, Any]:
    """도메인 전문성 분석 (프로젝트 경험 기반)"""
    try:
        emp_table = dynamodb.Table(EMPLOYEES_TABLE)
        emp_response = emp_table.scan()
        employees = emp_response.get('Items', [])
        
        # 프로젝트 이름에서 도메인 추출을 위한 키워드 매핑
        domain_keywords = {
            '금융': ['금융', '뱅킹', '은행', '증권', '보험', '카드', 'banking', 'finance'],
            '전자상거래': ['커머스', '쇼핑', '이커머스', '유통', '리테일', 'commerce', 'retail', 'shopping'],
            '의료': ['의료', '병원', '헬스케어', '건강', 'healthcare', 'medical', 'hospital'],
            '제조': ['제조', '공장', '생산', 'manufacturing', 'factory'],
            '통신': ['통신', '네트워크', '5G', 'telecom', 'network'],
            '교육': ['교육', '학습', '이러닝', 'education', 'learning'],
            '물류': ['물류', '배송', '운송', 'logistics', 'delivery'],
            '게임': ['게임', 'game', 'gaming'],
            '미디어': ['미디어', '콘텐츠', '방송', 'media', 'content'],
            '공공': ['공공', '정부', '행정', 'government', 'public']
        }
        
        def extract_domain(project_name: str) -> str:
            """프로젝트 이름에서 도메인 추출"""
            if not project_name:
                return '기타'
            
            project_name_lower = project_name.lower()
            for domain, keywords in domain_keywords.items():
                for keyword in keywords:
                    if keyword in project_name_lower:
                        return domain
            return '기타'
        
        # 직원별 경험한 도메인 집계
        domain_exp_count = {}
        multi_domain_count = 0
        total_projects = 0
        
        for employee in employees:
            work_exp = employee.get('work_experience', [])
            employee_domains = set()
            
            for exp in work_exp:
                if isinstance(exp, dict):
                    project_name = exp.get('project_name', '')
                    if project_name:
                        domain = extract_domain(project_name)
                        employee_domains.add(domain)
                        total_projects += 1
            
            # 2개 이상 도메인 경험
            if len(employee_domains) >= 2:
                multi_domain_count += 1
            
            # 도메인별 경험 인력 수 집계
            for domain in employee_domains:
                domain_exp_count[domain] = domain_exp_count.get(domain, 0) + 1
        
        # 평균 프로젝트 수
        avg_projects = round(total_projects / len(employees), 1) if len(employees) > 0 else 0
        
        # 상위 도메인
        top_domains = sorted(domain_exp_count.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            'multi_domain_experts': multi_domain_count,
            'average_domain_years': avg_projects,
            'top_domains': [{'name': k, 'count': v} for k, v in top_domains],
            'total_domains': len(domain_exp_count)
        }
    except Exception as e:
        print(f"Error in domain expertise analysis: {str(e)}")
        return {
            'multi_domain_experts': 0,
            'average_domain_years': 0,
            'top_domains': [],
            'total_domains': 0
        }


def calculate_employee_score(employee: Dict) -> float:
    """직원 평가 점수 계산 (간소화 버전)"""
    try:
        score = 0
        
        # 1. 기술 역량 (40점)
        skills = employee.get('skills', [])
        skill_score = 0
        for skill in skills:
            if isinstance(skill, dict):
                level = skill.get('level', 'Beginner')
                years = skill.get('years', 0)
                if isinstance(years, Decimal):
                    years = float(years)
                
                level_score = {'Expert': 10, 'Advanced': 7, 'Intermediate': 5, 'Beginner': 3}.get(level, 3)
                skill_score += level_score + min(years, 5)
        
        score += min(skill_score / len(skills) * 4, 40) if skills else 0
        
        # 2. 경력 (30점)
        years_exp = employee.get('basic_info', {}).get('years_of_experience', 0)
        if isinstance(years_exp, Decimal):
            years_exp = float(years_exp)
        score += min(years_exp * 2, 30)
        
        # 3. 프로젝트 경험 (20점)
        work_exp = employee.get('work_experience', [])
        project_score = len(work_exp) * 5
        # 성과 기록 보너스
        for exp in work_exp:
            if isinstance(exp, dict) and exp.get('performance_result'):
                project_score += 5
                break
        score += min(project_score, 20)
        
        # 4. 자격증 (10점)
        certs = employee.get('certifications', [])
        cert_count = len(certs) if isinstance(certs, list) else 0
        score += min(cert_count * 2, 10)
        
        return round(min(score, 100), 1)
    except Exception as e:
        print(f"Error calculating score: {str(e)}")
        return 0


def get_evaluation_score_analysis() -> Dict[str, Any]:
    """평가 점수 분석"""
    try:
        table = dynamodb.Table(EMPLOYEES_TABLE)
        response = table.scan()
        items = response.get('Items', [])
        
        scores = []
        score_by_role = {}
        score_by_dept = {}
        score_by_experience = {'신입': [], '주니어': [], '시니어': [], '리드': []}
        
        # 점수 분포
        score_dist = {'우수 (90+)': 0, '양호 (80-89)': 0, '보통 (70-79)': 0, '개선필요 (<70)': 0}
        
        for employee in items:
            score = calculate_employee_score(employee)
            scores.append(score)
            
            # 점수 분포
            if score >= 90:
                score_dist['우수 (90+)'] += 1
            elif score >= 80:
                score_dist['양호 (80-89)'] += 1
            elif score >= 70:
                score_dist['보통 (70-79)'] += 1
            else:
                score_dist['개선필요 (<70)'] += 1
            
            # 역할별
            role = employee.get('basic_info', {}).get('role', '미지정')
            if role not in score_by_role:
                score_by_role[role] = []
            score_by_role[role].append(score)
            
            # 부서별
            dept = employee.get('department', '미지정')
            if dept not in score_by_dept:
                score_by_dept[dept] = []
            score_by_dept[dept].append(score)
            
            # 경력별
            years = employee.get('basic_info', {}).get('years_of_experience', 0)
            if isinstance(years, Decimal):
                years = float(years)
            if years < 3:
                score_by_experience['신입'].append(score)
            elif years < 6:
                score_by_experience['주니어'].append(score)
            elif years < 11:
                score_by_experience['시니어'].append(score)
            else:
                score_by_experience['리드'].append(score)
        
        # 평균 계산
        avg_score = round(sum(scores) / len(scores), 1) if scores else 0
        
        # 역할별 평균 (상위 5개)
        role_avg = [(role, round(sum(scores) / len(scores), 1)) for role, scores in score_by_role.items() if scores]
        role_avg.sort(key=lambda x: x[1], reverse=True)
        
        # 경력별 평균
        exp_avg = [(level, round(sum(scores) / len(scores), 1)) for level, scores in score_by_experience.items() if scores]
        
        return {
            'average_score': avg_score,
            'score_distribution': [{'name': k, 'count': v} for k, v in score_dist.items()],
            'top_roles_by_score': [{'name': role, 'avg_score': score} for role, score in role_avg[:5]],
            'score_by_experience': [{'name': level, 'avg_score': score} for level, score in exp_avg],
            'high_performers': score_dist['우수 (90+)'],
            'low_performers': score_dist['개선필요 (<70)']
        }
    except Exception as e:
        print(f"Error in evaluation score analysis: {str(e)}")
        return {
            'average_score': 0,
            'score_distribution': [],
            'top_roles_by_score': [],
            'score_by_experience': [],
            'high_performers': 0,
            'low_performers': 0
        }


def get_skill_gap_analysis() -> Dict[str, Any]:
    """역량 갭 분석"""
    try:
        emp_table = dynamodb.Table(EMPLOYEES_TABLE)
        proj_table = dynamodb.Table(PROJECTS_TABLE)
        
        emp_response = emp_table.scan()
        proj_response = proj_table.scan()
        
        employees = emp_response.get('Items', [])
        projects = proj_response.get('Items', [])
        
        # 직원 보유 기술 집계
        employee_skills = {}
        for emp in employees:
            for skill in emp.get('skills', []):
                if isinstance(skill, dict):
                    skill_name = skill.get('name', '')
                    if skill_name:
                        employee_skills[skill_name] = employee_skills.get(skill_name, 0) + 1
        
        # 프로젝트 필요 기술 집계
        project_skills = {}
        for proj in projects:
            tech_stack = proj.get('tech_stack', {})
            for category in ['backend', 'frontend', 'data', 'infra']:
                skills = tech_stack.get(category, [])
                for skill in skills:
                    project_skills[skill] = project_skills.get(skill, 0) + 1
        
        # 부족한 기술 (수요 > 공급)
        skill_gaps = []
        for skill, demand in project_skills.items():
            supply = employee_skills.get(skill, 0)
            if demand > supply:
                gap = demand - supply
                skill_gaps.append({'skill': skill, 'gap': gap, 'demand': demand, 'supply': supply})
        
        skill_gaps.sort(key=lambda x: x['gap'], reverse=True)
        
        # 교육 필요 인력 수 (평균 이하 점수)
        scores = [calculate_employee_score(emp) for emp in employees]
        avg_score = sum(scores) / len(scores) if scores else 0
        training_needed = sum(1 for score in scores if score < avg_score)
        
        return {
            'top_skill_gaps': skill_gaps[:10],
            'total_skill_gaps': len(skill_gaps),
            'training_needed_count': training_needed
        }
    except Exception as e:
        print(f"Error in skill gap analysis: {str(e)}")
        return {
            'top_skill_gaps': [],
            'total_skill_gaps': 0,
            'training_needed_count': 0
        }


def get_top_skills() -> List[Dict[str, Any]]:
    """주요 기술 스택 분포 조회"""
    try:
        table = dynamodb.Table(EMPLOYEES_TABLE)
        response = table.scan()
        items = response.get('Items', [])
        
        # 모든 직원의 기술 스택 집계
        skill_counts = {}
        total_employees = len(items)
        
        for employee in items:
            skills = employee.get('skills', [])
            for skill in skills:
                skill_name = skill.get('name', '') if isinstance(skill, dict) else str(skill)
                if skill_name:
                    skill_counts[skill_name] = skill_counts.get(skill_name, 0) + 1
        
        # 상위 5개 기술 추출
        sorted_skills = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        top_skills = []
        for skill_name, count in sorted_skills:
            percentage = int((count / total_employees) * 100) if total_employees > 0 else 0
            top_skills.append({
                "name": skill_name,
                "count": count,
                "percentage": percentage
            })
        
        return top_skills
    except Exception as e:
        print(f"Error getting top skills: {str(e)}")
        return []


def lambda_handler(event, context):
    """
    Lambda 핸들러 함수
    대시보드 메트릭을 집계하여 반환
    """
    try:
        # CORS 헤더 설정
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Methods': 'GET,OPTIONS'
        }
        
        # OPTIONS 요청 처리 (CORS preflight)
        if event.get('httpMethod') == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({'message': 'OK'})
            }
        
        # 메트릭 집계
        total_employees = get_total_employees()
        active_projects = get_active_projects()
        available_employees = get_available_employees()
        pending_candidates = get_pending_candidates()
        top_skills = get_top_skills()
        
        # 기존 상세 지표들
        employee_distribution = get_employee_distribution()
        project_distribution = get_project_distribution()
        evaluation_stats = get_evaluation_stats()
        pending_candidates_detail = get_pending_candidates_detail()
        action_required = get_action_required_items()
        
        # 새로운 인력 분석 지표들
        skill_competency = get_skill_competency_analysis()
        career_growth = get_career_growth_analysis()
        project_experience = get_project_experience_analysis()
        utilization = get_utilization_analysis()
        education_cert = get_education_certification_analysis()
        portfolio_health = get_portfolio_health_analysis()
        employee_quality = get_employee_quality_analysis()
        domain_expertise = get_domain_expertise_analysis()
        evaluation_scores = get_evaluation_score_analysis()
        skill_gaps = get_skill_gap_analysis()
        
        # 응답 데이터 구성
        metrics = {
            'total_employees': total_employees,
            'active_projects': active_projects,
            'available_employees': available_employees,
            'pending_candidates': pending_candidates,
            'top_skills': top_skills,
            'employee_distribution': employee_distribution,
            'project_distribution': project_distribution,
            'evaluation_stats': evaluation_stats,
            'pending_candidates_detail': pending_candidates_detail,
            'action_required': action_required,
            # 새로운 분석 지표
            'skill_competency': skill_competency,
            'career_growth': career_growth,
            'project_experience': project_experience,
            'utilization': utilization,
            'education_certification': education_cert,
            'portfolio_health': portfolio_health,
            'employee_quality': employee_quality,
            'domain_expertise': domain_expertise,
            'evaluation_scores': evaluation_scores,
            'skill_gaps': skill_gaps
        }
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(metrics, cls=DecimalEncoder)
        }
        
    except Exception as e:
        print(f"Error in lambda_handler: {str(e)}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({
                'error': 'Internal server error',
                'message': str(e)
            })
        }

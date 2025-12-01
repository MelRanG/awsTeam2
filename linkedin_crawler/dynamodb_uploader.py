"""
DynamoDB 업로더
크롤링된 LinkedIn 프로필을 DynamoDB Employees 테이블에 저장
"""

import boto3
import uuid
import re
from typing import Dict, Any, List
from decimal import Decimal
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DynamoDBUploader:
    """DynamoDB 업로더"""
    
    def __init__(self, region: str = 'us-east-2'):
        """
        Args:
            region: AWS 리전
        """
        self.dynamodb = boto3.resource('dynamodb', region_name=region)
        self.employees_table = self.dynamodb.Table('Employees')
        
    def upload_profiles(self, profiles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        프로필 리스트를 DynamoDB에 업로드
        
        Args:
            profiles: 크롤링된 프로필 리스트
            
        Returns:
            업로드 결과 통계
        """
        success_count = 0
        fail_count = 0
        failed_profiles = []
        
        for idx, profile in enumerate(profiles, 1):
            try:
                logger.info(f"[{idx}/{len(profiles)}] 업로드 중: {profile.get('name', 'Unknown')}")
                
                # DynamoDB 형식으로 변환
                employee_data = self._convert_to_employee_format(profile)
                
                # DynamoDB에 저장
                self.employees_table.put_item(Item=employee_data)
                
                success_count += 1
                logger.info(f"✓ 업로드 성공: {employee_data['user_id']}")
                
            except Exception as e:
                fail_count += 1
                failed_profiles.append({
                    'name': profile.get('name', 'Unknown'),
                    'error': str(e)
                })
                logger.error(f"✗ 업로드 실패: {profile.get('name', 'Unknown')} - {str(e)}")
        
        result = {
            'total': len(profiles),
            'success': success_count,
            'failed': fail_count,
            'failed_profiles': failed_profiles
        }
        
        logger.info(f"\n업로드 완료: 성공 {success_count}개, 실패 {fail_count}개")
        return result
    
    def _convert_to_employee_format(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        LinkedIn 프로필을 DynamoDB Employee 형식으로 변환
        
        Args:
            profile: LinkedIn 프로필 데이터
            
        Returns:
            DynamoDB Employee 형식 데이터
        """
        # 고유 user_id 생성
        user_id = f"EMP_{uuid.uuid4().hex[:8].upper()}"
        
        # 기본 정보
        basic_info = {
            'name': profile.get('name', 'Unknown'),
            'role': profile.get('current_role', 'Unknown'),
            'years_of_experience': profile.get('years_of_experience', 0),
            'email': f"{user_id.lower()}@linkedin.com"  # 가상 이메일
        }
        
        # 기술 스택 변환
        skills = self._convert_skills(profile.get('skills', []))
        
        # 경력 사항 변환
        work_experience = self._convert_work_experience(profile.get('experience', []))
        
        # 학력 정보 변환
        education = self._convert_education(profile.get('education', []))
        
        # DynamoDB 형식
        employee_data = {
            'user_id': user_id,
            'basic_info': basic_info,
            'self_introduction': profile.get('about', ''),
            'skills': skills,
            'work_experience': work_experience,
            'education': education,
            'certifications': [],
            'source': 'linkedin',
            'profile_url': profile.get('profile_url', ''),
            'location': profile.get('location', '')
        }
        
        # Decimal 변환 (DynamoDB 호환)
        return self._convert_to_decimal(employee_data)
    
    def _convert_skills(self, skills: List[str]) -> List[Dict[str, Any]]:
        """
        기술 목록을 DynamoDB 형식으로 변환
        
        Args:
            skills: 기술 이름 리스트
            
        Returns:
            DynamoDB Skill 형식 리스트
        """
        converted_skills = []
        
        for skill in skills:
            # 기술 레벨 추정 (간단한 휴리스틱)
            level = self._estimate_skill_level(skill)
            
            # 경험 연수 추정 (기본값)
            years = self._estimate_skill_years(skill, level)
            
            converted_skills.append({
                'name': skill,
                'level': level,
                'years': years
            })
        
        return converted_skills
    
    def _estimate_skill_level(self, skill: str) -> str:
        """
        기술 레벨 추정
        
        Args:
            skill: 기술명
            
        Returns:
            레벨 (Beginner, Intermediate, Advanced, Expert)
        """
        # 간단한 휴리스틱: 일반적인 기술은 Intermediate, 최신 기술은 Advanced
        advanced_skills = [
            'Kubernetes', 'Microservices', 'GraphQL', 'Go', 'Rust',
            'Machine Learning', 'AI', 'Blockchain', 'WebAssembly'
        ]
        
        if skill in advanced_skills:
            return 'Advanced'
        else:
            return 'Intermediate'
    
    def _estimate_skill_years(self, skill: str, level: str) -> int:
        """
        기술 경험 연수 추정
        
        Args:
            skill: 기술명
            level: 레벨
            
        Returns:
            경험 연수
        """
        level_years = {
            'Beginner': 1,
            'Intermediate': 2,
            'Advanced': 4,
            'Expert': 6
        }
        
        return level_years.get(level, 2)
    
    def _convert_work_experience(self, experiences: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        경력 사항을 DynamoDB 형식으로 변환
        
        Args:
            experiences: LinkedIn 경력 사항
            
        Returns:
            DynamoDB WorkExperience 형식 리스트
        """
        converted_experiences = []
        
        for exp in experiences:
            project_id = f"PROJ_{uuid.uuid4().hex[:8].upper()}"
            
            # 기간 정규화
            duration = exp.get('duration', '')
            period = self._normalize_period(duration)
            
            converted_experiences.append({
                'project_id': project_id,
                'project_name': f"{exp.get('company', 'Unknown')} - {exp.get('title', 'Project')}",
                'role': exp.get('title', 'Unknown'),
                'duration': period,
                'main_tasks': [exp.get('description', '')] if exp.get('description') else [],
                'performance_result': exp.get('description', '')
            })
        
        return converted_experiences
    
    def _normalize_period(self, duration: str) -> str:
        """
        기간을 정규화된 형식으로 변환
        
        Args:
            duration: LinkedIn 기간 (예: "Jan 2020 - Dec 2022 · 3 yrs")
            
        Returns:
            정규화된 기간 (예: "2020-01 ~ 2022-12")
        """
        # 간단한 파싱
        months = {
            'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
            'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
            'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
        }
        
        # "Jan 2020 - Dec 2022" 형식 파싱
        match = re.search(r'(\w+)\s+(\d{4})\s*-\s*(\w+)\s+(\d{4})', duration)
        if match:
            start_month = months.get(match.group(1), '01')
            start_year = match.group(2)
            end_month = months.get(match.group(3), '12')
            end_year = match.group(4)
            return f"{start_year}-{start_month} ~ {end_year}-{end_month}"
        
        # "Jan 2020 - Present" 형식
        match = re.search(r'(\w+)\s+(\d{4})\s*-\s*Present', duration)
        if match:
            start_month = months.get(match.group(1), '01')
            start_year = match.group(2)
            return f"{start_year}-{start_month} ~ Present"
        
        # 파싱 실패 시 원본 반환
        return duration
    
    def _convert_education(self, education_list: List[Dict[str, str]]) -> Dict[str, str]:
        """
        학력 정보를 DynamoDB 형식으로 변환
        
        Args:
            education_list: LinkedIn 학력 리스트
            
        Returns:
            DynamoDB Education 형식 (첫 번째 학력만)
        """
        if not education_list:
            return None
        
        first_edu = education_list[0]
        return {
            'degree': first_edu.get('degree', 'Unknown'),
            'university': first_edu.get('school', 'Unknown')
        }
    
    def _convert_to_decimal(self, obj):
        """
        float/int를 Decimal로 변환 (DynamoDB 호환)
        
        Args:
            obj: 변환할 객체
            
        Returns:
            Decimal로 변환된 객체
        """
        if isinstance(obj, dict):
            return {k: self._convert_to_decimal(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_to_decimal(item) for item in obj]
        elif isinstance(obj, float):
            return Decimal(str(obj))
        elif isinstance(obj, int):
            return obj  # int는 그대로 유지
        else:
            return obj

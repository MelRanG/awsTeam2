"""
LinkedIn 자동 크롤러
Selenium을 사용하여 LinkedIn에서 프로필을 자동으로 수집
"""

import time
import json
import re
from typing import List, Dict, Any, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LinkedInCrawler:
    """LinkedIn 프로필 크롤러"""
    
    def __init__(self, email: str, password: str, headless: bool = True):
        """
        Args:
            email: LinkedIn 로그인 이메일
            password: LinkedIn 로그인 비밀번호
            headless: 헤드리스 모드 사용 여부
        """
        self.email = email
        self.password = password
        self.driver = self._setup_driver(headless)
        
    def _setup_driver(self, headless: bool) -> webdriver.Chrome:
        """Chrome 드라이버 설정"""
        options = Options()
        if headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        driver = webdriver.Chrome(options=options)
        return driver
    
    def login(self) -> bool:
        """LinkedIn 로그인"""
        try:
            logger.info("LinkedIn 로그인 시작...")
            self.driver.get('https://www.linkedin.com/login')
            time.sleep(2)
            
            # 이메일 입력
            email_field = self.driver.find_element(By.ID, 'username')
            email_field.send_keys(self.email)
            
            # 비밀번호 입력
            password_field = self.driver.find_element(By.ID, 'password')
            password_field.send_keys(self.password)
            
            # 로그인 버튼 클릭
            login_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
            login_button.click()
            
            time.sleep(5)
            
            # 로그인 성공 확인
            if 'feed' in self.driver.current_url or 'mynetwork' in self.driver.current_url:
                logger.info("로그인 성공!")
                return True
            else:
                logger.error("로그인 실패")
                return False
                
        except Exception as e:
            logger.error(f"로그인 중 오류: {str(e)}")
            return False
    
    def search_profiles(
        self, 
        keywords: str, 
        location: str = "South Korea",
        max_results: int = 100
    ) -> List[str]:
        """
        프로필 검색
        
        Args:
            keywords: 검색 키워드 (예: "Backend Developer")
            location: 지역
            max_results: 최대 결과 수
            
        Returns:
            프로필 URL 리스트
        """
        profile_urls = []
        
        try:
            # 검색 페이지로 이동
            search_url = f'https://www.linkedin.com/search/results/people/?keywords={keywords}&origin=GLOBAL_SEARCH_HEADER'
            if location:
                search_url += f'&geoUrn=["103644278"]'  # South Korea
            
            self.driver.get(search_url)
            time.sleep(3)
            
            page = 1
            while len(profile_urls) < max_results:
                logger.info(f"페이지 {page} 크롤링 중... (현재 {len(profile_urls)}개)")
                
                # 스크롤하여 모든 결과 로드
                self._scroll_page()
                
                # 프로필 링크 추출
                profile_links = self.driver.find_elements(
                    By.CSS_SELECTOR, 
                    'a.app-aware-link[href*="/in/"]'
                )
                
                for link in profile_links:
                    url = link.get_attribute('href')
                    if url and '/in/' in url and url not in profile_urls:
                        # 쿼리 파라미터 제거
                        clean_url = url.split('?')[0]
                        profile_urls.append(clean_url)
                        
                        if len(profile_urls) >= max_results:
                            break
                
                # 다음 페이지로 이동
                try:
                    next_button = self.driver.find_element(
                        By.CSS_SELECTOR, 
                        'button[aria-label="Next"]'
                    )
                    if next_button.is_enabled():
                        next_button.click()
                        time.sleep(3)
                        page += 1
                    else:
                        break
                except NoSuchElementException:
                    break
            
            logger.info(f"총 {len(profile_urls)}개 프로필 URL 수집 완료")
            return profile_urls[:max_results]
            
        except Exception as e:
            logger.error(f"프로필 검색 중 오류: {str(e)}")
            return profile_urls
    
    def crawl_profile(self, profile_url: str) -> Optional[Dict[str, Any]]:
        """
        개별 프로필 크롤링
        
        Args:
            profile_url: LinkedIn 프로필 URL
            
        Returns:
            프로필 데이터
        """
        try:
            logger.info(f"프로필 크롤링: {profile_url}")
            self.driver.get(profile_url)
            time.sleep(3)
            
            # 페이지 스크롤하여 모든 섹션 로드
            self._scroll_page()
            
            profile_data = {
                'profile_url': profile_url,
                'name': self._extract_name(),
                'headline': self._extract_headline(),
                'location': self._extract_location(),
                'about': self._extract_about(),
                'experience': self._extract_experience(),
                'education': self._extract_education(),
                'skills': self._extract_skills(),
            }
            
            # 연차 계산
            profile_data['years_of_experience'] = self._calculate_years_of_experience(
                profile_data['experience']
            )
            
            # 현재 직책 추출
            profile_data['current_role'] = self._extract_current_role(
                profile_data['experience']
            )
            
            logger.info(f"프로필 크롤링 완료: {profile_data['name']}")
            return profile_data
            
        except Exception as e:
            logger.error(f"프로필 크롤링 중 오류: {str(e)}")
            return None
    
    def _scroll_page(self):
        """페이지 스크롤"""
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        
        for _ in range(3):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
    
    def _extract_name(self) -> str:
        """이름 추출"""
        try:
            name = self.driver.find_element(By.CSS_SELECTOR, 'h1.text-heading-xlarge').text
            return name.strip()
        except:
            return "Unknown"
    
    def _extract_headline(self) -> str:
        """헤드라인 추출 (현재 직책)"""
        try:
            headline = self.driver.find_element(By.CSS_SELECTOR, 'div.text-body-medium').text
            return headline.strip()
        except:
            return ""
    
    def _extract_location(self) -> str:
        """위치 추출"""
        try:
            location = self.driver.find_element(
                By.CSS_SELECTOR, 
                'span.text-body-small.inline.t-black--light.break-words'
            ).text
            return location.strip()
        except:
            return ""
    
    def _extract_about(self) -> str:
        """자기소개 추출"""
        try:
            about_section = self.driver.find_element(By.ID, 'about')
            about_text = about_section.find_element(
                By.CSS_SELECTOR, 
                'div.display-flex.ph5.pv3'
            ).text
            return about_text.strip()
        except:
            return ""
    
    def _extract_experience(self) -> List[Dict[str, Any]]:
        """경력 사항 추출"""
        experiences = []
        
        try:
            exp_section = self.driver.find_element(By.ID, 'experience')
            exp_items = exp_section.find_elements(By.CSS_SELECTOR, 'li.artdeco-list__item')
            
            for item in exp_items:
                try:
                    exp_data = {}
                    
                    # 직책
                    title = item.find_element(By.CSS_SELECTOR, 'div.display-flex.align-items-center span[aria-hidden="true"]').text
                    exp_data['title'] = title.strip()
                    
                    # 회사명
                    company = item.find_element(By.CSS_SELECTOR, 'span.t-14.t-normal span[aria-hidden="true"]').text
                    exp_data['company'] = company.strip()
                    
                    # 기간
                    duration = item.find_element(By.CSS_SELECTOR, 'span.t-14.t-normal.t-black--light span[aria-hidden="true"]').text
                    exp_data['duration'] = duration.strip()
                    
                    # 설명
                    try:
                        description = item.find_element(By.CSS_SELECTOR, 'div.display-flex.full-width').text
                        exp_data['description'] = description.strip()
                    except:
                        exp_data['description'] = ""
                    
                    experiences.append(exp_data)
                    
                except Exception as e:
                    continue
                    
        except Exception as e:
            logger.warning(f"경력 추출 실패: {str(e)}")
        
        return experiences
    
    def _extract_education(self) -> List[Dict[str, str]]:
        """학력 추출"""
        education_list = []
        
        try:
            edu_section = self.driver.find_element(By.ID, 'education')
            edu_items = edu_section.find_elements(By.CSS_SELECTOR, 'li.artdeco-list__item')
            
            for item in edu_items:
                try:
                    edu_data = {}
                    
                    # 학교명
                    school = item.find_element(By.CSS_SELECTOR, 'div.display-flex.align-items-center span[aria-hidden="true"]').text
                    edu_data['school'] = school.strip()
                    
                    # 학위
                    try:
                        degree = item.find_element(By.CSS_SELECTOR, 'span.t-14.t-normal span[aria-hidden="true"]').text
                        edu_data['degree'] = degree.strip()
                    except:
                        edu_data['degree'] = ""
                    
                    education_list.append(edu_data)
                    
                except:
                    continue
                    
        except Exception as e:
            logger.warning(f"학력 추출 실패: {str(e)}")
        
        return education_list
    
    def _extract_skills(self) -> List[str]:
        """기술 추출"""
        skills = []
        
        try:
            # Skills 섹션으로 스크롤
            skills_section = self.driver.find_element(By.ID, 'skills')
            self.driver.execute_script("arguments[0].scrollIntoView();", skills_section)
            time.sleep(1)
            
            # "Show all skills" 버튼 클릭
            try:
                show_all_button = skills_section.find_element(
                    By.CSS_SELECTOR, 
                    'a[aria-label*="Show all"]'
                )
                show_all_button.click()
                time.sleep(2)
            except:
                pass
            
            # 기술 목록 추출
            skill_items = self.driver.find_elements(
                By.CSS_SELECTOR, 
                'div[data-view-name="profile-skills"] span[aria-hidden="true"]'
            )
            
            for item in skill_items:
                skill_name = item.text.strip()
                if skill_name and skill_name not in skills:
                    skills.append(skill_name)
                    
        except Exception as e:
            logger.warning(f"기술 추출 실패: {str(e)}")
        
        return skills
    
    def _calculate_years_of_experience(self, experiences: List[Dict[str, Any]]) -> int:
        """총 경력 연수 계산"""
        total_months = 0
        
        for exp in experiences:
            duration = exp.get('duration', '')
            
            # "2 yrs 3 mos" 형식 파싱
            years_match = re.search(r'(\d+)\s*yr', duration)
            months_match = re.search(r'(\d+)\s*mo', duration)
            
            if years_match:
                total_months += int(years_match.group(1)) * 12
            if months_match:
                total_months += int(months_match.group(1))
        
        return total_months // 12
    
    def _extract_current_role(self, experiences: List[Dict[str, Any]]) -> str:
        """현재 직책 추출"""
        if experiences:
            return experiences[0].get('title', 'Unknown')
        return 'Unknown'
    
    def close(self):
        """드라이버 종료"""
        if self.driver:
            self.driver.quit()
            logger.info("크롤러 종료")

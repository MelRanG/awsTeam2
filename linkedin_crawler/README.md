# LinkedIn 자동 크롤러 및 DynamoDB 업로더

LinkedIn에서 자동으로 100개 이상의 프로필을 크롤링하여 DynamoDB Employees 테이블에 저장합니다.
저장된 데이터는 기존 HR 시스템의 커리어 추천 기능에서 자동으로 분석됩니다.

## 🎯 주요 기능

### 1. 자동 프로필 크롤링
- Selenium을 사용한 LinkedIn 자동 로그인
- 검색 조건에 맞는 프로필 자동 수집 (최대 100개+)
- 각 프로필의 상세 정보 추출:
  - 이름, 현재 직책, 위치
  - 경력 사항 (회사, 직책, 기간, 설명)
  - 학력 정보
  - 보유 기술 목록
  - 총 경력 연수 자동 계산

### 2. DynamoDB 자동 저장
- DynamoDB Employees 테이블 형식에 맞게 자동 변환
- 고유 user_id 자동 생성 (EMP_XXXXXXXX)
- 기술 레벨 자동 추정 (Beginner/Intermediate/Advanced/Expert)
- 경력 사항을 프로젝트 형식으로 변환
- 배치 업로드 지원

### 3. 기존 시스템 연동
- 저장된 데이터는 기존 Lambda 함수들이 자동 분석:
  - **domain_analysis**: 커리어 패스 추천
  - **quantitative_analysis**: 정량적 평가
  - **qualitative_analysis**: 정성적 평가
  - **recommendation_engine**: 프로젝트 투입 추천

## 📦 설치

### 1. Python 패키지 설치

```bash
cd linkedin_crawler
pip install -r requirements.txt
```

### 2. AWS 자격 증명 설정

```bash
# AWS CLI 설치 및 설정
aws configure

# 또는 환경 변수 설정
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_DEFAULT_REGION="us-east-2"
```

### 3. Chrome 드라이버 설치

```bash
# webdriver-manager가 자동으로 설치하므로 별도 설치 불필요
```

## 🚀 사용 방법

### 기본 실행

```bash
python main.py \
  --email "your-email@example.com" \
  --password "your-password" \
  --keywords "Backend Developer" \
  --location "South Korea" \
  --max-profiles 100 \
  --headless
```

### 옵션 설명

| 옵션 | 설명 | 기본값 |
|------|------|--------|
| `--email` | LinkedIn 로그인 이메일 (필수) | - |
| `--password` | LinkedIn 로그인 비밀번호 (필수) | - |
| `--keywords` | 검색 키워드 | Backend Developer |
| `--location` | 검색 지역 | South Korea |
| `--max-profiles` | 최대 프로필 수 | 100 |
| `--output` | 로컬 JSON 파일 저장 (선택) | profiles.json |
| `--headless` | 헤드리스 모드 (브라우저 숨김) | False |
| `--region` | AWS 리전 | us-east-2 |
| `--skip-upload` | DynamoDB 업로드 건너뛰기 | False |

### 실행 예제

#### 1. Backend Developer 100명 크롤링
```bash
python main.py \
  --email "myemail@gmail.com" \
  --password "mypassword" \
  --keywords "Backend Developer" \
  --max-profiles 100 \
  --headless
```

#### 2. Frontend Developer 50명 크롤링
```bash
python main.py \
  --email "myemail@gmail.com" \
  --password "mypassword" \
  --keywords "Frontend Developer" \
  --max-profiles 50
```

#### 3. DevOps Engineer 크롤링
```bash
python main.py \
  --email "myemail@gmail.com" \
  --password "mypassword" \
  --keywords "DevOps Engineer" \
  --location "Seoul" \
  --max-profiles 80
```

## 📊 DynamoDB 저장 형식

### Employees 테이블에 저장되는 데이터

```json
{
  "user_id": "EMP_A1B2C3D4",
  "basic_info": {
    "name": "김철수",
    "role": "Senior Backend Developer",
    "years_of_experience": 7,
    "email": "emp_a1b2c3d4@linkedin.com"
  },
  "self_introduction": "7년차 백엔드 개발자...",
  "skills": [
    {
      "name": "Java",
      "level": "Expert",
      "years": 6
    },
    {
      "name": "Spring",
      "level": "Advanced",
      "years": 5
    }
  ],
  "work_experience": [
    {
      "project_id": "PROJ_12345678",
      "project_name": "ABC Company - Senior Backend Developer",
      "role": "Senior Backend Developer",
      "duration": "2020-01 ~ 2023-12",
      "main_tasks": ["마이크로서비스 아키텍처 설계..."],
      "performance_result": "응답 시간 40% 개선..."
    }
  ],
  "education": {
    "degree": "Computer Science, BS",
    "university": "서울대학교"
  },
  "certifications": [],
  "source": "linkedin",
  "profile_url": "https://linkedin.com/in/...",
  "location": "Seoul, South Korea"
}
```

### 로컬 파일 (선택사항)

`--output profiles.json` 옵션 사용 시 로컬에도 저장됩니다.

## 🔄 데이터 흐름

```
1. LinkedIn 크롤링
   ↓
2. 프로필 데이터 추출
   ↓
3. DynamoDB 형식으로 변환
   ↓
4. Employees 테이블에 저장
   ↓
5. 기존 Lambda 함수들이 자동 분석
   ├── domain_analysis: 커리어 패스 추천
   ├── quantitative_analysis: 정량적 평가
   ├── qualitative_analysis: 정성적 평가
   └── recommendation_engine: 프로젝트 투입 추천
```

## 🎯 기존 시스템 연동

### 1. 커리어 추천 (domain_analysis Lambda)
DynamoDB에 저장된 데이터를 기반으로:
- 연차/직책별 그룹화
- 부족한 기술 자동 분석
- 우선순위 기반 학습 추천

### 2. 인력 평가 (quantitative/qualitative_analysis Lambda)
- 기술 스택 평가
- 프로젝트 경험 점수 계산
- 이력서 신뢰도 검증

### 3. 프로젝트 추천 (recommendation_engine Lambda)
- 프로젝트 요구사항 매칭
- 기술 적합도 계산
- 팀 구성 추천

## ⚠️ 주의사항

### 1. LinkedIn 이용 약관
- LinkedIn의 이용 약관을 준수하세요
- 과도한 크롤링은 계정 제재를 받을 수 있습니다
- 개인정보 보호법을 준수하세요

### 2. 크롤링 속도
- 각 프로필 사이에 2-3초 대기 시간 포함
- 100개 프로필 크롤링에 약 10-15분 소요
- 너무 빠른 속도는 차단될 수 있습니다

### 3. 로그인 보안
- 2단계 인증이 활성화된 경우 비활성화 필요
- 또는 앱 비밀번호 사용

### 4. 브라우저 호환성
- Chrome 브라우저 필요
- 최신 버전 권장

## 🐛 문제 해결

### 로그인 실패
```bash
# 헤드리스 모드 비활성화하여 확인
python main.py --email "..." --password "..." 
# (--headless 옵션 제거)
```

### 프로필 추출 실패
- LinkedIn UI가 변경되었을 수 있음
- CSS 선택자 업데이트 필요

### 메모리 부족
```bash
# 프로필 수 줄이기
python main.py --max-profiles 50 ...
```

## 📈 사용 시나리오

### 시나리오 1: 초기 데이터 수집
```bash
# Backend Developer 100명 수집
python main.py \
  --email "myemail@gmail.com" \
  --password "mypassword" \
  --keywords "Backend Developer" \
  --max-profiles 100 \
  --headless

# Frontend Developer 50명 추가 수집
python main.py \
  --email "myemail@gmail.com" \
  --password "mypassword" \
  --keywords "Frontend Developer" \
  --max-profiles 50 \
  --headless
```

### 시나리오 2: 데이터 확인 후 업로드
```bash
# 1단계: 로컬에만 저장 (DynamoDB 업로드 건너뛰기)
python main.py \
  --email "myemail@gmail.com" \
  --password "mypassword" \
  --keywords "DevOps Engineer" \
  --max-profiles 30 \
  --skip-upload

# 2단계: profiles.json 확인 후 수동 업로드
python -c "
from dynamodb_uploader import DynamoDBUploader
import json

with open('profiles.json', 'r') as f:
    profiles = json.load(f)

uploader = DynamoDBUploader()
uploader.upload_profiles(profiles)
"
```

### 시나리오 3: 프론트엔드에서 커리어 추천 확인
```
1. 크롤러 실행하여 DynamoDB에 데이터 저장
2. 프론트엔드 접속
3. "커리어 추천" 메뉴 클릭
4. domain_analysis Lambda가 자동으로 분석 수행
5. 연차/직책별 부족한 기술 확인
```

## 📈 향후 개선 사항

- [ ] 프록시 서버 지원 (IP 차단 방지)
- [ ] 멀티스레딩 (병렬 크롤링)
- [ ] 증분 업데이트 (이미 크롤링한 프로필 스킵)
- [ ] 이메일 알림 (크롤링 완료 시)
- [ ] 웹 대시보드 (실시간 진행 상황)

## 📞 문의

기술 지원: tech-support@example.com

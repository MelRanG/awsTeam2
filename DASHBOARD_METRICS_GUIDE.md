# 대시보드 지표 데이터 기준 가이드

## 📊 각 분석 지표의 데이터 출처 및 계산 방법

### 1. 직원 품질 분석 (Employee Quality Analysis)

**데이터 출처**: `Employees` 테이블의 직원 데이터

#### 고급 기술 보유자
- **기준**: 다음 키워드를 포함한 기술 보유 여부
  - `kubernetes`, `k8s`, `msa`, `microservices`
  - `aws`, `azure`, `gcp`
  - `ai`, `ml`, `machine learning`
- **계산**: 위 기술 중 하나라도 보유한 직원 수
- **예시**: Kubernetes를 보유한 직원 = 고급 기술 보유자

#### 역량 레벨 분포
- **데이터**: `employee.skills[].level` 필드
- **레벨**: Expert, Advanced, Intermediate, Beginner
- **계산**: 모든 직원의 모든 기술 레벨을 집계
- **예시**: 
  - 직원 A: Java(Expert), Python(Advanced) → Expert +1, Advanced +1
  - 직원 B: React(Intermediate) → Intermediate +1

#### 성과 기록 보유자
- **데이터**: `employee.work_experience[].performance_result` 필드
- **기준**: 프로젝트 경험 중 하나라도 성과 기록이 있는 경우
- **예시**: "시스템 응답 시간 60% 개선" 같은 기록이 있으면 카운트

#### 다중 역할 경험자
- **데이터**: `employee.work_experience[].role` 필드
- **기준**: 3개 이상의 서로 다른 역할 경험
- **예시**: System Architect, Tech Lead, Developer 3가지 역할 경험

---

### 2. 도메인 전문성 분석 (Domain Expertise Analysis)

**데이터 출처**: `Employees` 테이블의 `domain_experience` 필드

#### 다중 도메인 전문가
- **데이터**: `employee.domain_experience.knowledge_domains[]`
- **기준**: 2개 이상의 도메인 경험 보유
- **예시**: 
  ```json
  {
    "knowledge_domains": [
      {"domain": "전자상거래", "years": 3, "projects": 2},
      {"domain": "금융", "years": 2, "projects": 1}
    ]
  }
  ```
  → 다중 도메인 전문가로 카운트

#### 평균 도메인 경력
- **데이터**: `knowledge_domains[].years`
- **계산**: 모든 도메인 경험 연수의 평균
- **예시**: 
  - 직원 A: 전자상거래 3년
  - 직원 B: 금융 2년
  - 평균 = (3 + 2) / 2 = 2.5년

#### 주요 도메인 TOP 5
- **데이터**: `knowledge_domains[].domain`
- **계산**: 각 도메인을 경험한 직원 수를 집계하여 상위 5개
- **예시**:
  - 전자상거래: 150명
  - 금융: 120명
  - 헬스케어: 80명

---

### 3. 평가 점수 분석 (Evaluation Scores)

**데이터 출처**: `Employees` 테이블 데이터를 기반으로 실시간 계산

#### 평가 점수 계산 공식 (총 100점)

1. **기술 역량 (40점)**
   - 각 기술의 레벨 점수: Expert=10, Advanced=7, Intermediate=5, Beginner=3
   - 경험 연수 보너스: 최대 5점
   - 계산: `(레벨 점수 + min(경험 연수, 5)) / 기술 수 * 4`

2. **경력 (30점)**
   - 경력 연수 × 2점 (최대 30점)
   - 예시: 15년 경력 = 30점

3. **프로젝트 경험 (20점)**
   - 프로젝트 수 × 5점
   - 성과 기록 보너스: +5점
   - 최대 20점

4. **자격증 (10점)**
   - 자격증 수 × 2점 (최대 10점)

#### 점수 분포
- **우수 (90+)**: 90점 이상
- **양호 (80-89)**: 80~89점
- **보통 (70-79)**: 70~79점
- **개선 필요 (<70)**: 70점 미만

---

### 4. 역량 갭 분석 (Skill Gap Analysis)

**데이터 출처**: `Employees` 테이블 + `Projects` 테이블

#### 부족한 기술 계산
- **수요**: `Projects` 테이블의 `tech_stack` 필드에서 필요한 기술 집계
- **공급**: `Employees` 테이블의 `skills` 필드에서 보유 기술 집계
- **갭**: 수요 - 공급
- **예시**:
  - Spring Boot 수요: 78개 프로젝트
  - Spring Boot 공급: 0명
  - 갭: 78명 부족

#### 교육 필요 인력
- **기준**: 평균 평가 점수 미만인 직원
- **계산**: 전체 평균 점수를 계산한 후, 그보다 낮은 점수의 직원 수
- **예시**: 평균 68.3점 → 68.3점 미만인 직원 = 교육 필요

---

## 📈 실제 데이터 예시

### 직원 데이터 구조
```json
{
  "user_id": "U_003",
  "basic_info": {
    "name": "박민수",
    "years_of_experience": 11,
    "role": "Senior System Architect"
  },
  "skills": [
    {"name": "Java", "level": "Expert", "years": 11},
    {"name": "Kubernetes", "level": "Intermediate", "years": 3}
  ],
  "work_experience": [
    {
      "project_name": "차세대 금융 시스템",
      "role": "System Architect",
      "performance_result": "시스템 응답 시간 60% 개선"
    }
  ],
  "domain_experience": {
    "knowledge_domains": [
      {"domain": "전자상거래", "years": 3, "projects": 2}
    ]
  },
  "certifications": ["AWS Solutions Architect Professional", "CKAD"]
}
```

### 이 직원의 분석 결과
- ✅ 고급 기술 보유자 (Kubernetes 보유)
- ✅ 성과 기록 보유자 (성과 기록 있음)
- ✅ 역량 레벨: Expert 1개, Intermediate 1개
- ❌ 다중 역할 경험자 아님 (역할 1개)
- ❌ 다중 도메인 전문가 아님 (도메인 1개)
- 📊 평가 점수: 약 85점 (양호)

---

## 🔍 데이터 확인 방법

직원 데이터 구조를 확인하려면:
```bash
python deployment/check_employee_data_structure.py
```

현재 분석 결과를 확인하려면:
```bash
python deployment/test_dashboard_metrics.py
```

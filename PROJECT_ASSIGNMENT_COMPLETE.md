# 프로젝트 투입 기능 구현 완료

## 개요
프로젝트에 직원을 투입하는 기능을 구현했습니다. 투입 역할, 기간, 투입률, 근거 등을 상세하게 설정할 수 있습니다.

---

## 구현된 기능

### 1. 투입 정보 입력
- **투입 역할 선택**: PM, 개발자, 디자이너 등 10가지 역할
- **투입 기간 설정**: 시작일, 종료일 (선택)
- **투입률 설정**: 1~100% (50%, 100% 빠른 선택 버튼)
- **투입 근거 기록**: 왜 이 직원을 선택했는지 텍스트로 기록

### 2. 가용성 확인
- 직원이 현재 다른 프로젝트에 배정되어 있는지 확인
- 배정되어 있는 경우 경고 메시지 표시
- 409 Conflict 응답으로 중복 배정 방지

### 3. 데이터 저장
- **Employees 테이블**: 직원의 현재 프로젝트 정보 업데이트
  - `current_project`: 프로젝트 ID
  - `current_role`: 투입 역할
  - `assignment_start_date`: 투입 시작일
  - `assignment_end_date`: 투입 종료일 (선택)
  - `allocation_rate`: 투입률 (%)
  - `assignment_reason`: 투입 근거

- **Projects 테이블**: 프로젝트의 팀 멤버 목록에 추가
  - `team_members[]`: 팀 멤버 배열에 새 멤버 추가
    - `employee_id`: 직원 ID
    - `role`: 역할
    - `start_date`: 시작일
    - `end_date`: 종료일 (선택)
    - `allocation_rate`: 투입률
    - `assigned_date`: 배정 일시

---

## API 엔드포인트

### POST /projects/{projectId}/assign

**요청 예시:**
```json
{
  "employee_id": "U_045",
  "role": "Backend Developer",
  "start_date": "2025-12-04",
  "end_date": "2026-06-02",
  "allocation_rate": 100,
  "assignment_reason": "AI 추천 기반 투입 - 기술 매칭 점수 85점, 팀 친밀도 우수"
}
```

**응답 예시 (성공):**
```json
{
  "message": "프로젝트 배정이 완료되었습니다",
  "assignment": {
    "project_id": "PRJ012",
    "project_name": "AI 기반 추천 시스템 개발",
    "employee_id": "U_045",
    "employee_name": "조주원",
    "role": "Backend Developer",
    "start_date": "2025-12-04",
    "end_date": "2026-06-02",
    "allocation_rate": 100,
    "assignment_reason": "AI 추천 기반 투입 - 기술 매칭 점수 85점, 팀 친밀도 우수"
  }
}
```

**응답 예시 (실패 - 이미 배정됨):**
```json
{
  "error": "직원이 현재 다른 프로젝트에 배정되어 있습니다",
  "conflict": {
    "available": false,
    "reason": "다른 프로젝트에 배정되어 있습니다",
    "current_project": "PRJ050"
  }
}
```

---

## 프론트엔드 UI

### 투입 모달 (ProjectAssignmentModal)

```
┌─────────────────────────────────────────┐
│  프로젝트 배정 확인                  [X] │
├─────────────────────────────────────────┤
│                                          │
│  직원: 조주원                            │
│  프로젝트: AI 기반 추천 시스템 개발      │
│                                          │
│  투입 역할: [Backend Developer ▼]       │
│                                          │
│  시작일: [2025-12-04]  종료일: [선택]   │
│                                          │
│  투입률 (%): [100] [50%] [100%]         │
│  100% 투입 = 주 5.0일 근무              │
│                                          │
│  투입 근거 (선택):                       │
│  ┌────────────────────────────────────┐ │
│  │ AI 추천 기반 투입                  │ │
│  │ - 기술 매칭 점수 85점              │ │
│  │ - 팀 친밀도 우수                   │ │
│  └────────────────────────────────────┘ │
│                                          │
│  [취소]              [배정 확인]         │
└─────────────────────────────────────────┘
```

### 투입 역할 옵션
1. 프로젝트 매니저 (PM)
2. 기술 리드 (Tech Lead)
3. 개발자 (Developer)
4. 프론트엔드 개발자
5. 백엔드 개발자
6. 풀스택 개발자
7. 데브옵스 엔지니어
8. QA 엔지니어
9. UI/UX 디자이너
10. 데이터 분석가

---

## 사용 흐름

### 1. AI 인력 추천
```
프로젝트 관리 → AI 인력 추천받기 → 인력 추천 페이지
```

### 2. 추천 결과 확인
```
추천 후보자 목록 (필요 인력 × 2명)
- 종합 점수, 기술 매칭, 팀 친밀도, 가용성
- 상세한 추천 근거 (4단계 분석)
```

### 3. 프로젝트 투입
```
[프로젝트에 투입] 버튼 클릭
→ 투입 정보 입력 모달
→ 역할, 기간, 투입률, 근거 입력
→ [배정 확인] 버튼 클릭
→ 투입 완료
```

---

## 기술 스택

### Backend
- **Lambda 함수**: ProjectAssignment
- **언어**: Python 3.12
- **DynamoDB**: Employees, Projects 테이블

### Frontend
- **컴포넌트**: ProjectAssignmentModal.tsx
- **UI 라이브러리**: shadcn/ui
- **애니메이션**: framer-motion

### API Gateway
- **엔드포인트**: POST /projects/{projectId}/assign
- **CORS**: 활성화 (OPTIONS 메서드)
- **통합**: AWS_PROXY (Lambda)

---

## 테스트 결과

### API 테스트
```bash
python deployment/test_project_assign_api.py
```

**결과:**
- ✅ CORS 헤더 정상 작동
- ✅ 가용성 확인 정상 작동
- ✅ 409 Conflict 응답 정상 작동

### 가용한 직원 확인
```bash
python deployment/find_available_employee.py
```

**결과:**
- 전체 직원: 300명
- 가용한 직원: 297명
- 투입 중인 직원: 3명

---

## 배포 스크립트

### Lambda 함수 업데이트
```bash
python deployment/update_project_assign_lambda.py
```

### API Gateway 생성
```bash
python deployment/create_project_assign_api.py
```

### 프론트엔드 배포
```bash
npm --prefix frontend run build
python deploy_frontend_boto3.py
```

---

## 주요 개선 사항

### 이전 버전
- 단순 배정만 가능
- 역할, 기간, 투입률 정보 없음
- 투입 근거 기록 불가
- 이미 배정된 직원도 추천됨

### 현재 버전
- ✅ 투입 역할 선택 (10가지)
- ✅ 투입 기간 설정 (시작일, 종료일)
- ✅ 투입률 설정 (1~100%)
- ✅ 투입 근거 기록
- ✅ 가용성 확인 및 중복 방지
- ✅ 상세한 투입 정보 저장
- ✅ **추천 단계에서 이미 배정된 직원 자동 제외**

---

## 향후 개선 방향

### 1. 투입 이력 관리
- 직원의 과거 프로젝트 투입 이력 조회
- 투입 기간별 통계 및 분석

### 2. 투입률 자동 계산
- 여러 프로젝트 동시 투입 시 총 투입률 계산
- 100% 초과 시 경고 메시지

### 3. 투입 승인 워크플로우
- PM 승인 후 투입 확정
- 투입 요청 → 검토 → 승인/거부

### 4. 투입 알림
- 투입 확정 시 직원에게 알림
- 투입 종료 예정일 알림

---

## 관련 파일

### Backend
- `lambda_functions/project_assign/index.py`
- `deployment/update_project_assign_lambda.py`
- `deployment/create_project_assign_api.py`

### Frontend
- `frontend/src/components/ProjectAssignmentModal.tsx`
- `frontend/src/components/PersonnelRecommendation.tsx`
- `frontend/src/config/api.ts`

### 테스트
- `deployment/test_project_assign_api.py`
- `deployment/find_available_employee.py`

---

## 완료 일시
2025-12-04

## 구현자
Kiro AI Assistant

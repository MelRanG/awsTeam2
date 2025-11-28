# 프론트엔드 API 연동 가이드

## 배포 완료

### 프론트엔드 URL
http://hr-resource-optimization-frontend-hosting-prod.s3-website.us-east-2.amazonaws.com

### API Gateway URL
https://xoc7x1m6p8.execute-api.us-east-2.amazonaws.com/prod

## 연동된 API

### 1. 도메인 분석 API
- **컴포넌트**: `DomainAnalysis.tsx`
- **엔드포인트**: POST /domain-analysis
- **사용법**: 직원 ID 입력 후 "분석하기" 버튼 클릭
- **기능**: 직원의 현재 도메인과 추천 도메인 분석

### 2. 정량적 분석 API
- **컴포넌트**: `PersonnelEvaluation.tsx`
- **엔드포인트**: POST /quantitative-analysis
- **사용법**: 직원 ID 입력 후 "분석하기" 버튼 클릭
- **기능**: 
  - 경력 메트릭 (경력 년수, 프로젝트 수, 기술 다양성)
  - 기술 평가 (트렌드 점수, 수요 점수)
  - 프로젝트 점수
  - 종합 점수

### 3. 정성적 분석 API
- **컴포넌트**: `PersonnelEvaluation.tsx`
- **엔드포인트**: POST /qualitative-analysis
- **사용법**: 정량적 분석과 함께 자동 호출
- **기능**:
  - 강점/약점 분석
  - 적합 프로젝트 추천
  - 주의사항 플래그

### 4. 인력 추천 API (개발 중)
- **컴포넌트**: `ProjectRecommendations.tsx` (생성됨)
- **엔드포인트**: POST /recommendations
- **상태**: Lambda 함수 오류로 현재 사용 불가
- **예정 기능**: 프로젝트에 적합한 인력 추천

## 사용 가능한 테스트 데이터

### 직원 ID
- `U_003`: 박민수 (Senior System Architect, 11년 경력)
- `U_001`: 김철수
- `U_002`: 이영희
- `U_004`: 최지은
- `U_005`: 정민호

### 프로젝트 ID
- `PRJ002`: 테스트 프로젝트
- `P_001`: 차세대 금융 코어 뱅킹 시스템

## API 사용 예시

### 프론트엔드에서 API 호출

```typescript
import { api } from './config/api';

// 도메인 분석
const domainResult = await api.domainAnalysis({
  employee_id: 'U_003',
  analysis_type: 'skills'
});

// 정량적 분석
const quantitativeResult = await api.quantitativeAnalysis({
  user_id: 'U_003'
});

// 정성적 분석
const qualitativeResult = await api.qualitativeAnalysis({
  user_id: 'U_003'
});

// 인력 추천 (현재 오류)
const recommendations = await api.recommendations({
  project_id: 'PRJ002'
});
```

### 직접 API 테스트 (PowerShell)

```powershell
# 도메인 분석
Invoke-RestMethod -Uri "https://xoc7x1m6p8.execute-api.us-east-2.amazonaws.com/prod/domain-analysis" `
  -Method Post `
  -Headers @{"Content-Type"="application/json"} `
  -Body '{"employee_id":"U_003","analysis_type":"skills"}'

# 정량적 분석
Invoke-RestMethod -Uri "https://xoc7x1m6p8.execute-api.us-east-2.amazonaws.com/prod/quantitative-analysis" `
  -Method Post `
  -Headers @{"Content-Type"="application/json"} `
  -Body '{"user_id":"U_003"}'

# 정성적 분석
Invoke-RestMethod -Uri "https://xoc7x1m6p8.execute-api.us-east-2.amazonaws.com/prod/qualitative-analysis" `
  -Method Post `
  -Headers @{"Content-Type"="application/json"} `
  -Body '{"user_id":"U_003"}'
```

## 주요 기능

### 인력 평가 페이지
1. 좌측 메뉴에서 "인력 평가" 클릭
2. 직원 ID 입력 (예: U_003)
3. "분석하기" 버튼 클릭
4. 실시간으로 정량적/정성적 분석 결과 확인
5. 종합 점수, 경력 메트릭, 주의사항 등 표시

### 도메인 분석 페이지
1. 좌측 메뉴에서 "도메인 분석" 클릭
2. 직원 ID 입력
3. "분석하기" 버튼 클릭
4. 현재 도메인과 추천 도메인 확인

## 파일 구조

```
frontend/
├── src/
│   ├── config/
│   │   └── api.ts              # API 설정 및 함수
│   ├── components/
│   │   ├── PersonnelEvaluation.tsx    # 인력 평가 (API 연동)
│   │   ├── DomainAnalysis.tsx         # 도메인 분석 (API 연동)
│   │   ├── ProjectRecommendations.tsx # 인력 추천 (생성됨)
│   │   └── EmployeeAnalysis.tsx       # 직원 분석 (생성됨)
│   └── App.tsx
├── .env                        # 환경 변수
└── build/                      # 빌드 결과물
```

## 환경 변수

`.env` 파일:
```
VITE_API_BASE_URL=https://xoc7x1m6p8.execute-api.us-east-2.amazonaws.com/prod
VITE_AWS_REGION=us-east-2
VITE_S3_RESUME_BUCKET=hr-resource-optimization-resumes-prod
```

## 다음 단계

1. **Recommendations API 수정**: Lambda 함수 오류 해결
2. **추가 컴포넌트 통합**: ProjectRecommendations, EmployeeAnalysis 컴포넌트를 메인 앱에 추가
3. **에러 핸들링 개선**: 더 나은 사용자 피드백
4. **로딩 상태 개선**: 스켈레톤 UI 추가
5. **데이터 캐싱**: React Query 또는 SWR 도입

## 문제 해결

### API 호출 실패
- 네트워크 탭에서 요청/응답 확인
- CORS 설정 확인 (현재 '*' 허용)
- API Gateway 배포 상태 확인

### 빌드 오류
```bash
cd frontend
npm install
npm run build
```

### 재배포
```bash
cd frontend
npm run build
aws s3 sync build/ s3://hr-resource-optimization-frontend-hosting-prod --region us-east-2 --delete
```

## 성능 최적화

- API 응답 캐싱
- 이미지 최적화
- 코드 스플리팅
- Lazy loading

## 보안

- API 인증: 현재 NONE (개발용)
- 프로덕션: AWS Cognito 또는 IAM 인증 추가 필요
- HTTPS 사용
- 입력 검증

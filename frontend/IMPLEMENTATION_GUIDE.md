# 프론트엔드 구현 가이드

## 개요

이 문서는 HR Resource Optimization 시스템의 프론트엔드 구현 상태와 백엔드 API 매핑 정보를 제공합니다.

## 구현 완료 항목

### ✅ 1. 프로젝트 구조 및 설정
- TypeScript + React + Vite 기반 프로젝트
- Tailwind CSS + Framer Motion 스타일링
- 환경 변수 설정 (.env.example)
- 배포 스크립트 (Bash, PowerShell)

### ✅ 2. 타입 정의 (src/types/models.ts)
백엔드 Python Pydantic 모델과 1:1 매핑되는 TypeScript 인터페이스:
- `Employee` - 직원 프로필
- `Project` - 프로젝트 정보
- `Recommendation` - 추천 결과
- `DomainInsight` - 도메인 분석
- `QuantitativeAnalysisResponse` - 정량적 분석
- `QualitativeAnalysisResponse` - 정성적 분석
- `DashboardMetrics` - 대시보드 메트릭

### ✅ 3. API 서비스 레이어 (src/services/api.service.ts)
백엔드 API 엔드포인트와 연동하는 서비스 클래스:
- `getDashboardMetrics()` - 대시보드 데이터
- `getEmployees()` - 직원 목록
- `getProjects()` - 프로젝트 목록
- `getRecommendations()` - 인력 추천
- `getDomainAnalysis()` - 도메인 분석
- `getQuantitativeAnalysis()` - 정량적 분석
- `getQualitativeAnalysis()` - 정성적 분석
- `uploadResume()` - 이력서 업로드

### ✅ 4. UI 컴포넌트
- `Dashboard.tsx` - 대시보드 (통계, 최근 추천, 기술 분포)
- `PersonnelManagement.tsx` - 인력 관리 (검색, 필터, 상세 정보)
- `ProjectManagement.tsx` - 프로젝트 관리 (목록, 투입 현황)
- `PersonnelRecommendation.tsx` - AI 인력 추천
- `DomainAnalysis.tsx` - 도메인 분석 및 팀 구성 제안
- `PersonnelEvaluation.tsx` - 인력 평가 (이력서 업로드, 검증)

## 백엔드 API 매핑

### API Gateway 엔드포인트

| 프론트엔드 기능 | API 엔드포인트 | HTTP 메서드 | 상태 |
|--------------|--------------|-----------|------|
| 인력 추천 | `/recommendations` | POST | ✅ 매핑 완료 |
| 도메인 분석 | `/domain-analysis` | POST | ✅ 매핑 완료 |
| 정량적 분석 | `/quantitative-analysis` | POST | ✅ 매핑 완료 |
| 정성적 분석 | `/qualitative-analysis` | POST | ✅ 매핑 완료 |
| 직원 목록 | `/employees` | GET | ⚠️ 백엔드 구현 필요 |
| 직원 상세 | `/employees/{id}` | GET | ⚠️ 백엔드 구현 필요 |
| 직원 생성 | `/employees` | POST | ⚠️ 백엔드 구현 필요 |
| 프로젝트 목록 | `/projects` | GET | ⚠️ 백엔드 구현 필요 |
| 프로젝트 상세 | `/projects/{id}` | GET | ⚠️ 백엔드 구현 필요 |
| 대시보드 메트릭 | `/dashboard/metrics` | GET | ⚠️ 백엔드 구현 필요 |
| 이력서 업로드 | `/resume/upload` | POST | ⚠️ 백엔드 구현 필요 |

## 추가 구현 필요 항목

### 🔧 백엔드 API 엔드포인트 추가

현재 백엔드에는 4개의 주요 Lambda 함수만 API Gateway에 연결되어 있습니다:
1. Recommendation Engine
2. Domain Analysis
3. Quantitative Analysis
4. Qualitative Analysis

다음 엔드포인트를 추가로 구현해야 합니다:

#### 1. 직원 관리 API
```python
# Lambda: employee_management
GET    /employees              # 전체 직원 목록
GET    /employees/{id}         # 특정 직원 조회
POST   /employees              # 신규 직원 등록
PUT    /employees/{id}         # 직원 정보 수정
DELETE /employees/{id}         # 직원 삭제
GET    /employees/by-skill     # 기술로 검색
```

#### 2. 프로젝트 관리 API
```python
# Lambda: project_management
GET    /projects               # 전체 프로젝트 목록
GET    /projects/{id}          # 특정 프로젝트 조회
POST   /projects               # 신규 프로젝트 등록
PUT    /projects/{id}          # 프로젝트 정보 수정
DELETE /projects/{id}          # 프로젝트 삭제
```

#### 3. 대시보드 API
```python
# Lambda: dashboard_metrics
GET    /dashboard/metrics      # 대시보드 통계 데이터
```

#### 4. 이력서 처리 API
```python
# Lambda: resume_upload_handler
POST   /resume/upload          # S3 Presigned URL 생성
GET    /resume/status/{job_id} # 파싱 상태 조회
```

### 🔧 프론트엔드 개선 사항

#### 1. AWS 인증 구현
현재 `getAuthHeaders()` 함수는 빈 헤더를 반환합니다. 다음 중 하나를 구현해야 합니다:

**옵션 A: AWS Cognito 사용**
```typescript
import { Auth } from 'aws-amplify';

export const getAuthHeaders = async () => {
  const session = await Auth.currentSession();
  const token = session.getIdToken().getJwtToken();
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`,
  };
};
```

**옵션 B: AWS Signature V4 (IAM 인증)**
```typescript
import { SignatureV4 } from '@aws-sdk/signature-v4';

export const getAuthHeaders = async () => {
  // AWS Signature V4 서명 생성
  // ...
};
```

#### 2. 에러 처리 개선
```typescript
// src/services/api.service.ts에 에러 핸들링 추가
try {
  const response = await apiService.getEmployees();
} catch (error) {
  if (error instanceof ApiError) {
    // 사용자에게 친화적인 에러 메시지 표시
    toast.error(error.message);
  }
}
```

#### 3. 로딩 상태 관리
```typescript
// React Query 또는 SWR 사용 권장
import { useQuery } from '@tanstack/react-query';

const { data, isLoading, error } = useQuery({
  queryKey: ['employees'],
  queryFn: () => apiService.getEmployees(),
});
```

#### 4. 실시간 데이터 업데이트
```typescript
// WebSocket 또는 Polling으로 실시간 업데이트
useEffect(() => {
  const interval = setInterval(() => {
    refetch(); // 데이터 새로고침
  }, 30000); // 30초마다
  
  return () => clearInterval(interval);
}, []);
```

## 배포 가이드

### 1. 환경 변수 설정

`.env` 파일 생성:
```bash
VITE_API_BASE_URL=https://abc123.execute-api.us-east-2.amazonaws.com/prod
VITE_AWS_REGION=us-east-2
VITE_S3_RESUME_BUCKET=hr-resumes-team2
```

### 2. S3 버킷 설정

```bash
# S3 버킷 생성
aws s3 mb s3://hr-frontend-team2 --region us-east-2

# 정적 웹사이트 호스팅 활성화
aws s3 website s3://hr-frontend-team2 \
  --index-document index.html \
  --error-document index.html

# 퍼블릭 액세스 설정
aws s3api put-bucket-policy \
  --bucket hr-frontend-team2 \
  --policy file://bucket-policy.json
```

`bucket-policy.json`:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::hr-frontend-team2/*"
    }
  ]
}
```

### 3. 배포 실행

**Linux/Mac:**
```bash
npm run deploy
```

**Windows:**
```powershell
npm run deploy:win
```

### 4. CloudFront 설정 (선택사항)

CloudFront를 사용하면 HTTPS와 더 빠른 전송 속도를 제공할 수 있습니다:

```bash
# CloudFront Distribution 생성
aws cloudfront create-distribution \
  --origin-domain-name hr-frontend-team2.s3-website.us-east-2.amazonaws.com \
  --default-root-object index.html
```

## 테스트 가이드

### 1. 로컬 개발 서버

```bash
npm run dev
```

### 2. Mock API 사용

백엔드가 준비되지 않은 경우, Mock Service Worker (MSW)를 사용할 수 있습니다:

```bash
npm install -D msw
```

```typescript
// src/mocks/handlers.ts
import { rest } from 'msw';

export const handlers = [
  rest.get('/employees', (req, res, ctx) => {
    return res(ctx.json([/* mock data */]));
  }),
];
```

## 다음 단계

1. ✅ 프론트엔드 기본 구조 완성
2. ⚠️ 백엔드 CRUD API 엔드포인트 추가 (Task 4, 17)
3. ⚠️ AWS 인증 구현 (Cognito 또는 IAM)
4. ⚠️ 에러 처리 및 로딩 상태 개선
5. ⚠️ 실제 데이터로 테스트
6. ⚠️ S3 + CloudFront 배포

## 참고 자료

- [AWS API Gateway](https://docs.aws.amazon.com/apigateway/)
- [AWS Amplify](https://docs.amplify.aws/)
- [React Query](https://tanstack.com/query/latest)
- [Vite 환경 변수](https://vitejs.dev/guide/env-and-mode.html)

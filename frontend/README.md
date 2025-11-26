# HR Resource Optimization - Frontend

AI 기반 인력 배치 최적화 및 프로젝트 투입 인력 추천 시스템의 프론트엔드 애플리케이션입니다.

## 주요 기능

- **대시보드**: 전체 인력 및 프로젝트 현황 실시간 모니터링
- **인력 관리**: 직원 프로필 조회, 등록, 수정
- **프로젝트 관리**: 프로젝트 정보 관리 및 투입 인력 현황
- **AI 인력 추천**: 프로젝트 요구사항 기반 최적 인력 추천
- **도메인 분석**: 신규 도메인 진출 가능성 분석 및 팀 구성 제안
- **인력 평가**: 신규 경력직/프리랜서 이력 검증 및 평가

## 기술 스택

- **React 18** + **TypeScript**
- **Vite** - 빌드 도구
- **Tailwind CSS** - 스타일링
- **Framer Motion** - 애니메이션
- **Radix UI** - UI 컴포넌트
- **AWS SDK** - AWS 서비스 연동

## 시작하기

### 1. 의존성 설치

```bash
npm install
```

### 2. 환경 변수 설정

`.env.example` 파일을 복사하여 `.env` 파일을 생성하고 API Gateway URL을 설정합니다:

```bash
cp .env.example .env
```

`.env` 파일 수정:
```
VITE_API_BASE_URL=https://your-api-gateway-id.execute-api.us-east-2.amazonaws.com/prod
VITE_AWS_REGION=us-east-2
VITE_S3_RESUME_BUCKET=hr-resumes-team2
```

### 3. 개발 서버 실행

```bash
npm run dev
```

브라우저에서 http://localhost:5173 접속

### 4. 프로덕션 빌드

```bash
npm run build
```

빌드된 파일은 `dist/` 폴더에 생성됩니다.

## 프로젝트 구조

```
frontend/
├── src/
│   ├── components/          # React 컴포넌트
│   │   ├── ui/             # 재사용 가능한 UI 컴포넌트
│   │   ├── Dashboard.tsx
│   │   ├── PersonnelManagement.tsx
│   │   ├── ProjectManagement.tsx
│   │   ├── PersonnelRecommendation.tsx
│   │   ├── DomainAnalysis.tsx
│   │   └── PersonnelEvaluation.tsx
│   ├── services/           # API 서비스 레이어
│   │   └── api.service.ts
│   ├── types/              # TypeScript 타입 정의
│   │   └── models.ts
│   ├── config/             # 설정 파일
│   │   └── api.ts
│   ├── App.tsx             # 메인 앱 컴포넌트
│   └── main.tsx            # 엔트리 포인트
├── .env.example            # 환경 변수 예제
└── package.json
```

## API 연동

프론트엔드는 다음 백엔드 API 엔드포인트와 연동됩니다:

- `POST /recommendations` - 프로젝트 인력 추천
- `POST /domain-analysis` - 도메인 분석
- `POST /quantitative-analysis` - 정량적 인력 평가
- `POST /qualitative-analysis` - 정성적 인력 평가
- `GET /employees` - 직원 목록 조회
- `GET /projects` - 프로젝트 목록 조회
- `POST /resume/upload` - 이력서 업로드

## S3 배포

프로덕션 빌드 후 S3에 배포:

```bash
# 빌드
npm run build

# S3에 업로드
aws s3 sync dist/ s3://your-bucket-name --delete

# CloudFront 캐시 무효화 (선택사항)
aws cloudfront create-invalidation --distribution-id YOUR_DIST_ID --paths "/*"
```

## 개발 가이드

### 새로운 컴포넌트 추가

1. `src/components/` 에 컴포넌트 파일 생성
2. 필요한 타입을 `src/types/models.ts` 에 정의
3. API 호출이 필요하면 `src/services/api.service.ts` 에 메서드 추가
4. `App.tsx` 에서 라우팅 설정

### API 서비스 사용 예제

```typescript
import { apiService } from './services/api.service';

// 직원 목록 조회
const employees = await apiService.getEmployees();

// 인력 추천 요청
const recommendations = await apiService.getRecommendations({
  project_id: 'project-123',
  required_skills: ['React', 'Node.js'],
  team_size: 5,
});
```

## 원본 디자인

The original Figma design is available at: https://www.figma.com/design/aiLbLBoTFiRs21VzKEdnlE/Team-Allocation-Web-Service

## 라이선스

MIT

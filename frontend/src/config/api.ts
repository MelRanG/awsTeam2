/**
 * API 설정 및 엔드포인트 정의
 */

// API Gateway URL - 환경변수에서 가져오거나 기본값 사용
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://your-api-gateway-url.execute-api.us-east-2.amazonaws.com/prod';

// API 엔드포인트
export const API_ENDPOINTS = {
  // 인력 추천
  RECOMMENDATIONS: '/recommendations',
  
  // 도메인 분석
  DOMAIN_ANALYSIS: '/domain-analysis',
  
  // 정량적 분석
  QUANTITATIVE_ANALYSIS: '/quantitative-analysis',
  
  // 정성적 분석
  QUALITATIVE_ANALYSIS: '/qualitative-analysis',
  
  // 직원 관리 (추가 필요)
  EMPLOYEES: '/employees',
  EMPLOYEE_BY_ID: (id: string) => `/employees/${id}`,
  EMPLOYEES_BY_SKILL: '/employees/by-skill',
  
  // 프로젝트 관리 (추가 필요)
  PROJECTS: '/projects',
  PROJECT_BY_ID: (id: string) => `/projects/${id}`,
  
  // 대시보드 메트릭 (추가 필요)
  DASHBOARD_METRICS: '/dashboard/metrics',
  
  // 이력서 업로드 (추가 필요)
  RESUME_UPLOAD: '/resume/upload',
  RESUME_PARSE_STATUS: (jobId: string) => `/resume/status/${jobId}`,
} as const;

// AWS 인증 헤더 생성 (IAM 인증 사용 시)
export const getAuthHeaders = async (): Promise<Record<string, string>> => {
  // TODO: AWS Signature V4 인증 구현
  // 또는 Cognito 토큰 사용
  return {
    'Content-Type': 'application/json',
    // 'Authorization': `Bearer ${token}`,
  };
};

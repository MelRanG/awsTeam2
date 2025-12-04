/**
 * API 설정 및 엔드포인트 정의
 */

/// <reference types="vite/client" />

// API Gateway URL
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://ifeniowvpb.execute-api.us-east-2.amazonaws.com/prod';

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
  
  // 직원 목록 조회 (추가)
  EMPLOYEES_LIST: '/employees',
  
  // 프로젝트 목록 조회 (추가)
  PROJECTS_LIST: '/projects',
  
  // 대시보드 메트릭
  DASHBOARD_METRICS: '/dashboard/metrics',
  
  // 프로젝트 배정
  PROJECT_ASSIGN: (projectId: string) => `/projects/${projectId}/assign`,
  
  // 평가 관련
  EVALUATIONS: '/evaluations',
  EVALUATION_APPROVE: (evaluationId: string) => `/evaluations/${evaluationId}/approve`,
  EVALUATION_REVIEW: (evaluationId: string) => `/evaluations/${evaluationId}/review`,
  EVALUATION_REJECT: (evaluationId: string) => `/evaluations/${evaluationId}/reject`,
} as const;

// API 요청 헤더
const getHeaders = (): Record<string, string> => {
  return {
    'Content-Type': 'application/json',
  };
};

// 인증 헤더 가져오기 (API 서비스에서 사용)
export const getAuthHeaders = async (): Promise<Record<string, string>> => {
  return {
    'Content-Type': 'application/json',
  };
};

// API 호출 헬퍼 함수
async function apiCall<T>(endpoint: string, body: any): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  console.log('API 호출:', url, body);
  
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify(body),
    });

    console.log('API 응답 상태:', response.status);

    if (!response.ok) {
      const errorText = await response.text();
      console.error('API 에러 응답:', errorText);
      let error;
      try {
        error = JSON.parse(errorText);
      } catch {
        error = { message: errorText || 'Unknown error' };
      }
      throw new Error(error.message || `API Error: ${response.status}`);
    }

    const data = await response.json();
    console.log('API 응답 데이터:', data);
    return data;
  } catch (err) {
    console.error('API 호출 실패:', err);
    throw err;
  }
}

// API 타입 정의
export interface DomainAnalysisRequest {
  analysis_type?: string;
}

export interface DomainAnalysisResponse {
  current_domains: string[];
  identified_domains: Array<{
    domain_name: string;
    feasibility_score: number;
    reasoning: string;
  }>;
}

export interface QuantitativeAnalysisRequest {
  user_id: string;
}

export interface QuantitativeAnalysisResponse {
  user_id: string;
  name: string;
  experience_metrics: {
    years_of_experience: number;
    project_count: number;
    skill_diversity: number;
    experience_score: number;
    project_score: number;
    diversity_score: number;
  };
  tech_evaluation: {
    skill_evaluations: Array<{
      skill_name: string;
      trend_score: number;
      demand_score: number;
    }>;
    avg_trend_score: number;
    avg_demand_score: number;
    tech_stack_score: number;
  };
  project_scores: {
    project_evaluations: any[];
    avg_scale_score: number;
    avg_role_score: number;
    avg_performance_score: number;
    project_experience_score: number;
  };
  overall_score: number;
}

export interface QualitativeAnalysisRequest {
  user_id: string;
}

export interface QualitativeAnalysisResponse {
  user_id: string;
  name: string;
  strengths: any[];
  weaknesses: any[];
  suitable_projects: any[];
  development_areas: any[];
  suspicious_flags: Array<{
    type: string;
    description: string;
    severity: string;
  }>;
  overall_assessment: string;
}

export interface RecommendationsRequest {
  project_id: string;
}

export interface RecommendationsResponse {
  project_id: string;
  recommendations: Array<{
    user_id: string;
    name: string;
    score: number;
    reasoning: string;
  }>;
}

// 직원 목록 응답 타입
export interface Employee {
  user_id: string;
  basic_info: {
    name: string;
    role: string;
    email: string;
    years_of_experience: number;
  };
  skills: Array<{
    name: string;
    level: string;
    years: number;
  }>;
}

export interface EmployeesListResponse {
  employees: Employee[];
  count: number;
}

// 프로젝트 목록 응답 타입
export interface Project {
  project_id: string;
  project_name: string;
  status: string;
  start_date: string;
  end_date: string;
  required_skills: string[];
  client_industry?: string;
  assigned_members?: Array<{
    employee_id: string;
    name: string;
    role: string;
  }>;
  required_members?: number;
}

export interface ProjectsListResponse {
  projects: Project[];
  count: number;
}

// 대시보드 메트릭 응답 타입
export interface DashboardMetricsResponse {
  total_employees: number;
  active_projects: number;
  available_employees: number;
  pending_candidates: number;
  top_skills: {
    name: string;
    count: number;
    percentage: number;
  }[];
  employee_distribution: {
    by_department: { name: string; count: number }[];
    by_experience: { name: string; count: number }[];
    by_role: { name: string; count: number }[];
  };
  project_distribution: {
    by_status: { name: string; count: number }[];
    by_industry: { name: string; count: number }[];
    by_budget: { name: string; count: number }[];
  };
  evaluation_stats: {
    by_status: { name: string; count: number }[];
    by_type: { name: string; count: number }[];
    average_score: number;
    approval_rate: number;
    total_evaluations: number;
  };
  pending_candidates_detail: {
    total: number;
    by_wait_period: { name: string; count: number }[];
    average_wait_days: number;
  };
  action_required: {
    long_waiting_employees: number;
    delayed_evaluations: number;
    verification_needed: number;
  };
  skill_competency: {
    rare_skills: { name: string; count: number }[];
    multi_skilled_count: number;
    top_proficiency_skills: { name: string; avg_level: number; count: number }[];
    total_unique_skills: number;
  };
  career_growth: {
    average_years: number;
    senior_count: number;
    senior_ratio: number;
    skill_growth_rate: number;
  };
  project_experience: {
    average_projects: number;
    no_experience_count: number;
    multi_industry_count: number;
    leader_experience_count: number;
  };
  utilization: {
    assigned_count: number;
    available_count: number;
    utilization_rate: number;
  };
  education_certification: {
    education_distribution: { name: string; count: number }[];
    average_certifications: number;
    no_certification_count: number;
  };
  portfolio_health: {
    role_distribution: { name: string; count: number }[];
    skill_diversity_index: number;
    unique_skills_count: number;
  };
  employee_quality: {
    advanced_tech_count: number;
    advanced_tech_ratio: number;
    skill_level_distribution: { name: string; count: number }[];
    performance_record_count: number;
    performance_ratio: number;
    multi_role_count: number;
  };
  domain_expertise: {
    multi_domain_experts: number;
    average_domain_years: number;
    top_domains: { name: string; count: number }[];
    total_domains: number;
  };
  evaluation_scores: {
    average_score: number;
    score_distribution: { name: string; count: number }[];
    top_roles_by_score: { name: string; avg_score: number }[];
    score_by_experience: { name: string; avg_score: number }[];
    high_performers: number;
    low_performers: number;
  };
  skill_gaps: {
    top_skill_gaps: { skill: string; gap: number; demand: number; supply: number }[];
    total_skill_gaps: number;
    training_needed_count: number;
  };
  recent_recommendations: Array<{
    project: string;
    recommended: number;
    match_rate: number;
    status: string;
  }>;
  top_skills: Array<{
    name: string;
    count: number;
    percentage: number;
  }>;
}

// API 함수들
export const api = {
  /**
   * 도메인 분석 API
   */
  domainAnalysis: (request: DomainAnalysisRequest): Promise<DomainAnalysisResponse> => {
    return apiCall(API_ENDPOINTS.DOMAIN_ANALYSIS, request);
  },

  /**
   * 정량적 분석 API
   */
  quantitativeAnalysis: (request: QuantitativeAnalysisRequest): Promise<QuantitativeAnalysisResponse> => {
    return apiCall(API_ENDPOINTS.QUANTITATIVE_ANALYSIS, request);
  },

  /**
   * 정성적 분석 API
   */
  qualitativeAnalysis: (request: QualitativeAnalysisRequest): Promise<QualitativeAnalysisResponse> => {
    return apiCall(API_ENDPOINTS.QUALITATIVE_ANALYSIS, request);
  },

  /**
   * 인력 추천 API
   */
  recommendations: (request: RecommendationsRequest): Promise<RecommendationsResponse> => {
    return apiCall(API_ENDPOINTS.RECOMMENDATIONS, request);
  },

  /**
   * 직원 목록 조회 API
   */
  getEmployees: async (): Promise<EmployeesListResponse> => {
    const url = `${API_BASE_URL}${API_ENDPOINTS.EMPLOYEES_LIST}`;
    console.log('직원 목록 조회:', url);
    
    try {
      const response = await fetch(url, {
        method: 'GET',
        headers: getHeaders(),
      });

      console.log('직원 목록 응답 상태:', response.status);

      if (!response.ok) {
        const errorText = await response.text();
        console.error('직원 목록 조회 에러:', errorText);
        throw new Error(`API Error: ${response.status}`);
      }

      const data = await response.json();
      console.log('직원 목록 데이터:', data);
      return data;
    } catch (err) {
      console.error('직원 목록 조회 실패:', err);
      throw err;
    }
  },

  /**
   * 프로젝트 목록 조회 API
   */
  getProjects: async (): Promise<ProjectsListResponse> => {
    const url = `${API_BASE_URL}${API_ENDPOINTS.PROJECTS_LIST}`;
    console.log('프로젝트 목록 조회:', url);
    
    try {
      const response = await fetch(url, {
        method: 'GET',
        headers: getHeaders(),
      });

      console.log('프로젝트 목록 응답 상태:', response.status);

      if (!response.ok) {
        const errorText = await response.text();
        console.error('프로젝트 목록 조회 에러:', errorText);
        throw new Error(`API Error: ${response.status}`);
      }

      const data = await response.json();
      console.log('프로젝트 목록 데이터:', data);
      return data;
    } catch (err) {
      console.error('프로젝트 목록 조회 실패:', err);
      throw err;
    }
  },

  /**
   * 대시보드 메트릭 조회 API
   */
  getDashboardMetrics: async (): Promise<DashboardMetricsResponse> => {
    const url = `${API_BASE_URL}${API_ENDPOINTS.DASHBOARD_METRICS}`;
    console.log('대시보드 메트릭 조회:', url);
    
    try {
      const response = await fetch(url, {
        method: 'GET',
        headers: getHeaders(),
      });

      console.log('대시보드 메트릭 응답 상태:', response.status);

      if (!response.ok) {
        const errorText = await response.text();
        console.error('대시보드 메트릭 조회 에러:', errorText);
        throw new Error(`API Error: ${response.status}`);
      }

      const data = await response.json();
      console.log('대시보드 메트릭 데이터:', data);
      return data;
    } catch (err) {
      console.error('대시보드 메트릭 조회 실패:', err);
      throw err;
    }
  },

  /**
   * 직원 생성 API
   */
  createEmployee: async (employeeData: any): Promise<Employee> => {
    const url = `${API_BASE_URL}${API_ENDPOINTS.EMPLOYEES_LIST}`;
    console.log('직원 생성:', url, employeeData);
    
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: getHeaders(),
        body: JSON.stringify(employeeData),
      });

      console.log('직원 생성 응답 상태:', response.status);

      if (!response.ok) {
        const errorText = await response.text();
        console.error('직원 생성 에러:', errorText);
        let errorData;
        try {
          errorData = JSON.parse(errorText);
        } catch {
          errorData = { message: errorText || 'Unknown error' };
        }
        throw new Error(errorData.message || `API Error: ${response.status}`);
      }

      const data = await response.json();
      console.log('직원 생성 데이터:', data);
      return data.employee;
    } catch (err) {
      console.error('직원 생성 실패:', err);
      throw err;
    }
  },

  /**
   * 프로젝트 생성 API
   */
  createProject: async (projectData: any): Promise<Project> => {
    const url = `${API_BASE_URL}${API_ENDPOINTS.PROJECTS_LIST}`;
    console.log('프로젝트 생성:', url, projectData);
    
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: getHeaders(),
        body: JSON.stringify(projectData),
      });

      console.log('프로젝트 생성 응답 상태:', response.status);

      if (!response.ok) {
        const errorText = await response.text();
        console.error('프로젝트 생성 에러:', errorText);
        let errorData;
        try {
          errorData = JSON.parse(errorText);
        } catch {
          errorData = { message: errorText || 'Unknown error' };
        }
        throw new Error(errorData.message || `API Error: ${response.status}`);
      }

      const data = await response.json();
      console.log('프로젝트 생성 데이터:', data);
      return data;
    } catch (err) {
      console.error('프로젝트 생성 실패:', err);
      throw err;
    }
  },

  /**
   * 프로젝트 배정 API
   */
  assignProject: async (projectId: string, employeeId: string, assignmentData?: any): Promise<any> => {
    const url = `${API_BASE_URL}/projects/${projectId}/assign`;
    
    const requestBody = {
      employee_id: employeeId,
      ...(assignmentData && {
        role: assignmentData.role,
        start_date: assignmentData.startDate,
        end_date: assignmentData.endDate,
        allocation_rate: assignmentData.allocationRate,
        assignment_reason: assignmentData.reason,
      }),
    };
    
    console.log('프로젝트 배정:', url, requestBody);
    
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: getHeaders(),
        body: JSON.stringify(requestBody),
      });

      console.log('프로젝트 배정 응답 상태:', response.status);

      if (!response.ok) {
        const errorText = await response.text();
        console.error('프로젝트 배정 에러:', errorText);
        let errorData;
        try {
          errorData = JSON.parse(errorText);
        } catch {
          errorData = { message: errorText || 'Unknown error' };
        }
        throw new Error(errorData.error || errorData.message || `API Error: ${response.status}`);
      }

      const data = await response.json();
      console.log('프로젝트 배정 데이터:', data);
      return data;
    } catch (err) {
      console.error('프로젝트 배정 실패:', err);
      throw err;
    }
  },
};

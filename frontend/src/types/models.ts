/**
 * 백엔드 데이터 모델과 매핑되는 TypeScript 타입 정의
 */

// 기술 숙련도 레벨
export enum SkillLevel {
  BEGINNER = 'Beginner',
  INTERMEDIATE = 'Intermediate',
  ADVANCED = 'Advanced',
  EXPERT = 'Expert',
}

// 기술 스택
export interface Skill {
  name: string;
  level: SkillLevel;
  years: number;
}

// 직원 기본 정보
export interface BasicInfo {
  name: string;
  role: string;
  years_of_experience: number;
  email: string;
}

// 학력 정보
export interface Education {
  degree: string;
  university: string;
}

// 프로젝트 참여 이력
export interface WorkExperience {
  project_id: string;
  project_name: string;
  role: string;
  period: string;
  main_tasks: string[];
  performance_result?: string;
}

// 직원 프로필
export interface Employee {
  user_id: string;
  basic_info: BasicInfo;
  self_introduction?: string;
  skills: Skill[];
  work_experience: WorkExperience[];
  education?: Education;
  certifications: string[];
  // UI 전용 필드
  availability?: 'available' | 'busy' | 'pending';
  currentProject?: string | null;
  department?: string;
}

// 프로젝트 기간
export interface ProjectPeriod {
  start: string;
  end: string;
  duration_months: number;
}

// 기술 스택
export interface TechStack {
  backend: string[];
  frontend: string[];
  data: string[];
  infra: string[];
}

// 프로젝트
export interface Project {
  project_id: string;
  project_name: string;
  client_industry: string;
  period: ProjectPeriod;
  budget_scale?: string;
  description?: string;
  tech_stack: TechStack;
  requirements: string[];
  team_composition?: Record<string, number>;
  // UI 전용 필드
  status?: 'planning' | 'in-progress' | 'completed';
  assignedMembers?: number;
  requiredMembers?: number;
  matchRate?: number;
}

// 추천 결과
export interface Recommendation {
  user_id: string;
  name: string;
  skill_match_score: number;
  affinity_score: number;
  availability_score: number;
  overall_score: number;
  reasoning: string;
  matched_skills: string[];
  team_synergy: string[];
  // UI 전용 필드
  position?: string;
  experience?: number;
  skills?: string[];
  reasons?: string[];
}

// 프로젝트 추천 요청
export interface RecommendationRequest {
  project_id: string;
  required_skills: string[];
  team_size: number;
  project_duration_months?: number;
}

// 프로젝트 추천 응답
export interface RecommendationResponse {
  project_id: string;
  recommendations: Recommendation[];
}

// 도메인 분석 결과
export interface DomainInsight {
  domain: string;
  confidence: number;
  potential_projects: number;
  required_skills: string[];
  available_experts: number;
  insights: string[];
  market_demand: 'high' | 'medium' | 'low';
}

// 도메인 분석 응답
export interface DomainAnalysisResponse {
  insights: DomainInsight[];
  team_suggestions?: TeamSuggestion[];
}

// 팀 구성 제안
export interface TeamSuggestion {
  role: string;
  required_count: number;
  suggested_personnel: string[];
  skills: string[];
}

// 정량적 분석 요청
export interface QuantitativeAnalysisRequest {
  employee_id: string;
}

// 정량적 분석 응답
export interface QuantitativeAnalysisResponse {
  employee_id: string;
  experience_metrics: {
    years_of_experience: number;
    project_count: number;
    skill_diversity: number;
  };
  tech_stack_evaluation: {
    recency_score: number;
    demand_score: number;
    overall_score: number;
  };
  project_experience_scores: {
    scale_score: number;
    role_score: number;
    performance_score: number;
    overall_score: number;
  };
}

// 정성적 분석 요청
export interface QualitativeAnalysisRequest {
  employee_id: string;
}

// 정성적 분석 응답
export interface QualitativeAnalysisResponse {
  employee_id: string;
  resume_analysis: {
    strengths: string[];
    weaknesses: string[];
    recommendations: string[];
  };
  suspicious_content: {
    flagged_items: string[];
    verification_needed: boolean;
  };
  overall_evaluation: string;
}

// 인력 평가
export interface PersonnelEvaluation {
  evaluation_id: string;
  user_id: string;
  name: string;
  type: 'career' | 'freelancer';
  status: 'pending' | 'approved' | 'rejected' | 'review';
  overall_score: number;
  submitted_at: string;
  quantitative_analysis?: QuantitativeAnalysisResponse;
  qualitative_analysis?: QualitativeAnalysisResponse;
  review_comments?: string;
  rejection_reason?: string;
}

// 대시보드 메트릭
export interface DashboardMetrics {
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
}

// 이력서 업로드 응답
export interface ResumeUploadResponse {
  job_id: string;
  status: 'processing' | 'completed' | 'failed';
  message: string;
}

// 이력서 파싱 상태
export interface ResumeParseStatus {
  job_id: string;
  status: 'processing' | 'completed' | 'failed';
  progress: number;
  result?: {
    employee_id: string;
    parsed_data: Partial<Employee>;
  };
  error?: string;
}

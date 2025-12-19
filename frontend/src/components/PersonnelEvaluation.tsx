import { useState, useEffect } from 'react';
import { Search, Upload, User, TrendingUp, Shield, Users, FileText, CheckCircle, AlertCircle, BarChart3, Target, X } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { Card, CardContent } from './ui/card';
import { Badge } from './ui/badge';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Progress } from './ui/progress';
import { apiService } from '../services/api.service';
import { ResumeUploadModal } from './ResumeUploadModal';
import { VerificationQuestionsModal } from './VerificationQuestionsModal';
import { toast } from 'sonner';
import { API_BASE_URL } from '../config/api';

interface EvaluationResult {
  evaluation_id: string;
  employee_id: string;
  employee_name: string;
  evaluation_date: string;
  scores: {
    technical_skills: number;
    project_experience: number;
    resume_credibility: number;
    cultural_fit: number;
  };
  overall_score: number;
  strengths: string[];
  weaknesses: string[];
  analysis: {
    tech_stack: string;
    project_similarity: string;
    credibility: string;
    market_comparison: string;
  };
  ai_recommendation: string;
  skill_gap_analysis?: {
    missing_skills: Array<{
      name: string;
      percentage: number;
      count: number;
      total: number;
    }>;
    recommended_skills: Array<{
      name: string;
      percentage: number;
      count: number;
      total: number;
    }>;
    peer_comparison: string;
    peer_count: number;
  };
  project_history: any[];
  skills: any[];
  experience_years: number;
  status: string;
}

export function PersonnelEvaluation() {
  const [searchMode, setSearchMode] = useState<'name' | 'upload' | 'pending'>('name');
  const [searchQuery, setSearchQuery] = useState('');
  const [employees, setEmployees] = useState<any[]>([]);
  const [allEmployees, setAllEmployees] = useState<any[]>([]); // 전체 직원 목록
  const [currentPage, setCurrentPage] = useState(1); // 현재 페이지
  const [itemsPerPage] = useState(10); // 페이지당 항목 수
  const [pendingCandidates, setPendingCandidates] = useState<any[]>([]);
  const [searchingEmployee, setSearchingEmployee] = useState(false);
  const [selectedEmployee, setSelectedEmployee] = useState<any>(null);
  const [evaluationResult, setEvaluationResult] = useState<EvaluationResult | null>(null);
  const [evaluating, setEvaluating] = useState(false);
  const [isUploadModalOpen, setIsUploadModalOpen] = useState(false);
  const [isFromResume, setIsFromResume] = useState(false); // 이력서 업로드로 평가된 경우
  const [saving, setSaving] = useState(false);
  const [loadingPending, setLoadingPending] = useState(false);
  const [showVerificationModal, setShowVerificationModal] = useState(false);
  const [verificationQuestions, setVerificationQuestions] = useState<any[]>([]);

  // 대기자 명단 불러오기
  const loadPendingCandidates = async () => {
    try {
      setLoadingPending(true);
      console.log('대기자 명단 로딩 시작...');
      
      // PendingCandidates API 호출 (임시로 직접 fetch 사용)
      const response = await fetch(`${API_BASE_URL}/pending-candidates`);
      
      if (!response.ok) {
        throw new Error('대기자 조회 실패');
      }
      
      const data = await response.json();
      const candidates = data.candidates || [];
      
      console.log('대기자 수:', candidates.length);
      setPendingCandidates(candidates);
      
      if (candidates.length === 0) {
        toast.info('대기 중인 지원자가 없습니다');
      } else {
        toast.success(`${candidates.length}명의 대기자를 찾았습니다`);
      }
    } catch (error) {
      console.error('대기자 목록 조회 실패:', error);
      toast.error('대기자 목록 조회에 실패했습니다');
    } finally {
      setLoadingPending(false);
    }
  };

  // 전체 직원 목록 로드
  const loadAllEmployees = async () => {
    try {
      setSearchingEmployee(true);
      const data = await apiService.getEmployees(); // 배열을 직접 반환
      setAllEmployees(data);
      console.log(`전체 직원 ${data.length}명 로드 완료`);
    } catch (error) {
      console.error('직원 목록 로드 실패:', error);
      toast.error('직원 목록을 불러오는데 실패했습니다');
    } finally {
      setSearchingEmployee(false);
    }
  };

  // 필터링된 직원 목록 가져오기
  const getFilteredEmployees = () => {
    if (!searchQuery.trim()) {
      return allEmployees;
    }
    return allEmployees.filter((emp: any) => {
      const name = emp.name || emp.employeeName || emp.basic_info?.name || '';
      return name.toLowerCase().includes(searchQuery.toLowerCase());
    });
  };

  // 현재 페이지의 직원 목록
  const getCurrentPageEmployees = () => {
    const filtered = getFilteredEmployees();
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    return filtered.slice(startIndex, endIndex);
  };

  // 전체 페이지 수 계산
  const totalPages = Math.ceil(getFilteredEmployees().length / itemsPerPage);

  // 페이지 변경
  const handlePageChange = (page: number) => {
    setCurrentPage(page);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  // searchMode가 변경될 때 자동으로 로드
  useEffect(() => {
    if (searchMode === 'pending') {
      loadPendingCandidates();
    } else if (searchMode === 'name') {
      loadAllEmployees();
    }
  }, [searchMode]);

  // 컴포넌트 마운트 시 전체 직원 목록 로드
  useEffect(() => {
    loadAllEmployees();
  }, []);

  // 검색어 변경 시 첫 페이지로 이동
  useEffect(() => {
    setCurrentPage(1);
  }, [searchQuery]);

  // 직원 검색
  const handleSearchEmployee = async () => {
    console.log('=== handleSearchEmployee 함수 호출됨 ===');
    console.log('검색어:', searchQuery);
    
    if (!searchQuery.trim()) {
      console.log('검색어가 비어있음');
      toast.error('검색할 이름을 입력하세요');
      return;
    }

    try {
      setSearchingEmployee(true);
      console.log('직원 검색 시작:', searchQuery);
      
      const response = await apiService.getEmployees();
      console.log('API 응답:', response);
      
      // API 응답 구조 확인 및 처리
      let allEmployees = [];
      if (Array.isArray(response)) {
        allEmployees = response;
      } else if (response.employees && Array.isArray(response.employees)) {
        allEmployees = response.employees;
      } else if (response.Items && Array.isArray(response.Items)) {
        allEmployees = response.Items;
      }
      
      console.log('전체 직원 수:', allEmployees.length);
      console.log('첫 번째 직원 데이터:', allEmployees[0]);
      
      const filtered = allEmployees.filter((emp: any) => {
        // 다양한 필드명 지원
        const name = emp.name || emp.employeeName || emp.basic_info?.name || '';
        console.log('직원 이름:', name, '검색어:', searchQuery);
        return name.toLowerCase().includes(searchQuery.toLowerCase());
      });
      
      console.log('검색 결과:', filtered.length);
      console.log('필터링된 직원:', filtered);
      
      // 검색 결과도 무한 스크롤 적용
      setAllEmployees(filtered);
      setEmployees(filtered.slice(0, 10));
      setDisplayedCount(10);

      if (filtered.length === 0) {
        toast.info('검색 결과가 없습니다');
      } else {
        toast.success(`${filtered.length}명의 직원을 찾았습니다`);
      }
    } catch (error) {
      console.error('직원 검색 실패:', error);
      toast.error('직원 검색에 실패했습니다');
    } finally {
      setSearchingEmployee(false);
    }
  };

  // 직원 평가 수행
  const handleEvaluateEmployee = async (employee: any) => {
    try {
      setEvaluating(true);
      setSelectedEmployee(employee);
      
      // employee_id 추출 (다양한 필드명 지원)
      const employeeId = employee.user_id || employee.employeeId || employee.employee_id || employee.id;
      console.log('평가 대상 직원 ID:', employeeId);
      console.log('직원 데이터:', employee);
      
      // API 호출 (employee_evaluation Lambda)
      const response = await fetch(
        `${API_BASE_URL}/employee-evaluation`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            employee_id: employeeId,
          }),
        }
      );

      if (!response.ok) {
        throw new Error('평가 요청 실패');
      }

      const result = await response.json();
      setEvaluationResult(result);
      toast.success('평가가 완료되었습니다');
    } catch (error) {
      console.error('평가 실패:', error);
      toast.error('평가에 실패했습니다');
    } finally {
      setEvaluating(false);
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 85) return 'text-green-600';
    if (score >= 70) return 'text-blue-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreBgColor = (score: number) => {
    if (score >= 85) return 'bg-green-50';
    if (score >= 70) return 'bg-blue-50';
    if (score >= 60) return 'bg-yellow-50';
    return 'bg-red-50';
  };

  return (
    <div className="space-y-6">
      {/* 헤더 */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-center justify-between"
      >
        <div>
          <h2 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
            인력 평가
          </h2>
          <p className="text-gray-600 mt-1">
            등록된 직원 검색 또는 이력서 업로드를 통해 인력을 평가합니다
          </p>
        </div>
      </motion.div>

      {/* 평가 방법 선택 */}
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="grid grid-cols-3 gap-4"
      >
        <Button
          onClick={() => {
            setSearchMode('name');
            // 평가 정보 초기화
            setEvaluationResult(null);
            setSelectedEmployee(null);
            setVerificationQuestions([]);
            setIsFromResume(false);
          }}
          variant={searchMode === 'name' ? 'default' : 'outline'}
          className={`py-6 text-base font-semibold ${
            searchMode === 'name'
              ? 'bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700'
              : 'hover:bg-gray-50'
          }`}
        >
          <User className="w-5 h-5 mr-2" />
          등록된 직원 검색
        </Button>
        <Button
          onClick={() => {
            setSearchMode('upload');
            // 평가 정보 초기화
            setEvaluationResult(null);
            setSelectedEmployee(null);
            setVerificationQuestions([]);
            setIsFromResume(false);
          }}
          variant={searchMode === 'upload' ? 'default' : 'outline'}
          className={`py-6 text-base font-semibold ${
            searchMode === 'upload'
              ? 'bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700'
              : 'hover:bg-gray-50'
          }`}
        >
          <Upload className="w-5 h-5 mr-2" />
          이력서 업로드
        </Button>
        <Button
          onClick={() => {
            setSearchMode('pending');
            // 평가 정보 초기화
            setEvaluationResult(null);
            setSelectedEmployee(null);
            setVerificationQuestions([]);
            setIsFromResume(false);
            loadPendingCandidates();
          }}
          variant={searchMode === 'pending' ? 'default' : 'outline'}
          className={`py-6 text-base font-semibold ${
            searchMode === 'pending'
              ? 'bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700'
              : 'hover:bg-gray-50'
          }`}
        >
          <Users className="w-5 h-5 mr-2" />
          대기자 명단
        </Button>
      </motion.div>

      {/* 검색 영역 */}
      <AnimatePresence mode="wait">
        {searchMode === 'name' ? (
          <motion.div
            key="search"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 20 }}
            className="space-y-4"
          >
            <Card>
              <CardContent className="p-6">
                <div className="flex gap-3">
                  <div className="relative flex-1">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                    <Input
                      placeholder="직원 이름으로 검색"
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                      onKeyPress={(e) => e.key === 'Enter' && handleSearchEmployee()}
                      className="pl-10 h-12"
                    />
                  </div>
                  <Button
                    onClick={handleSearchEmployee}
                    disabled={searchingEmployee}
                    className="h-12 px-8 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700"
                  >
                    {searchingEmployee ? (
                      <>
                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                        검색 중...
                      </>
                    ) : (
                      <>
                        <Search className="w-4 h-4 mr-2" />
                        검색
                      </>
                    )}
                  </Button>
                </div>

                {/* 직원 목록 */}
                {allEmployees.length > 0 && (
                  <div className="mt-6 space-y-3">
                    <h3 className="font-semibold text-gray-900">
                      {searchQuery ? `검색 결과 (페이지 ${currentPage}/${totalPages} - 전체 ${getFilteredEmployees().length}명)` : `전체 직원 (페이지 ${currentPage}/${totalPages} - 전체 ${allEmployees.length}명)`}
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                      {getCurrentPageEmployees().map((employee, idx) => {
                        const name = employee.name || employee.employeeName || employee.basic_info?.name || '이름 없음';
                        // role 필드를 직책으로 사용
                        const position = employee.position || employee.role || employee.basic_info?.role || '직책 미정';
                        // 경력 년수 추출
                        const experience = employee.experienceYears || employee.experience_years || employee.basic_info?.years_of_experience || 0;
                        const employeeId = employee.user_id || employee.employeeId || employee.employee_id || employee.id || idx;
                        
                        return (
                          <motion.div
                            key={employeeId}
                            initial={{ opacity: 0, scale: 0.95 }}
                            animate={{ opacity: 1, scale: 1 }}
                            className="p-4 border border-gray-200 rounded-lg hover:border-blue-500 hover:shadow-md transition-all cursor-pointer"
                            onClick={() => handleEvaluateEmployee(employee)}
                          >
                            <div className="flex items-center justify-between">
                              <div className="flex items-center gap-3">
                                <div className="w-12 h-12 rounded-full bg-gradient-to-br from-blue-500 to-indigo-500 flex items-center justify-center text-white font-bold">
                                  {name.charAt(0)}
                                </div>
                                <div>
                                  <div className="font-semibold text-gray-900">{name}</div>
                                  <div className="text-sm text-gray-500">
                                    {position} · {experience}년 경력
                                  </div>
                                </div>
                              </div>
                              <Button size="sm" variant="outline">
                                평가하기
                              </Button>
                            </div>
                          </motion.div>
                        );
                      })}
                    </div>
                    
                    {/* 페이지네이션 */}
                    {totalPages > 1 && (
                      <div className="flex justify-center items-center gap-2 mt-6">
                        <Button
                          onClick={() => handlePageChange(currentPage - 1)}
                          disabled={currentPage === 1}
                          variant="outline"
                          size="sm"
                        >
                          이전
                        </Button>
                        
                        <div className="flex gap-2">
                          {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => {
                            if (
                              page === 1 ||
                              page === totalPages ||
                              (page >= currentPage - 2 && page <= currentPage + 2)
                            ) {
                              return (
                                <Button
                                  key={page}
                                  onClick={() => handlePageChange(page)}
                                  variant="outline"
                                  size="sm"
                                  style={
                                    currentPage === page
                                      ? {
                                          backgroundColor: '#2563eb',
                                          color: 'white',
                                          fontWeight: 'bold',
                                          borderColor: '#2563eb',
                                        }
                                      : {}
                                  }
                                >
                                  {page}
                                </Button>
                              );
                            } else if (
                              page === currentPage - 3 ||
                              page === currentPage + 3
                            ) {
                              return <span key={page} className="px-2">...</span>;
                            }
                            return null;
                          })}
                        </div>

                        <Button
                          onClick={() => handlePageChange(currentPage + 1)}
                          disabled={currentPage === totalPages}
                          variant="outline"
                          size="sm"
                        >
                          다음
                        </Button>
                      </div>
                    )}
                  </div>
                )}
              </CardContent>
            </Card>
          </motion.div>
        ) : searchMode === 'upload' ? (
          <motion.div
            key="upload"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
          >
            <Card>
              <CardContent className="p-12 text-center">
                <Upload className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  이력서를 업로드하세요
                </h3>
                <p className="text-gray-600 mb-6">
                  PDF 형식의 이력서를 업로드하면 AI가 자동으로 분석하여 평가합니다
                </p>
                <Button
                  onClick={() => setIsUploadModalOpen(true)}
                  className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 px-8 py-6 text-base"
                >
                  <Upload className="w-5 h-5 mr-2" />
                  이력서 업로드
                </Button>
              </CardContent>
            </Card>
          </motion.div>
        ) : (
          <motion.div
            key="pending"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            className="space-y-4"
          >
            <Card>
              <CardContent className="p-6">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="font-semibold text-gray-900 text-lg">대기자 명단 ({pendingCandidates.length}명)</h3>
                  <Button
                    onClick={loadPendingCandidates}
                    disabled={loadingPending}
                    variant="outline"
                    size="sm"
                  >
                    {loadingPending ? '로딩 중...' : '새로고침'}
                  </Button>
                </div>

                {loadingPending ? (
                  <div className="text-center py-12">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-4 border-blue-600 mx-auto mb-4"></div>
                    <p className="text-gray-600">대기자 목록을 불러오는 중...</p>
                  </div>
                ) : pendingCandidates.length === 0 ? (
                  <div className="text-center py-12">
                    <Users className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                    <p className="text-gray-600">대기 중인 지원자가 없습니다</p>
                  </div>
                ) : (
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    {pendingCandidates.map((candidate, idx) => {
                      const name = candidate.name || candidate.basic_info?.name || '이름 없음';
                      const position = candidate.role || candidate.basic_info?.role || '신규 지원자';
                      const experience = candidate.years_of_experience || candidate.basic_info?.years_of_experience || 0;
                      const candidateId = candidate.candidate_id || candidate.user_id || candidate.id || idx;
                      
                      return (
                        <motion.div
                          key={candidateId}
                          initial={{ opacity: 0, scale: 0.95 }}
                          animate={{ opacity: 1, scale: 1 }}
                          className="p-4 border border-gray-200 rounded-lg hover:border-blue-500 hover:shadow-md transition-all cursor-pointer"
                          onClick={async () => {
                            // 카드 또는 버튼 클릭 시 평가 데이터 표시
                            if (candidate.evaluation_data) {
                              setEvaluationResult(candidate.evaluation_data);
                              setSelectedEmployee(candidate);
                              setIsFromResume(false);
                              setSearchMode('pending');
                              
                              // 최신 대기자 정보 다시 불러오기 (검증 질문 업데이트 확인)
                              try {
                                const response = await fetch(`${API_BASE_URL}/pending-candidates`);
                                if (response.ok) {
                                  const data = await response.json();
                                  const updatedCandidate = data.candidates.find(
                                    (c: any) => c.candidate_id === candidate.candidate_id
                                  );
                                  
                                  if (updatedCandidate && updatedCandidate.verification_questions) {
                                    setVerificationQuestions(updatedCandidate.verification_questions);
                                    console.log('검증 질문 로드:', updatedCandidate.verification_questions.length, '개');
                                  } else {
                                    setVerificationQuestions([]);
                                    console.log('검증 질문 아직 생성 중...');
                                  }
                                }
                              } catch (error) {
                                console.error('최신 데이터 로드 실패:', error);
                                // 실패해도 기존 데이터 사용
                                if (candidate.verification_questions && candidate.verification_questions.length > 0) {
                                  setVerificationQuestions(candidate.verification_questions);
                                } else {
                                  setVerificationQuestions([]);
                                }
                              }
                            } else {
                              toast.error('평가 데이터를 찾을 수 없습니다');
                            }
                          }}
                        >
                          <div className="flex items-center justify-between">
                            <div className="flex items-center gap-3">
                              <div className="w-12 h-12 rounded-full bg-gradient-to-br from-orange-500 to-yellow-500 flex items-center justify-center text-white font-bold">
                                {name.charAt(0)}
                              </div>
                              <div>
                                <div className="font-semibold text-gray-900">{name}</div>
                                <div className="text-sm text-gray-500">
                                  {position} · {experience}년 경력
                                </div>
                              </div>
                            </div>
                            <Button size="sm" variant="outline">
                              정보보기
                            </Button>
                          </div>
                        </motion.div>
                      );
                    })}
                  </div>
                )}
              </CardContent>
            </Card>
          </motion.div>
        )}
      </AnimatePresence>

      {/* 평가 진행 중 */}
      {evaluating && (
        <Card>
          <CardContent className="p-12 text-center">
            <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-blue-600 mx-auto mb-4"></div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">평가 진행 중...</h3>
            <p className="text-gray-600">
              AI가 {selectedEmployee?.name}님의 이력을 분석하고 있습니다
            </p>
          </CardContent>
        </Card>
      )}

      {/* 평가 결과 */}
      <AnimatePresence>
        {evaluationResult && !evaluating && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="space-y-6"
          >
            {/* 종합 점수 카드 */}
            <Card className="overflow-hidden">
              <div className="bg-gradient-to-r from-blue-600 to-indigo-600 p-6 text-white">
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <h3 className="text-2xl font-bold mb-1">{evaluationResult.employee_name}</h3>
                    <p className="text-blue-100">
                      {evaluationResult.experience_years}년 경력 · 평가일: {new Date(evaluationResult.evaluation_date).toLocaleDateString()}
                    </p>
                  </div>
                  <div className="text-right flex-shrink-0 ml-6">
                    <div className="text-sm text-blue-100 mb-1">종합 점수</div>
                    <div className="text-5xl font-bold whitespace-nowrap">{evaluationResult.overall_score} <span className="text-5xl font-bold text-blue-100">/ 100</span></div>
                  </div>
                </div>
              </div>
            </Card>

            {/* 평가 항목 상세 */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {[
                {
                  key: 'technical_skills',
                  label: '기술 역량',
                  icon: Target,
                  description: '보유 기술 스택 및 숙련도',
                  color: 'blue',
                },
                {
                  key: 'project_experience',
                  label: '프로젝트 경험',
                  icon: BarChart3,
                  description: '프로젝트 경험 유사도',
                  color: 'indigo',
                },
                {
                  key: 'resume_credibility',
                  label: '이력 신뢰도',
                  icon: Shield,
                  description: '경력 이력 진위 여부',
                  color: 'green',
                },
                {
                  key: 'cultural_fit',
                  label: '문화 적합성',
                  icon: Users,
                  description: '조직 문화 적합도',
                  color: 'purple',
                },
              ].map((item) => {
                const score = evaluationResult.scores[item.key as keyof typeof evaluationResult.scores];
                const Icon = item.icon;
                
                return (
                  <motion.div
                    key={item.key}
                    initial={{ opacity: 0, scale: 0.95 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: 0.1 }}
                  >
                    <Card className={`${getScoreBgColor(score)} border-2`}>
                      <CardContent className="p-6">
                        <div className="flex items-start justify-between mb-4">
                          <div className="flex items-center gap-3">
                            <div className={`w-12 h-12 rounded-lg bg-${item.color}-100 flex items-center justify-center`}>
                              <Icon className={`w-6 h-6 text-${item.color}-600`} />
                            </div>
                            <div>
                              <h4 className="font-semibold text-gray-900">{item.label}</h4>
                              <p className="text-sm text-gray-600">{item.description}</p>
                            </div>
                          </div>
                          <div className={`text-3xl font-bold ${getScoreColor(score)}`}>
                            {score}
                          </div>
                        </div>
                        <Progress value={score} className="h-3" />
                        <div className="mt-2 text-xs text-gray-500 text-right">
                          상위 {Math.round(100 - score)}% 수준
                        </div>
                      </CardContent>
                    </Card>
                  </motion.div>
                );
              })}
            </div>

            {/* 상세 분석 */}
            <Card>
              <CardContent className="p-6 space-y-6">
                <h3 className="text-xl font-bold text-gray-900">상세 분석</h3>

                {/* 기술 스택 분석 */}
                <div>
                  <div className="flex items-center gap-2 mb-3">
                    <Target className="w-5 h-5 text-blue-600" />
                    <h4 className="font-semibold text-gray-900">기술 스택 및 숙련도 평가</h4>
                  </div>
                  <p className="text-gray-700 leading-relaxed">{evaluationResult.analysis.tech_stack}</p>
                  <div className="mt-3 flex flex-wrap gap-2">
                    {evaluationResult.skills.slice(0, 10).map((skill: any, idx: number) => (
                      <Badge key={idx} className="bg-blue-100 text-blue-700">
                        {typeof skill === 'string' ? skill : skill.name}
                      </Badge>
                    ))}
                  </div>
                </div>

                {/* 프로젝트 경험 유사도 */}
                <div>
                  <div className="flex items-center gap-2 mb-3">
                    <BarChart3 className="w-5 h-5 text-indigo-600" />
                    <h4 className="font-semibold text-gray-900">프로젝트 경험 유사도 분석</h4>
                  </div>
                  <p className="text-gray-700 leading-relaxed">{evaluationResult.analysis.project_similarity}</p>
                </div>

                {/* 이력 진위 검증 */}
                <div>
                  <div className="flex items-center gap-2 mb-3">
                    <Shield className="w-5 h-5 text-green-600" />
                    <h4 className="font-semibold text-gray-900">경력 이력 진위 여부 검증</h4>
                  </div>
                  <p className="text-gray-700 leading-relaxed">{evaluationResult.analysis.credibility}</p>
                </div>

                {/* 시장 비교 */}
                <div>
                  <div className="flex items-center gap-2 mb-3">
                    <TrendingUp className="w-5 h-5 text-purple-600" />
                    <h4 className="font-semibold text-gray-900">시장 평균 대비 역량 비교</h4>
                  </div>
                  <p className="text-gray-700 leading-relaxed">{evaluationResult.analysis.market_comparison}</p>
                </div>
              </CardContent>
            </Card>

            {/* 강점과 약점 */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Card>
                <CardContent className="p-6">
                  <div className="flex items-center gap-2 mb-4">
                    <CheckCircle className="w-5 h-5 text-green-600" />
                    <h4 className="font-semibold text-gray-900">강점</h4>
                  </div>
                  <ul className="space-y-2">
                    {evaluationResult.strengths.map((strength, idx) => (
                      <li key={idx} className="flex items-start gap-2">
                        <div className="w-1.5 h-1.5 rounded-full bg-green-600 mt-2"></div>
                        <span className="text-gray-700">{strength}</span>
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>

              <Card>
                <CardContent className="p-6">
                  <div className="flex items-center gap-2 mb-4">
                    <AlertCircle className="w-5 h-5 text-yellow-600" />
                    <h4 className="font-semibold text-gray-900">개선 필요 사항</h4>
                  </div>
                  <ul className="space-y-2">
                    {evaluationResult.weaknesses.map((weakness, idx) => (
                      <li key={idx} className="flex items-start gap-2">
                        <div className="w-1.5 h-1.5 rounded-full bg-yellow-600 mt-2"></div>
                        <span className="text-gray-700">{weakness}</span>
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            </div>

            {/* 기술 격차 분석 */}
            {evaluationResult.skill_gap_analysis && evaluationResult.skill_gap_analysis.peer_count > 0 && (
              <Card className="border-2 border-purple-200 bg-purple-50">
                <CardContent className="p-6">
                  <div className="flex items-center gap-2 mb-4">
                    <Users className="w-5 h-5 text-purple-600" />
                    <h4 className="font-semibold text-gray-900">동료 대비 기술 격차 분석</h4>
                  </div>
                  <p className="text-sm text-gray-600 mb-4">
                    {evaluationResult.skill_gap_analysis.peer_comparison}
                  </p>

                  {/* 필수 기술 (50% 이상의 동료가 보유) */}
                  {evaluationResult.skill_gap_analysis.missing_skills && 
                   evaluationResult.skill_gap_analysis.missing_skills.length > 0 && (
                    <div className="mb-4">
                      <h5 className="font-semibold text-red-700 mb-2 flex items-center gap-2">
                        <AlertCircle className="w-4 h-4" />
                        필수 기술 (동료의 50% 이상 보유)
                      </h5>
                      <div className="space-y-2">
                        {evaluationResult.skill_gap_analysis.missing_skills.map((skill, idx) => (
                          <div key={idx} className="bg-white rounded-lg p-3 border border-red-200">
                            <div className="flex items-center justify-between mb-1">
                              <span className="font-medium text-gray-900">{skill.name}</span>
                              <Badge className="bg-red-100 text-red-700">
                                {skill.percentage}% ({skill.count}/{skill.total}명)
                              </Badge>
                            </div>
                            <Progress value={skill.percentage} className="h-2" />
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* 추천 기술 (30-50%의 동료가 보유) */}
                  {evaluationResult.skill_gap_analysis.recommended_skills && 
                   evaluationResult.skill_gap_analysis.recommended_skills.length > 0 && (
                    <div>
                      <h5 className="font-semibold text-blue-700 mb-2 flex items-center gap-2">
                        <TrendingUp className="w-4 h-4" />
                        경쟁력 향상 추천 기술 (동료의 30-50% 보유)
                      </h5>
                      <div className="space-y-2">
                        {evaluationResult.skill_gap_analysis.recommended_skills.map((skill, idx) => (
                          <div key={idx} className="bg-white rounded-lg p-3 border border-blue-200">
                            <div className="flex items-center justify-between mb-1">
                              <span className="font-medium text-gray-900">{skill.name}</span>
                              <Badge className="bg-blue-100 text-blue-700">
                                {skill.percentage}% ({skill.count}/{skill.total}명)
                              </Badge>
                            </div>
                            <Progress value={skill.percentage} className="h-2" />
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* 데이터 부족 메시지 */}
                  {(!evaluationResult.skill_gap_analysis.missing_skills || 
                    evaluationResult.skill_gap_analysis.missing_skills.length === 0) &&
                   (!evaluationResult.skill_gap_analysis.recommended_skills || 
                    evaluationResult.skill_gap_analysis.recommended_skills.length === 0) && (
                    <div className="text-center py-4 text-gray-600">
                      <p>동료들과 비교했을 때 기술 스택이 우수합니다!</p>
                      <p className="text-sm mt-1">지속적인 학습으로 경쟁력을 유지하세요.</p>
                    </div>
                  )}
                </CardContent>
              </Card>
            )}

            {/* AI 추천 의견 */}
            <Card className="bg-gradient-to-r from-blue-50 to-indigo-50 border-2 border-blue-200">
              <CardContent className="p-6">
                <div className="flex items-start gap-3">
                  <div className="w-10 h-10 rounded-lg bg-blue-100 flex items-center justify-center flex-shrink-0">
                    <FileText className="w-5 h-5 text-blue-600" />
                  </div>
                  <div className="flex-1">
                    <h4 className="font-semibold text-gray-900 mb-2">AI 추천 의견</h4>
                    <p className="text-gray-700 leading-relaxed">{evaluationResult.ai_recommendation}</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* 검증 질문 리스트 (대기자 명단에서만 표시) */}
            {searchMode === 'pending' && verificationQuestions.length > 0 && (
              <Card className="bg-gradient-to-r from-orange-50 to-red-50 border-2 border-orange-200">
                <CardContent className="p-6">
                  <div className="flex items-center gap-3 mb-6">
                    <div className="w-10 h-10 rounded-lg bg-orange-100 flex items-center justify-center flex-shrink-0">
                      <AlertCircle className="w-5 h-5 text-orange-600" />
                    </div>
                    <div>
                      <h4 className="font-semibold text-gray-900 mb-1">이력서 검증 질문</h4>
                      <p className="text-sm text-gray-600">
                        면접 시 확인이 필요한 {verificationQuestions.length}개의 질문
                      </p>
                    </div>
                  </div>

                  {/* 질문 리스트 */}
                  <div className="space-y-4">
                    {verificationQuestions.map((q: any, idx: number) => {
                      const severityColors = {
                        high: 'bg-red-100 text-red-700 border-red-200',
                        medium: 'bg-yellow-100 text-yellow-700 border-yellow-200',
                        low: 'bg-green-100 text-green-700 border-green-200'
                      };
                      const severityLabels = {
                        high: '높음',
                        medium: '중간',
                        low: '낮음'
                      };
                      
                      return (
                        <div key={idx} className="bg-white p-4 rounded-lg border border-orange-200">
                          <div className="flex items-start gap-3 mb-2">
                            <div className="flex-shrink-0 w-6 h-6 rounded-full bg-orange-600 text-white flex items-center justify-center text-sm font-bold">
                              {idx + 1}
                            </div>
                            <div className="flex-1">
                              <div className="flex items-center gap-2 mb-2">
                                <span className="text-xs font-medium text-gray-600">{q.category}</span>
                                <span className={`text-xs px-2 py-0.5 rounded-full border ${severityColors[q.severity as keyof typeof severityColors] || severityColors.medium}`}>
                                  {severityLabels[q.severity as keyof typeof severityLabels] || '중간'}
                                </span>
                              </div>
                              <p className="text-gray-900 font-medium mb-2">{q.question}</p>
                              <p className="text-sm text-gray-600 italic">💡 {q.reason}</p>
                            </div>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </CardContent>
              </Card>
            )}

            {/* 액션 버튼 */}
            <div className="flex gap-3">
              {isFromResume || searchMode === 'pending' ? (
                <>
                  {/* 이력서 업로드 또는 대기자 조회: 승인/반려 버튼 */}
                  <button
                    onClick={async () => {
                      try {
                        setSaving(true);
                        
                        if (isFromResume) {
                          // 이력서 업로드 후 승인: 대기자로 저장 후 백그라운드에서 검증 질문 생성
                          toast.info('대기자 명단에 등록 중...');
                          
                          // 1. 대기자로 저장 (검증 질문 없이)
                          const response = await fetch(
                            `${API_BASE_URL}/pending-candidates`,
                            {
                              method: 'POST',
                              headers: {
                                'Content-Type': 'application/json',
                              },
                              body: JSON.stringify({
                                name: evaluationResult.employee_name,
                                email: `${evaluationResult.employee_name.replace(/\s/g, '')}@temp.com`,
                                role: '신규 지원자',
                                years_of_experience: evaluationResult.experience_years,
                                skills: evaluationResult.skills.map((skill: any) => ({
                                  name: typeof skill === 'string' ? skill : skill.name,
                                  level: 'Intermediate',
                                  years: 0
                                })),
                                status: 'pending',
                                evaluation_data: evaluationResult,
                                verification_questions: [], // 빈 배열로 시작
                              }),
                            }
                          );

                          if (!response.ok) {
                            throw new Error('대기자 등록 실패');
                          }

                          const candidateData = await response.json();
                          const candidateId = candidateData.id || candidateData.data?.candidate_id || candidateData.candidate_id;
                          console.log('대기자 등록 완료, candidate_id:', candidateId);
                          console.log('응답 데이터:', candidateData);

                          toast.success('대기자 명단에 추가되었습니다!');
                          
                          // 2. 백그라운드에서 검증 질문 생성 (응답 기다리지 않음)
                          toast.info('검증 질문 생성 중... (백그라운드)');
                          
                          // fetch를 호출하되 await 하지 않음 (fire and forget)
                          fetch(
                            `${API_BASE_URL}/resume/verification-questions`,
                            {
                              method: 'POST',
                              headers: {
                                'Content-Type': 'application/json',
                              },
                              body: JSON.stringify({
                                candidate_id: candidateId,
                                resume_data: {
                                  name: evaluationResult.employee_name,
                                  experience_years: evaluationResult.experience_years,
                                  skills: evaluationResult.skills,
                                  project_history: evaluationResult.project_history,
                                  strengths: evaluationResult.strengths,
                                  weaknesses: evaluationResult.weaknesses,
                                  analysis: evaluationResult.analysis,
                                }
                              }),
                            }
                          ).then(res => {
                            if (res.ok) {
                              console.log('검증 질문 생성 완료 (백그라운드)');
                            } else {
                              console.error('검증 질문 생성 실패:', res.status);
                            }
                          }).catch(err => {
                            console.error('검증 질문 생성 오류:', err);
                          });
                        } else {
                          // 대기자 명단에서 승인: PendingCandidates에서 삭제 후 Employees에 추가
                          const candidateId = selectedEmployee.candidate_id;
                          
                          // 1. PendingCandidates에서 삭제
                          await fetch(`${API_BASE_URL}/pending-candidates/${candidateId}`, {
                            method: 'DELETE'
                          });
                          
                          // 2. Employees에 추가 (status 없이)
                          const response = await fetch(
                            `${API_BASE_URL}/employees`,
                            {
                              method: 'POST',
                              headers: {
                                'Content-Type': 'application/json',
                              },
                              body: JSON.stringify({
                                name: selectedEmployee.name || selectedEmployee.basic_info?.name,
                                email: selectedEmployee.email || selectedEmployee.basic_info?.email || `${selectedEmployee.name}@temp.com`,
                                role: selectedEmployee.role || selectedEmployee.basic_info?.role || '신규 지원자',
                                years_of_experience: selectedEmployee.years_of_experience || selectedEmployee.basic_info?.years_of_experience || 0,
                                skills: selectedEmployee.skills || [],
                              }),
                            }
                          );

                          if (!response.ok) {
                            throw new Error('직원 승인 실패');
                          }

                          toast.success('직원이 정식으로 등록되었습니다!');
                        }
                        
                        // 화면 초기화
                        setEvaluationResult(null);
                        setSelectedEmployee(null);
                        setEmployees([]);
                        setPendingCandidates([]);
                        setSearchQuery('');
                        setIsFromResume(false);
                        
                        // 대기자 명단 새로고침
                        if (searchMode === 'pending') {
                          loadPendingCandidates();
                        }
                      } catch (error) {
                        console.error('승인 실패:', error);
                        toast.error('승인에 실패했습니다');
                      } finally {
                        setSaving(false);
                      }
                    }}
                    style={{ backgroundColor: '#4CAF50' }}
                    className="flex-1 hover:opacity-90 text-white font-semibold py-5 rounded-lg shadow-md transition-all text-lg flex items-center justify-center"
                    disabled={saving}
                  >
                    {saving ? (
                      <>
                        <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                        저장 중...
                      </>
                    ) : (
                      <>
                        <CheckCircle className="w-5 h-5 mr-2" />
                        승인
                      </>
                    )}
                  </button>
                  <button
                    onClick={async () => {
                      try {
                        if (!isFromResume && selectedEmployee && selectedEmployee.candidate_id) {
                          // 대기자 명단에서 반려: PendingCandidates에서 삭제
                          setSaving(true);
                          const candidateId = selectedEmployee.candidate_id;
                          
                          const response = await fetch(`${API_BASE_URL}/pending-candidates/${candidateId}`, {
                            method: 'DELETE'
                          });

                          if (!response.ok) {
                            throw new Error('삭제 실패');
                          }

                          toast.success('대기자가 삭제되었습니다');
                          
                          // 대기자 명단 새로고침
                          if (searchMode === 'pending') {
                            loadPendingCandidates();
                          }
                        } else {
                          // 이력서 업로드 후 반려: 화면만 초기화
                          toast.info('평가가 반려되었습니다');
                        }
                        
                        // 화면 초기화
                        setEvaluationResult(null);
                        setSelectedEmployee(null);
                        setEmployees([]);
                        setPendingCandidates([]);
                        setSearchQuery('');
                        setIsFromResume(false);
                      } catch (error) {
                        console.error('반려 실패:', error);
                        toast.error('반려 처리에 실패했습니다');
                      } finally {
                        setSaving(false);
                      }
                    }}
                    style={{ backgroundColor: '#dc3545' }}
                    className="flex-1 hover:opacity-90 text-white font-semibold py-5 rounded-lg shadow-md transition-all text-lg flex items-center justify-center"
                    disabled={saving}
                  >
                    <X className="w-5 h-5 mr-2" />
                    반려
                  </button>
                </>
              ) : (
                <>
                  {/* 기존 직원 평가의 경우: 새로운 평가/평가 결과 저장 버튼 */}
                  <Button
                    onClick={() => {
                      setEvaluationResult(null);
                      setSelectedEmployee(null);
                      setEmployees([]);
                      setSearchQuery('');
                    }}
                    variant="outline"
                    className="flex-1"
                  >
                    새로운 평가
                  </Button>
                  <Button
                    onClick={() => {
                      toast.success('평가 결과가 저장되었습니다');
                    }}
                    className="flex-1 bg-gradient-to-r from-blue-600 to-indigo-600"
                  >
                    평가 결과 저장
                  </Button>
                </>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* 이력서 업로드 모달 */}
      <ResumeUploadModal
        isOpen={isUploadModalOpen}
        onClose={() => setIsUploadModalOpen(false)}
        onUploadSuccess={(evaluationResult) => {
          console.log('이력서 분석 완료:', evaluationResult);
          setIsUploadModalOpen(false);
          
          // 평가 결과를 메인 화면에 표시
          setEvaluationResult(evaluationResult);
          setSelectedEmployee({
            name: evaluationResult.employee_name,
            user_id: evaluationResult.employee_id,
          });
          setIsFromResume(true); // 이력서 업로드로 평가됨
          
          toast.success('이력서 분석이 완료되었습니다!');
        }}
      />
    </div>
  );
}

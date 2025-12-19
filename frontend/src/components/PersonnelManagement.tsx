import { useState, useEffect } from 'react';
import { Search, Filter, UserPlus } from 'lucide-react';
import { motion } from 'framer-motion';
import { Card, CardContent } from './ui/card';
import { Badge } from './ui/badge';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from './ui/dialog';
import { api, Employee } from '../config/api';
import { EmployeeRegistrationModal } from './EmployeeRegistrationModal';
import { toast } from 'sonner';

interface Personnel {
  id: string;
  name: string;
  position: string;
  department: string;
  skills: string[];
  experience: number;
  currentProject: string | null;
  availability: 'available' | 'busy' | 'pending';
  projectHistory?: Array<{
    project_name: string;
    period?: string;
    duration?: string;
    role?: string;
    description?: string;
    main_tasks?: string[];
  }>;
}

export function PersonnelManagement() {
  const [searchQuery, setSearchQuery] = useState('');
  const [personnel, setPersonnel] = useState<Personnel[]>([]);
  const [allPersonnel, setAllPersonnel] = useState<Personnel[]>([]); // 전체 직원 목록
  const [currentPage, setCurrentPage] = useState(1); // 현재 페이지
  const [itemsPerPage] = useState(20); // 페이지당 항목 수
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  // DB에서 직원 목록 가져오기
  const fetchEmployees = async () => {
    try {
      setLoading(true);
      const response = await api.getEmployees();
      
      // API 응답을 Personnel 형식으로 변환
      const transformedData: Personnel[] = response.employees.map((emp: Employee) => ({
        id: emp.user_id,
        name: emp.basic_info.name,
        position: emp.basic_info.role,
        department: '개발팀', // 기본값 (DB에 없는 경우)
        skills: emp.skills.map(s => s.name),
        experience: emp.basic_info.years_of_experience,
        currentProject: null, // 기본값 (DB에 없는 경우)
        availability: 'available' as const, // 기본값
        projectHistory: emp.work_experience || [], // 프로젝트 이력 추가
      }));
      
      setAllPersonnel(transformedData);
      setError(null);
    } catch (err) {
      console.error('직원 목록 조회 실패:', err);
      setError(err instanceof Error ? err.message : '직원 목록을 불러오는데 실패했습니다');
    } finally {
      setLoading(false);
    }
  };

  // 필터링된 직원 목록 가져오기
  const getFilteredPersonnel = () => {
    if (!searchQuery.trim()) {
      return allPersonnel;
    }
    return allPersonnel.filter((person) =>
      person.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      person.position.toLowerCase().includes(searchQuery.toLowerCase()) ||
      person.skills.some((skill) => skill.toLowerCase().includes(searchQuery.toLowerCase()))
    );
  };

  // 현재 페이지의 직원 목록
  const getCurrentPagePersonnel = () => {
    const filtered = getFilteredPersonnel();
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    return filtered.slice(startIndex, endIndex);
  };

  // 전체 페이지 수 계산
  const totalPages = Math.ceil(getFilteredPersonnel().length / itemsPerPage);

  // 페이지 변경
  const handlePageChange = (page: number) => {
    setCurrentPage(page);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  // 검색어 변경 시 첫 페이지로 이동
  useEffect(() => {
    setCurrentPage(1);
  }, [searchQuery]);

  useEffect(() => {
    fetchEmployees();
  }, []);

  const filteredPersonnel = getCurrentPagePersonnel();

  const getAvailabilityColor = (availability: Personnel['availability']) => {
    switch (availability) {
      case 'available':
        return 'bg-green-100 text-green-700';
      case 'busy':
        return 'bg-red-100 text-red-700';
      case 'pending':
        return 'bg-yellow-100 text-yellow-700';
    }
  };

  const getAvailabilityText = (availability: Personnel['availability']) => {
    switch (availability) {
      case 'available':
        return '투입 가능';
      case 'busy':
        return '프로젝트 중';
      case 'pending':
        return '대기 중';
    }
  };

  return (
    <div className="space-y-6">
      <motion.div 
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-center justify-between"
      >
        <div>
          <h2 className="text-gray-900 mb-2 bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">인력 관리</h2>
          <p className="text-gray-600">전체 인력 정보를 확인하고 관리하세요 (페이지 {currentPage}/{totalPages} - 전체 {getFilteredPersonnel().length}명)</p>
        </div>
        <div className="flex gap-3">
          <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
            <Button 
              onClick={() => setIsModalOpen(true)}
              className="gap-2 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 shadow-lg shadow-blue-500/30"
            >
              <UserPlus className="w-4 h-4" />
              신규 인력 등록
            </Button>
          </motion.div>
        </div>
      </motion.div>

      {/* 로딩 및 에러 상태 */}
      {loading && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="text-center py-12"
        >
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          <p className="mt-4 text-gray-600">직원 목록을 불러오는 중...</p>
        </motion.div>
      )}

      {error && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="p-4 bg-red-50 border border-red-200 rounded-xl text-red-700"
        >
          {error}
        </motion.div>
      )}

      {/* Search and Filter */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
      >
        <Card className="bg-white/80 backdrop-blur-sm border-0 shadow-lg">
          <CardContent className="p-4">
            <div className="flex gap-4">
              <div className="flex-1 relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                <Input
                  placeholder="이름, 직급, 기술 스택으로 검색..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-10 border-0 bg-gray-50 focus:bg-white transition-colors"
                />
              </div>
              <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                <Button variant="outline" className="gap-2 border-gray-200">
                  <Filter className="w-4 h-4" />
                  필터
                </Button>
              </motion.div>
            </div>
          </CardContent>
        </Card>
      </motion.div>

      {/* Personnel Grid */}
      {!loading && !error && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredPersonnel.length === 0 ? (
            <div className="col-span-full text-center py-12">
              <p className="text-gray-600">검색 결과가 없습니다</p>
            </div>
          ) : (
            filteredPersonnel.map((person, index) => (
          <Dialog key={person.id}>
            <DialogTrigger asChild>
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4, delay: index * 0.05 }}
                whileHover={{ scale: 1.03, y: -5 }}
              >
                <Card className="cursor-pointer bg-white/80 backdrop-blur-sm border-0 shadow-lg hover:shadow-xl transition-all">
                  <CardContent className="p-6">
                    <div className="flex items-start justify-between mb-4">
                      <div className="flex items-center gap-3">
                        <motion.div 
                          whileHover={{ scale: 1.1, rotate: 5 }}
                          className="w-12 h-12 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-full flex items-center justify-center shadow-lg"
                        >
                          <span className="text-white">{person.name[0]}</span>
                        </motion.div>
                        <div>
                          <p className="text-gray-900">{person.name}</p>
                          <p className="text-sm text-gray-600">{person.position}</p>
                        </div>
                      </div>
                      <motion.span 
                        whileHover={{ scale: 1.1 }}
                        className={`px-2 py-1 rounded-full text-xs ${getAvailabilityColor(person.availability)}`}
                      >
                        {getAvailabilityText(person.availability)}
                      </motion.span>
                    </div>

                    <div className="space-y-3">
                      <div>
                        <p className="text-sm text-gray-600 mb-1">부서</p>
                        <p className="text-gray-900">{person.department}</p>
                      </div>

                      <div>
                        <p className="text-sm text-gray-600 mb-2">주요 기술</p>
                        <div className="flex flex-wrap gap-2">
                          {person.skills.slice(0, 3).map((skill, idx) => (
                            <motion.div
                              key={skill}
                              initial={{ opacity: 0, scale: 0 }}
                              animate={{ opacity: 1, scale: 1 }}
                              transition={{ delay: index * 0.05 + idx * 0.05 }}
                            >
                              <Badge variant="secondary" className="bg-blue-50 text-blue-700">
                                {skill}
                              </Badge>
                            </motion.div>
                          ))}
                          {person.skills.length > 3 && (
                            <Badge variant="secondary" className="bg-gray-100">+{person.skills.length - 3}</Badge>
                          )}
                        </div>
                      </div>

                      <div className="pt-3 border-t border-gray-200">
                        <p className="text-sm text-gray-600">경력: {person.experience}년</p>
                        {person.currentProject && (
                          <p className="text-sm text-gray-600 mt-1">현재: {person.currentProject}</p>
                        )}
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            </DialogTrigger>
            <DialogContent className="max-w-2xl">
              <DialogHeader>
                <DialogTitle>{person.name} - 상세 정보</DialogTitle>
              </DialogHeader>
              <div className="space-y-6">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-sm text-gray-600 mb-1">직급</p>
                    <p className="text-gray-900">{person.position}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600 mb-1">부서</p>
                    <p className="text-gray-900">{person.department}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600 mb-1">경력</p>
                    <p className="text-gray-900">{person.experience}년</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600 mb-1">상태</p>
                    <span className={`px-2 py-1 rounded-full text-xs ${getAvailabilityColor(person.availability)}`}>
                      {getAvailabilityText(person.availability)}
                    </span>
                  </div>
                </div>

                <div>
                  <p className="text-sm text-gray-600 mb-2">보유 기술</p>
                  <div className="flex flex-wrap gap-2">
                    {person.skills.map((skill) => (
                      <Badge key={skill}>{skill}</Badge>
                    ))}
                  </div>
                </div>

                {person.currentProject && (
                  <div>
                    <p className="text-sm text-gray-600 mb-1">현재 프로젝트</p>
                    <p className="text-gray-900">{person.currentProject}</p>
                  </div>
                )}

                <div>
                  <p className="text-sm text-gray-600 mb-3">프로젝트 참여 이력</p>
                  <div className="space-y-2">
                    {person.projectHistory && person.projectHistory.length > 0 ? (
                      person.projectHistory.slice(0, 5).map((project, idx) => (
                        <div key={idx} className="p-3 bg-gray-50 rounded-lg">
                          <div className="flex items-start justify-between mb-1">
                            <p className="text-gray-900 font-medium">{project.project_name}</p>
                            {project.role && (
                              <span className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded">
                                {project.role}
                              </span>
                            )}
                          </div>
                          <p className="text-sm text-gray-600">{project.period || project.duration || '기간 정보 없음'}</p>
                          {project.description && (
                            <p className="text-xs text-gray-500 mt-1 line-clamp-2">{project.description}</p>
                          )}
                          {project.main_tasks && project.main_tasks.length > 0 && (
                            <div className="mt-2">
                              <p className="text-xs text-gray-600">주요 업무:</p>
                              <ul className="text-xs text-gray-500 list-disc list-inside">
                                {project.main_tasks.slice(0, 2).map((task, taskIdx) => (
                                  <li key={taskIdx} className="truncate">{task}</li>
                                ))}
                              </ul>
                            </div>
                          )}
                        </div>
                      ))
                    ) : (
                      <div className="p-3 bg-gray-50 rounded-lg text-center">
                        <p className="text-sm text-gray-500">프로젝트 이력이 없습니다</p>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </DialogContent>
          </Dialog>
            ))
          )}
        </div>
      )}

      {/* 페이지네이션 */}
      {!loading && !error && totalPages > 1 && (
        <div className="flex justify-center items-center gap-2 mt-8">
          <Button
            onClick={() => handlePageChange(currentPage - 1)}
            disabled={currentPage === 1}
            variant="outline"
            className="px-4 py-2"
          >
            이전
          </Button>
          
          <div className="flex gap-2">
            {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => {
              // 현재 페이지 주변 5개만 표시
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
                    className={`px-4 py-2 ${
                      currentPage === page
                        ? ""
                        : "bg-white hover:bg-gray-50 text-gray-700"
                    }`}
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
            className="px-4 py-2"
          >
            다음
          </Button>
        </div>
      )}

      {/* 직원 등록 모달 */}
      <EmployeeRegistrationModal
        open={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSubmit={async (data) => {
          try {
            // API 호출하여 직원 생성
            await api.createEmployee(data);
            
            // 성공 시 직원 목록 새로고침
            await fetchEmployees();
            
            // 성공 알림
            toast.success('직원이 성공적으로 등록되었습니다', {
              description: `${data.name}님이 시스템에 추가되었습니다`,
            });
          } catch (error) {
            // 에러는 모달 컴포넌트에서 처리됨
            throw error;
          }
        }}
      />
    </div>
  );
}
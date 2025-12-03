import { Users, Briefcase, TrendingUp, AlertCircle, ArrowUp, ArrowDown, Clock, CheckCircle, XCircle, FileText, Bell } from 'lucide-react';
import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { useEffect, useState } from 'react';
import { api, DashboardMetricsResponse } from '../config/api';
import { Badge } from './ui/badge';

export function Dashboard() {
  const [metrics, setMetrics] = useState<DashboardMetricsResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // 대시보드 메트릭 데이터 가져오기
  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        setLoading(true);
        setError(null);
        const data = await api.getDashboardMetrics();
        setMetrics(data);
      } catch (err) {
        console.error('대시보드 메트릭 로드 실패:', err);
        setError(err instanceof Error ? err.message : '데이터를 불러오는데 실패했습니다.');
      } finally {
        setLoading(false);
      }
    };

    fetchMetrics();
  }, []);

  // 로딩 상태
  if (loading) {
    return (
      <div className="space-y-6">
        <div>
          <h2 className="text-gray-900 mb-2 bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">대시보드</h2>
          <p className="text-gray-600">전체 인력 및 프로젝트 현황을 확인하세요</p>
        </div>
        <div className="flex items-center justify-center h-64">
          <div className="text-gray-500">데이터를 불러오는 중...</div>
        </div>
      </div>
    );
  }

  // 에러 상태
  if (error || !metrics) {
    return (
      <div className="space-y-6">
        <div>
          <h2 className="text-gray-900 mb-2 bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">대시보드</h2>
          <p className="text-gray-600">전체 인력 및 프로젝트 현황을 확인하세요</p>
        </div>
        <div className="flex items-center justify-center h-64">
          <div className="text-red-500">{error || '데이터를 불러올 수 없습니다.'}</div>
        </div>
      </div>
    );
  }

  // 통계 데이터 구성
  const stats = [
    { 
      label: '전체 인력', 
      value: metrics.total_employees.toString(), 
      change: '+0', 
      icon: Users, 
      color: 'from-blue-500 to-blue-600' 
    },
    { 
      label: '진행 중인 프로젝트', 
      value: metrics.active_projects.toString(), 
      change: '+0', 
      icon: Briefcase, 
      color: 'from-green-500 to-emerald-600' 
    },
    { 
      label: '투입 대기 인력', 
      value: metrics.available_employees.toString(), 
      change: '+0', 
      icon: TrendingUp, 
      color: 'from-purple-500 to-purple-600' 
    },
    { 
      label: '대기자명단', 
      value: metrics.pending_candidates.toString(), 
      change: '+0', 
      icon: AlertCircle, 
      color: 'from-orange-500 to-orange-600' 
    },
  ];

  const topSkills = metrics.top_skills;

  return (
    <div className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h2 className="text-3xl font-bold text-gray-900 mb-2 bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">대시보드</h2>
        <p className="text-gray-600">전체 인력 및 프로젝트 현황을 확인하세요</p>
      </motion.div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6">
        {stats.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <motion.div
              key={stat.label}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              whileHover={{ scale: 1.05, y: -5 }}
            >
              <Card className="overflow-hidden bg-white/80 backdrop-blur-sm border-0 shadow-lg hover:shadow-xl transition-shadow">
                <CardContent className="p-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-gray-600 mb-1">{stat.label}</p>
                      <motion.p 
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        transition={{ duration: 0.5, delay: index * 0.1 + 0.2 }}
                        className="text-3xl font-bold text-gray-900"
                      >
                        {stat.value}
                      </motion.p>
                      <div className="flex items-center gap-1 text-xs mt-1">
                        {stat.change.startsWith('+') ? (
                          <>
                            <motion.div
                              initial={{ opacity: 0, y: 5 }}
                              animate={{ opacity: 1, y: 0 }}
                              className="flex items-center text-green-600"
                            >
                              <ArrowUp className="w-3 h-3" />
                              <span className="font-medium">{stat.change}</span>
                            </motion.div>
                            <span className="text-gray-500">이번 달</span>
                          </>
                        ) : stat.change.startsWith('-') ? (
                          <>
                            <motion.div
                              initial={{ opacity: 0, y: -5 }}
                              animate={{ opacity: 1, y: 0 }}
                              className="flex items-center text-red-600"
                            >
                              <ArrowDown className="w-3 h-3" />
                              <span className="font-medium">{stat.change}</span>
                            </motion.div>
                            <span className="text-gray-500">이번 달</span>
                          </>
                        ) : (
                          <span className="text-gray-500">변동 없음</span>
                        )}
                      </div>
                    </div>
                    <motion.div 
                      whileHover={{ rotate: 360, scale: 1.1 }}
                      transition={{ duration: 0.6 }}
                      className={`w-12 h-12 bg-gradient-to-br ${stat.color} rounded-xl flex items-center justify-center shadow-lg`}
                    >
                      <Icon className="w-6 h-6 text-white" />
                    </motion.div>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          );
        })}
      </div>

      {/* 알림/액션 필요 항목 */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.4 }}
      >
        <Card className="bg-gradient-to-br from-orange-50 to-red-50 border-orange-200 shadow-lg">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-orange-900">
              <Bell className="w-5 h-5" />
              액션 필요 항목
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <motion.div
                whileHover={{ scale: 1.05 }}
                className="p-4 bg-white rounded-xl border border-orange-200"
              >
                <div className="flex items-center gap-3 mb-2">
                  <Clock className="w-5 h-5 text-orange-600" />
                  <p className="text-sm font-semibold text-gray-700">장기 대기 인력</p>
                </div>
                <p className="text-2xl font-bold text-orange-600">{metrics.action_required.long_waiting_employees}명</p>
                <p className="text-xs text-gray-600 mt-1">프로젝트 미배정</p>
              </motion.div>
              
              <motion.div
                whileHover={{ scale: 1.05 }}
                className="p-4 bg-white rounded-xl border border-red-200"
              >
                <div className="flex items-center gap-3 mb-2">
                  <FileText className="w-5 h-5 text-red-600" />
                  <p className="text-sm font-semibold text-gray-700">평가 지연 건</p>
                </div>
                <p className="text-2xl font-bold text-red-600">{metrics.action_required.delayed_evaluations}건</p>
                <p className="text-xs text-gray-600 mt-1">7일 이상 대기</p>
              </motion.div>
              
              <motion.div
                whileHover={{ scale: 1.05 }}
                className="p-4 bg-white rounded-xl border border-yellow-200"
              >
                <div className="flex items-center gap-3 mb-2">
                  <AlertCircle className="w-5 h-5 text-yellow-600" />
                  <p className="text-sm font-semibold text-gray-700">검증 필요</p>
                </div>
                <p className="text-2xl font-bold text-yellow-600">{metrics.action_required.verification_needed}건</p>
                <p className="text-xs text-gray-600 mt-1">이력서 검증 미완료</p>
              </motion.div>
            </div>
          </CardContent>
        </Card>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* 인력 현황 상세 */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.5 }}
        >
          <Card className="bg-white/80 backdrop-blur-sm border-0 shadow-lg">
            <CardHeader>
              <CardTitle className="bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">인력 현황 상세</CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* 경력 분포 */}
              <div>
                <p className="text-sm font-semibold text-gray-700 mb-3">경력 분포</p>
                <div className="space-y-2">
                  {metrics.employee_distribution.by_experience.map((item, index) => (
                    <div key={item.name} className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">{item.name}</span>
                      <div className="flex items-center gap-2">
                        <div className="w-32 bg-gray-200 rounded-full h-2">
                          <motion.div
                            initial={{ width: 0 }}
                            animate={{ width: `${(item.count / metrics.total_employees) * 100}%` }}
                            transition={{ duration: 1, delay: index * 0.1 }}
                            className="bg-gradient-to-r from-blue-500 to-indigo-500 h-2 rounded-full"
                          />
                        </div>
                        <span className="text-sm font-semibold text-gray-900 w-8 text-right">{item.count}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* 역할별 분포 */}
              <div>
                <p className="text-sm font-semibold text-gray-700 mb-3">역할별 분포</p>
                <div className="flex flex-wrap gap-2">
                  {metrics.employee_distribution.by_role.map((item, index) => (
                    <motion.div
                      key={item.name}
                      initial={{ opacity: 0, scale: 0 }}
                      animate={{ opacity: 1, scale: 1 }}
                      transition={{ delay: index * 0.05 }}
                    >
                      <Badge variant="secondary" className="text-sm">
                        {item.name} ({item.count})
                      </Badge>
                    </motion.div>
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* 프로젝트 현황 */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.6 }}
        >
          <Card className="bg-white/80 backdrop-blur-sm border-0 shadow-lg">
            <CardHeader>
              <CardTitle className="bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent">프로젝트 현황</CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* 상태별 분포 */}
              <div>
                <p className="text-sm font-semibold text-gray-700 mb-3">상태별 분포</p>
                <div className="grid grid-cols-3 gap-2">
                  {metrics.project_distribution.by_status.map((item) => (
                    <motion.div
                      key={item.name}
                      whileHover={{ scale: 1.05 }}
                      className="p-3 bg-gradient-to-br from-gray-50 to-green-50 rounded-lg border border-gray-200 text-center"
                    >
                      <p className="text-xs text-gray-600 mb-1">
                        {item.name === 'planning' ? '기획' : item.name === 'in-progress' ? '진행중' : '완료'}
                      </p>
                      <p className="text-xl font-bold text-gray-900">{item.count}</p>
                    </motion.div>
                  ))}
                </div>
              </div>

              {/* 산업별 분포 */}
              <div>
                <p className="text-sm font-semibold text-gray-700 mb-3">산업별 분포</p>
                <div className="flex flex-wrap gap-2">
                  {metrics.project_distribution.by_industry.slice(0, 6).map((item, index) => (
                    <motion.div
                      key={item.name}
                      initial={{ opacity: 0, scale: 0 }}
                      animate={{ opacity: 1, scale: 1 }}
                      transition={{ delay: index * 0.05 }}
                    >
                      <Badge className="bg-green-100 text-green-700 border-green-200">
                        {item.name} ({item.count})
                      </Badge>
                    </motion.div>
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* 평가 현황 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.7 }}
        >
          <Card className="bg-white/80 backdrop-blur-sm border-0 shadow-lg">
            <CardHeader>
              <CardTitle className="!text-purple-700 font-bold text-lg" style={{ color: '#7c3aed' }}>평가 현황</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* 평가 통계 */}
              <div className="grid grid-cols-2 gap-4">
                <div className="p-4 bg-gradient-to-br from-purple-50 to-pink-50 rounded-xl">
                  <p className="text-xs text-gray-600 mb-1">평균 점수</p>
                  <p className="text-2xl font-bold text-purple-600">{metrics.evaluation_stats.average_score}</p>
                </div>
                <div className="p-4 bg-gradient-to-br from-green-50 to-emerald-50 rounded-xl">
                  <p className="text-xs text-gray-600 mb-1">승인율</p>
                  <p className="text-2xl font-bold text-green-600">{metrics.evaluation_stats.approval_rate}%</p>
                </div>
              </div>

              {/* 상태별 분포 */}
              <div>
                <p className="text-sm font-semibold text-gray-700 mb-3">상태별 분포</p>
                <div className="grid grid-cols-2 gap-2">
                  {metrics.evaluation_stats.by_status.map((item) => {
                    const statusConfig = {
                      pending: { label: '대기중', icon: Clock, color: 'text-yellow-600', bg: 'bg-yellow-50' },
                      approved: { label: '승인', icon: CheckCircle, color: 'text-green-600', bg: 'bg-green-50' },
                      rejected: { label: '반려', icon: XCircle, color: 'text-red-600', bg: 'bg-red-50' },
                      review: { label: '검토중', icon: FileText, color: 'text-blue-600', bg: 'bg-blue-50' }
                    };
                    const config = statusConfig[item.name as keyof typeof statusConfig];
                    const Icon = config?.icon || Clock;
                    
                    return (
                      <motion.div
                        key={item.name}
                        whileHover={{ scale: 1.05 }}
                        className={`p-3 ${config?.bg} rounded-lg border border-gray-200`}
                      >
                        <div className="flex items-center gap-2 mb-1">
                          <Icon className={`w-4 h-4 ${config?.color}`} />
                          <p className="text-xs text-gray-600">{config?.label}</p>
                        </div>
                        <p className={`text-xl font-bold ${config?.color}`}>{item.count}</p>
                      </motion.div>
                    );
                  })}
                </div>
              </div>

              {/* 유형별 분포 */}
              <div>
                <p className="text-sm font-semibold text-gray-700 mb-3">유형별 분포</p>
                <div className="flex gap-2">
                  {metrics.evaluation_stats.by_type.map((item) => (
                    <div key={item.name} className="flex-1 p-3 bg-gray-50 rounded-lg text-center">
                      <p className="text-xs text-gray-600 mb-1">
                        {item.name === 'career' ? '경력직' : '프리랜서'}
                      </p>
                      <p className="text-xl font-bold text-gray-900">{item.count}</p>
                    </div>
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* 대기자명단 상세 & 주요 기술 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.8 }}
          className="space-y-6"
        >
          {/* 대기자명단 상세 */}
          <Card className="bg-white/80 backdrop-blur-sm border-0 shadow-lg">
            <CardHeader>
              <CardTitle className="!text-orange-700 font-bold text-lg" style={{ color: '#c2410c' }}>대기자명단 상세</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="p-4 bg-gradient-to-br from-orange-50 to-red-50 rounded-xl">
                <p className="text-xs text-gray-600 mb-1">평균 대기 기간</p>
                <p className="text-2xl font-bold text-orange-600">{metrics.pending_candidates_detail.average_wait_days}일</p>
              </div>

              <div>
                <p className="text-sm font-semibold text-gray-700 mb-3">대기 기간별 분포</p>
                <div className="space-y-2">
                  {metrics.pending_candidates_detail.by_wait_period.map((item, index) => (
                    <div key={item.name} className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">{item.name}</span>
                      <div className="flex items-center gap-2">
                        <div className="w-24 bg-gray-200 rounded-full h-2">
                          <motion.div
                            initial={{ width: 0 }}
                            animate={{ width: `${(item.count / metrics.pending_candidates_detail.total) * 100}%` }}
                            transition={{ duration: 1, delay: index * 0.1 }}
                            className="bg-gradient-to-r from-orange-500 to-red-500 h-2 rounded-full"
                          />
                        </div>
                        <span className="text-sm font-semibold text-gray-900 w-6 text-right">{item.count}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>

          {/* 주요 기술 스택 */}
          <Card className="bg-white/80 backdrop-blur-sm border-0 shadow-lg">
            <CardHeader>
              <CardTitle className="bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">주요 기술 스택</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {topSkills.map((skill, index) => (
                  <motion.div 
                    key={skill.name}
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.4, delay: index * 0.1 }}
                  >
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-sm font-medium text-gray-900">{skill.name}</span>
                      <div className="flex items-center gap-2">
                        <span className="text-xs text-gray-600">{skill.count}명</span>
                        <span className="text-xs text-gray-500">({skill.percentage}%)</span>
                      </div>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
                      <motion.div
                        initial={{ width: 0 }}
                        animate={{ width: `${skill.percentage}%` }}
                        transition={{ duration: 1, delay: index * 0.1, ease: "easeOut" }}
                        className="bg-gradient-to-r from-blue-600 to-indigo-600 h-2 rounded-full"
                      />
                    </div>
                  </motion.div>
                ))}
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>
    </div>
  );
}
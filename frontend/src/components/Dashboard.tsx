import { Users, Briefcase, TrendingUp, AlertCircle, ArrowUp, ArrowDown, Clock, CheckCircle, XCircle, FileText, Bell, Award, Target, Zap, BookOpen, Activity } from 'lucide-react';
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

      {/* 인력활용도, 기술역량분석, 학력&자격증 - 한 줄로 배치 */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 items-stretch">
        {/* 인력 활용도 */}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.4 }} className="flex">
          <Card className="border-0 shadow-lg h-full w-full flex flex-col" style={{ backgroundColor: '#fed7aa' }}>
            <CardHeader className="flex-shrink-0">
              <CardTitle className="text-orange-900 font-bold text-lg flex items-center gap-2">
                <Activity className="w-5 h-5" />
                인력 활용도
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3 flex-1 flex flex-col justify-between py-4">
              <div className="p-4 bg-white/90 rounded-xl shadow-sm text-center">
                <p className="text-xs text-gray-600 mb-1">배정률</p>
                <p className="text-3xl font-bold text-orange-600">{metrics.utilization.utilization_rate}%</p>
              </div>
              <div className="grid grid-cols-2 gap-2">
                <div className="p-3 bg-white/90 rounded-xl shadow-sm text-center">
                  <p className="text-xs text-gray-600 mb-1">투입 중</p>
                  <p className="text-xl font-bold text-green-600">{metrics.utilization.assigned_count}</p>
                </div>
                <div className="p-3 bg-white/90 rounded-xl shadow-sm text-center">
                  <p className="text-xs text-gray-600 mb-1">대기 중</p>
                  <p className="text-xl font-bold text-gray-700">{metrics.utilization.available_count}</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* 기술 역량 분석 */}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.5 }} className="flex">
          <Card className="border-0 shadow-lg h-full w-full flex flex-col" style={{ backgroundColor: '#e9d5ff' }}>
            <CardHeader className="flex-shrink-0">
              <CardTitle className="text-purple-900 font-bold text-lg flex items-center gap-2">
                <Award className="w-5 h-5" />
                기술 역량 분석
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3 flex-1 flex flex-col justify-center">
              <div className="grid grid-cols-2 gap-3">
                <div className="p-4 bg-white/90 rounded-xl shadow-sm">
                  <p className="text-xs text-gray-700 mb-2 font-medium">다재다능 인력</p>
                  <p className="text-2xl font-bold text-purple-600">{metrics.skill_competency?.multi_skilled_count || 0}명</p>
                  <p className="text-xs text-gray-600 mt-1">5개 이상 기술</p>
                </div>
                <div className="p-4 bg-white/90 rounded-xl shadow-sm">
                  <p className="text-xs text-gray-700 mb-2 font-medium">고유 기술</p>
                  <p className="text-2xl font-bold text-blue-600">{metrics.skill_competency?.total_unique_skills || 0}개</p>
                  <p className="text-xs text-gray-600 mt-1">전체 보유</p>
                </div>
              </div>
              <div className="p-4 bg-white/90 rounded-xl shadow-sm">
                <p className="text-xs text-gray-700 mb-2 font-medium">희소 기술 (3명 이하)</p>
                <div className="flex flex-wrap gap-1.5">
                  {(metrics.skill_competency?.rare_skills || []).slice(0, 4).map((skill, idx) => (
                    <Badge key={idx} className="text-xs bg-purple-200 text-purple-800 border-0">{skill.name} ({skill.count})</Badge>
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* 학력 & 자격증 */}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.6 }} className="flex">
          <Card className="border-0 shadow-lg h-full w-full flex flex-col" style={{ backgroundColor: '#dbeafe' }}>
            <CardHeader className="flex-shrink-0">
              <CardTitle className="text-blue-900 font-bold text-lg flex items-center gap-2">
                <BookOpen className="w-5 h-5" />
                학력 & 자격증
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3 flex-1 flex flex-col justify-between py-4">
              <div className="p-4 bg-white/90 rounded-xl shadow-sm text-center">
                <p className="text-xs text-gray-600 mb-1">평균 자격증 수</p>
                <p className="text-3xl font-bold text-blue-600">{metrics.education_certification.average_certifications}개</p>
              </div>
              <div className="bg-white/90 rounded-xl shadow-sm p-3">
                <p className="text-xs font-semibold text-gray-700 mb-2">학력 분포</p>
                <div className="space-y-1.5">
                  {metrics.education_certification.education_distribution.slice(0, 3).map((item, idx) => (
                    <div key={idx} className="flex items-center justify-between p-2 bg-blue-50 rounded-lg">
                      <span className="text-xs text-gray-700">{item.name}</span>
                      <span className="text-sm font-bold text-blue-700">{item.count}명</span>
                    </div>
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>

      {/* 액션 필요 항목 */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.7 }}
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

      {/* 인력현황상세, 프로젝트현황 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 items-stretch">
        {/* 인력 현황 상세 */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.8 }}
          className="flex"
        >
          <Card className="border-0 shadow-lg h-full w-full flex flex-col" style={{ backgroundColor: '#eff6ff' }}>
            <CardHeader className="flex-shrink-0">
              <CardTitle className="text-blue-900 font-bold text-lg flex items-center gap-2">
                <Users className="w-5 h-5 text-blue-700" />
                인력 현황 상세
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6 flex-1 overflow-auto">
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
          className="flex"
        >
          <Card className="border-0 shadow-lg h-full w-full flex flex-col" style={{ backgroundColor: '#f0fdf4' }}>
            <CardHeader className="flex-shrink-0">
              <CardTitle className="text-green-900 font-bold text-lg flex items-center gap-2">
                <Briefcase className="w-5 h-5 text-green-700" />
                프로젝트 현황
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6 flex-1 overflow-auto">
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

      {/* 평가점수분석, 역량갭분석 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 items-stretch">
        {/* 평가 점수 분석 */}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.9 }} className="flex">
          <Card className="border-0 shadow-lg h-full w-full flex flex-col" style={{ backgroundColor: '#f0fdf4' }}>
            <CardHeader className="flex-shrink-0">
              <CardTitle className="text-green-900 font-bold text-lg flex items-center gap-2">
                <TrendingUp className="w-5 h-5 text-green-700" />
                평가 점수 분석
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4 flex-1 overflow-auto">
              <div className="p-4 bg-gradient-to-br from-green-50 to-emerald-50 rounded-xl">
                <p className="text-xs text-gray-600 mb-1">평균 평가 점수</p>
                <p className="text-3xl font-bold text-green-600">{metrics.evaluation_scores.average_score}점</p>
              </div>
              <div>
                <p className="text-sm font-semibold text-gray-700 mb-2">점수 분포</p>
                <div className="grid grid-cols-2 gap-2">
                  {metrics.evaluation_scores.score_distribution.map((item, idx) => (
                    <div key={idx} className="p-3 bg-gray-50 rounded-lg text-center">
                      <p className="text-xs text-gray-600 mb-1">{item.name}</p>
                      <p className="text-lg font-bold text-gray-900">{item.count}명</p>
                    </div>
                  ))}
                </div>
              </div>
              <div>
                <p className="text-sm font-semibold text-gray-700 mb-2">경력별 평균 점수</p>
                <div className="space-y-2">
                  {metrics.evaluation_scores.score_by_experience.map((item, idx) => (
                    <div key={idx} className="flex items-center justify-between p-2 bg-gradient-to-r from-green-50 to-emerald-50 rounded-lg">
                      <span className="text-sm text-gray-700">{item.name}</span>
                      <span className="text-sm font-semibold text-green-600">{item.avg_score}점</span>
                    </div>
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* 역량 갭 분석 */}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 1.0 }} className="flex">
          <Card className="border-0 shadow-lg h-full w-full flex flex-col" style={{ backgroundColor: '#fef2f2' }}>
            <CardHeader className="flex-shrink-0">
              <CardTitle className="text-red-900 font-bold text-lg flex items-center gap-2">
                <AlertCircle className="w-5 h-5 text-red-700" />
                역량 갭 분석
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4 flex-1 overflow-auto">
              <div className="grid grid-cols-2 gap-4">
                <div className="p-4 bg-gradient-to-br from-red-50 to-orange-50 rounded-xl">
                  <p className="text-xs text-gray-600 mb-1">부족한 기술</p>
                  <p className="text-2xl font-bold text-red-600">{metrics.skill_gaps.total_skill_gaps}개</p>
                </div>
                <div className="p-4 bg-gradient-to-br from-yellow-50 to-orange-50 rounded-xl">
                  <p className="text-xs text-gray-600 mb-1">교육 필요</p>
                  <p className="text-2xl font-bold text-yellow-600">{metrics.skill_gaps.training_needed_count}명</p>
                </div>
              </div>
              <div>
                <p className="text-sm font-semibold text-gray-700 mb-2">부족한 기술 TOP 5</p>
                <div className="space-y-2">
                  {metrics.skill_gaps.top_skill_gaps.slice(0, 5).map((gap, idx) => (
                    <div key={idx} className="p-2 bg-red-50 rounded-lg">
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-sm font-medium text-gray-700">{gap.skill}</span>
                        <Badge variant="destructive" className="text-xs">부족 {gap.gap}</Badge>
                      </div>
                      <div className="flex items-center gap-2 text-xs text-gray-600">
                        <span>수요: {gap.demand}</span>
                        <span>|</span>
                        <span>공급: {gap.supply}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6" style={{ display: 'none' }}>
        {/* 평가 현황 - 숨김 */}
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

      {/* 직원 품질 & 도메인 전문성 분석 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 items-stretch">
        {/* 직원 품질 분석 */}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 1.1 }} className="flex">
          <Card className="border-0 shadow-lg h-full w-full flex flex-col" style={{ backgroundColor: '#eef2ff' }}>
            <CardHeader className="flex-shrink-0">
              <CardTitle className="text-indigo-900 font-bold text-lg flex items-center gap-2">
                <Award className="w-5 h-5 text-indigo-700" />
                직원 품질 분석
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4 flex-1 overflow-auto">
              <div className="grid grid-cols-2 gap-4">
                <div className="p-4 bg-gradient-to-br from-indigo-50 to-purple-50 rounded-xl">
                  <p className="text-xs text-gray-600 mb-1">고급 기술 보유</p>
                  <p className="text-2xl font-bold text-indigo-600">{metrics.employee_quality.advanced_tech_count}명</p>
                  <p className="text-xs text-gray-500 mt-1">{metrics.employee_quality.advanced_tech_ratio}%</p>
                </div>
                <div className="p-4 bg-gradient-to-br from-green-50 to-emerald-50 rounded-xl">
                  <p className="text-xs text-gray-600 mb-1">성과 기록</p>
                  <p className="text-2xl font-bold text-green-600">{metrics.employee_quality.performance_record_count}명</p>
                  <p className="text-xs text-gray-500 mt-1">{metrics.employee_quality.performance_ratio}%</p>
                </div>
              </div>
              <div>
                <p className="text-sm font-semibold text-gray-700 mb-2">역량 레벨 분포</p>
                <div className="space-y-2">
                  {metrics.employee_quality.skill_level_distribution.map((item, idx) => (
                    <div key={idx} className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">{item.name}</span>
                      <div className="flex items-center gap-2">
                        <div className="w-24 bg-gray-200 rounded-full h-2">
                          <motion.div initial={{ width: 0 }} animate={{ width: `${(item.count / 1500) * 100}%` }} transition={{ duration: 1, delay: idx * 0.1 }} className="bg-gradient-to-r from-indigo-500 to-purple-500 h-2 rounded-full" />
                        </div>
                        <span className="text-sm font-semibold text-gray-900 w-10 text-right">{item.count}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
              <div className="p-4 bg-gradient-to-r from-purple-50 to-pink-50 rounded-xl">
                <p className="text-xs text-gray-600 mb-1">다중 역할 경험자</p>
                <p className="text-xl font-bold text-purple-600">{metrics.employee_quality.multi_role_count}명</p>
                <p className="text-xs text-gray-500 mt-1">3개 이상 역할 경험</p>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* 도메인 전문성 분석 */}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 1.2 }} className="flex">
          <Card className="border-0 shadow-lg h-full w-full flex flex-col" style={{ backgroundColor: '#ecfeff' }}>
            <CardHeader className="flex-shrink-0">
              <CardTitle className="text-cyan-900 font-bold text-lg flex items-center gap-2">
                <Target className="w-5 h-5 text-cyan-700" />
                도메인 전문성
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4 flex-1 overflow-auto">
              <div className="grid grid-cols-2 gap-4">
                <div className="p-4 bg-gradient-to-br from-blue-50 to-cyan-50 rounded-xl">
                  <p className="text-xs text-gray-600 mb-1">다중 도메인 전문가</p>
                  <p className="text-2xl font-bold text-blue-600">{metrics.domain_expertise.multi_domain_experts}명</p>
                  <p className="text-xs text-gray-500 mt-1">2개 이상 도메인</p>
                </div>
                <div className="p-4 bg-gradient-to-br from-green-50 to-teal-50 rounded-xl">
                  <p className="text-xs text-gray-600 mb-1">평균 도메인 경력</p>
                  <p className="text-2xl font-bold text-green-600">{metrics.domain_expertise.average_domain_years}년</p>
                </div>
              </div>
              <div>
                <p className="text-sm font-semibold text-gray-700 mb-2">주요 도메인 TOP 5</p>
                <div className="space-y-2">
                  {metrics.domain_expertise.top_domains.map((domain, idx) => (
                    <div key={idx} className="flex items-center justify-between p-2 bg-gradient-to-r from-blue-50 to-cyan-50 rounded-lg">
                      <span className="text-sm text-gray-700">{domain.name}</span>
                      <span className="text-sm font-semibold text-blue-600">{domain.count}명</span>
                    </div>
                  ))}
                </div>
              </div>
              <div className="p-4 bg-gradient-to-r from-indigo-50 to-blue-50 rounded-xl">
                <p className="text-xs text-gray-600 mb-1">전체 도메인 수</p>
                <p className="text-xl font-bold text-indigo-600">{metrics.domain_expertise.total_domains}개</p>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>
    </div>
  );
}
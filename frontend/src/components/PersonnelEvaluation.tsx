import { useState } from 'react';
import { Upload, CheckCircle, AlertTriangle, XCircle, FileText, Search } from 'lucide-react';
import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Button } from './ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { api } from '../config/api';

interface Evaluation {
  id: string;
  name: string;
  type: 'career' | 'freelancer';
  status: 'pending' | 'approved' | 'rejected';
  overallScore: number;
  submittedAt: string;
  evaluations: {
    category: string;
    score: number;
    maxScore: number;
    feedback: string;
  }[];
  projects: {
    name: string;
    role: string;
    period: string;
    verified: boolean;
  }[];
  recommendations: string[];
}

export function PersonnelEvaluation() {
  console.log('PersonnelEvaluation 컴포넌트 렌더링됨');
  
  const [selectedTab, setSelectedTab] = useState('pending');
  const [userId, setUserId] = useState('U_003');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [quantitativeData, setQuantitativeData] = useState<any>(null);
  const [qualitativeData, setQualitativeData] = useState<any>(null);
  
  console.log('현재 상태:', { userId, loading, error, hasQuantitativeData: !!quantitativeData });

  const handleAnalyze = async () => {
    console.log('handleAnalyze 호출됨! userId:', userId);
    setLoading(true);
    setError(null);
    try {
      console.log('API 호출 시작...');
      const [quantitative, qualitative] = await Promise.all([
        api.quantitativeAnalysis({ user_id: userId }),
        api.qualitativeAnalysis({ user_id: userId }),
      ]);
      console.log('API 호출 성공!', quantitative, qualitative);
      setQuantitativeData(quantitative);
      setQualitativeData(qualitative);
    } catch (err) {
      console.error('API 호출 실패:', err);
      setError(err instanceof Error ? err.message : '분석 실패');
    } finally {
      setLoading(false);
    }
  };

  // 하드코딩 데이터 제거 - 실제 데이터는 API에서 가져옴
  const evaluations: Evaluation[] = [];

  const filteredEvaluations = evaluations.filter((evaluation) => {
    if (selectedTab === 'pending') return evaluation.status === 'pending';
    if (selectedTab === 'approved') return evaluation.status === 'approved';
    if (selectedTab === 'rejected') return evaluation.status === 'rejected';
    return true;
  });

  const getScoreColor = (score: number) => {
    if (score >= 85) return 'text-green-600';
    if (score >= 70) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreBgColor = (score: number) => {
    if (score >= 85) return 'bg-green-100';
    if (score >= 70) return 'bg-yellow-100';
    return 'bg-red-100';
  };

  return (
    <div className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-center justify-between"
      >
        <div>
          <h2 className="text-gray-900 mb-2 bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">인력 평가</h2>
          <p className="text-gray-600">신규 경력직 및 프리랜서의 이력을 검증하고 평가합니다</p>
        </div>
        <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
          <Button className="gap-2 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 shadow-lg shadow-blue-500/30">
            <Upload className="w-4 h-4" />
            이력서 업로드
          </Button>
        </motion.div>
      </motion.div>

      {/* API Analysis Section */}
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 0.1 }}
      >
        <Card className="bg-white/80 backdrop-blur-sm border-0 shadow-lg overflow-hidden">
          <div className="absolute top-0 right-0 w-64 h-64 bg-gradient-to-br from-blue-500/10 to-indigo-500/10 rounded-full blur-3xl pointer-events-none" />
          <CardHeader>
            <CardTitle>실시간 인력 분석</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex gap-4 mb-6">
              <input
                type="text"
                value={userId}
                onChange={(e) => {
                  console.log('Input 변경:', e.target.value);
                  setUserId(e.target.value);
                }}
                placeholder="직원 ID (예: U_003)"
                className="flex-1 px-4 py-2 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <button 
                onClick={(e) => {
                  console.log('버튼 클릭됨!', e);
                  handleAnalyze();
                }}
                disabled={loading}
                className="gap-2 px-4 py-2 rounded-xl text-white bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 disabled:opacity-50 flex items-center"
              >
                <Search className="w-4 h-4" />
                {loading ? '분석 중...' : '분석하기'}
              </button>
            </div>

            {error && (
              <div className="p-4 bg-red-50 border border-red-200 rounded-xl text-red-700 mb-4">
                {error}
              </div>
            )}

            {quantitativeData && (
              <div className="space-y-4">
                <div className="p-4 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl border border-blue-100">
                  <h3 className="text-lg font-semibold text-blue-900 mb-3">정량적 분석 결과</h3>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div className="text-center">
                      <p className="text-2xl font-bold text-blue-600">{quantitativeData.overall_score.toFixed(1)}</p>
                      <p className="text-sm text-gray-600">종합 점수</p>
                    </div>
                    <div className="text-center">
                      <p className="text-2xl font-bold text-blue-600">{quantitativeData.experience_metrics.years_of_experience}</p>
                      <p className="text-sm text-gray-600">경력 (년)</p>
                    </div>
                    <div className="text-center">
                      <p className="text-2xl font-bold text-blue-600">{quantitativeData.experience_metrics.project_count}</p>
                      <p className="text-sm text-gray-600">프로젝트 수</p>
                    </div>
                    <div className="text-center">
                      <p className="text-2xl font-bold text-blue-600">{quantitativeData.experience_metrics.skill_diversity}</p>
                      <p className="text-sm text-gray-600">기술 다양성</p>
                    </div>
                  </div>
                </div>

                {qualitativeData && qualitativeData.suspicious_flags.length > 0 && (
                  <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-xl">
                    <h3 className="text-lg font-semibold text-yellow-900 mb-2">주의사항</h3>
                    <ul className="space-y-1">
                      {qualitativeData.suspicious_flags.map((flag: any, idx: number) => (
                        <li key={idx} className="text-sm text-yellow-800 flex items-start gap-2">
                          <AlertTriangle className="w-4 h-4 mt-0.5 flex-shrink-0" />
                          <span>{flag.description}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}

            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="mt-4 p-4 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl border border-blue-100"
            >
              <p className="text-sm text-blue-900 mb-2">AI 분석 항목</p>
              <ul className="text-sm text-blue-700 space-y-1">
                <li>• 기술 스택 및 숙련도 평가</li>
                <li>• 프로젝트 경험 유사도 분석</li>
                <li>• 경력 이력 진위 여부 검증</li>
                <li>• 시장 평균 대비 역량 비교</li>
              </ul>
            </motion.div>
          </CardContent>
        </Card>
      </motion.div>

      {/* Evaluation List */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
      >
        <Card className="bg-white/80 backdrop-blur-sm border-0 shadow-lg">
          <CardHeader>
            <CardTitle>평가 현황</CardTitle>
          </CardHeader>
          <CardContent>
            <Tabs value={selectedTab} onValueChange={setSelectedTab}>
              <TabsList className="grid w-full grid-cols-3">
                <TabsTrigger value="pending">
                  검토 대기 ({evaluations.filter((e) => e.status === 'pending').length})
                </TabsTrigger>
                <TabsTrigger value="approved">
                  승인됨 ({evaluations.filter((e) => e.status === 'approved').length})
                </TabsTrigger>
                <TabsTrigger value="rejected">
                  반려됨 ({evaluations.filter((e) => e.status === 'rejected').length})
                </TabsTrigger>
              </TabsList>

              <TabsContent value={selectedTab} className="mt-6">
                <div className="space-y-6">
                  {filteredEvaluations.map((evaluation, index) => (
                    <motion.div
                      key={evaluation.id}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: index * 0.1 }}
                      whileHover={{ scale: 1.01 }}
                    >
                      <Card className="border-2 bg-white/50 backdrop-blur-sm overflow-hidden">
                        <div className="absolute top-0 right-0 w-48 h-48 bg-gradient-to-br from-blue-500/5 to-indigo-500/5 rounded-full blur-2xl pointer-events-none" />
                        <CardHeader>
                          <div className="flex items-start justify-between">
                            <div>
                              <div className="flex items-center gap-3 mb-2">
                                <CardTitle>{evaluation.name}</CardTitle>
                                <Badge
                                  variant={evaluation.type === 'career' ? 'default' : 'secondary'}
                                  className={
                                    evaluation.type === 'career'
                                      ? 'bg-gradient-to-r from-blue-600 to-indigo-600'
                                      : ''
                                  }
                                >
                                  {evaluation.type === 'career' ? '경력직' : '프리랜서'}
                                </Badge>
                              </div>
                              <p className="text-sm text-gray-600">제출일: {evaluation.submittedAt}</p>
                            </div>
                            <motion.div
                              initial={{ scale: 0 }}
                              animate={{ scale: 1 }}
                              transition={{ delay: index * 0.1 + 0.2 }}
                              className="text-right"
                            >
                              <p className="text-sm text-gray-600 mb-1">종합 점수</p>
                              <div className="flex items-center gap-2">
                                <span className={`text-2xl ${getScoreColor(evaluation.overallScore)}`}>
                                  {evaluation.overallScore}
                                </span>
                                <span className="text-gray-600">/100</span>
                              </div>
                            </motion.div>
                          </div>
                        </CardHeader>
                        <CardContent>
                          <div className="space-y-6">
                            {/* Evaluation Scores */}
                            <div>
                              <p className="text-gray-900 mb-3">평가 항목</p>
                              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                {evaluation.evaluations.map((item, idx) => (
                                  <motion.div
                                    key={idx}
                                    initial={{ opacity: 0, x: -20 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    transition={{ delay: index * 0.1 + idx * 0.05 }}
                                    whileHover={{ scale: 1.02 }}
                                    className="p-4 bg-gradient-to-br from-gray-50 to-blue-50/30 rounded-xl border border-gray-100"
                                  >
                                    <div className="flex items-center justify-between mb-2">
                                      <span className="text-gray-900">{item.category}</span>
                                      <span className={`${getScoreColor(item.score)}`}>
                                        {item.score}/{item.maxScore}
                                      </span>
                                    </div>
                                    <div className="w-full bg-gray-200 rounded-full h-2 mb-2 overflow-hidden">
                                      <motion.div
                                        initial={{ width: 0 }}
                                        animate={{ width: `${item.score}%` }}
                                        transition={{ duration: 1, delay: index * 0.1 + idx * 0.05, ease: 'easeOut' }}
                                        className={`h-2 rounded-full ${
                                          item.score >= 85
                                            ? 'bg-gradient-to-r from-green-500 to-emerald-500'
                                            : item.score >= 70
                                            ? 'bg-gradient-to-r from-yellow-500 to-orange-500'
                                            : 'bg-gradient-to-r from-red-500 to-red-600'
                                        }`}
                                      />
                                    </div>
                                    <p className="text-xs text-gray-600">{item.feedback}</p>
                                  </motion.div>
                                ))}
                              </div>
                            </div>

                            {/* Project History */}
                            <div>
                              <p className="text-gray-900 mb-3">프로젝트 이력</p>
                              <div className="space-y-2">
                                {evaluation.projects.map((project, idx) => (
                                  <motion.div
                                    key={idx}
                                    initial={{ opacity: 0, x: -20 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    transition={{ delay: index * 0.1 + idx * 0.05 }}
                                    whileHover={{ x: 4 }}
                                    className="p-3 border border-gray-200 rounded-xl bg-white/50"
                                  >
                                    <div className="flex items-start justify-between">
                                      <div className="flex-1">
                                        <div className="flex items-center gap-2 mb-1">
                                          <p className="text-gray-900">{project.name}</p>
                                          {project.verified ? (
                                            <CheckCircle className="w-4 h-4 text-green-600" />
                                          ) : (
                                            <AlertTriangle className="w-4 h-4 text-yellow-600" />
                                          )}
                                        </div>
                                        <p className="text-sm text-gray-600">
                                          {project.role} · {project.period}
                                        </p>
                                      </div>
                                      <Badge
                                        variant={project.verified ? 'default' : 'secondary'}
                                        className={
                                          project.verified
                                            ? 'bg-gradient-to-r from-green-500 to-emerald-500'
                                            : ''
                                        }
                                      >
                                        {project.verified ? '검증됨' : '확인 중'}
                                      </Badge>
                                    </div>
                                  </motion.div>
                                ))}
                              </div>
                            </div>

                            {/* Recommendations */}
                            <div>
                              <p className="text-gray-900 mb-3">AI 추천 의견</p>
                              <div className="p-4 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl border border-blue-100">
                                <ul className="space-y-2">
                                  {evaluation.recommendations.map((rec, idx) => (
                                    <motion.li
                                      key={idx}
                                      initial={{ opacity: 0, x: -20 }}
                                      animate={{ opacity: 1, x: 0 }}
                                      transition={{ delay: index * 0.1 + idx * 0.1 }}
                                      className="text-sm text-blue-900 flex items-start gap-2"
                                    >
                                      <span className="text-blue-600 mt-1">•</span>
                                      <span>{rec}</span>
                                    </motion.li>
                                  ))}
                                </ul>
                              </div>
                            </div>

                            {/* Actions */}
                            {evaluation.status === 'pending' && (
                              <div className="flex gap-2 pt-4 border-t border-gray-200">
                                <motion.div className="flex-1" whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
                                  <Button className="w-full gap-2 bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700">
                                    <CheckCircle className="w-4 h-4" />
                                    승인
                                  </Button>
                                </motion.div>
                                <motion.div whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
                                  <Button variant="outline" className="gap-2">
                                    <FileText className="w-4 h-4" />
                                    추가 검토
                                  </Button>
                                </motion.div>
                                <motion.div whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
                                  <Button variant="destructive" className="gap-2">
                                    <XCircle className="w-4 h-4" />
                                    반려
                                  </Button>
                                </motion.div>
                              </div>
                            )}
                          </div>
                        </CardContent>
                      </Card>
                    </motion.div>
                  ))}
                </div>
              </TabsContent>
            </Tabs>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
}
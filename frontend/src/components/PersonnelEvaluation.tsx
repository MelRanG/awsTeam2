import { useState } from 'react';
import { Upload, CheckCircle, AlertTriangle, XCircle, FileText } from 'lucide-react';
import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Button } from './ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';

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
  const [selectedTab, setSelectedTab] = useState('pending');

  const evaluations: Evaluation[] = [
    {
      id: '1',
      name: '홍길동',
      type: 'career',
      status: 'pending',
      overallScore: 85,
      submittedAt: '2024.11.10',
      evaluations: [
        {
          category: '기술 역량',
          score: 90,
          maxScore: 100,
          feedback: '요구 기술 스택 대부분 보유. React, Node.js 숙련도 우수',
        },
        {
          category: '프로젝트 경험',
          score: 85,
          maxScore: 100,
          feedback: '유사 프로젝트 3건 수행. 금융 도메인 경험 풍부',
        },
        {
          category: '이력 신뢰도',
          score: 80,
          maxScore: 100,
          feedback: '대부분의 경력 검증 완료. 일부 프로젝트 추가 확인 필요',
        },
        {
          category: '문화 적합성',
          score: 85,
          maxScore: 100,
          feedback: '협업 능력 우수. 이전 직장 평판 양호',
        },
      ],
      projects: [
        {
          name: 'A은행 인터넷뱅킹 개편',
          role: 'Senior Developer',
          period: '2022.01 - 2023.12',
          verified: true,
        },
        {
          name: 'B증권 HTS 개발',
          role: 'Tech Lead',
          period: '2020.06 - 2021.12',
          verified: true,
        },
        {
          name: 'C카드 결제 시스템',
          role: 'Backend Developer',
          period: '2018.03 - 2020.05',
          verified: false,
        },
      ],
      recommendations: [
        '금융 프로젝트에 즉시 투입 가능',
        'Tech Lead 역할 수행 경험으로 팀 리더십 기대',
        '일부 프로젝트 이력 추가 검증 후 최종 승인 권장',
      ],
    },
    {
      id: '2',
      name: '김미영',
      type: 'freelancer',
      status: 'pending',
      overallScore: 78,
      submittedAt: '2024.11.09',
      evaluations: [
        {
          category: '기술 역량',
          score: 85,
          maxScore: 100,
          feedback: 'React Native 전문가. 모바일 앱 개발 경험 풍부',
        },
        {
          category: '프로젝트 경험',
          score: 75,
          maxScore: 100,
          feedback: '프리랜서로 다양한 프로젝트 수행. 장기 프로젝트 경험 부족',
        },
        {
          category: '이력 신뢰도',
          score: 70,
          maxScore: 100,
          feedback: '일부 프로젝트 검증 어려움. 레퍼런스 추가 확보 필요',
        },
        {
          category: '커뮤니케이션',
          score: 85,
          maxScore: 100,
          feedback: '원활한 소통 능력. 리모트 작업 경험 우수',
        },
      ],
      projects: [
        {
          name: '헬스케어 앱 개발',
          role: 'Frontend Developer',
          period: '2024.06 - 2024.09',
          verified: true,
        },
        {
          name: '배달 플랫폼 리뉴얼',
          role: 'React Native Developer',
          period: '2024.01 - 2024.05',
          verified: false,
        },
      ],
      recommendations: [
        '단기 프로젝트 투입 적합',
        '장기 프로젝트는 초기 성과 확인 후 결정',
        '레퍼런스 체크 추가 필요',
      ],
    },
    {
      id: '3',
      name: '박준호',
      type: 'career',
      status: 'approved',
      overallScore: 92,
      submittedAt: '2024.11.05',
      evaluations: [
        {
          category: '기술 역량',
          score: 95,
          maxScore: 100,
          feedback: '풀스택 개발 능력 우수. 최신 기술 트렌드 파악',
        },
        {
          category: '프로젝트 경험',
          score: 90,
          maxScore: 100,
          feedback: '대규모 프로젝트 다수 경험. 리더십 검증됨',
        },
        {
          category: '이력 신뢰도',
          score: 95,
          maxScore: 100,
          feedback: '모든 경력 검증 완료. 레퍼런스 매우 긍정적',
        },
        {
          category: '문화 적합성',
          score: 90,
          maxScore: 100,
          feedback: '팀워크 우수. 멘토링 능력 보유',
        },
      ],
      projects: [
        {
          name: 'D커머스 플랫폼 구축',
          role: 'Tech Lead',
          period: '2021.01 - 2023.12',
          verified: true,
        },
        {
          name: 'E물류 시스템 개발',
          role: 'Senior Developer',
          period: '2019.03 - 2020.12',
          verified: true,
        },
      ],
      recommendations: [
        '즉시 투입 승인',
        '핵심 프로젝트 Tech Lead 역할 추천',
        '신규 팀원 멘토링 가능',
      ],
    },
  ];

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

      {/* Upload Section */}
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 0.1 }}
      >
        <Card className="bg-white/80 backdrop-blur-sm border-0 shadow-lg overflow-hidden">
          <div className="absolute top-0 right-0 w-64 h-64 bg-gradient-to-br from-blue-500/10 to-indigo-500/10 rounded-full blur-3xl" />
          <CardHeader>
            <CardTitle>AI 기반 이력 분석</CardTitle>
          </CardHeader>
          <CardContent>
            <motion.div
              whileHover={{ scale: 1.01, borderColor: 'rgb(59, 130, 246)' }}
              className="border-2 border-dashed border-gray-300 rounded-xl p-8 text-center transition-colors cursor-pointer relative overflow-hidden"
            >
              <motion.div
                animate={{ y: [0, -10, 0] }}
                transition={{ duration: 2, repeat: Infinity }}
              >
                <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              </motion.div>
              <p className="text-gray-900 mb-2">이력서를 드래그하거나 클릭하여 업로드</p>
              <p className="text-sm text-gray-600">PDF, DOC, DOCX 파일 지원</p>
            </motion.div>
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
                        <div className="absolute top-0 right-0 w-48 h-48 bg-gradient-to-br from-blue-500/5 to-indigo-500/5 rounded-full blur-2xl" />
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
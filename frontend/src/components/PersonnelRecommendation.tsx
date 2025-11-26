import { useState } from 'react';
import { Sparkles, TrendingUp, Users, CheckCircle } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Button } from './ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';

interface Recommendation {
  id: string;
  name: string;
  position: string;
  matchRate: number;
  skills: string[];
  experience: number;
  reasons: string[];
  affinityScore: number;
}

export function PersonnelRecommendation() {
  const [selectedProject, setSelectedProject] = useState('project-1');
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const projects = [
    { id: 'project-1', name: '헬스케어 앱 개발' },
    { id: 'project-2', name: '스마트팩토리 시스템' },
    { id: 'project-3', name: '금융 플랫폼 구축' },
  ];

  const recommendations: Recommendation[] = [
    {
      id: '1',
      name: '이영희',
      position: 'Tech Lead',
      matchRate: 95,
      skills: ['React Native', 'Node.js', 'Firebase', 'GraphQL'],
      experience: 12,
      reasons: [
        '요구 기술 스택 100% 보유',
        '유사 프로젝트 5건 경험',
        '팀원과의 협업 경험 우수 (친밀도 92%)',
      ],
      affinityScore: 92,
    },
    {
      id: '2',
      name: '강동원',
      position: 'Backend Developer',
      matchRate: 88,
      skills: ['Node.js', 'GraphQL', 'PostgreSQL', 'Redis'],
      experience: 7,
      reasons: [
        'Backend 기술 전문성 우수',
        '헬스케어 도메인 경험 2건',
        '이영희와 과거 협업 이력',
      ],
      affinityScore: 88,
    },
    {
      id: '3',
      name: '정수진',
      position: 'Frontend Developer',
      matchRate: 85,
      skills: ['React Native', 'TypeScript', 'Redux', 'Jest'],
      experience: 4,
      reasons: [
        'React Native 전문 개발자',
        '모바일 앱 개발 경험 3건',
        '빠른 러닝커브',
      ],
      affinityScore: 75,
    },
    {
      id: '4',
      name: '최민수',
      position: 'Data Engineer',
      matchRate: 78,
      skills: ['Python', 'Firebase', 'Data Pipeline', 'AWS'],
      experience: 5,
      reasons: [
        'Firebase 실시간 데이터 처리 경험',
        '헬스케어 데이터 분석 경험',
        '새로운 기술 습득 능력 우수',
      ],
      affinityScore: 70,
    },
  ];

  const handleAnalyze = () => {
    setIsAnalyzing(true);
    setTimeout(() => {
      setIsAnalyzing(false);
    }, 2000);
  };

  return (
    <div className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h2 className="text-gray-900 mb-2 bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">인력 추천</h2>
        <p className="text-gray-600">AI가 프로젝트에 최적화된 인력을 추천합니다</p>
      </motion.div>

      {/* Project Selection */}
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 0.1 }}
      >
        <Card className="bg-white/80 backdrop-blur-sm border-0 shadow-lg overflow-hidden">
          <div className="absolute top-0 right-0 w-64 h-64 bg-gradient-to-br from-blue-500/10 to-indigo-500/10 rounded-full blur-3xl" />
          <CardHeader>
            <CardTitle className="flex items-center gap-2 relative">
              <motion.div
                animate={{ rotate: [0, 360] }}
                transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
              >
                <Sparkles className="w-5 h-5 text-blue-600" />
              </motion.div>
              프로젝트 선택 및 AI 분석
            </CardTitle>
          </CardHeader>
          <CardContent className="relative">
            <div className="flex gap-4">
              <div className="flex-1">
                <Select value={selectedProject} onValueChange={setSelectedProject}>
                  <SelectTrigger>
                    <SelectValue placeholder="프로젝트 선택" />
                  </SelectTrigger>
                  <SelectContent>
                    {projects.map((project) => (
                      <SelectItem key={project.id} value={project.id}>
                        {project.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                <Button 
                  onClick={handleAnalyze} 
                  disabled={isAnalyzing} 
                  className="gap-2 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 shadow-lg shadow-blue-500/30"
                >
                  {isAnalyzing ? (
                    <>
                      <motion.div 
                        animate={{ rotate: 360 }}
                        transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                        className="w-4 h-4 border-2 border-white border-t-transparent rounded-full"
                      />
                      분석 중...
                    </>
                  ) : (
                    <>
                      <Sparkles className="w-4 h-4" />
                      AI 분석 시작
                    </>
                  )}
                </Button>
              </motion.div>
            </div>

            <motion.div 
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="mt-4 p-4 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl border border-blue-100"
            >
              <p className="text-sm text-blue-900 mb-2">분석 기준</p>
              <ul className="text-sm text-blue-700 space-y-1">
                <li>• 기술 스택 매칭률 (40%)</li>
                <li>• 프로젝트 참여 이력 유사도 (30%)</li>
                <li>• 팀원 간 친밀도 및 협업 경험 (20%)</li>
                <li>• 현재 가용성 및 투입 가능 시기 (10%)</li>
              </ul>
            </motion.div>
          </CardContent>
        </Card>
      </motion.div>

      {/* Analysis Results */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-gray-900">추천 결과</h3>
          <span className="text-sm text-gray-600">{recommendations.length}명의 후보</span>
        </div>

        <div className="space-y-4">
          <AnimatePresence>
            {recommendations.map((rec, index) => (
              <motion.div
                key={rec.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.4, delay: index * 0.1 }}
                whileHover={{ scale: 1.02, y: -2 }}
              >
                <Card className="bg-white/80 backdrop-blur-sm border-0 shadow-lg hover:shadow-xl transition-all overflow-hidden">
                  <div className="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br from-blue-500/10 to-purple-500/10 rounded-full blur-2xl" />
                  <CardContent className="p-6 relative">
                    <div className="flex items-start justify-between mb-4">
                      <div className="flex items-center gap-4">
                        <motion.div 
                          whileHover={{ rotate: 360 }}
                          transition={{ duration: 0.6 }}
                          className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center shadow-lg"
                        >
                          <span className="text-white">#{index + 1}</span>
                        </motion.div>
                        <div>
                          <div className="flex items-center gap-2 mb-1">
                            <p className="text-gray-900">{rec.name}</p>
                            <Badge variant="secondary" className="bg-blue-50 text-blue-700">{rec.position}</Badge>
                          </div>
                          <p className="text-sm text-gray-600">경력 {rec.experience}년</p>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="flex items-center gap-2 mb-1">
                          <TrendingUp className="w-4 h-4 text-blue-600" />
                          <span className="text-blue-600">매칭률</span>
                        </div>
                        <motion.p 
                          initial={{ scale: 0 }}
                          animate={{ scale: 1 }}
                          transition={{ duration: 0.5, delay: index * 0.1 + 0.3 }}
                          className="text-gray-900"
                        >
                          {rec.matchRate}%
                        </motion.p>
                      </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-4">
                      <div>
                        <div className="flex items-center gap-2 text-gray-600 mb-2">
                          <CheckCircle className="w-4 h-4" />
                          <span className="text-sm">보유 기술</span>
                        </div>
                        <div className="flex flex-wrap gap-2">
                          {rec.skills.map((skill, idx) => (
                            <motion.div
                              key={skill}
                              initial={{ opacity: 0, scale: 0 }}
                              animate={{ opacity: 1, scale: 1 }}
                              transition={{ delay: index * 0.1 + idx * 0.05 }}
                            >
                              <Badge className="bg-gradient-to-r from-blue-600 to-indigo-600">{skill}</Badge>
                            </motion.div>
                          ))}
                        </div>
                      </div>

                      <div>
                        <div className="flex items-center gap-2 text-gray-600 mb-2">
                          <Users className="w-4 h-4" />
                          <span className="text-sm">팀 친밀도</span>
                        </div>
                        <div className="flex items-center gap-3">
                          <div className="flex-1 bg-gray-200 rounded-full h-2 overflow-hidden">
                            <motion.div
                              initial={{ width: 0 }}
                              animate={{ width: `${rec.affinityScore}%` }}
                              transition={{ duration: 1, delay: index * 0.1, ease: "easeOut" }}
                              className="bg-gradient-to-r from-green-500 to-emerald-500 h-2 rounded-full"
                            />
                          </div>
                          <span className="text-sm text-gray-900">{rec.affinityScore}%</span>
                        </div>
                      </div>
                    </div>

                    <div className="pt-4 border-t border-gray-200">
                      <p className="text-sm text-gray-600 mb-2">추천 이유</p>
                      <ul className="space-y-1">
                        {rec.reasons.map((reason, idx) => (
                          <motion.li 
                            key={idx}
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: index * 0.1 + idx * 0.1 }}
                            className="text-sm text-gray-700 flex items-start gap-2"
                          >
                            <span className="text-blue-600 mt-1">•</span>
                            <span>{reason}</span>
                          </motion.li>
                        ))}
                      </ul>
                    </div>

                    <div className="mt-4 flex gap-2">
                      <motion.div className="flex-1" whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
                        <Button size="sm" className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700">
                          프로젝트에 투입
                        </Button>
                      </motion.div>
                      <motion.div whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
                        <Button size="sm" variant="outline">
                          상세 정보
                        </Button>
                      </motion.div>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </AnimatePresence>
        </div>
      </div>
    </div>
  );
}
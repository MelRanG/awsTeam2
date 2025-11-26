import { useState } from 'react';
import { TrendingUp, Users, Lightbulb, ArrowRight } from 'lucide-react';
import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Button } from './ui/button';

interface DomainInsight {
  id: string;
  domain: string;
  confidence: number;
  potentialProjects: number;
  requiredSkills: string[];
  availableExperts: number;
  insights: string[];
  marketDemand: 'high' | 'medium' | 'low';
}

interface TeamSuggestion {
  role: string;
  requiredCount: number;
  suggestedPersonnel: string[];
  skills: string[];
}

export function DomainAnalysis() {
  const [selectedDomain, setSelectedDomain] = useState<string | null>(null);

  const domainInsights: DomainInsight[] = [
    {
      id: '1',
      domain: 'AI/머신러닝',
      confidence: 92,
      potentialProjects: 8,
      requiredSkills: ['Python', 'TensorFlow', 'PyTorch', 'NLP', 'Computer Vision'],
      availableExperts: 12,
      insights: [
        '최근 3년간 AI 관련 프로젝트 경험자 12명 확보',
        '대형 AI 프로젝트 2건 성공적 완료',
        '시장 수요 급증 추세 (전년 대비 150%)',
        '기존 인력의 40%가 AI 관련 기술 보유',
      ],
      marketDemand: 'high',
    },
    {
      id: '2',
      domain: '블록체인',
      confidence: 78,
      potentialProjects: 4,
      requiredSkills: ['Solidity', 'Web3.js', 'Ethereum', 'Smart Contract', 'DeFi'],
      availableExperts: 5,
      insights: [
        '블록체인 관련 프로젝트 경험자 5명',
        '금융 도메인 전문가 다수 보유로 진입 용이',
        'Web3 기술 트렌드 선점 기회',
        '추가 교육으로 10명 이상 확보 가능',
      ],
      marketDemand: 'medium',
    },
    {
      id: '3',
      domain: 'IoT/스마트팩토리',
      confidence: 85,
      potentialProjects: 6,
      requiredSkills: ['IoT', 'MQTT', 'Edge Computing', 'Time Series DB', 'Python'],
      availableExperts: 8,
      insights: [
        '제조업 프로젝트 경험 풍부',
        'IoT 플랫폼 구축 경험 3건',
        '정부 지원 사업 확대로 시장 성장',
        '기존 인프라팀 역량 활용 가능',
      ],
      marketDemand: 'high',
    },
    {
      id: '4',
      domain: '헬스테크',
      confidence: 72,
      potentialProjects: 5,
      requiredSkills: ['FHIR', 'HL7', 'Medical Data', 'React Native', 'HIPAA Compliance'],
      availableExperts: 4,
      insights: [
        '헬스케어 관련 프로젝트 2건 수행',
        '데이터 보안 전문 인력 확보',
        '고령화 사회 진입으로 시장 확대',
        '의료 도메인 전문가 영입 필요',
      ],
      marketDemand: 'high',
    },
  ];

  const teamSuggestions: TeamSuggestion[] = [
    {
      role: 'AI/ML Engineer',
      requiredCount: 3,
      suggestedPersonnel: ['최민수', '박지영', '김태현'],
      skills: ['Python', 'TensorFlow', 'PyTorch'],
    },
    {
      role: 'Backend Developer',
      requiredCount: 2,
      suggestedPersonnel: ['강동원', '이영희'],
      skills: ['Python', 'FastAPI', 'PostgreSQL'],
    },
    {
      role: 'Frontend Developer',
      requiredCount: 2,
      suggestedPersonnel: ['정수진', '김철수'],
      skills: ['React', 'TypeScript', 'D3.js'],
    },
    {
      role: 'DevOps Engineer',
      requiredCount: 1,
      suggestedPersonnel: ['박지민'],
      skills: ['AWS', 'Docker', 'Kubernetes'],
    },
  ];

  const getMarketDemandColor = (demand: DomainInsight['marketDemand']) => {
    switch (demand) {
      case 'high':
        return 'bg-red-100 text-red-700';
      case 'medium':
        return 'bg-yellow-100 text-yellow-700';
      case 'low':
        return 'bg-gray-100 text-gray-700';
    }
  };

  const getMarketDemandText = (demand: DomainInsight['marketDemand']) => {
    switch (demand) {
      case 'high':
        return '수요 높음';
      case 'medium':
        return '수요 보통';
      case 'low':
        return '수요 낮음';
    }
  };

  return (
    <div className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h2 className="text-gray-900 mb-2 bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">도메인 분석</h2>
        <p className="text-gray-600">인력 이력을 기반으로 신규 도메인 진출 가능성을 분석합니다</p>
      </motion.div>

      {/* Domain Insights */}
      <div>
        <motion.div 
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="flex items-center gap-2 mb-4"
        >
          <motion.div
            animate={{ scale: [1, 1.2, 1] }}
            transition={{ duration: 2, repeat: Infinity }}
          >
            <Lightbulb className="w-5 h-5 text-blue-600" />
          </motion.div>
          <h3 className="text-gray-900">신규 도메인 기회</h3>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {domainInsights.map((domain, index) => (
            <motion.div
              key={domain.id}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.4, delay: index * 0.1 }}
              whileHover={{ scale: 1.03, y: -5 }}
              onClick={() => setSelectedDomain(domain.id)}
            >
              <Card className="cursor-pointer bg-white/80 backdrop-blur-sm border-0 shadow-lg hover:shadow-xl transition-all overflow-hidden">
                <div className="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br from-blue-500/10 to-indigo-500/10 rounded-full blur-2xl" />
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div>
                      <CardTitle className="mb-2 bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">{domain.domain}</CardTitle>
                      <div className="flex items-center gap-2">
                        <motion.span 
                          whileHover={{ scale: 1.1 }}
                          className={`px-2 py-1 rounded-full text-xs ${getMarketDemandColor(domain.marketDemand)}`}
                        >
                          {getMarketDemandText(domain.marketDemand)}
                        </motion.span>
                        <span className="text-xs text-gray-600">잠재 프로젝트 {domain.potentialProjects}건</span>
                      </div>
                    </div>
                    <motion.div 
                      initial={{ scale: 0 }}
                      animate={{ scale: 1 }}
                      transition={{ delay: index * 0.1 + 0.2 }}
                      className="text-right"
                    >
                      <p className="text-sm text-gray-600 mb-1">신뢰도</p>
                      <p className="text-blue-600">{domain.confidence}%</p>
                    </motion.div>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div>
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-sm text-gray-600">전문 인력</span>
                        <span className="text-gray-900">{domain.availableExperts}명</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
                        <motion.div
                          initial={{ width: 0 }}
                          animate={{ width: `${Math.min(domain.availableExperts * 10, 100)}%` }}
                          transition={{ duration: 1, delay: index * 0.1, ease: "easeOut" }}
                          className="bg-gradient-to-r from-blue-600 to-indigo-600 h-2 rounded-full"
                        />
                      </div>
                    </div>

                    <div>
                      <p className="text-sm text-gray-600 mb-2">필요 기술</p>
                      <div className="flex flex-wrap gap-2">
                        {domain.requiredSkills.slice(0, 4).map((skill, idx) => (
                          <motion.div
                            key={skill}
                            initial={{ opacity: 0, scale: 0 }}
                            animate={{ opacity: 1, scale: 1 }}
                            transition={{ delay: index * 0.1 + idx * 0.05 }}
                          >
                            <Badge variant="outline" className="border-blue-200 text-blue-700">
                              {skill}
                            </Badge>
                          </motion.div>
                        ))}
                        {domain.requiredSkills.length > 4 && (
                          <Badge variant="outline">+{domain.requiredSkills.length - 4}</Badge>
                        )}
                      </div>
                    </div>

                    <div>
                      <p className="text-sm text-gray-600 mb-2">주요 인사이트</p>
                      <ul className="space-y-1">
                        {domain.insights.slice(0, 2).map((insight, idx) => (
                          <motion.li 
                            key={idx}
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: index * 0.1 + idx * 0.1 }}
                            className="text-xs text-gray-700 flex items-start gap-2"
                          >
                            <span className="text-blue-600 mt-0.5">•</span>
                            <span>{insight}</span>
                          </motion.li>
                        ))}
                      </ul>
                    </div>

                    <motion.div whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
                      <Button variant="outline" size="sm" className="w-full gap-2 border-blue-200 text-blue-700 hover:bg-blue-50">
                        상세 분석 보기
                        <ArrowRight className="w-4 h-4" />
                      </Button>
                    </motion.div>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Team Organization Suggestion */}
      {selectedDomain && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
        >
          <Card className="bg-white/80 backdrop-blur-sm border-0 shadow-lg overflow-hidden">
            <div className="absolute top-0 right-0 w-64 h-64 bg-gradient-to-br from-blue-500/10 to-indigo-500/10 rounded-full blur-3xl" />
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Users className="w-5 h-5 text-blue-600" />
                추천 팀 구성 - {domainInsights.find((d) => d.id === selectedDomain)?.domain}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-6">
                <motion.div 
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  className="p-4 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl border border-blue-100"
                >
                  <p className="text-sm text-blue-900 mb-2">팀 구성 전략</p>
                  <p className="text-sm text-blue-700">
                    기존 인력의 프로젝트 경험과 기술 스택을 분석하여 최적의 팀을 제안합니다.
                    추가 채용이 필요한 경우 우선순위와 함께 표시됩니다.
                  </p>
                </motion.div>

                <div className="space-y-4">
                  {teamSuggestions.map((suggestion, idx) => (
                    <motion.div 
                      key={idx}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: idx * 0.1 }}
                      whileHover={{ scale: 1.01, x: 4 }}
                      className="p-4 border border-gray-200 rounded-xl bg-white/50"
                    >
                      <div className="flex items-center justify-between mb-3">
                        <div>
                          <p className="text-gray-900 mb-1">{suggestion.role}</p>
                          <p className="text-sm text-gray-600">필요 인원: {suggestion.requiredCount}명</p>
                        </div>
                        <Badge>{suggestion.suggestedPersonnel.length}명 추천</Badge>
                      </div>

                      <div className="space-y-3">
                        <div>
                          <p className="text-sm text-gray-600 mb-2">추천 인력</p>
                          <div className="flex flex-wrap gap-2">
                            {suggestion.suggestedPersonnel.map((person) => (
                              <div key={person} className="px-3 py-1 bg-gray-100 rounded-full text-sm text-gray-900">
                                {person}
                              </div>
                            ))}
                          </div>
                        </div>

                        <div>
                          <p className="text-sm text-gray-600 mb-2">주요 기술</p>
                          <div className="flex flex-wrap gap-2">
                            {suggestion.skills.map((skill) => (
                              <Badge key={skill} variant="secondary">
                                {skill}
                              </Badge>
                            ))}
                          </div>
                        </div>
                      </div>
                    </motion.div>
                  ))}
                </div>

                <div className="flex gap-2">
                  <motion.div className="flex-1" whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
                    <Button className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700">팀 구성안 승인</Button>
                  </motion.div>
                  <motion.div whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
                    <Button variant="outline">수정</Button>
                  </motion.div>
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      )}

      {/* Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {[
          { icon: TrendingUp, label: '신규 도메인 기회', value: domainInsights.length, color: 'from-blue-500 to-blue-600' },
          { icon: Users, label: '활용 가능 인력', value: domainInsights.reduce((acc, d) => acc + d.availableExperts, 0), color: 'from-green-500 to-emerald-600' },
          { icon: Lightbulb, label: '잠재 프로젝트', value: domainInsights.reduce((acc, d) => acc + d.potentialProjects, 0), color: 'from-purple-500 to-purple-600' },
        ].map((stat, index) => {
          const Icon = stat.icon;
          return (
            <motion.div
              key={stat.label}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              whileHover={{ scale: 1.05, y: -5 }}
            >
              <Card className="bg-white/80 backdrop-blur-sm border-0 shadow-lg">
                <CardContent className="p-6">
                  <div className="flex items-center gap-4">
                    <motion.div 
                      whileHover={{ rotate: 360 }}
                      transition={{ duration: 0.6 }}
                      className={`w-12 h-12 bg-gradient-to-br ${stat.color} rounded-xl flex items-center justify-center shadow-lg`}
                    >
                      <Icon className="w-6 h-6 text-white" />
                    </motion.div>
                    <div>
                      <p className="text-sm text-gray-600 mb-1">{stat.label}</p>
                      <motion.p 
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        transition={{ delay: index * 0.1 + 0.2 }}
                        className="text-gray-900"
                      >
                        {stat.value}{stat.label.includes('인력') ? '명' : stat.label.includes('프로젝트') ? '건' : '개'}
                      </motion.p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}
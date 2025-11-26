import { useState } from 'react';
import { Search, Plus, Calendar, Users as UsersIcon } from 'lucide-react';
import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Button } from './ui/button';
import { Input } from './ui/input';

interface Project {
  id: string;
  name: string;
  client: string;
  status: 'planning' | 'in-progress' | 'completed';
  requiredSkills: string[];
  assignedMembers: number;
  requiredMembers: number;
  startDate: string;
  endDate: string;
  matchRate?: number;
}

export function ProjectManagement() {
  const [searchQuery, setSearchQuery] = useState('');

  const projects: Project[] = [
    {
      id: '1',
      name: '금융 플랫폼 구축',
      client: 'A은행',
      status: 'in-progress',
      requiredSkills: ['React', 'Java', 'Spring', 'AWS', 'PostgreSQL'],
      assignedMembers: 8,
      requiredMembers: 10,
      startDate: '2024.01.15',
      endDate: '2024.12.31',
      matchRate: 95,
    },
    {
      id: '2',
      name: 'AI 챗봇 개발',
      client: 'B기업',
      status: 'in-progress',
      requiredSkills: ['Python', 'TensorFlow', 'NLP', 'FastAPI', 'Docker'],
      assignedMembers: 5,
      requiredMembers: 6,
      startDate: '2024.03.01',
      endDate: '2024.08.30',
      matchRate: 88,
    },
    {
      id: '3',
      name: '물류 시스템 개선',
      client: 'C물류',
      status: 'in-progress',
      requiredSkills: ['React', 'Node.js', 'MongoDB', 'Redis'],
      assignedMembers: 6,
      requiredMembers: 6,
      startDate: '2024.02.01',
      endDate: '2024.10.31',
      matchRate: 92,
    },
    {
      id: '4',
      name: '헬스케어 앱 개발',
      client: 'D병원',
      status: 'planning',
      requiredSkills: ['React Native', 'Node.js', 'Firebase', 'GraphQL'],
      assignedMembers: 0,
      requiredMembers: 5,
      startDate: '2025.01.01',
      endDate: '2025.06.30',
    },
    {
      id: '5',
      name: '스마트팩토리 시스템',
      client: 'E제조',
      status: 'planning',
      requiredSkills: ['IoT', 'Python', 'AWS', 'React', 'Time Series DB'],
      assignedMembers: 2,
      requiredMembers: 8,
      startDate: '2024.12.01',
      endDate: '2025.08.31',
    },
    {
      id: '6',
      name: '전자상거래 플랫폼',
      client: 'F커머스',
      status: 'completed',
      requiredSkills: ['Vue.js', 'Java', 'Kafka', 'Elasticsearch'],
      assignedMembers: 10,
      requiredMembers: 10,
      startDate: '2023.06.01',
      endDate: '2024.05.31',
    },
  ];

  const filteredProjects = projects.filter((project) =>
    project.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    project.client.toLowerCase().includes(searchQuery.toLowerCase()) ||
    project.requiredSkills.some((skill) => skill.toLowerCase().includes(searchQuery.toLowerCase()))
  );

  const getStatusColor = (status: Project['status']) => {
    switch (status) {
      case 'planning':
        return 'bg-yellow-100 text-yellow-700';
      case 'in-progress':
        return 'bg-blue-100 text-blue-700';
      case 'completed':
        return 'bg-green-100 text-green-700';
    }
  };

  const getStatusText = (status: Project['status']) => {
    switch (status) {
      case 'planning':
        return '계획 중';
      case 'in-progress':
        return '진행 중';
      case 'completed':
        return '완료';
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
          <h2 className="text-gray-900 mb-2 bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">프로젝트 관리</h2>
          <p className="text-gray-600">진행 중인 프로젝트와 투입 인력을 관리하세요</p>
        </div>
        <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
          <Button className="gap-2 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 shadow-lg shadow-blue-500/30">
            <Plus className="w-4 h-4" />
            신규 프로젝트 등록
          </Button>
        </motion.div>
      </motion.div>

      {/* Search */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
      >
        <Card className="bg-white/80 backdrop-blur-sm border-0 shadow-lg">
          <CardContent className="p-4">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
              <Input
                placeholder="프로젝트명, 고객사, 기술 스택으로 검색..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10 border-0 bg-gray-50 focus:bg-white transition-colors"
              />
            </div>
          </CardContent>
        </Card>
      </motion.div>

      {/* Projects List */}
      <div className="space-y-4">
        {filteredProjects.map((project, index) => (
          <motion.div
            key={project.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: index * 0.05 }}
            whileHover={{ scale: 1.01, y: -2 }}
          >
            <Card className="bg-white/80 backdrop-blur-sm border-0 shadow-lg hover:shadow-xl transition-all overflow-hidden">
              <div className="absolute top-0 right-0 w-48 h-48 bg-gradient-to-br from-blue-500/5 to-indigo-500/5 rounded-full blur-2xl" />
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <CardTitle className="bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">{project.name}</CardTitle>
                      <motion.span 
                        whileHover={{ scale: 1.1 }}
                        className={`px-3 py-1 rounded-full text-xs ${getStatusColor(project.status)}`}
                      >
                        {getStatusText(project.status)}
                      </motion.span>
                    </div>
                    <p className="text-sm text-gray-600">{project.client}</p>
                  </div>
                  {project.matchRate && (
                    <motion.div 
                      initial={{ scale: 0 }}
                      animate={{ scale: 1 }}
                      transition={{ delay: index * 0.05 + 0.2 }}
                      className="text-right"
                    >
                      <p className="text-sm text-gray-600">AI 매칭률</p>
                      <p className="text-blue-600">{project.matchRate}%</p>
                    </motion.div>
                  )}
                </div>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <div>
                    <div className="flex items-center gap-2 text-gray-600 mb-3">
                      <Calendar className="w-4 h-4" />
                      <span className="text-sm">프로젝트 기간</span>
                    </div>
                    <p className="text-gray-900">{project.startDate} ~ {project.endDate}</p>
                  </div>

                  <div>
                    <div className="flex items-center gap-2 text-gray-600 mb-3">
                      <UsersIcon className="w-4 h-4" />
                      <span className="text-sm">투입 인력</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <p className="text-gray-900">
                        {project.assignedMembers} / {project.requiredMembers}명
                      </p>
                      {project.assignedMembers < project.requiredMembers && (
                        <span className="text-xs text-orange-600">
                          ({project.requiredMembers - project.assignedMembers}명 부족)
                        </span>
                      )}
                    </div>
                    <div className="mt-2 w-full bg-gray-200 rounded-full h-2 overflow-hidden">
                      <motion.div
                        initial={{ width: 0 }}
                        animate={{ width: `${(project.assignedMembers / project.requiredMembers) * 100}%` }}
                        transition={{ duration: 1, delay: index * 0.05, ease: "easeOut" }}
                        className="bg-gradient-to-r from-blue-600 to-indigo-600 h-2 rounded-full"
                      />
                    </div>
                  </div>

                  <div>
                    <p className="text-sm text-gray-600 mb-3">요구 기술</p>
                    <div className="flex flex-wrap gap-2">
                      {project.requiredSkills.map((skill, idx) => (
                        <motion.div
                          key={skill}
                          initial={{ opacity: 0, scale: 0 }}
                          animate={{ opacity: 1, scale: 1 }}
                          transition={{ delay: index * 0.05 + idx * 0.03 }}
                        >
                          <Badge variant="outline" className="border-blue-200 text-blue-700">
                            {skill}
                          </Badge>
                        </motion.div>
                      ))}
                    </div>
                  </div>
                </div>

                {project.assignedMembers < project.requiredMembers && (
                  <motion.div 
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: index * 0.05 + 0.3 }}
                    className="mt-4 pt-4 border-t border-gray-200"
                  >
                    <motion.div whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
                      <Button variant="outline" size="sm" className="w-full md:w-auto border-blue-200 text-blue-700 hover:bg-blue-50">
                        AI 인력 추천 받기
                      </Button>
                    </motion.div>
                  </motion.div>
                )}
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
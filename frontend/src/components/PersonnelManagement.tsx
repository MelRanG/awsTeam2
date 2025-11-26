import { useState } from 'react';
import { Search, Filter, UserPlus } from 'lucide-react';
import { motion } from 'framer-motion';
import { Card, CardContent } from './ui/card';
import { Badge } from './ui/badge';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from './ui/dialog';

interface Personnel {
  id: string;
  name: string;
  position: string;
  department: string;
  skills: string[];
  experience: number;
  currentProject: string | null;
  availability: 'available' | 'busy' | 'pending';
}

export function PersonnelManagement() {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedPerson, setSelectedPerson] = useState<Personnel | null>(null);

  const personnel: Personnel[] = [
    {
      id: '1',
      name: '김철수',
      position: 'Senior Developer',
      department: '개발팀',
      skills: ['React', 'Node.js', 'AWS', 'Docker'],
      experience: 8,
      currentProject: '금융 플랫폼 구축',
      availability: 'busy',
    },
    {
      id: '2',
      name: '이영희',
      position: 'Tech Lead',
      department: '개발팀',
      skills: ['Java', 'Spring', 'Kubernetes', 'PostgreSQL'],
      experience: 12,
      currentProject: null,
      availability: 'available',
    },
    {
      id: '3',
      name: '박지민',
      position: 'DevOps Engineer',
      department: '인프라팀',
      skills: ['AWS', 'Terraform', 'Jenkins', 'Docker'],
      experience: 6,
      currentProject: 'AI 챗봇 개발',
      availability: 'busy',
    },
    {
      id: '4',
      name: '최민수',
      position: 'Data Engineer',
      department: '데이터팀',
      skills: ['Python', 'Spark', 'Airflow', 'AWS'],
      experience: 5,
      currentProject: null,
      availability: 'available',
    },
    {
      id: '5',
      name: '정수진',
      position: 'Frontend Developer',
      department: '개발팀',
      skills: ['React', 'TypeScript', 'Next.js', 'Tailwind'],
      experience: 4,
      currentProject: '물류 시스템 개선',
      availability: 'busy',
    },
    {
      id: '6',
      name: '강동원',
      position: 'Backend Developer',
      department: '개발팀',
      skills: ['Python', 'Django', 'FastAPI', 'Redis'],
      experience: 7,
      currentProject: null,
      availability: 'available',
    },
  ];

  const filteredPersonnel = personnel.filter((person) =>
    person.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    person.position.toLowerCase().includes(searchQuery.toLowerCase()) ||
    person.skills.some((skill) => skill.toLowerCase().includes(searchQuery.toLowerCase()))
  );

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
          <p className="text-gray-600">전체 인력 정보를 확인하고 관리하세요</p>
        </div>
        <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
          <Button className="gap-2 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 shadow-lg shadow-blue-500/30">
            <UserPlus className="w-4 h-4" />
            신규 인력 등록
          </Button>
        </motion.div>
      </motion.div>

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
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredPersonnel.map((person, index) => (
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
                    <div className="p-3 bg-gray-50 rounded-lg">
                      <p className="text-gray-900 mb-1">금융 플랫폼 구축</p>
                      <p className="text-sm text-gray-600">2024.01 - 2024.08 (8개월)</p>
                    </div>
                    <div className="p-3 bg-gray-50 rounded-lg">
                      <p className="text-gray-900 mb-1">전자상거래 시스템 개선</p>
                      <p className="text-sm text-gray-600">2023.05 - 2023.12 (8개월)</p>
                    </div>
                  </div>
                </div>
              </div>
            </DialogContent>
          </Dialog>
        ))}
      </div>
    </div>
  );
}
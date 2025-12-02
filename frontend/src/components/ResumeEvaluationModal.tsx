import { useState } from 'react';
import { X, CheckCircle, XCircle, User, Briefcase, Award, TrendingUp } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { Button } from './ui/button';
import { Card } from './ui/card';

interface EvaluationData {
  employee_id: string;
  name: string;
  email: string;
  role: string;
  years_of_experience: number;
  department: string;
  skills: Array<{
    name: string;
    level: string;
    years: number;
  }>;
  quantitative_score: number;
  qualitative_analysis: string;
  domain_expertise: Record<string, number>;
  file_key: string;
}

interface ResumeEvaluationModalProps {
  isOpen: boolean;
  evaluationData: EvaluationData | null;
  onApprove: (data: EvaluationData) => Promise<void>;
  onReject: () => void;
  onClose: () => void;
}

export function ResumeEvaluationModal({
  isOpen,
  evaluationData,
  onApprove,
  onReject,
  onClose,
}: ResumeEvaluationModalProps) {
  const [loading, setLoading] = useState(false);

  const handleApprove = async () => {
    if (!evaluationData) return;
    
    setLoading(true);
    try {
      await onApprove(evaluationData);
      onClose();
    } catch (error) {
      console.error('승인 실패:', error);
      alert('승인 처리 중 오류가 발생했습니다.');
    } finally {
      setLoading(false);
    }
  };

  const handleReject = () => {
    onReject();
    onClose();
  };

  if (!evaluationData) return null;

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/90 backdrop-blur-sm">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            className="w-full max-w-4xl mx-4 max-h-[90vh] overflow-y-auto"
          >
            <Card className="bg-white p-6 shadow-2xl">
              {/* 헤더 */}
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                  이력서 분석 결과
                </h2>
                <button
                  onClick={onClose}
                  className="p-2 hover:bg-gray-100 rounded-full transition-colors"
                >
                  <X className="w-5 h-5 text-gray-500" />
                </button>
              </div>

              {/* 기본 정보 */}
              <div className="mb-6 p-4 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl">
                <div className="flex items-center gap-3 mb-4">
                  <div className="p-3 bg-blue-100 rounded-full">
                    <User className="w-6 h-6 text-blue-600" />
                  </div>
                  <div>
                    <h3 className="text-xl font-bold text-gray-900">{evaluationData.name}</h3>
                    <p className="text-sm text-gray-600">{evaluationData.email}</p>
                  </div>
                </div>
                
                <div className="grid grid-cols-3 gap-4">
                  <div>
                    <p className="text-xs text-gray-600 mb-1">직급</p>
                    <p className="font-semibold text-gray-900">{evaluationData.role}</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-600 mb-1">부서</p>
                    <p className="font-semibold text-gray-900">{evaluationData.department}</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-600 mb-1">경력</p>
                    <p className="font-semibold text-gray-900">{evaluationData.years_of_experience}년</p>
                  </div>
                </div>
              </div>

              {/* 정량적 점수 */}
              <div className="mb-6">
                <div className="flex items-center gap-2 mb-3">
                  <TrendingUp className="w-5 h-5 text-green-600" />
                  <h3 className="text-lg font-semibold text-gray-900">정량적 평가</h3>
                </div>
                <div className="flex items-center gap-4">
                  <div className="flex-1 bg-gray-200 rounded-full h-4 overflow-hidden">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: `${evaluationData.quantitative_score}%` }}
                      transition={{ duration: 1, ease: 'easeOut' }}
                      className={`h-full ${
                        evaluationData.quantitative_score >= 80
                          ? 'bg-gradient-to-r from-green-500 to-emerald-500'
                          : evaluationData.quantitative_score >= 60
                          ? 'bg-gradient-to-r from-blue-500 to-cyan-500'
                          : 'bg-gradient-to-r from-yellow-500 to-orange-500'
                      }`}
                    />
                  </div>
                  <span className="text-2xl font-bold text-gray-900">
                    {evaluationData.quantitative_score}점
                  </span>
                </div>
              </div>

              {/* 기술 스택 */}
              <div className="mb-6">
                <div className="flex items-center gap-2 mb-3">
                  <Award className="w-5 h-5 text-purple-600" />
                  <h3 className="text-lg font-semibold text-gray-900">기술 스택</h3>
                </div>
                <div className="grid grid-cols-2 gap-3">
                  {evaluationData.skills.map((skill, index) => (
                    <div key={index} className="p-3 bg-gray-50 rounded-lg">
                      <div className="flex items-center justify-between mb-1">
                        <span className="font-semibold text-gray-900">{skill.name}</span>
                        <span className="text-xs px-2 py-1 bg-blue-100 text-blue-700 rounded-full">
                          {skill.level}
                        </span>
                      </div>
                      <p className="text-xs text-gray-600">{skill.years}년 경험</p>
                    </div>
                  ))}
                </div>
              </div>

              {/* 도메인 전문성 */}
              <div className="mb-6">
                <div className="flex items-center gap-2 mb-3">
                  <Briefcase className="w-5 h-5 text-indigo-600" />
                  <h3 className="text-lg font-semibold text-gray-900">도메인 전문성</h3>
                </div>
                <div className="space-y-2">
                  {Object.entries(evaluationData.domain_expertise).map(([domain, score]) => (
                    <div key={domain}>
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-sm font-medium text-gray-700">{domain}</span>
                        <span className="text-sm font-semibold text-gray-900">{score}%</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-gradient-to-r from-indigo-500 to-purple-500 h-2 rounded-full"
                          style={{ width: `${score}%` }}
                        />
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* 정성적 분석 */}
              <div className="mb-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-3">정성적 분석</h3>
                <div className="p-4 bg-gray-50 rounded-xl">
                  <p className="text-sm text-gray-700 whitespace-pre-wrap">
                    {evaluationData.qualitative_analysis}
                  </p>
                </div>
              </div>

              {/* 액션 버튼 */}
              <div className="flex gap-3 pt-4 border-t">
                <Button
                  onClick={handleReject}
                  variant="outline"
                  className="flex-1 border-red-300 text-red-600 hover:bg-red-50"
                  disabled={loading}
                >
                  <XCircle className="w-4 h-4 mr-2" />
                  반려
                </Button>
                <Button
                  onClick={handleApprove}
                  className="flex-1 bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700"
                  disabled={loading}
                >
                  <CheckCircle className="w-4 h-4 mr-2" />
                  {loading ? '처리 중...' : '승인 및 등록'}
                </Button>
              </div>

              {/* 안내 사항 */}
              <div className="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
                <p className="text-xs text-yellow-800">
                  ⚠️ 승인을 누르면 이 직원 정보가 시스템에 등록됩니다. 반려를 누르면 데이터가 저장되지 않습니다.
                </p>
              </div>
            </Card>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}

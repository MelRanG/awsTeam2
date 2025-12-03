import { X, AlertTriangle, CheckCircle, AlertCircle } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { Card, CardContent } from './ui/card';
import { Badge } from './ui/badge';
import { Button } from './ui/button';

interface VerificationQuestion {
  category: string;
  question: string;
  reason: string;
  severity: 'high' | 'medium' | 'low';
}

interface VerificationQuestionsModalProps {
  isOpen: boolean;
  onClose: () => void;
  candidateName: string;
  questions: VerificationQuestion[];
}

export function VerificationQuestionsModal({
  isOpen,
  onClose,
  candidateName,
  questions = []
}: VerificationQuestionsModalProps) {
  
  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'high':
        return 'bg-red-100 text-red-700 border-red-300';
      case 'medium':
        return 'bg-yellow-100 text-yellow-700 border-yellow-300';
      case 'low':
        return 'bg-blue-100 text-blue-700 border-blue-300';
      default:
        return 'bg-gray-100 text-gray-700 border-gray-300';
    }
  };

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case 'high':
        return <AlertTriangle className="w-4 h-4" />;
      case 'medium':
        return <AlertCircle className="w-4 h-4" />;
      case 'low':
        return <CheckCircle className="w-4 h-4" />;
      default:
        return null;
    }
  };

  const getSeverityText = (severity: string) => {
    switch (severity) {
      case 'high':
        return '높음';
      case 'medium':
        return '중간';
      case 'low':
        return '낮음';
      default:
        return severity;
    }
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            className="w-full max-w-4xl max-h-[90vh] overflow-hidden"
          >
            <Card className="bg-white shadow-2xl">
              <CardContent className="p-6">
                {/* 헤더 */}
                <div className="flex items-center justify-between mb-6">
                  <div>
                    <h2 className="text-2xl font-bold text-gray-900">
                      이력서 검증 질문
                    </h2>
                    <p className="text-gray-600 mt-1">
                      {candidateName}님의 이력서 검증을 위한 면접 질문
                    </p>
                  </div>
                  <button
                    onClick={onClose}
                    className="p-2 hover:bg-gray-100 rounded-full transition-colors"
                  >
                    <X className="w-6 h-6 text-gray-500" />
                  </button>
                </div>

                {/* 질문 목록 */}
                <div className="space-y-4 max-h-[calc(90vh-200px)] overflow-y-auto pr-2">
                  {questions.length === 0 ? (
                    <div className="text-center py-12">
                      <AlertCircle className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                      <p className="text-gray-600">검증 질문이 없습니다</p>
                    </div>
                  ) : (
                    questions.map((q, idx) => (
                      <motion.div
                        key={idx}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: idx * 0.05 }}
                      >
                        <Card className="border-2 hover:shadow-md transition-shadow">
                          <CardContent className="p-4">
                            <div className="flex items-start justify-between mb-3">
                              <div className="flex items-center gap-2">
                                <span className="text-lg font-bold text-gray-400">
                                  Q{idx + 1}
                                </span>
                                <Badge variant="outline" className="text-xs">
                                  {q.category}
                                </Badge>
                              </div>
                              <Badge
                                className={`flex items-center gap-1 ${getSeverityColor(
                                  q.severity
                                )}`}
                              >
                                {getSeverityIcon(q.severity)}
                                {getSeverityText(q.severity)}
                              </Badge>
                            </div>

                            <div className="space-y-3">
                              <div>
                                <p className="text-base font-semibold text-gray-900 leading-relaxed">
                                  {q.question}
                                </p>
                              </div>

                              <div className="bg-gray-50 rounded-lg p-3 border-l-4 border-blue-500">
                                <p className="text-sm text-gray-700">
                                  <span className="font-semibold text-gray-900">
                                    검증 이유:
                                  </span>{' '}
                                  {q.reason}
                                </p>
                              </div>
                            </div>
                          </CardContent>
                        </Card>
                      </motion.div>
                    ))
                  )}
                </div>

                {/* 푸터 */}
                <div className="mt-6 pt-4 border-t border-gray-200">
                  <div className="flex items-center justify-between">
                    <p className="text-sm text-gray-600">
                      총 {questions.length}개의 검증 질문
                    </p>
                    <Button onClick={onClose} variant="outline">
                      닫기
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}

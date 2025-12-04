/**
 * 프로젝트 배정 확인 모달 컴포넌트
 * Requirements: 2.5 - 프로젝트 배정 기능
 */

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, AlertCircle, CheckCircle, Loader2, Calendar, Users, Percent } from 'lucide-react';
import { Button } from './ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Textarea } from './ui/textarea';

interface ProjectAssignmentModalProps {
  isOpen: boolean;
  onClose: () => void;
  onConfirm: (assignmentData: AssignmentData) => Promise<void>;
  employeeName: string;
  projectName: string;
  projectEndDate?: string;
  employeeAvailability?: 'available' | 'busy' | 'pending';
}

interface AssignmentData {
  role: string;
  startDate: string;
  endDate: string;
  allocationRate: number;
  reason: string;
}

export function ProjectAssignmentModal({
  isOpen,
  onClose,
  onConfirm,
  employeeName,
  projectName,
  projectEndDate,
  employeeAvailability = 'available',
}: ProjectAssignmentModalProps) {
  const [isAssigning, setIsAssigning] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  // 투입 정보 상태
  const [role, setRole] = useState('Developer');
  const [startDate, setStartDate] = useState(new Date().toISOString().split('T')[0]);
  const [endDate, setEndDate] = useState(projectEndDate || '');
  const [allocationRate, setAllocationRate] = useState(100);
  const [reason, setReason] = useState('');

  const handleConfirm = async () => {
    // 입력 검증
    if (!startDate) {
      setError('투입 시작일을 입력해주세요.');
      return;
    }
    
    if (endDate && new Date(endDate) < new Date(startDate)) {
      setError('종료일은 시작일 이후여야 합니다.');
      return;
    }
    
    if (allocationRate < 1 || allocationRate > 100) {
      setError('투입률은 1~100% 사이여야 합니다.');
      return;
    }

    try {
      setIsAssigning(true);
      setError(null);
      
      const assignmentData: AssignmentData = {
        role,
        startDate,
        endDate,
        allocationRate,
        reason,
      };
      
      await onConfirm(assignmentData);
      onClose();
    } catch (err: any) {
      setError(err.message || '배정에 실패했습니다.');
    } finally {
      setIsAssigning(false);
    }
  };

  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4"
        onClick={onClose}
      >
        <motion.div
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          exit={{ scale: 0.9, opacity: 0 }}
          onClick={(e) => e.stopPropagation()}
          className="w-full max-w-md"
        >
          <Card className="border-0 shadow-2xl">
            <CardHeader className="relative">
              <button
                onClick={onClose}
                className="absolute right-4 top-4 text-gray-400 hover:text-gray-600 transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
              <CardTitle className="flex items-center gap-2">
                <CheckCircle className="w-5 h-5 text-blue-600" />
                프로젝트 배정 확인
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* 배정 정보 */}
              <div className="space-y-3">
                <div className="p-4 bg-blue-50 rounded-lg">
                  <p className="text-sm text-gray-600 mb-1">직원</p>
                  <p className="font-semibold text-gray-900">{employeeName}</p>
                </div>
                <div className="p-4 bg-indigo-50 rounded-lg">
                  <p className="text-sm text-gray-600 mb-1">프로젝트</p>
                  <p className="font-semibold text-gray-900">{projectName}</p>
                </div>
              </div>

              {/* 투입 역할 선택 */}
              <div className="space-y-2">
                <Label className="flex items-center gap-2">
                  <Users className="w-4 h-4 text-gray-600" />
                  투입 역할
                </Label>
                <Select value={role} onValueChange={setRole}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="Project Manager">프로젝트 매니저 (PM)</SelectItem>
                    <SelectItem value="Tech Lead">기술 리드 (Tech Lead)</SelectItem>
                    <SelectItem value="Developer">개발자 (Developer)</SelectItem>
                    <SelectItem value="Frontend Developer">프론트엔드 개발자</SelectItem>
                    <SelectItem value="Backend Developer">백엔드 개발자</SelectItem>
                    <SelectItem value="Full Stack Developer">풀스택 개발자</SelectItem>
                    <SelectItem value="DevOps Engineer">데브옵스 엔지니어</SelectItem>
                    <SelectItem value="QA Engineer">QA 엔지니어</SelectItem>
                    <SelectItem value="UI/UX Designer">UI/UX 디자이너</SelectItem>
                    <SelectItem value="Data Analyst">데이터 분석가</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              {/* 투입 기간 */}
              <div className="grid grid-cols-2 gap-3">
                <div className="space-y-2">
                  <Label className="flex items-center gap-2">
                    <Calendar className="w-4 h-4 text-gray-600" />
                    시작일
                  </Label>
                  <Input
                    type="date"
                    value={startDate}
                    onChange={(e) => setStartDate(e.target.value)}
                  />
                </div>
                <div className="space-y-2">
                  <Label className="flex items-center gap-2">
                    <Calendar className="w-4 h-4 text-gray-600" />
                    종료일 (선택)
                  </Label>
                  <Input
                    type="date"
                    value={endDate}
                    onChange={(e) => setEndDate(e.target.value)}
                    min={startDate}
                  />
                </div>
              </div>

              {/* 투입률 */}
              <div className="space-y-2">
                <Label className="flex items-center gap-2">
                  <Percent className="w-4 h-4 text-gray-600" />
                  투입률 (%)
                </Label>
                <div className="flex items-center gap-3">
                  <Input
                    type="number"
                    min="1"
                    max="100"
                    value={allocationRate}
                    onChange={(e) => setAllocationRate(Number(e.target.value))}
                    className="flex-1"
                  />
                  <div className="flex gap-2">
                    <Button
                      type="button"
                      size="sm"
                      variant="outline"
                      onClick={() => setAllocationRate(50)}
                    >
                      50%
                    </Button>
                    <Button
                      type="button"
                      size="sm"
                      variant="outline"
                      onClick={() => setAllocationRate(100)}
                    >
                      100%
                    </Button>
                  </div>
                </div>
                <p className="text-xs text-gray-500">
                  {allocationRate}% 투입 = 주 {(allocationRate / 20).toFixed(1)}일 근무
                </p>
              </div>

              {/* 투입 근거 */}
              <div className="space-y-2">
                <Label>투입 근거 (선택)</Label>
                <Textarea
                  placeholder="이 직원을 선택한 이유를 입력하세요..."
                  value={reason}
                  onChange={(e) => setReason(e.target.value)}
                  rows={3}
                  className="resize-none"
                />
              </div>

              {/* 가용성 경고 */}
              {employeeAvailability !== 'available' && (
                <motion.div
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="flex items-start gap-2 p-3 bg-yellow-50 border border-yellow-200 rounded-lg"
                >
                  <AlertCircle className="w-5 h-5 text-yellow-600 flex-shrink-0 mt-0.5" />
                  <div>
                    <p className="text-sm font-medium text-yellow-900">가용성 확인 필요</p>
                    <p className="text-xs text-yellow-700 mt-1">
                      {employeeAvailability === 'busy'
                        ? '이 직원은 현재 다른 프로젝트에 투입되어 있습니다.'
                        : '이 직원의 가용성이 확인되지 않았습니다.'}
                    </p>
                  </div>
                </motion.div>
              )}

              {/* 에러 메시지 */}
              {error && (
                <motion.div
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="flex items-start gap-2 p-3 bg-red-50 border border-red-200 rounded-lg"
                >
                  <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
                  <p className="text-sm text-red-800">{error}</p>
                </motion.div>
              )}

              {/* 액션 버튼 */}
              <div className="flex gap-3 pt-2">
                <Button
                  variant="outline"
                  onClick={onClose}
                  disabled={isAssigning}
                  className="flex-1"
                >
                  취소
                </Button>
                <Button
                  onClick={handleConfirm}
                  disabled={isAssigning}
                  className="flex-1 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700"
                >
                  {isAssigning ? (
                    <>
                      <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                      배정 중...
                    </>
                  ) : (
                    '배정 확인'
                  )}
                </Button>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
}

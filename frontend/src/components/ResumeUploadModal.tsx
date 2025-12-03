import { useState, useRef } from 'react';
import { Upload, X, FileText, CheckCircle, AlertCircle } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { Button } from './ui/button';
import { Card } from './ui/card';
import { ResumeEvaluationModal } from './ResumeEvaluationModal';
import { API_BASE_URL } from '../config/api';

interface ResumeUploadModalProps {
  isOpen: boolean;
  onClose: () => void;
  onUploadSuccess?: (evaluationResult: any) => void;
}

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

export function ResumeUploadModal({ isOpen, onClose, onUploadSuccess }: ResumeUploadModalProps) {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploadStatus, setUploadStatus] = useState<'idle' | 'uploading' | 'success' | 'error'>('idle');
  const [errorMessage, setErrorMessage] = useState('');
  const [evaluationData, setEvaluationData] = useState<EvaluationData | null>(null);
  const [showEvaluationModal, setShowEvaluationModal] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0];
    if (selectedFile) {
      // PDF 파일만 허용
      if (selectedFile.type !== 'application/pdf') {
        setErrorMessage('PDF 파일만 업로드 가능합니다');
        setUploadStatus('error');
        return;
      }
      
      // 파일 크기 제한 (10MB)
      if (selectedFile.size > 10 * 1024 * 1024) {
        setErrorMessage('파일 크기는 10MB 이하여야 합니다');
        setUploadStatus('error');
        return;
      }
      
      setFile(selectedFile);
      setUploadStatus('idle');
      setErrorMessage('');
    }
  };

  const handleDrop = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    const droppedFile = event.dataTransfer.files[0];
    
    if (droppedFile) {
      if (droppedFile.type !== 'application/pdf') {
        setErrorMessage('PDF 파일만 업로드 가능합니다');
        setUploadStatus('error');
        return;
      }
      
      if (droppedFile.size > 10 * 1024 * 1024) {
        setErrorMessage('파일 크기는 10MB 이하여야 합니다');
        setUploadStatus('error');
        return;
      }
      
      setFile(droppedFile);
      setUploadStatus('idle');
      setErrorMessage('');
    }
  };

  const handleDragOver = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
  };

  const handleUpload = async () => {
    if (!file) return;

    setUploading(true);
    setUploadStatus('uploading');
    setUploadProgress(0);

    try {
      // 1. Presigned URL 요청
      const response = await fetch(`${API_BASE_URL}/resume/upload-url`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          file_name: file.name,
          content_type: file.type,
        }),
      });

      if (!response.ok) {
        throw new Error('업로드 URL 생성 실패');
      }

      const { upload_url, file_key } = await response.json();

      // 2. S3에 직접 업로드
      const uploadResponse = await fetch(upload_url, {
        method: 'PUT',
        headers: {
          'Content-Type': file.type,
        },
        body: file,
      });

      if (!uploadResponse.ok) {
        throw new Error('파일 업로드 실패');
      }

      setUploadProgress(100);
      setUploadStatus('success');
      
      // 3. 이력서 파싱 및 평가 요청
      console.log('=== 이력서 분석 시작 ===');
      console.log('파일 키:', file_key);
      console.log('API URL:', `${API_BASE_URL}/resume/parse`);
      
      const evaluationResponse = await fetch(`${API_BASE_URL}/resume/parse`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          file_key: file_key,
        }),
      });

      if (!evaluationResponse.ok) {
        const errorText = await evaluationResponse.text();
        console.error('이력서 분석 실패:', evaluationResponse.status, errorText);
        throw new Error(`이력서 분석 실패: ${evaluationResponse.status}`);
      }

      const evaluationResult = await evaluationResponse.json();
      console.log('=== 이력서 분석 완료 ===');
      console.log('분석 결과:', evaluationResult);
      
      // 성공 콜백 호출 - 부모 컴포넌트로 결과 전달
      if (onUploadSuccess) {
        onUploadSuccess(evaluationResult);
      }
      
      // 업로드 모달 닫기
      handleClose();

    } catch (error) {
      console.error('Upload error:', error);
      setUploadStatus('error');
      setErrorMessage(error instanceof Error ? error.message : '업로드 중 오류가 발생했습니다');
    } finally {
      setUploading(false);
    }
  };

  const handleClose = () => {
    setFile(null);
    setUploadStatus('idle');
    setUploadProgress(0);
    setErrorMessage('');
    onClose();
  };

  const handleApprove = async (data: EvaluationData) => {
    try {
      // 직원 등록 API 호출
      const response = await fetch(`${API_BASE_URL}/employees`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error('직원 등록 실패');
      }

      console.log('직원 등록 완료');
      
      // 성공 콜백 호출
      if (onUploadSuccess) {
        onUploadSuccess(data.file_key);
      }
      
      alert('직원이 성공적으로 등록되었습니다!');
    } catch (error) {
      console.error('직원 등록 에러:', error);
      throw error;
    }
  };

  const handleReject = () => {
    console.log('이력서 반려됨');
    alert('이력서가 반려되었습니다. 데이터가 저장되지 않았습니다.');
  };

  return (
    <>
    <AnimatePresence>
      {isOpen && (
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/95 backdrop-blur-sm">
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.95 }}
          className="w-80 mx-4"
        >
          <Card className="bg-white p-3 shadow-[0_25px_80px_rgba(0,0,0,0.8)] border-[6px] border-blue-500 rounded-2xl ring-4 ring-white">
            {/* 헤더 */}
            <div className="flex items-center justify-between mb-3">
              <h2 className="text-base font-bold text-gray-900">
                이력서 업로드
              </h2>
              <button
                onClick={handleClose}
                className="p-1 hover:bg-gray-100 rounded-full transition-colors"
              >
                <X className="w-4 h-4 text-gray-500" />
              </button>
            </div>

            {/* 파일 드롭 영역 */}
            <div
              onDrop={handleDrop}
              onDragOver={handleDragOver}
              onClick={() => fileInputRef.current?.click()}
              className={`
                border-2 border-dashed rounded-lg p-4 text-center cursor-pointer
                transition-all duration-200
                ${file ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-blue-400 hover:bg-gray-50'}
              `}
            >
              <input
                ref={fileInputRef}
                type="file"
                accept=".pdf"
                onChange={handleFileSelect}
                className="hidden"
              />

              {!file ? (
                <div className="space-y-2">
                  <div className="flex justify-center">
                    <div className="p-2 bg-blue-100 rounded-full">
                      <Upload className="w-5 h-5 text-blue-600" />
                    </div>
                  </div>
                  <div>
                    <p className="text-xs font-semibold text-gray-900 mb-0.5">
                      이력서를 업로드하세요
                    </p>
                    <p className="text-xs text-gray-500">
                      파일을 드래그하거나 클릭 (PDF, 최대 10MB)
                    </p>
                  </div>
                </div>
              ) : (
                <div className="space-y-2">
                  <div className="flex justify-center">
                    <div className="p-2 bg-green-100 rounded-full">
                      <FileText className="w-5 h-5 text-green-600" />
                    </div>
                  </div>
                  <div>
                    <p className="text-xs font-semibold text-gray-900 mb-0.5">
                      {file.name}
                    </p>
                    <p className="text-xs text-gray-600">
                      {(file.size / 1024 / 1024).toFixed(2)} MB
                    </p>
                  </div>
                </div>
              )}
            </div>

            {/* 업로드 진행 상태 */}
            {uploadStatus === 'uploading' && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="mt-4"
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-gray-600">업로드 중...</span>
                  <span className="text-sm font-semibold text-blue-600">{uploadProgress}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${uploadProgress}%` }}
                    className="h-full bg-gradient-to-r from-blue-500 to-indigo-500"
                  />
                </div>
              </motion.div>
            )}

            {/* 성공 메시지 */}
            {uploadStatus === 'success' && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="mt-4 p-4 bg-green-50 border border-green-200 rounded-xl flex items-center gap-3"
              >
                <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0" />
                <div>
                  <p className="text-sm font-semibold text-green-900">업로드 완료!</p>
                  <p className="text-xs text-green-700">이력서 파싱이 시작됩니다.</p>
                </div>
              </motion.div>
            )}

            {/* 에러 메시지 */}
            {uploadStatus === 'error' && errorMessage && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="mt-4 p-4 bg-red-50 border border-red-200 rounded-xl flex items-center gap-3"
              >
                <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0" />
                <p className="text-sm text-red-900">{errorMessage}</p>
              </motion.div>
            )}

            {/* 액션 버튼 */}
            <div className="flex gap-2 mt-3">
              <Button
                variant="outline"
                onClick={handleClose}
                className="flex-1 h-8 text-xs"
                disabled={uploading}
              >
                취소
              </Button>
              <Button
                onClick={handleUpload}
                className="flex-1 h-8 text-xs bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700"
                disabled={!file || uploading || uploadStatus === 'success'}
              >
                {uploading ? '업로드 중...' : '업로드'}
              </Button>
            </div>

            {/* 안내 사항 */}
            <div className="mt-3 p-2 bg-blue-50 rounded-lg">
              <p className="text-xs text-blue-900 font-semibold mb-1">업로드 후 자동 처리</p>
              <ul className="text-xs text-blue-700 space-y-0.5">
                <li>• Textract로 텍스트 추출</li>
                <li>• AI가 기술/경력 분석</li>
                <li>• 정량/정성 평가 수행</li>
              </ul>
            </div>
          </Card>
        </motion.div>
      </div>
      )}
    </AnimatePresence>
    
    {/* 평가 결과 모달 */}
    <ResumeEvaluationModal
      isOpen={showEvaluationModal}
      evaluationData={evaluationData}
      onApprove={handleApprove}
      onReject={handleReject}
      onClose={() => setShowEvaluationModal(false)}
    />
    </>
  );
}

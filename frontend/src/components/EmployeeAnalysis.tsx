import React, { useState } from 'react';
import { api, QuantitativeAnalysisResponse, QualitativeAnalysisResponse, DomainAnalysisResponse } from '../config/api';

export const EmployeeAnalysis: React.FC = () => {
  const [userId, setUserId] = useState('U_003');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const [quantitativeData, setQuantitativeData] = useState<QuantitativeAnalysisResponse | null>(null);
  const [qualitativeData, setQualitativeData] = useState<QualitativeAnalysisResponse | null>(null);
  const [domainData, setDomainData] = useState<DomainAnalysisResponse | null>(null);

  const handleQuantitativeAnalysis = async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await api.quantitativeAnalysis({ user_id: userId });
      setQuantitativeData(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : '정량적 분석 실패');
    } finally {
      setLoading(false);
    }
  };

  const handleQualitativeAnalysis = async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await api.qualitativeAnalysis({ user_id: userId });
      setQualitativeData(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : '정성적 분석 실패');
    } finally {
      setLoading(false);
    }
  };

  const handleDomainAnalysis = async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await api.domainAnalysis({ 
        employee_id: userId, 
        analysis_type: 'skills' 
      });
      setDomainData(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : '도메인 분석 실패');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="employee-analysis">
      <h2>직원 분석</h2>
      
      <div className="input-section">
        <label>
          직원 ID:
          <input 
            type="text" 
            value={userId} 
            onChange={(e) => setUserId(e.target.value)}
            placeholder="예: U_003"
          />
        </label>
      </div>

      <div className="button-group">
        <button onClick={handleQuantitativeAnalysis} disabled={loading}>
          정량적 분석
        </button>
        <button onClick={handleQualitativeAnalysis} disabled={loading}>
          정성적 분석
        </button>
        <button onClick={handleDomainAnalysis} disabled={loading}>
          도메인 분석
        </button>
      </div>

      {loading && <div className="loading">분석 중...</div>}
      {error && <div className="error">{error}</div>}

      {/* 정량적 분석 결과 */}
      {quantitativeData && (
        <div className="result-section">
          <h3>정량적 분석 결과</h3>
          <div className="result-card">
            <p><strong>이름:</strong> {quantitativeData.name}</p>
            <p><strong>종합 점수:</strong> {quantitativeData.overall_score.toFixed(2)}</p>
            
            <h4>경력 메트릭</h4>
            <ul>
              <li>경력: {quantitativeData.experience_metrics.years_of_experience}년</li>
              <li>프로젝트 수: {quantitativeData.experience_metrics.project_count}개</li>
              <li>기술 다양성: {quantitativeData.experience_metrics.skill_diversity}개</li>
              <li>경력 점수: {quantitativeData.experience_metrics.experience_score.toFixed(2)}</li>
            </ul>

            <h4>기술 평가</h4>
            <ul>
              <li>평균 트렌드 점수: {quantitativeData.tech_evaluation.avg_trend_score.toFixed(2)}</li>
              <li>평균 수요 점수: {quantitativeData.tech_evaluation.avg_demand_score.toFixed(2)}</li>
              <li>기술 스택 점수: {quantitativeData.tech_evaluation.tech_stack_score.toFixed(2)}</li>
            </ul>

            <h4>프로젝트 점수</h4>
            <ul>
              <li>평균 규모 점수: {quantitativeData.project_scores.avg_scale_score.toFixed(2)}</li>
              <li>평균 역할 점수: {quantitativeData.project_scores.avg_role_score.toFixed(2)}</li>
              <li>평균 성과 점수: {quantitativeData.project_scores.avg_performance_score.toFixed(2)}</li>
            </ul>
          </div>
        </div>
      )}

      {/* 정성적 분석 결과 */}
      {qualitativeData && (
        <div className="result-section">
          <h3>정성적 분석 결과</h3>
          <div className="result-card">
            <p><strong>이름:</strong> {qualitativeData.name}</p>
            <p><strong>종합 평가:</strong> {qualitativeData.overall_assessment}</p>
            
            {qualitativeData.suspicious_flags.length > 0 && (
              <>
                <h4>주의사항</h4>
                <ul>
                  {qualitativeData.suspicious_flags.map((flag, idx) => (
                    <li key={idx}>
                      <strong>[{flag.severity}]</strong> {flag.description}
                    </li>
                  ))}
                </ul>
              </>
            )}
          </div>
        </div>
      )}

      {/* 도메인 분석 결과 */}
      {domainData && (
        <div className="result-section">
          <h3>도메인 분석 결과</h3>
          <div className="result-card">
            <h4>현재 도메인</h4>
            <ul>
              {domainData.current_domains.map((domain, idx) => (
                <li key={idx}>{domain}</li>
              ))}
            </ul>

            <h4>추천 도메인</h4>
            {domainData.identified_domains.map((domain, idx) => (
              <div key={idx} className="domain-item">
                <p><strong>{domain.domain_name}</strong></p>
                <p>적합도: {domain.feasibility_score.toFixed(2)}</p>
                <p>{domain.reasoning}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

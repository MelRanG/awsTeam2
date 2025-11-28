import React, { useState } from 'react';
import { api, RecommendationsResponse } from '../config/api';

export const ProjectRecommendations: React.FC = () => {
  const [projectId, setProjectId] = useState('PRJ002');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [recommendations, setRecommendations] = useState<RecommendationsResponse | null>(null);

  const handleGetRecommendations = async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await api.recommendations({ project_id: projectId });
      setRecommendations(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : '추천 조회 실패');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="project-recommendations">
      <h2>프로젝트 인력 추천</h2>
      
      <div className="input-section">
        <label>
          프로젝트 ID:
          <input 
            type="text" 
            value={projectId} 
            onChange={(e) => setProjectId(e.target.value)}
            placeholder="예: PRJ002"
          />
        </label>
        <button onClick={handleGetRecommendations} disabled={loading}>
          추천 받기
        </button>
      </div>

      {loading && <div className="loading">추천 조회 중...</div>}
      {error && <div className="error">{error}</div>}

      {recommendations && (
        <div className="result-section">
          <h3>추천 인력 목록</h3>
          {recommendations.recommendations.map((rec, idx) => (
            <div key={idx} className="recommendation-card">
              <h4>{rec.name} ({rec.user_id})</h4>
              <p><strong>추천 점수:</strong> {rec.score.toFixed(2)}</p>
              <p><strong>추천 이유:</strong> {rec.reasoning}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

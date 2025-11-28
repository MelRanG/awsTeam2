# 근거 기반 추천 로직 가이드

## 개요
이 문서는 친밀도 점수 산정, 프로젝트 투입 추천, 신규 도메인 추천에 대한 근거 기반 알고리즘을 설명합니다.

## 1. 친밀도 점수 산정 (Affinity Score Calculation)

### 1.1 기본 공식
```
Score(A,B) = Σ(Mt × Wcontext × Wdecay)
```

**변수 설명:**
- `Mt`: 메시지 발생 건수
- `Wcontext`: 상황별 가중치
- `Wdecay`: 시간 감쇠 계수

### 1.2 상황별 가중치 (Wcontext)

| 상황 | 가중치 | 설명 |
|------|--------|------|
| 업무 시간 내 (09:00~18:00) | 1.0 | 일반 업무 대화 |
| 업무 시간 외 / 주말 | 1.5 | 사적 대화 가능성 증가 |
| 회사 행사 기간 | 2.0 | 동료애 형성 신호 |
| 연차/휴가 기간 | 3.0 | 높은 친밀도 또는 긴급 업무 |

### 1.3 시간 감쇠 (Wdecay)
```python
Wdecay = e^(-λt)
```
- λ = 0.1 (감쇠 계수)
- t = 경과 개월 수
- 최근 1개월: 100% 가중치
- 6개월 전: 약 55% 가중치
- 1년 전: 약 30% 가중치

### 1.4 구현 위치
- **Lambda 함수**: `affinity_calculator/index.py`
- **함수**: `analyze_messenger_communication()`
- **데이터 소스**: 
  - `MessengerLogs` 테이블
  - `CompanyEvents` 테이블

### 1.5 최종 점수 계산
```python
communication_score = min(100.0, weighted_score * 2.0)

# 응답 시간 보정 (빠른 응답 시 가점)
if avg_response_time > 0:
    response_bonus = max(0, 20 - (avg_response_time / 10.0))
    communication_score = min(100.0, communication_score + response_bonus)
```

---

## 2. 프로젝트 투입 추천 (Project Staffing Recommendation)

### 2.1 적합도 점수 공식
```
Score(P, E) = Σ(Smatch × Wlevel × Wrecency) + (Expdomain × Wdomain)
```

**변수 설명:**
- `Smatch`: 요구 기술 일치 여부 (0 or 1)
- `Wlevel`: 기술 숙련도 가중치
- `Wrecency`: 최신성 가중치
- `Expdomain`: 도메인 경험 여부
- `Wdomain`: 도메인 경험 가중치 (1.3)

### 2.2 기술 숙련도 가중치 (Wlevel)

| 숙련도 | 가중치 |
|--------|--------|
| Beginner | 1.0 |
| Intermediate | 1.5 |
| Advanced | 1.8 |
| Expert | 2.0 |

### 2.3 최신성 가중치 (Wrecency)
```python
Wrecency = e^(-0.3t)
```
- t = 마지막 사용 이후 경과 년수
- 최근 6개월: 약 85% 가중치
- 1년 전: 약 74% 가중치
- 3년 전: 약 41% 가중치

### 2.4 도메인 경험 보너스
- 유사 도메인 프로젝트 경험 시: **+30% 보너스**
- 예: 금융 프로젝트 경험자가 금융 프로젝트에 지원 시

### 2.5 종합 점수 계산
```python
# 가중치 설정 (우선순위에 따라 조정)
if priority == 'skill':
    weights = {'skill': 0.6, 'similarity': 0.3, 'affinity': 0.1}
elif priority == 'affinity':
    weights = {'skill': 0.3, 'similarity': 0.2, 'affinity': 0.5}
else:  # balanced
    weights = {'skill': 0.4, 'similarity': 0.3, 'affinity': 0.3}

overall_score = (
    skill_match_score * weights['skill'] +
    similarity_score * weights['similarity'] +
    affinity_score * weights['affinity']
)
```

### 2.6 구현 위치
- **Lambda 함수**: `recommendation_engine/index.py`
- **주요 함수**:
  - `find_employees_by_skills()`: 가중치 기반 기술 매칭
  - `search_similar_employees()`: 벡터 유사도 검색
  - `merge_and_score_candidates()`: 종합 점수 계산
  - `generate_reasoning()`: Claude를 사용한 추천 근거 생성

### 2.7 추천 근거 생성
Claude (Bedrock)를 사용하여 다음 정보를 포함한 상세 근거 생성:
1. **핵심 강점**: 보유 기술 및 숙련도
2. **프로젝트 적합성**: 도메인 경험 및 유사도
3. **추가 고려사항**: 가용성 및 팀 친밀도

---

## 3. 신규 도메인 추천 (New Domain Opportunity)

### 3.1 실현 가능성 점수 공식
```
Score(D) = (Trend_growth × W_market) - (Gap_skill × W_risk)
```

**실제 구현:**
```python
positive_score = (skill_coverage * market_weight * 0.5 + employee_availability * 0.3) * 100
negative_score = (gap_penalty * risk_weight * 0.2 + core_penalty) * 100
feasibility = max(0, positive_score - negative_score)
```

### 3.2 주요 요소

#### 3.2.1 기술 보유율 (Skill Coverage)
```
skill_coverage = 보유 기술 수 / 필요 기술 수
```

#### 3.2.2 인력 가용성 (Employee Availability)
```
employee_availability = min(1.0, 전환 가능 인력 / 최소 팀 크기)
```
- 최소 팀 크기: 5명

#### 3.2.3 기술 갭 페널티
```
gap_penalty = 부족한 기술 수 / 필요 기술 수
```

#### 3.2.4 핵심 기술 페널티
- 핵심 기술 목록: AWS, Python, Java, React, Database
- 핵심 기술 하나당 **-5% 페널티**

### 3.3 시장 가중치 (W_market)
- 기본값: 1.2 (시장 수요 높음 가정)
- 실제로는 `TechTrends` 테이블에서 동적으로 계산

### 3.4 리스크 가중치 (W_risk)
- 기본값: 1.0
- 진입 장벽이 높은 도메인은 가중치 증가

### 3.5 도메인별 필요 기술

| 도메인 | 필요 기술 |
|--------|-----------|
| Finance | Java, Spring, Oracle, Security, Compliance |
| Healthcare | Python, HIPAA, HL7, FHIR, Data Privacy |
| E-commerce | Node.js, React, MongoDB, Payment Gateway, AWS |
| Manufacturing | IoT, Python, Data Analytics, ERP, MES |
| Logistics | GPS, Route Optimization, Mobile, Real-time Tracking |

### 3.6 구현 위치
- **Lambda 함수**: `domain_analysis/index.py`
- **주요 함수**:
  - `analyze_domain_entry()`: 도메인 진입 분석
  - `calculate_feasibility_score()`: 실현 가능성 점수 계산
  - `generate_domain_reasoning()`: Claude를 사용한 분석 근거 생성

### 3.7 분석 근거 생성
Claude (Bedrock)를 사용하여 다음 정보를 포함한 상세 근거 생성:
1. **현재 강점**: 보유 기술 및 인력
2. **진입 장벽**: 부족한 기술 및 리스크
3. **추천 전략**: 채용, 교육, 파트너십 등

---

## 4. 벡터 검색 (Vector Search)

### 4.1 OpenSearch k-NN 검색
```python
query = {
    "size": 20,
    "query": {
        "knn": {
            "profile_vector": {
                "vector": requirement_vector,
                "k": 20
            }
        }
    }
}
```

### 4.2 임베딩 생성
- **모델**: Amazon Titan Embed Text v1
- **차원**: 1536
- **입력**: 프로젝트 요구사항 또는 직원 프로필 텍스트

### 4.3 하이브리드 검색
벡터 유사도 + 필터링 + 스크립트 점수:
```python
cosineSimilarity(...) * 0.7 + affinity_score * 0.2 + (is_available ? 1.0 : 0.0) * 0.1
```

---

## 5. 배포 및 테스트

### 5.1 Lambda 함수 업데이트
```bash
# 도메인 분석
cd lambda_functions/domain_analysis
Compress-Archive -Path index.py -DestinationPath function.zip -Force
aws lambda update-function-code --function-name DomainAnalysisEngine --zip-file "fileb://function.zip" --region us-east-2

# 추천 엔진
cd lambda_functions/recommendation_engine
Compress-Archive -Path index.py -DestinationPath function.zip -Force
aws lambda update-function-code --function-name ProjectRecommendationEngine --zip-file "fileb://function.zip" --region us-east-2

# 친밀도 계산
cd lambda_functions/affinity_calculator
Compress-Archive -Path index.py -DestinationPath function.zip -Force
aws lambda update-function-code --function-name AffinityScoreCalculator --zip-file "fileb://function.zip" --region us-east-2
```

### 5.2 API 테스트
```bash
# 프로젝트 추천
curl -X POST https://xoc7x1m6p8.execute-api.us-east-2.amazonaws.com/prod/recommendations \
  -H "Content-Type: application/json" \
  -d '{"project_id": "PRJ001", "required_skills": ["Java", "Spring"], "team_size": 5}'

# 도메인 분석
curl -X POST https://xoc7x1m6p8.execute-api.us-east-2.amazonaws.com/prod/domain-analysis \
  -H "Content-Type: application/json" \
  -d '{"employee_id": "U_003", "analysis_type": "skills"}'
```

---

## 6. 모니터링 및 최적화

### 6.1 주요 메트릭
- **추천 정확도**: 실제 투입된 인력과 추천 결과 비교
- **친밀도 점수 분포**: 팀 내 평균 친밀도 추적
- **도메인 진입 성공률**: 추천된 도메인의 실제 진입 여부

### 6.2 로그 확인
```bash
# CloudWatch Logs 확인
aws logs tail /aws/lambda/ProjectRecommendationEngine --follow
aws logs tail /aws/lambda/DomainAnalysisEngine --follow
aws logs tail /aws/lambda/AffinityScoreCalculator --follow
```

### 6.3 가중치 튜닝
- 프로덕션 데이터를 기반으로 가중치 조정
- A/B 테스트를 통한 최적 가중치 탐색

---

## 7. 참고 자료

### 7.1 관련 문서
- `API_DOCUMENTATION.md`: API 엔드포인트 상세 설명
- `DEPLOYMENT_GUIDE.md`: 전체 시스템 배포 가이드
- `MONITORING_GUIDE.md`: 모니터링 및 알림 설정

### 7.2 데이터 모델
- `common/models.py`: 데이터 모델 정의
- `common/repositories.py`: 데이터 접근 레이어

### 7.3 알고리즘 참고
- Node2Vec: 그래프 기반 임베딩
- BERTopic: 토픽 모델링
- HNSW: 고속 벡터 검색

---

## 변경 이력

| 날짜 | 버전 | 변경 내용 |
|------|------|-----------|
| 2025-11-28 | 1.0 | 초기 버전 작성 - 근거 기반 추천 로직 구현 |

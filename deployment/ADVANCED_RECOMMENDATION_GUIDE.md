# 고급 알고리즘 기반 AI 인력 추천 시스템

## 개요
프로젝트 투입 인력 추천 시스템에 고급 알고리즘과 수학적 모델을 적용하여 정확하고 신뢰할 수 있는 추천 근거를 제공합니다.

---

## 1. 프로젝트 투입 추천 (Project Staffing Recommendation)

### 1단계: 적합도 점수 산정 (Feature Engineering)

단순히 기술 보유 여부가 아니라, **숙련도와 최신 경험을 반영한 가중치 공식**을 적용합니다.

#### 기본 공식
```
Score(P, E) = Σ(Smatch × Wlevel × Wrecency) + (Expdomain × Wdomain)
```

**변수 설명:**
- `Smatch`: 요구 기술 일치 여부 (0 or 1)
- `Wlevel`: 기술 숙련도 가중치 (Beginner: 1.0 ~ Expert: 2.0)
- `Wrecency`: 해당 기술 사용의 최신성 (최근 프로젝트 사용 시 가중치 높음)
- `Wdomain`: 프로젝트 산업 도메인(금융, 커머스 등) 경험 유무

#### 가중치 전략

**1) Core Skill 가중치 (W=1.5)**
- 프로젝트의 필수 핵심 기술(예: Java, AWS) 보유 시 가중치 부여

**2) 유사 프로젝트 경험 (W=1.3)**
- 동일한 산업군(Client Industry) 프로젝트 수행 이력에 가점

**3) 시간 감쇠 (Time Decay)**
- 3년 전 사용한 기술보다 최근 6개월 내 사용한 기술에 더 높은 점수 부여
- 공식: `e^(-λt)` (λ = 0.3)

#### 숙련도 가중치 매핑
```
Beginner     → 1.0
Intermediate → 1.5
Advanced     → 1.8
Expert       → 2.0
```

#### 최신성 가중치 계산
```python
import math
from datetime import datetime

current_year = datetime.now().year
end_year = project_end_year
years_ago = current_year - end_year

# 시간 감쇠 적용
w_recency = math.exp(-0.3 * years_ago)

# 예시:
# 최근 6개월: w_recency ≈ 1.0
# 1년 전: w_recency ≈ 0.74
# 3년 전: w_recency ≈ 0.41
```

---

### 2단계: 추천 알고리즘 및 벡터 생성 (Modeling)

프로젝트 요구사항(JD)과 직원 이력서(Resume)의 **의미적 유사성**을 찾기 위해 텍스트 임베딩을 사용합니다.

#### 추천 알고리즘: Content-based Filtering

**사용 모델:**
- SBERT (Sentence-BERT)
- AWS Titan Embeddings

**벡터 생성:**
1. **Project Vector**: 프로젝트 설명 + 요구 기술 텍스트를 임베딩
2. **Employee Vector**: 직원 자기소개 + 보유 기술 + 수행 프로젝트 요약을 임베딩

**이유:**
키워드 매칭의 한계(예: 'React'를 찾는데 'Next.js' 경험자 누락)를 극복하고, 문맥적 적합성을 판단하기 위함.

#### 구현 예시
```python
# AWS Bedrock Titan Embeddings 사용
import boto3
import json

bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-2')

def generate_embedding(text):
    """텍스트를 벡터로 변환"""
    response = bedrock_runtime.invoke_model(
        modelId='amazon.titan-embed-text-v1',
        body=json.dumps({
            'inputText': text
        })
    )
    
    result = json.loads(response['body'].read())
    return result['embedding']

# 프로젝트 벡터 생성
project_text = f"{project_description} {' '.join(required_skills)}"
project_vector = generate_embedding(project_text)

# 직원 벡터 생성
employee_text = f"{employee_intro} {' '.join(employee_skills)} {' '.join(project_summaries)}"
employee_vector = generate_embedding(employee_text)
```

---

### 3단계: OpenSearch 구성 및 쿼리 전략

#### 인덱스 매핑 (Mapping)
```json
{
  "mappings": {
    "properties": {
      "user_id": { "type": "keyword" },
      "skill_vector": { 
        "type": "knn_vector", 
        "dimension": 1536, 
        "method": { 
          "name": "hnsw",
          "space_type": "cosinesimil",
          "engine": "nmslib"
        } 
      },
      "availability_status": { "type": "keyword" },
      "skills": { "type": "text" },
      "years_of_experience": { "type": "integer" }
    }
  }
}
```

#### 추천 쿼리 (k-NN Search)
```json
{
  "size": 20,
  "query": {
    "knn": {
      "skill_vector": {
        "vector": [0.123, 0.456, ...],
        "k": 20
      }
    }
  },
  "filter": {
    "term": {
      "availability_status": "Available"
    }
  }
}
```

---

### 4단계: 하이브리드 추천 (심화 - 벡터 + 필터링)

#### Painless Script Score

벡터 유사도로 1차 후보를 뽑은 뒤, **가용성(Availability) 필터**와 **친밀도(Affinity) 점수**를 보정치로 적용합니다.

```json
{
  "query": {
    "script_score": {
      "query": {
        "knn": {
          "skill_vector": {
            "vector": [0.123, 0.456, ...],
            "k": 50
          }
        }
      },
      "script": {
        "source": """
          double vectorScore = cosineSimilarity(params.query_vector, 'skill_vector');
          double affinityScore = doc['affinity_score'].value;
          double availabilityBonus = doc['availability_status'].value == 'Available' ? 1.0 : 0.0;
          
          return vectorScore * 0.7 + affinityScore * 0.2 + availabilityBonus * 0.1;
        """,
        "params": {
          "query_vector": [0.123, 0.456, ...]
        }
      }
    }
  }
}
```

#### 가중치 배분
- 벡터 유사도: 70%
- 친밀도 점수: 20%
- 가용성 보너스: 10%

---

## 2. 신규 도메인 추천 (New Domain Opportunity)

### 1단계: 시장 기회 점수 산정 (Feature Engineering)

외부 트렌드와 내부 역량의 격차(Gap)를 수치화하여 진입 가능성을 계산합니다.

#### 기본 공식
```
Score(D) = (Trendgrowth × Wmarket) - (Gapskill × Wrisk)
```

**변수 설명:**
- `Trendgrowth`: 기술 트렌드 성장률 (외부 API/크롤링 데이터)
- `Gapskill`: 내부 보유 기술과 해당 도메인 요구 기술 간의 거리
- `Wmarket`: 시장 규모 가중치
- `Wrisk`: 진입 장벽(리스크) 가중치

#### 가중치 전략

**1) 급상승 트렌드 (W=2.0)**
- 최근 3개월 내 검색량/뉴스 언급량이 급증한 키워드

**2) 내부 유사성 (W=1.5)**
- 우리가 이미 잘하는 기술(예: AI)을 활용할 수 있는 인접 도메인(예: AI 의료)인 경우 가점

---

### 2단계: 추천 알고리즘 및 벡터 생성 (Modeling)

시장 뉴스/리포트와 우리 회사의 프로젝트 이력을 **토픽 모델링**하여 비교합니다.

#### 추천 알고리즘: Topic Modeling (BERTopic) & Clustering

**벡터 생성:**
1. **Market Vector**: 최신 기술 블로그, 뉴스 기사들을 크롤링하여 토픽 벡터 생성
2. **Internal Vector**: 우리 회사의 지난 3년간 프로젝트 산출물 요약 벡터

**분석 방법:**
Market Vector 군집 중 Internal Vector가 존재하지 않는 **'빈 공간(White Space)'**을 탐색

#### 구현 예시
```python
from bertopic import BERTopic
from sklearn.cluster import KMeans

# 시장 트렌드 데이터 수집
market_documents = [
    "AI in healthcare diagnostics",
    "Blockchain for supply chain",
    "Edge computing for IoT",
    ...
]

# 내부 프로젝트 데이터
internal_documents = [
    "E-commerce platform development",
    "Financial trading system",
    ...
]

# BERTopic 모델 생성
topic_model = BERTopic()
market_topics, _ = topic_model.fit_transform(market_documents)
internal_topics, _ = topic_model.transform(internal_documents)

# 빈 공간(White Space) 탐색
market_set = set(market_topics)
internal_set = set(internal_topics)
opportunity_topics = market_set - internal_set
```

---

### 3단계: OpenSearch 구성 및 쿼리 전략

#### 인덱스 매핑 (Mapping)
```json
{
  "mappings": {
    "properties": {
      "domain_name": { "type": "keyword" },
      "trend_vector": { 
        "type": "knn_vector", 
        "dimension": 1536 
      },
      "growth_rate": { "type": "float" },
      "market_size": { "type": "float" },
      "entry_barrier": { "type": "keyword" }
    }
  }
}
```

#### 추천 쿼리 (Search)

현재 우리의 핵심 역량 벡터와 **'거리가 멀면서도(새로운 분야)' + '성장률이 높은'** 도메인을 검색

```json
{
  "size": 10,
  "query": {
    "script_score": {
      "query": {
        "bool": {
          "must": [
            {
              "range": {
                "growth_rate": {
                  "gte": 0.2
                }
              }
            }
          ]
        }
      },
      "script": {
        "source": """
          double distance = 1.0 - cosineSimilarity(params.internal_vector, 'trend_vector');
          double growth = doc['growth_rate'].value;
          
          return distance * 0.6 + growth * 0.4;
        """,
        "params": {
          "internal_vector": [0.123, 0.456, ...]
        }
      }
    }
  },
  "sort": [
    {
      "_score": {
        "order": "desc"
      }
    }
  ]
}
```

---

### 4단계: 하이브리드 추천 (심화 - 트렌드 + 전략)

#### 전략적 우선순위 반영

```python
def calculate_domain_opportunity_score(domain):
    """도메인 기회 점수 계산"""
    
    # 1. 시장 성장률
    growth_rate = domain['growth_rate']
    
    # 2. 내부 역량과의 거리 (새로운 정도)
    distance = 1.0 - cosine_similarity(
        internal_capability_vector,
        domain['trend_vector']
    )
    
    # 3. 시장 규모
    market_size = domain['market_size']
    
    # 4. 진입 장벽
    entry_barrier_weights = {
        'Low': 1.0,
        'Medium': 0.7,
        'High': 0.4
    }
    barrier_weight = entry_barrier_weights[domain['entry_barrier']]
    
    # 종합 점수 계산
    opportunity_score = (
        growth_rate * 0.4 +
        distance * 0.3 +
        (market_size / 1000) * 0.2 +
        barrier_weight * 0.1
    )
    
    return opportunity_score
```

---

## 실제 적용 결과

### 추천 근거 예시

```
【1단계: 적합도 점수 산정】
▸ 기본 프로필: 9년 경력의 Security Engineer
▸ 종합 적합도 점수: 61.0/100점

【점수 산정 공식】
Score(P,E) = Σ(Smatch × Wlevel × Wrecency) + (Expdomain × Wdomain)

【기술별 가중치 분석】
  • Python: Expert (5년 경험)
    - 숙련도 가중치(Wlevel): 2.0 (전문가)
    - 최신성 가중치(Wrecency): 최근 프로젝트 활용 반영
    - 기술 점수: 1.85점
  • React: Advanced (3년 경험)
    - 숙련도 가중치(Wlevel): 1.8 (고급)
    - 최신성 가중치(Wrecency): 최근 프로젝트 활용 반영
    - 기술 점수: 1.62점

【2단계: 추천 알고리즘】
▸ 알고리즘: Content-based Filtering
▸ 매칭된 핵심 기술: Python, React

【3단계: 하이브리드 점수】
▸ 팀 친밀도: 신규 팀원 (친밀도 데이터 없음)

【4단계: 가용성 필터】
▸ 상태: 즉시 투입 가능 ✓
  - 가용성 가중치: 1.0 (최대)

【최종 추천 근거】
✓ 적정 기술 적합도 (61.0점)
✓ 즉시 투입 가능
```

---

## 향후 개선 방향

### 1. OpenSearch 벡터 검색 통합
- 현재: 기술 매칭 기반
- 개선: OpenSearch k-NN 검색 추가

### 2. 실시간 트렌드 분석
- 외부 API 연동 (Google Trends, Stack Overflow Trends)
- 뉴스 크롤링 및 토픽 모델링

### 3. 강화학습 적용
- 추천 결과에 대한 피드백 수집
- 모델 지속적 개선

### 4. 설명 가능한 AI (XAI)
- SHAP, LIME 등을 활용한 추천 근거 시각화
- 의사결정 투명성 강화

---

## 참고 자료

- [OpenSearch k-NN Plugin](https://opensearch.org/docs/latest/search-plugins/knn/)
- [AWS Bedrock Titan Embeddings](https://docs.aws.amazon.com/bedrock/latest/userguide/titan-embedding-models.html)
- [BERTopic Documentation](https://maartengr.github.io/BERTopic/)
- [Content-based Filtering](https://en.wikipedia.org/wiki/Recommender_system#Content-based_filtering)

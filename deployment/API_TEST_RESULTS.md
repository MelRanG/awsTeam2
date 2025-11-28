# API 테스트 결과

## 테스트 일시
2025-11-28

## API Gateway URL
https://xoc7x1m6p8.execute-api.us-east-2.amazonaws.com/prod

## 프론트엔드 URL
http://hr-resource-optimization-frontend-hosting-prod.s3-website.us-east-2.amazonaws.com

## 엔드포인트 테스트 결과

### ✅ 1. Domain Analysis API
- **엔드포인트**: POST /domain-analysis
- **상태**: 정상 작동
- **요청 예시**:
```json
{
  "employee_id": "U_003",
  "analysis_type": "skills"
}
```
- **응답**: 현재 도메인 및 추천 도메인 반환

### ✅ 2. Quantitative Analysis API
- **엔드포인트**: POST /quantitative-analysis
- **상태**: 정상 작동
- **요청 예시**:
```json
{
  "user_id": "U_003"
}
```
- **응답**: 경력 메트릭, 기술 평가, 프로젝트 점수 반환
- **결과 예시**:
  - 경력: 11년
  - 프로젝트 수: 1개
  - 기술 다양성: 5개
  - 종합 점수: 47.37

### ✅ 3. Qualitative Analysis API
- **엔드포인트**: POST /qualitative-analysis
- **상태**: 정상 작동 (일부 분석 오류)
- **요청 예시**:
```json
{
  "user_id": "U_003"
}
```
- **응답**: 강점, 약점, 적합 프로젝트, 개발 영역 분석
- **주의사항**: 프로젝트 수 불일치 플래그 발생

### ❌ 4. Recommendations API
- **엔드포인트**: POST /recommendations
- **상태**: Internal Server Error
- **요청 예시**:
```json
{
  "project_id": "PRJ002"
}
```
- **문제**: Lambda 함수 내부 오류 발생
- **조치 필요**: Lambda 로그 확인 및 코드 수정 필요

## Lambda 이벤트 소스 매핑 상태

### ✅ Employees 테이블 스트림
- **UUID**: 2a805865-4e67-4d98-ab24-5aad1eb414e6
- **상태**: Enabled
- **Lambda**: VectorEmbeddingGenerator
- **스트림 ARN**: arn:aws:dynamodb:us-east-2:412677576136:table/Employees/stream/2025-11-26T07:43:21.370

### ⚠️ MessengerLogs 테이블 스트림
- **UUID**: cd650e84-58fd-4e5c-ac1e-219976d243ea
- **상태**: Disabled (스트림 종료됨)
- **Lambda**: VectorEmbeddingGenerator
- **스트림 ARN**: arn:aws:dynamodb:us-east-2:412677576136:table/MessengerLogs/stream/2025-11-28T04:54:25.355
- **조치 필요**: 새로운 스트림 ARN으로 매핑 재생성 필요

## DynamoDB 테이블 상태

### ✅ 데이터 로드 완료
- Employees: 데이터 있음 (U_003: 박민수)
- Projects: 데이터 있음 (PRJ002)
- CompanyEvents: 생성됨
- EmployeeAffinity: 생성됨
- MessengerLogs: 생성됨 (스트림 활성화됨)
- TechTrends: 생성됨

## 다음 단계

1. **Recommendations Lambda 수정**: Internal Server Error 원인 파악 및 수정
2. **MessengerLogs 스트림 매핑 재생성**: 현재 스트림이 종료되어 새로운 매핑 필요
3. **프론트엔드 테스트**: 브라우저에서 프론트엔드 접속 및 API 연동 확인
4. **추가 테스트 데이터 로드**: 더 많은 직원 및 프로젝트 데이터 추가

## 테스트 명령어

### API 테스트
```powershell
# Domain Analysis
Invoke-RestMethod -Uri "https://xoc7x1m6p8.execute-api.us-east-2.amazonaws.com/prod/domain-analysis" -Method Post -Headers @{"Content-Type"="application/json"} -Body '{"employee_id":"U_003","analysis_type":"skills"}'

# Quantitative Analysis
Invoke-RestMethod -Uri "https://xoc7x1m6p8.execute-api.us-east-2.amazonaws.com/prod/quantitative-analysis" -Method Post -Headers @{"Content-Type"="application/json"} -Body '{"user_id":"U_003"}'

# Qualitative Analysis
Invoke-RestMethod -Uri "https://xoc7x1m6p8.execute-api.us-east-2.amazonaws.com/prod/qualitative-analysis" -Method Post -Headers @{"Content-Type"="application/json"} -Body '{"user_id":"U_003"}'
```

### Lambda 이벤트 소스 매핑 확인
```powershell
aws lambda list-event-source-mappings --function-name VectorEmbeddingGenerator --region us-east-2
```

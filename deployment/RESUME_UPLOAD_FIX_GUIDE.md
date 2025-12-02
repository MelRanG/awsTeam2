# 이력서 업로드 403 에러 해결 가이드

## 문제 상황
PDF 파일 업로드 시 403 Forbidden 에러 발생

## 원인 분석
1. **S3 버킷 CORS 설정 부족** - PUT 메서드 허용 필요
2. **Presigned URL 권한 문제** - ACL 관련 권한 충돌
3. **버킷 정책 미설정** - Lambda가 생성한 URL의 권한 부족

## 해결 방법

### 1단계: S3 버킷 CORS 설정 수정

```bash
python deployment/fix_resume_bucket_cors.py
```

이 스크립트는 다음을 수행합니다:
- PUT, POST, DELETE 메서드 허용
- 모든 헤더 허용
- CORS 설정 확인

### 2단계: Lambda 함수 업데이트

```bash
python deployment/update_resume_upload_lambda.py
```

변경 사항:
- ACL 없이 Presigned URL 생성
- HttpMethod 명시적 지정
- 권한 충돌 방지

### 3단계: 프론트엔드 재배포

```powershell
# 빌드 폴더 삭제 후 재배포
.\rebuild_and_deploy.ps1

# 또는 빠른 배포
.\force_deploy.ps1
```

### 4단계: 테스트

```bash
python deployment/test_resume_upload.py
```

## 추가 개선 사항

### 모달 배경 가독성 개선
- 배경 투명도: `bg-black/70` → `bg-black/80`
- 블러 효과: `backdrop-blur-md` → `backdrop-blur-sm`
- 인력 등록 모달과 동일한 스타일 적용

### 배포 스크립트 개선
모든 배포 스크립트에 빌드 폴더 자동 삭제 기능 추가:
- `rebuild_and_deploy.ps1` ✓
- `force_deploy.ps1` ✓
- `deploy_now.ps1` ✓
- `simple_deploy.ps1` ✓
- `clean_and_deploy.ps1` ✓

## 배포 스크립트 사용법

### rebuild_and_deploy.ps1 (권장)
완전히 새로 빌드하고 배포
```powershell
.\rebuild_and_deploy.ps1
```

### force_deploy.ps1
강제 재배포 (캐시 무시)
```powershell
.\force_deploy.ps1
```

### deploy_now.ps1
빠른 배포 (캐시 활용)
```powershell
.\deploy_now.ps1
```

### simple_deploy.ps1
간단한 배포
```powershell
.\simple_deploy.ps1
```

### clean_and_deploy.ps1
캐시 삭제 후 배포
```powershell
.\clean_and_deploy.ps1
```

## 문제 해결 체크리스트

- [ ] S3 버킷 CORS 설정 확인
- [ ] Lambda 함수 환경 변수 확인 (RESUMES_BUCKET)
- [ ] Lambda 함수 IAM 역할에 S3 권한 있는지 확인
- [ ] 프론트엔드 API URL 설정 확인 (.env 파일)
- [ ] 브라우저 캐시 삭제 후 테스트
- [ ] 네트워크 탭에서 실제 요청/응답 확인

## 참고 사항

### S3 Presigned URL 생성 시 주의사항
1. ACL 파라미터 제거 (버킷 정책으로 관리)
2. ContentType 명시적 지정
3. HttpMethod 명시 (PUT)
4. 적절한 만료 시간 설정 (3600초)

### CORS 설정 필수 항목
- AllowedMethods: GET, PUT, POST, DELETE, HEAD
- AllowedOrigins: * (프로덕션에서는 특정 도메인으로 제한)
- AllowedHeaders: *
- ExposeHeaders: ETag, x-amz-* 헤더들

## 추가 도움말

문제가 계속되면:
1. CloudWatch Logs에서 Lambda 로그 확인
2. S3 버킷 액세스 로그 활성화
3. API Gateway 로그 확인
4. 브라우저 개발자 도구 네트워크 탭 확인

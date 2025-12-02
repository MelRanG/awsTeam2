# 변경 사항 요약

## 1. 배포 스크립트 개선 ✅

모든 배포 스크립트에 **빌드 폴더 자동 삭제** 기능 추가:

### 수정된 파일
- `rebuild_and_deploy.ps1` - 이미 포함되어 있음
- `force_deploy.ps1` - 빌드 폴더 삭제 및 재빌드 추가
- `deploy_now.ps1` - 빌드 폴더 삭제 및 재빌드 추가
- `simple_deploy.ps1` - 빌드 폴더 삭제 및 재빌드 추가
- `clean_and_deploy.ps1` - 이미 포함되어 있음

### 동작 방식
```powershell
# 1. 기존 빌드 폴더 삭제
if (Test-Path "frontend/build") {
    Remove-Item -Path "frontend/build" -Recurse -Force
}

# 2. 새로 빌드
Set-Location frontend
npm run build
Set-Location ..

# 3. S3에 업로드
```

## 2. 모달 배경 가독성 개선 ✅

### ResumeUploadModal.tsx 수정
```tsx
// 변경 전
bg-black/70 backdrop-blur-md

// 변경 후
bg-black/80 backdrop-blur-sm
```

**효과:**
- 배경이 더 어두워져서 모달 내용이 더 잘 보임
- 인력 등록 모달과 동일한 스타일
- 가독성 향상

## 3. PDF 업로드 403 에러 해결 🔧

### Lambda 함수 수정 (resume_upload/index.py)
```python
# Presigned URL 생성 시 ACL 제거
presigned_url = s3_client.generate_presigned_url(
    'put_object',
    Params={
        'Bucket': RESUMES_BUCKET,
        'Key': file_key,
        'ContentType': content_type,
        # ACL 제거 - 버킷 정책으로 관리
    },
    ExpiresIn=3600,
    HttpMethod='PUT'  # 명시적 지정
)
```

### 새로운 스크립트 추가

1. **fix_resume_bucket_cors.py**
   - S3 버킷 CORS 설정 수정
   - PUT, POST, DELETE 메서드 허용
   - 버킷 정책 및 퍼블릭 액세스 설정 확인

2. **update_resume_upload_lambda.py**
   - Lambda 함수 코드 자동 업데이트
   - 환경 변수 확인
   - 배포 패키지 생성 및 업로드

3. **test_resume_upload.py**
   - Presigned URL 생성 테스트
   - 실제 파일 업로드 테스트
   - CORS 헤더 확인

4. **RESUME_UPLOAD_FIX_GUIDE.md**
   - 상세한 문제 해결 가이드
   - 단계별 해결 방법
   - 체크리스트 제공

## 실행 순서

### 1. S3 CORS 설정 수정
```bash
python deployment/fix_resume_bucket_cors.py
```

### 2. Lambda 함수 업데이트
```bash
python deployment/update_resume_upload_lambda.py
```

### 3. 프론트엔드 재배포
```powershell
.\rebuild_and_deploy.ps1
```

### 4. 테스트
```bash
python deployment/test_resume_upload.py
```

## 예상 결과

✅ 배포 시 항상 최신 빌드 생성
✅ 모달 배경이 더 어두워져 가독성 향상
✅ PDF 업로드 403 에러 해결
✅ 이력서 업로드 정상 작동

## 주의 사항

1. **API Gateway URL 확인**
   - `test_resume_upload.py`에서 실제 API URL로 변경 필요

2. **테스트 파일 준비**
   - PDF 파일을 `test_data/sample_resume.pdf`에 준비

3. **브라우저 캐시**
   - 배포 후 브라우저 캐시 삭제 또는 시크릿 모드 사용

4. **Lambda 권한 확인**
   - Lambda 실행 역할에 S3 PutObject 권한 필요
   - `s3:PutObject`, `s3:GetObject` 권한 확인

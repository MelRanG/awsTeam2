# 수동 설정 가이드

## AWS CLI가 없는 경우 AWS Console에서 직접 설정

### 1. S3 버킷 CORS 설정

1. **AWS Console 접속**
   - https://console.aws.amazon.com/s3/
   - `hr-resource-optimization-resumes-prod` 버킷 선택

2. **권한(Permissions) 탭 클릭**

3. **CORS(Cross-origin resource sharing) 섹션에서 편집 클릭**

4. **다음 설정 붙여넣기:**

```json
[
    {
        "AllowedHeaders": ["*"],
        "AllowedMethods": ["GET", "PUT", "POST", "DELETE", "HEAD"],
        "AllowedOrigins": ["*"],
        "ExposeHeaders": [
            "ETag",
            "x-amz-server-side-encryption",
            "x-amz-request-id",
            "x-amz-id-2"
        ],
        "MaxAgeSeconds": 3000
    }
]
```

5. **변경 사항 저장 클릭**

### 2. Lambda 함수 업데이트

1. **AWS Console 접속**
   - https://console.aws.amazon.com/lambda/
   - `resume_upload` 함수 선택

2. **코드 소스 섹션에서 index.py 열기**

3. **다음 부분 수정:**

기존 코드:
```python
presigned_url = s3_client.generate_presigned_url(
    'put_object',
    Params={
        'Bucket': RESUMES_BUCKET,
        'Key': file_key,
        'ContentType': content_type
    },
    ExpiresIn=3600
)
```

수정된 코드:
```python
presigned_url = s3_client.generate_presigned_url(
    'put_object',
    Params={
        'Bucket': RESUMES_BUCKET,
        'Key': file_key,
        'ContentType': content_type,
    },
    ExpiresIn=3600,
    HttpMethod='PUT'
)
```

4. **Deploy 버튼 클릭**

### 3. 프론트엔드 빌드 및 배포

로컬에서 실행:

```powershell
# 빌드 폴더 삭제
Remove-Item -Path "frontend/build" -Recurse -Force -ErrorAction SilentlyContinue

# 새로 빌드
cd frontend
npm run build
cd ..

# S3에 업로드 (AWS CLI 필요)
# 또는 AWS Console에서 수동 업로드
```

### 4. AWS Console에서 수동 업로드 방법

1. **S3 Console 접속**
   - https://console.aws.amazon.com/s3/
   - `hr-resource-optimization-frontend-hosting-prod` 버킷 선택

2. **기존 파일 모두 삭제**
   - 모든 파일 선택 → 삭제

3. **새 파일 업로드**
   - 업로드 버튼 클릭
   - `frontend/build` 폴더의 모든 파일 선택
   - 업로드

4. **캐시 설정**
   - 업로드된 파일들 선택
   - 작업 → 메타데이터 편집
   - Cache-Control: `no-cache, no-store, must-revalidate`

## 확인 사항

- [ ] S3 버킷 CORS 설정 완료
- [ ] Lambda 함수 코드 업데이트 완료
- [ ] 프론트엔드 빌드 및 배포 완료
- [ ] 브라우저 캐시 삭제 후 테스트

## 테스트

1. 브라우저 시크릿 모드로 접속
2. 이력서 업로드 모달 열기
3. PDF 파일 업로드 시도
4. 403 에러 없이 정상 업로드 확인

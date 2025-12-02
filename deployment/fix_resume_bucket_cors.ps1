# 이력서 업로드 S3 버킷 CORS 설정 수정
# 403 Forbidden 에러 해결

$BucketName = "hr-resource-optimization-resumes-prod"
$Region = "us-east-2"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "S3 버킷 CORS 설정 수정" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan

# CORS 설정 JSON 파일 생성
$corsConfig = @"
{
    "CORSRules": [
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
}
"@

# 임시 파일에 저장
$tempFile = [System.IO.Path]::GetTempFileName()
$corsConfig | Out-File -FilePath $tempFile -Encoding UTF8

Write-Host "`n[1/3] CORS 설정 적용 중..." -ForegroundColor Yellow
try {
    aws s3api put-bucket-cors --bucket $BucketName --cors-configuration file://$tempFile --region $Region
    Write-Host "✓ CORS 설정 완료" -ForegroundColor Green
} catch {
    Write-Host "✗ CORS 설정 실패: $_" -ForegroundColor Red
    Remove-Item $tempFile -ErrorAction SilentlyContinue
    exit 1
}

# 임시 파일 삭제
Remove-Item $tempFile -ErrorAction SilentlyContinue

Write-Host "`n[2/3] CORS 설정 확인 중..." -ForegroundColor Yellow
aws s3api get-bucket-cors --bucket $BucketName --region $Region

Write-Host "`n[3/3] 버킷 정책 확인 중..." -ForegroundColor Yellow
try {
    aws s3api get-bucket-policy --bucket $BucketName --region $Region
} catch {
    Write-Host "버킷 정책이 설정되지 않았습니다." -ForegroundColor Yellow
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "완료!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan

$BucketName = "hr-resource-optimization-resumes-prod"
$Region = "us-east-2"
$CorsConfigPath = Join-Path $PSScriptRoot "cors-config.json"

Write-Host "S3 CORS 설정 업데이트 중..." -ForegroundColor Yellow
Write-Host "CORS 파일 경로: $CorsConfigPath" -ForegroundColor Cyan

& "C:\Program Files\Amazon\AWSCLIV2\aws.exe" s3api put-bucket-cors `
    --bucket $BucketName `
    --cors-configuration "file://$CorsConfigPath" `
    --region $Region

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ CORS 설정 완료!" -ForegroundColor Green
    
    Write-Host "`nCORS 설정 확인 중..." -ForegroundColor Yellow
    & "C:\Program Files\Amazon\AWSCLIV2\aws.exe" s3api get-bucket-cors `
        --bucket $BucketName `
        --region $Region
} else {
    Write-Host "✗ CORS 설정 실패" -ForegroundColor Red
}

Write-Host "S3 CORS 설정 업데이트 중..." -ForegroundColor Yellow

$env:AWS_PAGER = ""

aws s3api put-bucket-cors --bucket hr-resource-optimization-resumes-prod --cors-configuration file://cors-config.json --region us-east-2

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✓ CORS 설정 완료!" -ForegroundColor Green
    
    Write-Host "`nCORS 설정 확인:" -ForegroundColor Yellow
    aws s3api get-bucket-cors --bucket hr-resource-optimization-resumes-prod --region us-east-2
} else {
    Write-Host "`n✗ CORS 설정 실패 (Exit Code: $LASTEXITCODE)" -ForegroundColor Red
}

$S3Bucket = "hr-resource-optimization-frontend-hosting-prod"
$AwsRegion = "us-east-2"

Write-Host "========================================" -ForegroundColor Red
Write-Host "강제 업데이트 시작" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Red

# 1. S3 완전히 비우기
Write-Host "`n[1/3] S3 버킷 완전히 비우기..." -ForegroundColor Yellow
aws s3 rm s3://$S3Bucket/ --recursive --region $AwsRegion
Write-Host "✓ S3 비우기 완료" -ForegroundColor Green

# 2. 업로드 (캐시 완전 비활성화)
Write-Host "`n[2/3] 새 파일 업로드 (캐시 비활성화)..." -ForegroundColor Yellow
aws s3 sync frontend/build/ s3://$S3Bucket `
    --region $AwsRegion `
    --delete `
    --cache-control "no-cache, no-store, must-revalidate, max-age=0" `
    --metadata-directive REPLACE
Write-Host "✓ 업로드 완료" -ForegroundColor Green

# 3. 확인
Write-Host "`n[3/3] 업로드된 파일 확인..." -ForegroundColor Yellow
aws s3 ls s3://$S3Bucket/ --region $AwsRegion --recursive
Write-Host "✓ 확인 완료" -ForegroundColor Green

$timestamp = Get-Date -Format "yyyyMMddHHmmss"
Write-Host "`n========================================" -ForegroundColor Red
Write-Host "배포 완료!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Red
Write-Host "`n🔥 반드시 이렇게 접속하세요:" -ForegroundColor Yellow
Write-Host "1. 브라우저 완전 종료" -ForegroundColor White
Write-Host "2. 브라우저 재시작" -ForegroundColor White
Write-Host "3. 이 URL로 접속:" -ForegroundColor White
Write-Host "   http://$S3Bucket.s3-website.$AwsRegion.amazonaws.com/?nocache=$timestamp" -ForegroundColor Cyan
Write-Host "`n또는 시크릿 모드로 접속하세요!" -ForegroundColor Yellow

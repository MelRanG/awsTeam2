$S3Bucket = "hr-resource-optimization-frontend-hosting-prod"
$AwsRegion = "us-east-2"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "완전 새로 빌드 및 배포" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan

# 1. node_modules/.vite 캐시 삭제
Write-Host "`n[1/4] Vite 캐시 삭제..." -ForegroundColor Yellow
if (Test-Path "frontend/node_modules/.vite") {
    Remove-Item -Path "frontend/node_modules/.vite" -Recurse -Force
    Write-Host "캐시 삭제 완료!" -ForegroundColor Green
} else {
    Write-Host "캐시 없음 (정상)" -ForegroundColor Green
}

# 2. 새로 빌드
Write-Host "`n[2/4] 새로 빌드 중..." -ForegroundColor Yellow
Set-Location frontend
npm run build
Set-Location ..
Write-Host "빌드 완료!" -ForegroundColor Green

# 3. S3 버킷 비우기
Write-Host "`n[3/4] S3 버킷 비우는 중..." -ForegroundColor Yellow
aws s3 rm s3://$S3Bucket/ --recursive --region $AwsRegion
Write-Host "S3 비우기 완료!" -ForegroundColor Green

# 4. 새 파일 업로드 (캐시 없음)
Write-Host "`n[4/4] S3에 업로드 중..." -ForegroundColor Yellow
aws s3 sync frontend/build/ s3://$S3Bucket --region $AwsRegion --cache-control "no-cache, no-store, must-revalidate"
Write-Host "업로드 완료!" -ForegroundColor Green

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "배포 완료!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "`n업로드된 파일:" -ForegroundColor Yellow
aws s3 ls s3://$S3Bucket/ --region $AwsRegion --recursive

$timestamp = Get-Date -Format "yyyyMMddHHmmss"
Write-Host "`n🔥 이 URL로 접속하세요:" -ForegroundColor Yellow
Write-Host "http://$S3Bucket.s3-website.$AwsRegion.amazonaws.com/?v=$timestamp" -ForegroundColor Green

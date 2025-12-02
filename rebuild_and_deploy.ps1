# 완전히 새로 빌드하고 배포하는 스크립트

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "프론트엔드 완전 재빌드 및 배포" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan

$S3Bucket = "hr-resource-optimization-frontend-hosting-prod"
$AwsRegion = "us-east-2"

# 1. Vite 캐시 삭제 (빌드 폴더는 Vite가 자동으로 재생성)
Write-Host "`n[1/4] Vite 캐시 삭제 중..." -ForegroundColor Yellow
if (Test-Path "frontend/node_modules/.vite") {
    Remove-Item -Path "frontend/node_modules/.vite" -Recurse -Force
    Write-Host "✓ Vite 캐시 삭제 완료" -ForegroundColor Green
} else {
    Write-Host "✓ Vite 캐시 없음 (정상)" -ForegroundColor Green
}

# 2. 새로 빌드
Write-Host "`n[2/4] 프론트엔드 빌드 중..." -ForegroundColor Yellow
Set-Location frontend
npm run build
Set-Location ..
Write-Host "✓ 빌드 완료" -ForegroundColor Green

# 3. S3 버킷 완전히 비우기
Write-Host "`n[3/4] S3 버킷 기존 파일 삭제 중..." -ForegroundColor Yellow
aws s3 rm s3://$S3Bucket/ --recursive --region $AwsRegion
Write-Host "✓ 기존 파일 삭제 완료" -ForegroundColor Green

# 4. 새 파일 업로드 (캐시 완전 무효화)
Write-Host "`n[4/4] S3에 새 파일 업로드 중..." -ForegroundColor Yellow
aws s3 sync frontend/build/ s3://$S3Bucket --region $AwsRegion --cache-control "no-cache, no-store, must-revalidate, max-age=0" --metadata-directive REPLACE
Write-Host "✓ 업로드 완료" -ForegroundColor Green

$timestamp = Get-Date -Format "yyyyMMddHHmmss"
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "배포 완료!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "`nURL: http://$S3Bucket.s3-website.$AwsRegion.amazonaws.com/?v=$timestamp" -ForegroundColor Cyan
Write-Host "`n⚠️  브라우저 완전 재시작 또는 시크릿 모드로 접속하세요!" -ForegroundColor Yellow

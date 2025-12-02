$S3Bucket = "hr-resource-optimization-frontend-hosting-prod"
$AwsRegion = "us-east-2"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "강제 재배포 시작" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan

# 1. 기존 빌드 폴더 삭제
Write-Host "`n[1/4] 기존 빌드 폴더 삭제 중..." -ForegroundColor Yellow
if (Test-Path "frontend/build") {
    Remove-Item -Path "frontend/build" -Recurse -Force
    Write-Host "✓ 빌드 폴더 삭제 완료" -ForegroundColor Green
}

# 2. 새로 빌드
Write-Host "`n[2/4] 프론트엔드 빌드 중..." -ForegroundColor Yellow
Set-Location frontend
npm run build
Set-Location ..
Write-Host "✓ 빌드 완료" -ForegroundColor Green

# 3. S3 버킷 완전히 비우기
Write-Host "`n[3/4] S3 버킷 비우는 중..." -ForegroundColor Yellow
aws s3 rm s3://$S3Bucket/ --recursive --region $AwsRegion
Write-Host "완료!" -ForegroundColor Green

# 4. 정적 파일 업로드 (캐시 없음으로 변경)
Write-Host "`n[4/4] 정적 파일 업로드 중..." -ForegroundColor Yellow
aws s3 sync frontend/build/ s3://$S3Bucket --region $AwsRegion --cache-control "no-cache, no-store, must-revalidate" --delete
Write-Host "완료!" -ForegroundColor Green

# 5. 확인
Write-Host "`n[5/5] 업로드된 파일 확인..." -ForegroundColor Yellow
aws s3 ls s3://$S3Bucket/ --region $AwsRegion --recursive
Write-Host "완료!" -ForegroundColor Green

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "배포 완료!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "`n⚠️  브라우저에서 다음을 시도하세요:" -ForegroundColor Yellow
Write-Host "1. Ctrl + Shift + Delete (브라우저 데이터 삭제)" -ForegroundColor White
Write-Host "2. 시크릿 모드로 접속" -ForegroundColor White
Write-Host "3. URL 끝에 ?v=$(Get-Date -Format 'yyyyMMddHHmmss') 추가" -ForegroundColor White

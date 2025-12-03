# 프론트엔드 빌드 및 배포 스크립트

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "프론트엔드 빌드 및 배포" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

# 1. 프론트엔드 디렉토리로 이동
Write-Host "`n[1단계] 프론트엔드 빌드 중..." -ForegroundColor Yellow
Set-Location -Path "frontend"

# 2. 빌드 실행
npm run build

if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ 빌드 실패!" -ForegroundColor Red
    Set-Location -Path ".."
    exit 1
}

Write-Host "✓ 빌드 완료!" -ForegroundColor Green

# 3. 상위 디렉토리로 이동
Set-Location -Path ".."

# 4. S3 배포
Write-Host "`n[2단계] S3 배포 중..." -ForegroundColor Yellow
python deploy_frontend_boto3.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ 배포 실패!" -ForegroundColor Red
    exit 1
}

Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "✓ 빌드 및 배포 완료!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "`nURL: http://hr-resource-optimization-frontend-hosting-prod.s3-website.us-east-2.amazonaws.com/" -ForegroundColor Cyan
Write-Host "⚠️  브라우저 캐시를 삭제하거나 시크릿 모드로 접속하세요!" -ForegroundColor Yellow

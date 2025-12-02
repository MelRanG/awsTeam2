$S3Bucket = "hr-resource-optimization-frontend-hosting-prod"
$AwsRegion = "us-east-2"

# 기존 빌드 폴더 삭제
Write-Host "기존 빌드 폴더 삭제 중..." -ForegroundColor Yellow
if (Test-Path "frontend/build") {
    Remove-Item -Path "frontend/build" -Recurse -Force
    Write-Host "✓ 빌드 폴더 삭제 완료" -ForegroundColor Green
}

# 새로 빌드
Write-Host "프론트엔드 빌드 중..." -ForegroundColor Yellow
Set-Location frontend
npm run build
Set-Location ..
Write-Host "✓ 빌드 완료" -ForegroundColor Green

Write-Host "정적 파일 업로드 중..." -ForegroundColor Yellow
aws s3 sync frontend/build/ s3://$S3Bucket --region $AwsRegion --delete --cache-control "public, max-age=31536000" --exclude "index.html"

Write-Host "index.html 업로드 중..." -ForegroundColor Yellow
aws s3 cp frontend/build/index.html s3://$S3Bucket/index.html --region $AwsRegion --cache-control "no-cache, no-store, must-revalidate" --content-type "text/html"

Write-Host "배포 완료!" -ForegroundColor Green

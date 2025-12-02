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

Write-Host "S3 버킷 비우기..." -ForegroundColor Yellow
aws s3 rm s3://$S3Bucket/ --recursive --region $AwsRegion

Write-Host "새 파일 업로드..." -ForegroundColor Yellow
aws s3 sync frontend/build/ s3://$S3Bucket --region $AwsRegion --delete --cache-control "no-cache, no-store, must-revalidate"

Write-Host "완료!" -ForegroundColor Green
aws s3 ls s3://$S3Bucket/ --region $AwsRegion --recursive

$timestamp = Get-Date -Format "yyyyMMddHHmmss"
Write-Host "`nURL: http://$S3Bucket.s3-website.$AwsRegion.amazonaws.com/?t=$timestamp" -ForegroundColor Cyan

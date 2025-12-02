$S3Bucket = "hr-resource-optimization-frontend-hosting-prod"
$AwsRegion = "us-east-2"

Write-Host "1. Vite 캐시 삭제..." -ForegroundColor Yellow
Remove-Item -Path "frontend/node_modules/.vite" -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "완료!" -ForegroundColor Green

Write-Host "`n2. 새로 빌드..." -ForegroundColor Yellow
Set-Location frontend
npm run build
Set-Location ..
Write-Host "완료!" -ForegroundColor Green

Write-Host "`n3. S3 비우기..." -ForegroundColor Yellow
aws s3 rm s3://$S3Bucket/ --recursive --region $AwsRegion
Write-Host "완료!" -ForegroundColor Green

Write-Host "`n4. 업로드..." -ForegroundColor Yellow
aws s3 sync frontend/build/ s3://$S3Bucket --region $AwsRegion --cache-control "no-cache"
Write-Host "완료!" -ForegroundColor Green

Write-Host "`n업로드된 파일:" -ForegroundColor Cyan
aws s3 ls s3://$S3Bucket/ --region $AwsRegion --recursive

$timestamp = Get-Date -Format "yyyyMMddHHmmss"
Write-Host "`n=== 이 URL로 접속하세요 ===" -ForegroundColor Green
Write-Host "http://$S3Bucket.s3-website.$AwsRegion.amazonaws.com/?v=$timestamp" -ForegroundColor Cyan

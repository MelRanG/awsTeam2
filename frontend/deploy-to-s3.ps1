# HR Resource Optimization Frontend - S3 배포 스크립트 (PowerShell)

param(
    [string]$S3Bucket = "hr-frontend-team2",
    [string]$AwsRegion = "us-east-2",
    [string]$CloudFrontDistId = ""
)

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Green
Write-Host "HR Frontend S3 배포 시작" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

# 1. 환경 변수 확인
if (-not (Test-Path ".env")) {
    Write-Host "경고: .env 파일이 없습니다. .env.example을 참고하여 생성하세요." -ForegroundColor Yellow
}

# 2. 의존성 설치
Write-Host "`n[1/4] 의존성 설치 중..." -ForegroundColor Yellow
npm install

# 3. 프로덕션 빌드
Write-Host "`n[2/4] 프로덕션 빌드 중..." -ForegroundColor Yellow
npm run build

# 4. S3에 업로드
Write-Host "`n[3/4] S3 버킷에 업로드 중..." -ForegroundColor Yellow
Write-Host "버킷: s3://$S3Bucket"
Write-Host "리전: $AwsRegion"

# 정적 파일 업로드 (캐시 적용)
aws s3 sync dist/ s3://$S3Bucket `
    --region $AwsRegion `
    --delete `
    --cache-control "public, max-age=31536000" `
    --exclude "index.html" `
    --exclude "*.map"

# index.html은 캐시 없이 업로드
aws s3 cp dist/index.html s3://$S3Bucket/index.html `
    --region $AwsRegion `
    --cache-control "no-cache, no-store, must-revalidate" `
    --content-type "text/html"

Write-Host "✓ S3 업로드 완료" -ForegroundColor Green

# 5. CloudFront 캐시 무효화 (선택사항)
if ($CloudFrontDistId) {
    Write-Host "`n[4/4] CloudFront 캐시 무효화 중..." -ForegroundColor Yellow
    Write-Host "Distribution ID: $CloudFrontDistId"
    
    aws cloudfront create-invalidation `
        --distribution-id $CloudFrontDistId `
        --paths "/*"
    
    Write-Host "✓ CloudFront 캐시 무효화 완료" -ForegroundColor Green
} else {
    Write-Host "`n[4/4] CloudFront 캐시 무효화 건너뛰기 (CloudFrontDistId 미설정)" -ForegroundColor Yellow
}

# 완료
Write-Host "`n========================================" -ForegroundColor Green
Write-Host "배포 완료!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "S3 URL: http://$S3Bucket.s3-website.$AwsRegion.amazonaws.com"

if ($CloudFrontDistId) {
    Write-Host "CloudFront URL: https://your-cloudfront-domain.cloudfront.net"
}

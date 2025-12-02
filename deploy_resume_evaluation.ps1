$env:AWS_PAGER = ""
$Region = "us-east-2"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "이력서 평가 기능 배포" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan

# 1. Lambda 배포 패키지 생성
Write-Host "`n[1/3] Lambda 배포 패키지 생성 중..." -ForegroundColor Yellow

$tempDir = "temp_lambda_parse"
if (Test-Path $tempDir) {
    Remove-Item -Path $tempDir -Recurse -Force
}
New-Item -ItemType Directory -Path $tempDir | Out-Null

Copy-Item -Path "lambda_functions\resume_parse_evaluate\index.py" -Destination "$tempDir\index.py"

$zipPath = "resume_parse_evaluate.zip"
if (Test-Path $zipPath) {
    Remove-Item -Path $zipPath -Force
}

Compress-Archive -Path "$tempDir\*" -DestinationPath $zipPath -Force
Remove-Item -Path $tempDir -Recurse -Force

Write-Host "✓ 배포 패키지 생성 완료" -ForegroundColor Green

# 2. Lambda 함수 생성 또는 업데이트
Write-Host "`n[2/3] Lambda 함수 배포 중..." -ForegroundColor Yellow

# 함수 존재 확인
$functionExists = aws lambda get-function --function-name ResumeParseEvaluate --region $Region 2>$null

if ($LASTEXITCODE -eq 0) {
    Write-Host "기존 함수 업데이트 중..." -ForegroundColor Cyan
    aws lambda update-function-code `
        --function-name ResumeParseEvaluate `
        --zip-file "fileb://$zipPath" `
        --region $Region
} else {
    Write-Host "새 함수 생성 중..." -ForegroundColor Cyan
    aws lambda create-function `
        --function-name ResumeParseEvaluate `
        --runtime python3.11 `
        --role arn:aws:iam::412677576136:role/LambdaExecutionRole-Team2 `
        --handler index.lambda_handler `
        --zip-file "fileb://$zipPath" `
        --timeout 300 `
        --memory-size 1024 `
        --environment "Variables={RESUMES_BUCKET=hr-resource-optimization-resumes-prod}" `
        --region $Region
}

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Lambda 함수 배포 완료!" -ForegroundColor Green
} else {
    Write-Host "✗ Lambda 함수 배포 실패" -ForegroundColor Red
}

# 3. 프론트엔드 재배포
Write-Host "`n[3/3] 프론트엔드 재배포 중..." -ForegroundColor Yellow
& .\rebuild_and_deploy.ps1

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "배포 완료!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "`n다음 단계:" -ForegroundColor Yellow
Write-Host "1. API Gateway에 /resume/parse 엔드포인트 추가" -ForegroundColor White
Write-Host "2. ResumeParseEvaluate Lambda 함수 연결" -ForegroundColor White
Write-Host "3. 브라우저 캐시 삭제 후 테스트" -ForegroundColor White

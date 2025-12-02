$env:AWS_PAGER = ""
$Region = "us-east-2"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "올바른 Lambda 함수 업데이트" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan

# Lambda 배포 패키지 생성
Write-Host "`n[1/2] Lambda 배포 패키지 생성 중..." -ForegroundColor Yellow

$tempDir = "temp_lambda"
if (Test-Path $tempDir) {
    Remove-Item -Path $tempDir -Recurse -Force
}
New-Item -ItemType Directory -Path $tempDir | Out-Null

Copy-Item -Path "lambda_functions\resume_upload\index.py" -Destination "$tempDir\index.py"

$zipPath = "resume_upload_lambda.zip"
if (Test-Path $zipPath) {
    Remove-Item -Path $zipPath -Force
}

Compress-Archive -Path "$tempDir\*" -DestinationPath $zipPath -Force
Remove-Item -Path $tempDir -Recurse -Force

Write-Host "✓ 배포 패키지 생성 완료" -ForegroundColor Green

# ResumeUploadURLGenerator 함수 업데이트
Write-Host "`n[2/2] ResumeUploadURLGenerator Lambda 함수 업데이트 중..." -ForegroundColor Yellow

aws lambda update-function-code `
    --function-name ResumeUploadURLGenerator `
    --zip-file "fileb://$zipPath" `
    --region $Region `
    --output json

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✓ Lambda 함수 업데이트 완료!" -ForegroundColor Green
} else {
    Write-Host "`n✗ Lambda 함수 업데이트 실패" -ForegroundColor Red
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "완료!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan

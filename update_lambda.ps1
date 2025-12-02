Write-Host "Lambda 함수 배포 패키지 생성 중..." -ForegroundColor Yellow

# 임시 디렉토리 생성
$tempDir = "temp_lambda"
if (Test-Path $tempDir) {
    Remove-Item -Path $tempDir -Recurse -Force
}
New-Item -ItemType Directory -Path $tempDir | Out-Null

# Lambda 함수 파일 복사
Copy-Item -Path "lambda_functions\resume_upload\index.py" -Destination "$tempDir\index.py"

# ZIP 파일 생성
$zipPath = "resume_upload_lambda.zip"
if (Test-Path $zipPath) {
    Remove-Item -Path $zipPath -Force
}

Compress-Archive -Path "$tempDir\*" -DestinationPath $zipPath

# 임시 디렉토리 삭제
Remove-Item -Path $tempDir -Recurse -Force

Write-Host "✓ 배포 패키지 생성 완료: $zipPath" -ForegroundColor Green

# Lambda 함수 업데이트
Write-Host "`nLambda 함수 업데이트 중..." -ForegroundColor Yellow

$env:AWS_PAGER = ""

aws lambda update-function-code `
    --function-name resume_upload `
    --zip-file "fileb://$zipPath" `
    --region us-east-2

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✓ Lambda 함수 업데이트 완료!" -ForegroundColor Green
} else {
    Write-Host "`n✗ Lambda 함수 업데이트 실패 (Exit Code: $LASTEXITCODE)" -ForegroundColor Red
    Write-Host "수동으로 AWS Console에서 업데이트해주세요." -ForegroundColor Yellow
}

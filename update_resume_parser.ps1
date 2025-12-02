$env:AWS_PAGER = ""
$Region = "us-east-2"

Write-Host "ResumeParser Lambda update starting..." -ForegroundColor Yellow

# Create deployment package
$tempDir = "temp_resume_parser"
if (Test-Path $tempDir) {
    Remove-Item -Path $tempDir -Recurse -Force
}
New-Item -ItemType Directory -Path $tempDir | Out-Null

# Copy all files
Copy-Item -Path "lambda_functions\resume_parser\*.py" -Destination $tempDir

$zipPath = "resume_parser_updated.zip"
if (Test-Path $zipPath) {
    Remove-Item -Path $zipPath -Force
}

Compress-Archive -Path "$tempDir\*" -DestinationPath $zipPath -Force
Remove-Item -Path $tempDir -Recurse -Force

Write-Host "Package created" -ForegroundColor Green

# Update function
Write-Host "Updating ResumeParser function..." -ForegroundColor Cyan
aws lambda update-function-code --function-name ResumeParser --zip-file "fileb://$zipPath" --region $Region

if ($LASTEXITCODE -eq 0) {
    Write-Host "Lambda update complete!" -ForegroundColor Green
} else {
    Write-Host "Lambda update failed!" -ForegroundColor Red
}

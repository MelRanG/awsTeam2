$env:AWS_PAGER = ""
$Region = "us-east-2"

Write-Host "Lambda deployment starting..." -ForegroundColor Yellow

# Create deployment package
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

Write-Host "Package created" -ForegroundColor Green

# Check if function exists
$functionExists = aws lambda get-function --function-name ResumeParseEvaluate --region $Region 2>$null

if ($LASTEXITCODE -eq 0) {
    Write-Host "Updating existing function..." -ForegroundColor Cyan
    aws lambda update-function-code --function-name ResumeParseEvaluate --zip-file "fileb://$zipPath" --region $Region
} else {
    Write-Host "Creating new function..." -ForegroundColor Cyan
    aws lambda create-function --function-name ResumeParseEvaluate --runtime python3.11 --role arn:aws:iam::412677576136:role/LambdaExecutionRole-Team2 --handler index.lambda_handler --zip-file "fileb://$zipPath" --timeout 300 --memory-size 1024 --environment "Variables={RESUMES_BUCKET=hr-resource-optimization-resumes-prod}" --region $Region
}

Write-Host "Lambda deployment complete!" -ForegroundColor Green

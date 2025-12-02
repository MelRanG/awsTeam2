$env:AWS_PAGER = ""

Write-Host "AWS 자격 증명 확인 중..." -ForegroundColor Yellow
aws sts get-caller-identity --region us-east-2

Write-Host "`nLambda 함수 목록 확인 중..." -ForegroundColor Yellow
aws lambda list-functions --region us-east-2 --query "Functions[].FunctionName" --output table

Write-Host "`nS3 버킷 확인 중..." -ForegroundColor Yellow
aws s3 ls --region us-east-2

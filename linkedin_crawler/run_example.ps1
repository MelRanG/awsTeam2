# LinkedIn 크롤러 실행 예제 스크립트 (PowerShell)

Write-Host "================================" -ForegroundColor Cyan
Write-Host "LinkedIn 크롤러 실행" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# LinkedIn 계정 정보 입력
$LINKEDIN_EMAIL = Read-Host "LinkedIn 이메일"
$LINKEDIN_PASSWORD = Read-Host "LinkedIn 비밀번호" -AsSecureString
$LINKEDIN_PASSWORD_PLAIN = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
    [Runtime.InteropServices.Marshal]::SecureStringToBSTR($LINKEDIN_PASSWORD)
)

Write-Host ""

# 검색 조건 입력
$KEYWORDS = Read-Host "검색 키워드 (기본: Backend Developer)"
if ([string]::IsNullOrWhiteSpace($KEYWORDS)) {
    $KEYWORDS = "Backend Developer"
}

$MAX_PROFILES = Read-Host "최대 프로필 수 (기본: 100)"
if ([string]::IsNullOrWhiteSpace($MAX_PROFILES)) {
    $MAX_PROFILES = 100
}

Write-Host ""
Write-Host "크롤링 시작..." -ForegroundColor Yellow
Write-Host "키워드: $KEYWORDS"
Write-Host "최대 프로필: $MAX_PROFILES 개"
Write-Host ""

# Python 스크립트 실행
python main.py `
  --email "$LINKEDIN_EMAIL" `
  --password "$LINKEDIN_PASSWORD_PLAIN" `
  --keywords "$KEYWORDS" `
  --location "South Korea" `
  --max-profiles $MAX_PROFILES `
  --headless

Write-Host ""
Write-Host "================================" -ForegroundColor Green
Write-Host "완료!" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host ""
Write-Host "생성된 파일:" -ForegroundColor Cyan
Write-Host "  - profiles.json (프로필 데이터)"
Write-Host "  - profiles_analysis.json (분석 결과)"
Write-Host "  - profiles_report.md (리포트)"

#!/bin/bash

# LinkedIn 크롤러 실행 예제 스크립트

echo "================================"
echo "LinkedIn 크롤러 실행"
echo "================================"
echo ""

# LinkedIn 계정 정보 입력
read -p "LinkedIn 이메일: " LINKEDIN_EMAIL
read -sp "LinkedIn 비밀번호: " LINKEDIN_PASSWORD
echo ""
echo ""

# 검색 조건 입력
read -p "검색 키워드 (기본: Backend Developer): " KEYWORDS
KEYWORDS=${KEYWORDS:-"Backend Developer"}

read -p "최대 프로필 수 (기본: 100): " MAX_PROFILES
MAX_PROFILES=${MAX_PROFILES:-100}

echo ""
echo "크롤링 시작..."
echo "키워드: $KEYWORDS"
echo "최대 프로필: $MAX_PROFILES개"
echo ""

# Python 스크립트 실행
python main.py \
  --email "$LINKEDIN_EMAIL" \
  --password "$LINKEDIN_PASSWORD" \
  --keywords "$KEYWORDS" \
  --location "South Korea" \
  --max-profiles $MAX_PROFILES \
  --headless

echo ""
echo "================================"
echo "완료!"
echo "================================"
echo ""
echo "생성된 파일:"
echo "  - profiles.json (프로필 데이터)"
echo "  - profiles_analysis.json (분석 결과)"
echo "  - profiles_report.md (리포트)"

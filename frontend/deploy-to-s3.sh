#!/bin/bash

# HR Resource Optimization Frontend - S3 배포 스크립트

set -e

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 설정
S3_BUCKET="${S3_BUCKET:-hr-frontend-team2}"
AWS_REGION="${AWS_REGION:-us-east-2}"
CLOUDFRONT_DIST_ID="${CLOUDFRONT_DIST_ID:-}"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}HR Frontend S3 배포 시작${NC}"
echo -e "${GREEN}========================================${NC}"

# 1. 환경 변수 확인
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}경고: .env 파일이 없습니다. .env.example을 참고하여 생성하세요.${NC}"
fi

# 2. 의존성 설치
echo -e "\n${YELLOW}[1/4] 의존성 설치 중...${NC}"
npm install

# 3. 프로덕션 빌드
echo -e "\n${YELLOW}[2/4] 프로덕션 빌드 중...${NC}"
npm run build

# 4. S3에 업로드
echo -e "\n${YELLOW}[3/4] S3 버킷에 업로드 중...${NC}"
echo "버킷: s3://${S3_BUCKET}"
echo "리전: ${AWS_REGION}"

aws s3 sync dist/ s3://${S3_BUCKET} \
    --region ${AWS_REGION} \
    --delete \
    --cache-control "public, max-age=31536000" \
    --exclude "index.html" \
    --exclude "*.map"

# index.html은 캐시 없이 업로드
aws s3 cp dist/index.html s3://${S3_BUCKET}/index.html \
    --region ${AWS_REGION} \
    --cache-control "no-cache, no-store, must-revalidate" \
    --content-type "text/html"

echo -e "${GREEN}✓ S3 업로드 완료${NC}"

# 5. CloudFront 캐시 무효화 (선택사항)
if [ -n "$CLOUDFRONT_DIST_ID" ]; then
    echo -e "\n${YELLOW}[4/4] CloudFront 캐시 무효화 중...${NC}"
    echo "Distribution ID: ${CLOUDFRONT_DIST_ID}"
    
    aws cloudfront create-invalidation \
        --distribution-id ${CLOUDFRONT_DIST_ID} \
        --paths "/*"
    
    echo -e "${GREEN}✓ CloudFront 캐시 무효화 완료${NC}"
else
    echo -e "\n${YELLOW}[4/4] CloudFront 캐시 무효화 건너뛰기 (CLOUDFRONT_DIST_ID 미설정)${NC}"
fi

# 완료
echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}배포 완료!${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "S3 URL: http://${S3_BUCKET}.s3-website.${AWS_REGION}.amazonaws.com"

if [ -n "$CLOUDFRONT_DIST_ID" ]; then
    echo -e "CloudFront URL: https://your-cloudfront-domain.cloudfront.net"
fi

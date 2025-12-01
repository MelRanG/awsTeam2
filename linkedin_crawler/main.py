"""
LinkedIn 크롤러 메인 실행 스크립트
LinkedIn에서 프로필을 크롤링하여 DynamoDB에 저장
"""

import json
import argparse
from crawler import LinkedInCrawler
from dynamodb_uploader import DynamoDBUploader
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description='LinkedIn 프로필 크롤러 및 DynamoDB 업로더')
    parser.add_argument('--email', required=True, help='LinkedIn 로그인 이메일')
    parser.add_argument('--password', required=True, help='LinkedIn 로그인 비밀번호')
    parser.add_argument('--keywords', default='Backend Developer', help='검색 키워드')
    parser.add_argument('--location', default='South Korea', help='검색 지역')
    parser.add_argument('--max-profiles', type=int, default=100, help='최대 프로필 수')
    parser.add_argument('--output', default='profiles.json', help='출력 파일명 (선택)')
    parser.add_argument('--headless', action='store_true', help='헤드리스 모드')
    parser.add_argument('--region', default='us-east-2', help='AWS 리전')
    parser.add_argument('--skip-upload', action='store_true', help='DynamoDB 업로드 건너뛰기')
    
    args = parser.parse_args()
    
    crawler = None
    
    try:
        # 1. 크롤러 초기화 및 로그인
        logger.info("=" * 60)
        logger.info("LinkedIn 크롤러 시작")
        logger.info("=" * 60)
        
        crawler = LinkedInCrawler(
            email=args.email,
            password=args.password,
            headless=args.headless
        )
        
        if not crawler.login():
            logger.error("로그인 실패. 프로그램을 종료합니다.")
            return
        
        # 2. 프로필 검색
        logger.info(f"\n검색 조건: {args.keywords} in {args.location}")
        logger.info(f"목표 프로필 수: {args.max_profiles}개\n")
        
        profile_urls = crawler.search_profiles(
            keywords=args.keywords,
            location=args.location,
            max_results=args.max_profiles
        )
        
        if not profile_urls:
            logger.error("프로필을 찾을 수 없습니다.")
            return
        
        # 3. 각 프로필 크롤링
        logger.info(f"\n{len(profile_urls)}개 프로필 크롤링 시작...\n")
        
        profiles = []
        for idx, url in enumerate(profile_urls, 1):
            logger.info(f"[{idx}/{len(profile_urls)}] 크롤링 중...")
            
            profile_data = crawler.crawl_profile(url)
            if profile_data:
                profiles.append(profile_data)
                logger.info(f"✓ {profile_data['name']} - {profile_data['current_role']} ({profile_data['years_of_experience']}년)")
            else:
                logger.warning(f"✗ 크롤링 실패: {url}")
            
            # 진행률 표시
            if idx % 10 == 0:
                logger.info(f"\n진행률: {idx}/{len(profile_urls)} ({idx/len(profile_urls)*100:.1f}%)\n")
        
        # 4. 프로필 데이터 저장 (선택)
        logger.info(f"\n총 {len(profiles)}개 프로필 수집 완료")
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(profiles, f, ensure_ascii=False, indent=2)
            logger.info(f"프로필 데이터 저장: {args.output}")
        
        # 5. DynamoDB 업로드
        if not args.skip_upload:
            logger.info("\n" + "=" * 60)
            logger.info("DynamoDB 업로드 시작")
            logger.info("=" * 60 + "\n")
            
            uploader = DynamoDBUploader(region=args.region)
            upload_result = uploader.upload_profiles(profiles)
            
            logger.info("\n" + "=" * 60)
            logger.info("업로드 결과")
            logger.info("=" * 60)
            logger.info(f"총 프로필: {upload_result['total']}개")
            logger.info(f"성공: {upload_result['success']}개")
            logger.info(f"실패: {upload_result['failed']}개")
            
            if upload_result['failed_profiles']:
                logger.info("\n실패한 프로필:")
                for failed in upload_result['failed_profiles']:
                    logger.info(f"  - {failed['name']}: {failed['error']}")
        else:
            logger.info("\nDynamoDB 업로드를 건너뜁니다 (--skip-upload)")
        
        logger.info("\n" + "=" * 60)
        logger.info("완료!")
        logger.info("=" * 60)
        logger.info("\n다음 단계:")
        logger.info("1. AWS Console에서 DynamoDB Employees 테이블 확인")
        logger.info("2. 프론트엔드에서 '커리어 추천' 기능 사용")
        logger.info("3. domain_analysis Lambda가 자동으로 분석 수행")
        
    except KeyboardInterrupt:
        logger.info("\n사용자에 의해 중단되었습니다.")
    
    except Exception as e:
        logger.error(f"오류 발생: {str(e)}", exc_info=True)
    
    finally:
        if crawler:
            crawler.close()


if __name__ == '__main__':
    main()

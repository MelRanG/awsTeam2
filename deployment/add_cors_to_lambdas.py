#!/usr/bin/env python3
"""
Lambda 함수들에 CORS 헤더 추가
"""

import os
import re

CORS_HEADERS = """'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,Authorization',
                'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'"""

def add_cors_to_file(filepath):
    """파일에 CORS 헤더 추가"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 'Content-Type': 'application/json' 을 CORS 헤더로 교체
    pattern = r"'Content-Type':\s*'application/json'"
    replacement = CORS_HEADERS
    
    new_content = re.sub(pattern, replacement, content)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✅ Updated: {filepath}")
        return True
    else:
        print(f"⏭️  Skipped: {filepath} (no changes needed)")
        return False

def main():
    lambda_dirs = [
        'lambda_functions/qualitative_analysis',
        'lambda_functions/domain_analysis',
        'lambda_functions/recommendation_engine'
    ]
    
    updated_count = 0
    for lambda_dir in lambda_dirs:
        index_file = os.path.join(lambda_dir, 'index.py')
        if os.path.exists(index_file):
            if add_cors_to_file(index_file):
                updated_count += 1
    
    print(f"\n총 {updated_count}개 파일 업데이트 완료")

if __name__ == '__main__':
    main()

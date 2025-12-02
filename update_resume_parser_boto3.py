#!/usr/bin/env python3
"""ResumeParser Lambda 함수 업데이트"""

import boto3
import zipfile
import os

lambda_client = boto3.client('lambda', region_name='us-east-2')

print("ResumeParser Lambda 업데이트 시작...")

# 1. ZIP 파일 생성
print("\n1. 배포 패키지 생성 중...")
zip_path = 'resume_parser_updated.zip'

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    # 모든 Python 파일 추가
    parser_dir = 'lambda_functions/resume_parser'
    for filename in os.listdir(parser_dir):
        if filename.endswith('.py'):
            file_path = os.path.join(parser_dir, filename)
            zipf.write(file_path, filename)
            print(f"  - {filename} 추가됨")

print(f"✓ 배포 패키지 생성 완료: {zip_path}")

# 2. Lambda 함수 업데이트
print("\n2. Lambda 함수 업데이트 중...")
try:
    with open(zip_path, 'rb') as f:
        zip_content = f.read()
    
    response = lambda_client.update_function_code(
        FunctionName='ResumeParser',
        ZipFile=zip_content,
        Publish=True
    )
    
    print(f"✓ Lambda 함수 업데이트 완료")
    print(f"  - 함수명: {response['FunctionName']}")
    print(f"  - 버전: {response['Version']}")
    print(f"  - 마지막 수정: {response['LastModified']}")
    print(f"  - 코드 크기: {response['CodeSize']} bytes")
    
    print("\n" + "=" * 60)
    print("✅ 업데이트 완료!")
    print("=" * 60)
    
except Exception as e:
    print(f"✗ 업데이트 실패: {str(e)}")
    import traceback
    traceback.print_exc()

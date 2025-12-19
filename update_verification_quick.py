"""
검증 질문 Lambda 함수 빠른 업데이트
"""
import boto3
import zipfile
import io

lambda_client = boto3.client('lambda', region_name='us-east-2')

print("검증 질문 Lambda 함수 업데이트 중...")

# Lambda 함수 코드 읽기
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
lambda_path = os.path.join(script_dir, 'lambda_functions', 'resume_verification_questions', 'index.py')

with open(lambda_path, 'r', encoding='utf-8') as f:
    code = f.read()

# ZIP 파일 생성
zip_buffer = io.BytesIO()
with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
    zip_file.writestr('index.py', code)

zip_buffer.seek(0)

# Lambda 함수 업데이트
try:
    response = lambda_client.update_function_code(
        FunctionName='ResumeVerificationQuestions',
        ZipFile=zip_buffer.read()
    )
    print(f"✓ 함수 업데이트 완료: {response['FunctionName']}")
    
    # 타임아웃 90초로 설정
    lambda_client.update_function_configuration(
        FunctionName='ResumeVerificationQuestions',
        Timeout=90
    )
    print("✓ 타임아웃 90초로 설정 완료")
    print("\n배포 완료! 이제 프론트엔드를 빌드하고 배포하세요.")
    
except Exception as e:
    print(f"✗ 오류: {e}")

"""
EmployeeCreate Lambda 함수 업데이트 (simple 버전)
"""
import boto3
import zipfile
import os

lambda_client = boto3.client('lambda', region_name='us-east-2')

print("="*60)
print("EmployeeCreate Lambda 함수 업데이트 (Simple 버전)")
print("="*60)

# 1. Lambda 함수 패키징
print("\n1. Lambda 함수 패키징...")
zip_path = 'employee_create_simple.zip'

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    # simple_index.py를 index.py로 패키징
    zipf.write(
        'lambda_functions/employee_create/simple_index.py',
        'index.py'
    )

print(f"✅ 패키징 완료: {zip_path}")

# 2. Lambda 함수 업데이트
print("\n2. Lambda 함수 코드 업데이트...")
function_name = 'EmployeeCreate'

with open(zip_path, 'rb') as f:
    zip_content = f.read()

try:
    response = lambda_client.update_function_code(
        FunctionName=function_name,
        ZipFile=zip_content
    )
    print(f"✅ Lambda 함수 업데이트 완료: {function_name}")
    print(f"   버전: {response['Version']}")
    print(f"   최종 수정: {response['LastModified']}")
except Exception as e:
    print(f"❌ 업데이트 실패: {str(e)}")
    exit(1)

# 정리
os.remove(zip_path)

print("\n" + "="*60)
print("업데이트 완료!")
print("="*60)
print("\n✅ verification_questions 필드 저장 지원")
print("✅ PendingCandidates 테이블에 저장")
print("✅ common 모듈 의존성 제거")

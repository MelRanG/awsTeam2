"""
검증 질문 생성 Lambda 함수 업데이트
candidate_id를 받아서 DynamoDB 자동 업데이트
"""
import boto3
import zipfile
import io
import os

lambda_client = boto3.client('lambda', region_name='us-east-2')

print("=" * 60)
print("검증 질문 Lambda 함수 업데이트")
print("=" * 60)

# Lambda 함수 코드 압축
zip_buffer = io.BytesIO()
with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
    # index.py 추가
    index_path = '../lambda_functions/resume_verification_questions/index.py'
    if not os.path.exists(index_path):
        index_path = 'lambda_functions/resume_verification_questions/index.py'
    
    if os.path.exists(index_path):
        zip_file.write(index_path, 'index.py')
        print(f"✓ {index_path} 추가")
    else:
        print(f"✗ {index_path} 파일을 찾을 수 없습니다")
        print(f"현재 디렉토리: {os.getcwd()}")
        exit(1)

zip_buffer.seek(0)

try:
    # Lambda 함수 업데이트
    print("\nLambda 함수 코드 업데이트 중...")
    response = lambda_client.update_function_code(
        FunctionName='verification_questions_generator',
        ZipFile=zip_buffer.read()
    )
    
    print(f"✓ 함수 업데이트 완료")
    print(f"  - 함수명: {response['FunctionName']}")
    print(f"  - 버전: {response['Version']}")
    print(f"  - 마지막 수정: {response['LastModified']}")
    
    # 타임아웃 설정 확인 및 조정
    print("\n타임아웃 설정 확인 중...")
    config = lambda_client.get_function_configuration(
        FunctionName='verification_questions_generator'
    )
    
    current_timeout = config['Timeout']
    print(f"  - 현재 타임아웃: {current_timeout}초")
    
    if current_timeout < 90:
        print(f"  - 타임아웃을 90초로 증가...")
        lambda_client.update_function_configuration(
            FunctionName='verification_questions_generator',
            Timeout=90
        )
        print(f"  ✓ 타임아웃 90초로 설정 완료")
    
    print("\n" + "=" * 60)
    print("✅ 배포 완료!")
    print("=" * 60)
    print("\n변경 사항:")
    print("  1. candidate_id 파라미터 추가")
    print("  2. 검증 질문 생성 후 DynamoDB 자동 업데이트")
    print("  3. 프론트엔드에서 백그라운드 호출 가능")
    
except lambda_client.exceptions.ResourceNotFoundException:
    print("✗ Lambda 함수를 찾을 수 없습니다: verification_questions_generator")
except Exception as e:
    print(f"✗ 오류 발생: {e}")
    import traceback
    traceback.print_exc()

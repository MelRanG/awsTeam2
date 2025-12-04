"""
프로젝트 투입 Lambda 함수 업데이트
"""

import boto3
import zipfile
import io

def update_lambda():
    """Lambda 함수 업데이트"""
    
    lambda_client = boto3.client('lambda', region_name='us-east-2')
    
    print("=" * 60)
    print("프로젝트 투입 Lambda 함수 업데이트")
    print("=" * 60)
    
    # Lambda 함수 코드 압축
    print("\n1. Lambda 함수 코드 압축 중...")
    
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        lambda_path = 'lambda_functions/project_assign/index.py'
        zip_file.write(lambda_path, 'index.py')
    
    zip_buffer.seek(0)
    print("  ✓ 코드 압축 완료")
    
    # Lambda 함수 업데이트
    print("\n2. Lambda 함수 업데이트 중...")
    
    try:
        response = lambda_client.update_function_code(
            FunctionName='ProjectAssignment',
            ZipFile=zip_buffer.read()
        )
        
        print(f"  ✓ 함수 업데이트 완료")
        print(f"  - 함수명: {response['FunctionName']}")
        print(f"  - 버전: {response['Version']}")
        print(f"  - 상태: {response['State']}")
        
    except Exception as e:
        print(f"  ✗ 업데이트 실패: {str(e)}")
        return False
    
    print("\n" + "=" * 60)
    print("✅ 프로젝트 투입 기능 업데이트 완료!")
    print("=" * 60)
    print("\n추가된 기능:")
    print("  1. 투입 역할 선택 (PM, 개발자, 디자이너 등)")
    print("  2. 투입 기간 설정 (시작일, 종료일)")
    print("  3. 투입률 설정 (1~100%)")
    print("  4. 투입 근거 기록")
    
    return True

if __name__ == '__main__':
    update_lambda()

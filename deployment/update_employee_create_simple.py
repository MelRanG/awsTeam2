#!/usr/bin/env python3
"""
employee_create Lambda 함수를 간단 버전으로 업데이트
"""
import boto3
import zipfile
import io
import os

def update_employee_create():
    """employee_create Lambda 함수 업데이트"""
    lambda_client = boto3.client('lambda', region_name='us-east-2')
    
    function_name = 'EmployeeCreate'
    
    print("=" * 60)
    print(f"{function_name} Lambda 함수 업데이트")
    print("=" * 60)
    
    # Lambda 함수 코드 압축
    print("\n1. Lambda 함수 코드 압축 중...")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        simple_index = os.path.join(project_root, 'lambda_functions', 'employee_create', 'simple_index.py')
        if os.path.exists(simple_index):
            zip_file.write(simple_index, 'index.py')
            print(f"  ✓ simple_index.py -> index.py 추가됨")
        else:
            print(f"  ✗ simple_index.py 파일을 찾을 수 없습니다")
            return False
    
    zip_buffer.seek(0)
    zip_content = zip_buffer.read()
    
    # Lambda 함수 업데이트
    print(f"\n2. Lambda 함수 코드 업데이트 중...")
    try:
        response = lambda_client.update_function_code(
            FunctionName=function_name,
            ZipFile=zip_content
        )
        print(f"  ✓ {function_name} 업데이트 완료")
        print(f"     버전: {response['Version']}")
        print(f"     최종 수정: {response['LastModified']}")
        return True
    except Exception as e:
        print(f"  ✗ Lambda 함수 업데이트 실패: {str(e)}")
        return False

if __name__ == '__main__':
    update_employee_create()

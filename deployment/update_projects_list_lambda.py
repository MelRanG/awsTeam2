"""
Projects List Lambda 함수 업데이트
"""
import boto3
import zipfile
import os
from io import BytesIO

def update_lambda():
    """Lambda 함수 업데이트"""
    lambda_client = boto3.client('lambda', region_name='us-east-2')
    
    # 현재 스크립트의 상위 디렉토리로 이동
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    lambda_path = os.path.join(project_root, 'lambda_functions', 'projects_list', 'index.py')
    
    # Lambda 함수 코드 압축
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.write(lambda_path, 'index.py')
    
    zip_buffer.seek(0)
    
    # Lambda 함수 업데이트
    function_name = 'ProjectsList'
    
    try:
        response = lambda_client.update_function_code(
            FunctionName=function_name,
            ZipFile=zip_buffer.read()
        )
        
        print(f"✓ Lambda 함수 '{function_name}' 업데이트 완료")
        print(f"  버전: {response['Version']}")
        print(f"  최종 수정: {response['LastModified']}")
        
    except Exception as e:
        print(f"✗ Lambda 함수 업데이트 실패: {str(e)}")
        raise

if __name__ == '__main__':
    update_lambda()

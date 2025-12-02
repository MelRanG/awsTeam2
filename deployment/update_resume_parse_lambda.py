#!/usr/bin/env python3
"""
이력서 파싱 Lambda 함수 업데이트 스크립트
"""
import boto3
import zipfile
import os
import io

def update_resume_parse_lambda():
    """resume_parser Lambda 함수 업데이트"""
    lambda_client = boto3.client('lambda', region_name='us-east-2')
    
    function_name = 'ResumeParser'
    
    # 프로젝트 루트 디렉토리 찾기
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    # Lambda 함수 코드 압축
    print(f"Lambda 함수 코드 압축 중: {function_name}")
    print(f"프로젝트 루트: {project_root}")
    
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # resume_parser 폴더의 모든 파일 추가
        resume_parser_dir = os.path.join(project_root, 'lambda_functions', 'resume_parser')
        
        for filename in ['index.py', 'parse_handler.py', '__init__.py']:
            file_path = os.path.join(resume_parser_dir, filename)
            if os.path.exists(file_path):
                zip_file.write(file_path, filename)
                print(f"  ✓ {filename} 추가됨")
            else:
                print(f"  ✗ {filename} 파일을 찾을 수 없습니다")
                if filename != '__init__.py':  # __init__.py는 선택사항
                    return False
    
    zip_buffer.seek(0)
    zip_content = zip_buffer.read()
    
    # Lambda 함수 업데이트
    print(f"\nLambda 함수 업데이트 중...")
    try:
        response = lambda_client.update_function_code(
            FunctionName=function_name,
            ZipFile=zip_content
        )
        print(f"✅ {function_name} 업데이트 완료")
        print(f"   버전: {response['Version']}")
        print(f"   최종 수정: {response['LastModified']}")
        return True
    except Exception as e:
        print(f"❌ Lambda 함수 업데이트 실패: {str(e)}")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("이력서 파싱 Lambda 함수 업데이트")
    print("=" * 60)
    update_resume_parse_lambda()

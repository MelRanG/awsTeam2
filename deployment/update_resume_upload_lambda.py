"""
이력서 업로드 Lambda 함수 업데이트 스크립트
"""

import boto3
import zipfile
import os
import json

lambda_client = boto3.client('lambda', region_name='us-east-2')

FUNCTION_NAME = 'resume_upload'
LAMBDA_DIR = '../lambda_functions/resume_upload'

def create_deployment_package():
    """배포 패키지 생성"""
    zip_path = '/tmp/resume_upload.zip'
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Lambda 함수 코드 추가
        index_path = os.path.join(LAMBDA_DIR, 'index.py')
        if os.path.exists(index_path):
            zipf.write(index_path, 'index.py')
            print(f"✓ {index_path} 추가됨")
        else:
            print(f"✗ {index_path} 파일을 찾을 수 없습니다")
            return None
    
    print(f"✓ 배포 패키지 생성 완료: {zip_path}")
    return zip_path

def update_lambda_function(zip_path):
    """Lambda 함수 코드 업데이트"""
    try:
        with open(zip_path, 'rb') as f:
            zip_content = f.read()
        
        response = lambda_client.update_function_code(
            FunctionName=FUNCTION_NAME,
            ZipFile=zip_content,
            Publish=True
        )
        
        print(f"✓ Lambda 함수 업데이트 완료")
        print(f"  - 함수명: {response['FunctionName']}")
        print(f"  - 버전: {response['Version']}")
        print(f"  - 마지막 수정: {response['LastModified']}")
        
        return True
        
    except Exception as e:
        print(f"✗ Lambda 함수 업데이트 실패: {str(e)}")
        return False

def verify_environment_variables():
    """환경 변수 확인"""
    try:
        response = lambda_client.get_function_configuration(
            FunctionName=FUNCTION_NAME
        )
        
        env_vars = response.get('Environment', {}).get('Variables', {})
        print("\n현재 환경 변수:")
        print(json.dumps(env_vars, indent=2, ensure_ascii=False))
        
        # 필수 환경 변수 확인
        required_vars = ['RESUMES_BUCKET']
        missing_vars = [var for var in required_vars if var not in env_vars]
        
        if missing_vars:
            print(f"\n⚠️  누락된 환경 변수: {', '.join(missing_vars)}")
            return False
        
        print("\n✓ 모든 필수 환경 변수가 설정되어 있습니다.")
        return True
        
    except Exception as e:
        print(f"✗ 환경 변수 확인 실패: {str(e)}")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("이력서 업로드 Lambda 함수 업데이트")
    print("=" * 60)
    
    # 1. 배포 패키지 생성
    print("\n1. 배포 패키지 생성 중...")
    zip_path = create_deployment_package()
    
    if not zip_path:
        print("\n✗ 배포 패키지 생성 실패")
        exit(1)
    
    # 2. Lambda 함수 업데이트
    print("\n2. Lambda 함수 업데이트 중...")
    if not update_lambda_function(zip_path):
        print("\n✗ Lambda 함수 업데이트 실패")
        exit(1)
    
    # 3. 환경 변수 확인
    print("\n3. 환경 변수 확인 중...")
    verify_environment_variables()
    
    print("\n" + "=" * 60)
    print("업데이트 완료!")
    print("=" * 60)
    print("\n다음 단계:")
    print("1. python deployment/fix_resume_bucket_cors.py 실행")
    print("2. 프론트엔드에서 이력서 업로드 테스트")

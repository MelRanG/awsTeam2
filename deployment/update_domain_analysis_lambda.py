"""
도메인 분석 Lambda 함수 업데이트
"""
import boto3
import zipfile
import os
import sys

def update_lambda():
    """Lambda 함수 업데이트"""
    lambda_client = boto3.client('lambda', region_name='us-east-2')
    
    # Lambda 함수 코드 압축
    zip_path = 'domain_analysis_temp.zip'
    
    print("Lambda 함수 코드 압축 중...")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # index.py 추가
        lambda_file = 'lambda_functions/domain_analysis/index.py'
        if os.path.exists(lambda_file):
            zipf.write(lambda_file, 'index.py')
            print(f"  ✓ {lambda_file} 추가")
        else:
            print(f"  ✗ {lambda_file} 파일을 찾을 수 없습니다")
            return False
    
    # Lambda 함수 업데이트
    print("\nLambda 함수 업데이트 중...")
    try:
        with open(zip_path, 'rb') as f:
            response = lambda_client.update_function_code(
                FunctionName='DomainAnalysisEngine',
                ZipFile=f.read()
            )
        
        print(f"  ✓ Lambda 함수 업데이트 완료")
        print(f"  - 함수명: {response['FunctionName']}")
        print(f"  - 버전: {response['Version']}")
        print(f"  - 마지막 수정: {response['LastModified']}")
        
        # 임시 파일 삭제
        os.remove(zip_path)
        
        return True
        
    except Exception as e:
        print(f"  ✗ Lambda 함수 업데이트 실패: {str(e)}")
        if os.path.exists(zip_path):
            os.remove(zip_path)
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("도메인 분석 Lambda 함수 업데이트")
    print("=" * 60)
    
    success = update_lambda()
    
    if success:
        print("\n✅ 업데이트 완료!")
    else:
        print("\n❌ 업데이트 실패")
        sys.exit(1)

"""
대시보드 Lambda 함수 복원 스크립트
"""
import boto3
import zipfile
import os

def main():
    """메인 실행 함수"""
    print("=" * 60)
    print("대시보드 Lambda 함수 복원")
    print("=" * 60)
    
    # 경로 설정
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    lambda_file = os.path.join(project_root, 'lambda_functions', 'dashboard_metrics', 'index.py')
    zip_file = os.path.join(project_root, 'dashboard_metrics.zip')
    
    try:
        # 1. Lambda 패키지 생성
        print("\nLambda 배포 패키지 생성 중...")
        with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(lambda_file, 'index.py')
        print(f"✓ {zip_file} 생성 완료")
        
        # 2. Lambda 함수 업데이트
        print("\nLambda 함수 업데이트 중...")
        lambda_client = boto3.client('lambda', region_name='us-east-2')
        
        with open(zip_file, 'rb') as f:
            zip_content = f.read()
        
        response = lambda_client.update_function_code(
            FunctionName='DashboardMetrics',
            ZipFile=zip_content
        )
        
        print(f"✓ Lambda 함수 업데이트 완료")
        print(f"  버전: {response['Version']}")
        print(f"  최종 수정: {response['LastModified']}")
        
        # 3. 임시 파일 정리
        if os.path.exists(zip_file):
            os.remove(zip_file)
            print("\n✓ 임시 파일 정리 완료")
        
        print("\n" + "=" * 60)
        print("✓ 복원 완료")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ 오류 발생: {str(e)}")
        if os.path.exists(zip_file):
            os.remove(zip_file)
        print("\n" + "=" * 60)
        print("✗ 복원 실패")
        print("=" * 60)

if __name__ == '__main__':
    main()

import boto3
import zipfile
import os

print("=" * 60)
print("대시보드 메트릭 Lambda 함수 업데이트")
print("=" * 60)

# ZIP 파일 생성
zip_path = 'dashboard_metrics.zip'
lambda_file = 'lambda_functions/dashboard_metrics/index.py'

print(f"\n1. ZIP 파일 생성 중...")
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipf.write(lambda_file, 'index.py')
print(f"  ✓ {zip_path} 생성 완료")

# Lambda 업데이트
print(f"\n2. Lambda 함수 업데이트 중...")
lambda_client = boto3.client('lambda', region_name='us-east-2')

try:
    with open(zip_path, 'rb') as f:
        response = lambda_client.update_function_code(
            FunctionName='DashboardMetrics',
            ZipFile=f.read()
        )
    
    print(f"  ✓ Lambda 함수 업데이트 완료")
    print(f"  - Function: {response['FunctionName']}")
    print(f"  - Version: {response['Version']}")
    print(f"  - Last Modified: {response['LastModified']}")
    
    # ZIP 파일 삭제
    os.remove(zip_path)
    print(f"\n3. 임시 파일 삭제 완료")
    
    print("\n" + "=" * 60)
    print("✅ 업데이트 완료!")
    print("=" * 60)
    
except Exception as e:
    print(f"\n✗ 에러 발생: {str(e)}")
    if os.path.exists(zip_path):
        os.remove(zip_path)

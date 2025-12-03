"""
대시보드 메트릭 Lambda 함수 업데이트
"""
import boto3
import zipfile
import os
import io

def update_dashboard_lambda():
    """대시보드 메트릭 Lambda 함수 업데이트"""
    lambda_client = boto3.client('lambda', region_name='us-east-2')
    
    # Lambda 함수 코드 압축
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        lambda_path = 'lambda_functions/dashboard_metrics/index.py'
        zip_file.write(lambda_path, 'index.py')
    
    zip_buffer.seek(0)
    
    try:
        # Lambda 함수 업데이트
        response = lambda_client.update_function_code(
            FunctionName='DashboardMetrics',
            ZipFile=zip_buffer.read()
        )
        
        print(f"✅ Lambda 함수 업데이트 완료: {response['FunctionName']}")
        print(f"   버전: {response['Version']}")
        print(f"   상태: {response['State']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Lambda 함수 업데이트 실패: {str(e)}")
        return False

if __name__ == '__main__':
    print("대시보드 메트릭 Lambda 함수 업데이트 시작...")
    success = update_dashboard_lambda()
    
    if success:
        print("\n✅ 업데이트 완료!")
    else:
        print("\n❌ 업데이트 실패")

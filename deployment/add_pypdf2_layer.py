#!/usr/bin/env python3
"""
PyPDF2 Lambda Layer 추가
"""
import boto3
import os
import zipfile
import subprocess
import shutil
from pathlib import Path

def create_pypdf2_layer():
    """PyPDF2 Lambda Layer 생성 및 추가"""
    lambda_client = boto3.client('lambda', region_name='us-east-2')
    
    print("=" * 60)
    print("PyPDF2 Lambda Layer 생성")
    print("=" * 60)
    
    # 임시 디렉토리 생성
    layer_dir = Path("temp_layer")
    python_dir = layer_dir / "python"
    python_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # PyPDF2 설치
        print("\nPyPDF2 설치 중...")
        subprocess.run([
            "pip", "install", "PyPDF2", "-t", str(python_dir)
        ], check=True)
        
        # ZIP 파일 생성
        print("ZIP 파일 생성 중...")
        zip_path = "pypdf2_layer.zip"
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(layer_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, layer_dir)
                    zipf.write(file_path, arcname)
        
        print(f"✓ ZIP 파일 생성 완료: {zip_path}")
        
        # Lambda Layer 생성
        print("\nLambda Layer 생성 중...")
        with open(zip_path, 'rb') as f:
            zip_content = f.read()
        
        response = lambda_client.publish_layer_version(
            LayerName='pypdf2-layer',
            Description='PyPDF2 library for PDF text extraction',
            Content={'ZipFile': zip_content},
            CompatibleRuntimes=['python3.11', 'python3.10', 'python3.9']
        )
        
        layer_arn = response['LayerVersionArn']
        print(f"✓ Lambda Layer 생성 완료")
        print(f"  ARN: {layer_arn}")
        
        # ResumeParser 함수에 Layer 추가
        print("\nResumeParser 함수에 Layer 추가 중...")
        function_config = lambda_client.get_function_configuration(
            FunctionName='ResumeParser'
        )
        
        existing_layers = function_config.get('Layers', [])
        layer_arns = [layer['Arn'] for layer in existing_layers]
        
        # 새 Layer ARN 추가 (버전 번호 제거한 ARN)
        base_layer_arn = ':'.join(layer_arn.split(':')[:-1])
        layer_arns = [arn for arn in layer_arns if not arn.startswith(base_layer_arn)]
        layer_arns.append(layer_arn)
        
        lambda_client.update_function_configuration(
            FunctionName='ResumeParser',
            Layers=layer_arns
        )
        
        print("✓ Layer 추가 완료")
        
        # 정리
        shutil.rmtree(layer_dir)
        os.remove(zip_path)
        
        print("\n✅ PyPDF2 Layer 설정 완료!")
        return True
        
    except Exception as e:
        print(f"\n❌ 에러 발생: {str(e)}")
        # 정리
        if layer_dir.exists():
            shutil.rmtree(layer_dir)
        if os.path.exists("pypdf2_layer.zip"):
            os.remove("pypdf2_layer.zip")
        return False

if __name__ == '__main__':
    create_pypdf2_layer()

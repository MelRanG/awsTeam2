#!/usr/bin/env python3
"""
DynamoDB 권한 확인
"""
import boto3
import json

def check_permissions():
    """DynamoDB 권한 확인"""
    dynamodb = boto3.client('dynamodb', region_name='us-east-2')
    iam = boto3.client('iam')
    sts = boto3.client('sts')
    
    print("=" * 60)
    print("DynamoDB 권한 확인")
    print("=" * 60)
    
    # 현재 사용자 정보
    try:
        identity = sts.get_caller_identity()
        print(f"\n현재 사용자: {identity['Arn']}")
        print(f"계정 ID: {identity['Account']}")
    except Exception as e:
        print(f"사용자 정보 조회 실패: {str(e)}")
    
    # 기존 테이블 목록
    print("\n기존 DynamoDB 테이블:")
    try:
        tables = dynamodb.list_tables()
        for table in tables['TableNames']:
            print(f"  - {table}")
    except Exception as e:
        print(f"  ✗ 테이블 목록 조회 실패: {str(e)}")
    
    # 테이블 생성 권한 테스트
    print("\n테이블 생성 권한 테스트:")
    test_table_name = 'TestPermissionTable'
    try:
        # 테스트 테이블 생성 시도
        dynamodb.create_table(
            TableName=test_table_name,
            KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S'}],
            BillingMode='PAY_PER_REQUEST'
        )
        print(f"  ✓ 테이블 생성 권한 있음")
        
        # 테스트 테이블 삭제
        dynamodb.delete_table(TableName=test_table_name)
        print(f"  ✓ 테스트 테이블 삭제 완료")
    except Exception as e:
        error_msg = str(e)
        print(f"  ✗ 테이블 생성 권한 없음")
        print(f"     에러: {error_msg}")
        
        if 'AccessDeniedException' in error_msg:
            print("\n권한 문제 해결 방법:")
            print("1. AWS 콘솔에서 직접 테이블 생성")
            print("2. 관리자에게 dynamodb:CreateTable 권한 요청")
            print("3. 또는 기존 Employees 테이블에 status 필드로 구분 (현재 방식)")

if __name__ == '__main__':
    check_permissions()

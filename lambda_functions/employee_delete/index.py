"""
직원 삭제 Lambda 함수

DynamoDB Employees 테이블에서 직원을 삭제합니다.
"""

import json
import os
import boto3
from botocore.exceptions import ClientError

# DynamoDB 클라이언트
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
employees_table = dynamodb.Table(os.environ.get('EMPLOYEES_TABLE', 'Employees'))


def lambda_handler(event, context):
    """
    Lambda 핸들러
    
    Args:
        event: API Gateway 이벤트
        context: Lambda 컨텍스트
        
    Returns:
        API Gateway 응답
    """
    print(f"직원 삭제 요청 수신: {json.dumps(event)}")
    
    try:
        # CORS 헤더
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Methods': 'DELETE,OPTIONS'
        }
        
        # OPTIONS 요청 처리 (CORS preflight)
        if event.get('httpMethod') == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({'message': 'OK'})
            }
        
        # Path parameter에서 employee_id 추출
        path_parameters = event.get('pathParameters', {})
        employee_id = path_parameters.get('employeeId')
        
        if not employee_id:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({
                    'error': 'employee_id is required',
                    'message': '직원 ID가 필요합니다'
                }, ensure_ascii=False)
            }
        
        print(f"삭제할 직원 ID: {employee_id}")
        
        # DynamoDB에서 삭제
        try:
            employees_table.delete_item(
                Key={'user_id': employee_id}
            )
            print(f"직원 삭제 완료: {employee_id}")
        except ClientError as e:
            print(f"DynamoDB 삭제 실패: {str(e)}")
            raise Exception(f"데이터베이스 삭제에 실패했습니다: {str(e)}")
        
        # 성공 응답
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'message': '직원이 성공적으로 삭제되었습니다',
                'employee_id': employee_id
            }, ensure_ascii=False)
        }
        
    except Exception as e:
        # 서버 에러
        print(f"직원 삭제 실패: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({
                'error': 'Internal Server Error',
                'message': '직원 삭제 중 오류가 발생했습니다'
            }, ensure_ascii=False)
        }

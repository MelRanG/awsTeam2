"""
대기자 삭제 Lambda 함수
"""
import json
import os
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
pending_candidates_table = dynamodb.Table('PendingCandidates')


def lambda_handler(event, context):
    """Lambda 핸들러"""
    print(f"대기자 삭제 요청: {json.dumps(event)}")
    
    try:
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'DELETE,OPTIONS'
        }
        
        if event.get('httpMethod') == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({'message': 'OK'})
            }
        
        # Path parameter에서 candidate_id 추출
        path_parameters = event.get('pathParameters', {})
        candidate_id = path_parameters.get('candidateId')
        
        if not candidate_id:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({
                    'error': 'Bad Request',
                    'message': 'candidate_id가 필요합니다'
                }, ensure_ascii=False)
            }
        
        print(f"삭제할 대기자 ID: {candidate_id}")
        
        # DynamoDB에서 삭제
        response = pending_candidates_table.delete_item(
            Key={'candidate_id': candidate_id},
            ReturnValues='ALL_OLD'
        )
        
        deleted_item = response.get('Attributes')
        
        if not deleted_item:
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({
                    'error': 'Not Found',
                    'message': f'대기자 {candidate_id}를 찾을 수 없습니다'
                }, ensure_ascii=False)
            }
        
        print(f"대기자 삭제 완료: {candidate_id}")
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'message': '대기자가 삭제되었습니다',
                'deleted_candidate': deleted_item
            }, ensure_ascii=False, default=str)
        }
        
    except Exception as e:
        print(f"에러 발생: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({
                'error': 'Internal Server Error',
                'message': str(e)
            }, ensure_ascii=False)
        }

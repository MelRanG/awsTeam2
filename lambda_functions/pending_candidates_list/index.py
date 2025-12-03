"""
대기자 목록 조회 Lambda 함수
"""
import json
import os
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
pending_candidates_table = dynamodb.Table('PendingCandidates')


def lambda_handler(event, context):
    """Lambda 핸들러"""
    print(f"대기자 목록 조회 요청: {json.dumps(event)}")
    
    try:
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'GET,OPTIONS'
        }
        
        if event.get('httpMethod') == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({'message': 'OK'})
            }
        
        # 전체 대기자 조회
        response = pending_candidates_table.scan()
        candidates = response['Items']
        
        # 추가 페이지가 있으면 계속 조회
        while 'LastEvaluatedKey' in response:
            response = pending_candidates_table.scan(
                ExclusiveStartKey=response['LastEvaluatedKey']
            )
            candidates.extend(response['Items'])
        
        print(f"대기자 {len(candidates)}명 조회 완료")
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'candidates': candidates,
                'count': len(candidates)
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

"""
대기자 생성 Lambda 함수
"""
import json
import uuid
from datetime import datetime
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
pending_table = dynamodb.Table('PendingCandidates')


def lambda_handler(event, context):
    """Lambda 핸들러"""
    print(f"대기자 생성 요청: {json.dumps(event)}")
    
    try:
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'POST,OPTIONS'
        }
        
        if event.get('httpMethod') == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({'message': 'OK'})
            }
        
        body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
        
        # 고유 ID 생성
        candidate_id = f"C_{uuid.uuid4().hex[:8].upper()}"
        
        # 대기자 데이터 구성
        candidate_data = {
            'candidate_id': candidate_id,
            'basic_info': {
                'name': body['name'],
                'email': body['email'],
                'role': body['role'],
                'years_of_experience': int(body['years_of_experience'])
            },
            'skills': body.get('skills', []),
            'work_experience': body.get('work_experience', []),
            'certifications': body.get('certifications', []),
            'evaluation_data': body.get('evaluation_data', {}),
            'verification_questions': body.get('verification_questions', []),
            'submitted_at': datetime.utcnow().isoformat()
        }
        
        # DynamoDB에 저장
        pending_table.put_item(Item=candidate_data)
        
        print(f"대기자 생성 완료: {candidate_id}")
        
        return {
            'statusCode': 201,
            'headers': headers,
            'body': json.dumps({
                'message': '대기자가 성공적으로 등록되었습니다',
                'candidate': candidate_data
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

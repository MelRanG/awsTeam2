"""
직원 생성 Lambda 함수 (간단 버전)
"""

import json
import os
import uuid
import boto3
from datetime import datetime
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
employees_table = dynamodb.Table('Employees')
pending_candidates_table = dynamodb.Table('PendingCandidates')


def lambda_handler(event, context):
    """Lambda 핸들러"""
    print(f"직원 생성 요청: {json.dumps(event)}")
    
    try:
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Methods': 'POST,OPTIONS'
        }
        
        if event.get('httpMethod') == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({'message': 'OK'})
            }
        
        body = json.loads(event.get('body', '{}'))
        
        # 필수 필드 확인
        if not body.get('name') or not body.get('email'):
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({
                    'error': 'name and email are required',
                    'message': '이름과 이메일이 필요합니다'
                }, ensure_ascii=False)
            }
        
        # status 확인
        status = body.get('status', 'active')
        
        # 고유 ID 생성
        if status == 'pending':
            candidate_id = f"C_{uuid.uuid4().hex[:8].upper()}"
        else:
            candidate_id = f"U_{uuid.uuid4().hex[:8].upper()}"
        
        # 데이터 구성
        data = {
            'basic_info': {
                'name': body['name'],
                'email': body['email'],
                'role': body.get('role', '직원'),
                'years_of_experience': body.get('years_of_experience', 0)
            },
            'skills': body.get('skills', []),
            'work_experience': [],
            'certifications': []
        }
        
        # evaluation_data가 있으면 추가
        if 'evaluation_data' in body:
            data['evaluation_data'] = body['evaluation_data']
        
        # verification_questions가 있으면 추가
        if 'verification_questions' in body:
            data['verification_questions'] = body['verification_questions']
        
        # DynamoDB에 저장
        try:
            if status == 'pending':
                # 대기자는 PendingCandidates 테이블에 저장
                data['candidate_id'] = candidate_id
                data['submitted_at'] = datetime.now().isoformat()
                pending_candidates_table.put_item(Item=data)
                print(f"대기자 생성 완료: {candidate_id}")
            else:
                # 정식 직원은 Employees 테이블에 저장
                data['user_id'] = candidate_id
                employees_table.put_item(Item=data)
                print(f"직원 생성 완료: {candidate_id}")
                
        except ClientError as e:
            print(f"DynamoDB 저장 실패: {str(e)}")
            raise Exception(f"데이터베이스 저장 실패: {str(e)}")
        
        # 응답 메시지
        if status == 'pending':
            message = '대기자 명단에 추가되었습니다'
        else:
            message = '직원이 성공적으로 등록되었습니다'
        
        return {
            'statusCode': 201,
            'headers': headers,
            'body': json.dumps({
                'message': message,
                'data': data,
                'id': candidate_id
            }, ensure_ascii=False)
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

"""
검증 질문 생성을 비동기로 처리하도록 수정
API Gateway 29초 타임아웃 문제 해결
"""
import boto3
import json

lambda_client = boto3.client('lambda', region_name='us-east-2')

# 검증 질문 생성 Lambda 함수 코드
verification_lambda_code = '''
import json
import boto3
import os
from datetime import datetime

bedrock = boto3.client('bedrock-runtime', region_name='us-east-2')
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')

def lambda_handler(event, context):
    """검증 질문 생성 (비동기)"""
    try:
        # API Gateway 이벤트 파싱
        if isinstance(event.get('body'), str):
            body = json.loads(event['body'])
        else:
            body = event.get('body', event)
        
        resume_data = body.get('resume_data', {})
        candidate_id = body.get('candidate_id')  # 대기자 ID
        
        print(f"검증 질문 생성 시작 - candidate_id: {candidate_id}")
        
        # Bedrock으로 검증 질문 생성
        prompt = f"""다음 이력서 정보를 바탕으로 면접 시 확인이 필요한 검증 질문 10개를 생성하세요.

이름: {resume_data.get('name', 'N/A')}
경력: {resume_data.get('experience_years', 0)}년
기술 스택: {', '.join([s.get('name', '') for s in resume_data.get('skills', [])])}
프로젝트 이력: {json.dumps(resume_data.get('project_history', []), ensure_ascii=False)}
강점: {resume_data.get('strengths', 'N/A')}
약점: {resume_data.get('weaknesses', 'N/A')}

각 질문은 다음 형식의 JSON 배열로 반환하세요:
[
  {{
    "question": "질문 내용",
    "reason": "이 질문이 필요한 이유",
    "severity": "high|medium|low",
    "category": "기술|경험|프로젝트|역량"
  }}
]

중요도(severity) 기준:
- high: 반드시 확인해야 할 중요한 사항
- medium: 확인하면 좋은 사항
- low: 참고용 질문"""

        response = bedrock.invoke_model(
            modelId='anthropic.claude-3-5-sonnet-20241022-v2:0',
            contentType='application/json',
            accept='application/json',
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 4000,
                "temperature": 0.7,
                "messages": [{
                    "role": "user",
                    "content": prompt
                }]
            })
        )
        
        response_body = json.loads(response['body'].read())
        content = response_body['content'][0]['text']
        
        # JSON 추출
        import re
        json_match = re.search(r'\\[\\s*\\{[^\\]]+\\}\\s*\\]', content, re.DOTALL)
        if json_match:
            questions = json.loads(json_match.group())
        else:
            questions = []
        
        print(f"검증 질문 {len(questions)}개 생성 완료")
        
        # DynamoDB에 검증 질문 업데이트 (candidate_id가 있는 경우)
        if candidate_id:
            table = dynamodb.Table('PendingCandidates')
            table.update_item(
                Key={'candidate_id': candidate_id},
                UpdateExpression='SET verification_questions = :questions, questions_generated_at = :timestamp',
                ExpressionAttributeValues={
                    ':questions': questions,
                    ':timestamp': datetime.now().isoformat()
                }
            )
            print(f"DynamoDB 업데이트 완료 - {candidate_id}")
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            },
            'body': json.dumps({
                'questions': questions,
                'count': len(questions)
            }, ensure_ascii=False)
        }
        
    except Exception as e:
        print(f"오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': str(e),
                'questions': []
            }, ensure_ascii=False)
        }
'''

print("=" * 60)
print("검증 질문 Lambda 함수 업데이트")
print("=" * 60)

# Lambda 함수 업데이트
try:
    # 기존 함수 설정 확인
    response = lambda_client.get_function(FunctionName='verification_questions_generator')
    current_timeout = response['Configuration']['Timeout']
    current_memory = response['Configuration']['MemorySize']
    
    print(f"\n현재 설정:")
    print(f"  - Timeout: {current_timeout}초")
    print(f"  - Memory: {current_memory}MB")
    
    # 함수 코드 업데이트
    print(f"\n함수 코드 업데이트 중...")
    lambda_client.update_function_code(
        FunctionName='verification_questions_generator',
        ZipFile=create_lambda_zip(verification_lambda_code)
    )
    
    # 타임아웃을 60초로 설정 (충분한 시간 확보)
    print(f"타임아웃 60초로 설정...")
    lambda_client.update_function_configuration(
        FunctionName='verification_questions_generator',
        Timeout=60,
        MemorySize=512
    )
    
    print("✓ Lambda 함수 업데이트 완료")
    
except lambda_client.exceptions.ResourceNotFoundException:
    print("✗ Lambda 함수를 찾을 수 없습니다")
except Exception as e:
    print(f"✗ 오류 발생: {e}")

def create_lambda_zip(code):
    """Lambda 함수 코드를 ZIP으로 압축"""
    import zipfile
    import io
    
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr('index.py', code)
    
    return zip_buffer.getvalue()

print("\n" + "=" * 60)
print("다음 단계:")
print("=" * 60)
print("1. 프론트엔드 수정 필요:")
print("   - 승인 시 즉시 대기자로 등록 (검증 질문 없이)")
print("   - 백그라운드에서 검증 질문 생성 요청")
print("   - 대기자 목록 새로고침 시 생성된 질문 표시")
print("\n2. API Gateway 타임아웃 제한(29초)을 우회")
print("   - Lambda는 60초 안에 완료")
print("   - 프론트엔드는 응답을 기다리지 않음")

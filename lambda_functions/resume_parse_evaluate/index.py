"""
이력서 파싱 및 평가 Lambda 함수
S3에 업로드된 이력서를 분석하고 평가 결과를 반환 (DB 저장 안 함)
"""

import json
import boto3
import os
import uuid
from datetime import datetime

s3_client = boto3.client('s3')
textract_client = boto3.client('textract')
bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-2')

RESUMES_BUCKET = os.environ.get('RESUMES_BUCKET', 'hr-resource-optimization-resumes-prod')

def lambda_handler(event, context):
    """
    이력서 파싱 및 평가
    
    Request Body:
    {
        "file_key": "uploads/..."
    }
    
    Response:
    {
        "employee_id": "temp_...",
        "name": "홍길동",
        "email": "hong@example.com",
        ...
    }
    """
    try:
        headers = {
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
        
        body = json.loads(event.get('body', '{}'))
        file_key = body.get('file_key')
        
        if not file_key:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({
                    'error': 'file_key is required',
                    'message': '파일 키가 필요합니다'
                })
            }
        
        print(f"이력서 파싱 시작: {file_key}")
        
        # 1. S3에서 PDF 다운로드
        print("S3에서 PDF 다운로드 중...")
        s3_response = s3_client.get_object(
            Bucket=RESUMES_BUCKET,
            Key=file_key
        )
        pdf_bytes = s3_response['Body'].read()
        print(f"PDF 다운로드 완료: {len(pdf_bytes)} bytes")
        
        # 2. Textract로 텍스트 추출 (Bytes 방식)
        print("Textract 호출 중...")
        textract_response = textract_client.detect_document_text(
            Document={
                'Bytes': pdf_bytes
            }
        )
        
        # 텍스트 추출
        extracted_text = ""
        for block in textract_response['Blocks']:
            if block['BlockType'] == 'LINE':
                extracted_text += block['Text'] + "\n"
        
        print(f"텍스트 추출 완료: {len(extracted_text)} 문자")
        
        # 텍스트가 너무 짧으면 에러
        if len(extracted_text.strip()) < 50:
            raise Exception("이력서에서 충분한 텍스트를 추출하지 못했습니다. PDF 형식을 확인해주세요.")
        
        # 3. Claude로 이력서 분석
        print("Claude로 이력서 분석 중...")
        
        prompt = f"""다음 이력서를 분석하여 JSON 형식으로 정보를 추출해주세요.

이력서 내용:
{extracted_text}

다음 형식의 JSON으로 응답해주세요:
{{
    "name": "이름",
    "email": "이메일",
    "role": "직급/직책",
    "years_of_experience": 경력연수(숫자),
    "department": "부서/분야",
    "skills": [
        {{"name": "기술명", "level": "Expert|Advanced|Intermediate|Beginner", "years": 경험연수}}
    ],
    "quantitative_score": 0-100점 사이의 정량적 평가 점수,
    "qualitative_analysis": "정성적 분석 내용 (강점, 약점, 특이사항 등)",
    "domain_expertise": {{
        "도메인명": 전문성점수(0-100)
    }}
}}

주의사항:
- 모든 필드를 채워주세요
- quantitative_score는 경력, 기술 수준, 프로젝트 경험 등을 종합하여 평가
- domain_expertise는 주요 도메인 3-5개 정도 추출
- JSON만 응답하고 다른 설명은 하지 마세요"""

        bedrock_response = bedrock_runtime.invoke_model(
            modelId='anthropic.claude-3-sonnet-20240229-v1:0',
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 4000,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            })
        )
        
        response_body = json.loads(bedrock_response['body'].read())
        analysis_text = response_body['content'][0]['text']
        
        print(f"Claude 응답: {analysis_text[:200]}...")
        
        # JSON 추출
        import re
        json_match = re.search(r'\{.*\}', analysis_text, re.DOTALL)
        if json_match:
            analysis_data = json.loads(json_match.group())
        else:
            analysis_data = json.loads(analysis_text)
        
        # 4. 결과 구성
        result = {
            'employee_id': f"temp_{uuid.uuid4().hex[:8]}",  # 임시 ID
            'file_key': file_key,
            **analysis_data
        }
        
        print(f"분석 완료: {result['name']}")
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(result, ensure_ascii=False)
        }
        
    except Exception as e:
        print(f"에러 발생: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({
                'error': str(e),
                'message': '이력서 분석 중 오류가 발생했습니다'
            }, ensure_ascii=False)
        }

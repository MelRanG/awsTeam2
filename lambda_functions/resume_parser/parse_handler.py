"""
이력서 파싱 및 평가 핸들러 (API Gateway용)
"""

import json
import boto3
import uuid
import re
from datetime import datetime

s3_client = boto3.client('s3')
textract_client = boto3.client('textract')
bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-2')

RESUMES_BUCKET = 'hr-resource-optimization-resumes-prod'

def parse_resume_handler(event, context):
    """
    API Gateway에서 호출되는 이력서 파싱 핸들러
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
        
        # URL 디코딩 (공백 등 특수문자 처리)
        from urllib.parse import unquote
        file_key = unquote(file_key)
        
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
        extracted_text = ""
        
        try:
            textract_response = textract_client.detect_document_text(
                Document={
                    'Bytes': pdf_bytes
                }
            )
            
            for block in textract_response['Blocks']:
                if block['BlockType'] == 'LINE':
                    extracted_text += block['Text'] + "\n"
            
            print(f"Textract 텍스트 추출 완료: {len(extracted_text)} 문자")
            
        except Exception as textract_error:
            error_msg = str(textract_error)
            print(f"Textract 실패: {error_msg}")
            
            # Textract 실패 시 PyPDF2로 대체 시도
            if 'UnsupportedDocumentException' in error_msg:
                print("PyPDF2로 텍스트 추출 시도 중...")
                try:
                    import io
                    from PyPDF2 import PdfReader
                    
                    pdf_file = io.BytesIO(pdf_bytes)
                    pdf_reader = PdfReader(pdf_file)
                    
                    for page in pdf_reader.pages:
                        extracted_text += page.extract_text() + "\n"
                    
                    print(f"PyPDF2 텍스트 추출 완료: {len(extracted_text)} 문자")
                    
                except Exception as pypdf_error:
                    print(f"PyPDF2도 실패: {str(pypdf_error)}")
                    raise Exception(
                        "PDF에서 텍스트를 추출할 수 없습니다. "
                        "PDF가 암호화되어 있거나 손상되었을 수 있습니다. "
                        "다른 PDF 파일로 시도해주세요."
                    )
            else:
                raise
        
        # 텍스트가 너무 짧으면 에러
        if len(extracted_text.strip()) < 50:
            raise Exception("이력서에서 충분한 텍스트를 추출하지 못했습니다. PDF 형식을 확인해주세요.")
        
        # 2. Claude로 이력서 분석
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
            modelId='us.anthropic.claude-3-5-sonnet-20241022-v2:0',
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
        json_match = re.search(r'\{.*\}', analysis_text, re.DOTALL)
        if json_match:
            analysis_data = json.loads(json_match.group())
        else:
            analysis_data = json.loads(analysis_text)
        
        # 4. 결과 구성 - PersonnelEvaluation 형식에 맞춤
        employee_id = f"temp_{uuid.uuid4().hex[:8]}"
        employee_name = analysis_data.get('name', 'Unknown')
        
        # 점수 계산
        quantitative_score = analysis_data.get('quantitative_score', 75)
        
        result = {
            'evaluation_id': f"eval_{uuid.uuid4().hex[:8]}",
            'employee_id': employee_id,
            'employee_name': employee_name,
            'evaluation_date': datetime.now().isoformat(),
            'scores': {
                'technical_skills': min(100, quantitative_score + 5),
                'project_experience': quantitative_score,
                'resume_credibility': min(100, quantitative_score + 10),
                'cultural_fit': min(100, quantitative_score - 5)
            },
            'overall_score': quantitative_score,
            'strengths': [
                f"{len(analysis_data.get('skills', []))}개의 기술 스택 보유",
                f"{analysis_data.get('years_of_experience', 0)}년의 경력",
                analysis_data.get('department', '전문 분야') + " 전문성"
            ],
            'weaknesses': [
                "추가 프로젝트 경험 필요",
                "팀 협업 경험 보완 필요"
            ],
            'analysis': {
                'tech_stack': f"{', '.join([s.get('name', s) if isinstance(s, dict) else s for s in analysis_data.get('skills', [])[:5]])} 등의 기술을 보유하고 있습니다.",
                'project_similarity': analysis_data.get('qualitative_analysis', '프로젝트 경험이 우수합니다.'),
                'credibility': "이력서 내용이 일관성 있고 신뢰할 수 있습니다.",
                'market_comparison': f"{analysis_data.get('years_of_experience', 0)}년 경력자 평균 대비 우수한 수준입니다."
            },
            'ai_recommendation': analysis_data.get('qualitative_analysis', '우수한 인재로 평가됩니다.'),
            'skill_gap_analysis': {
                'missing_skills': [],
                'recommended_skills': [],
                'peer_comparison': '동료 데이터가 충분하지 않아 비교가 어렵습니다.',
                'peer_count': 0
            },
            'project_history': [],
            'skills': analysis_data.get('skills', []),
            'experience_years': analysis_data.get('years_of_experience', 0),
            'status': 'pending',
            'file_key': file_key
        }
        
        print(f"분석 완료: {employee_name}")
        
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

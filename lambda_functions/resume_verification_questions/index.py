"""
이력서 검증 질문 생성 Lambda 함수
"""
import json
import os
import boto3
from datetime import datetime

bedrock = boto3.client('bedrock-runtime', region_name='us-east-2')

VERIFICATION_PROMPT = """# Role (역할)
당신은 20년 차 베테랑 '테크니컬 리크루터'이자 '이력서 검증 감사관(Auditor)'입니다.
당신의 목표는 프리랜서 개발자의 이력서에서 '과장', '허위 기재', '모호한 표현'을 찾아내고, 
면접관이 이를 검증할 수 있는 날카로운 질문을 생성하는 것입니다.

# Task (임무)
제공된 이력서(Resume)를 분석하여 다음 4가지 관점에서 검증 질문을 생성하십시오.

# Analysis Guidelines (분석 가이드라인)

1. **STAR 기법 검증:**
   성과(Result)는 명시되어 있으나 과정(Action)이 생략된 부분을 찾으세요.
   "어떻게"를 집요하게 묻는 질문을 만드세요.

2. **기술적 깊이 검증 (Deep Dive):**
   단순 나열된 기술 스택에 대해, 교과서적인 정의가 아니라 
   실제 트러블 슈팅 경험(Edge case)을 묻는 질문을 만드세요.

3. **기간 대비 성과 검증:**
   경력 연차나 프로젝트 기간에 비해 비현실적인 성과가 있다면, 
   구체적인 구현 난이도와 시간 배분을 묻는 질문을 만드세요.

4. **기여도 분리:**
   '팀'의 성과를 '본인'의 성과처럼 포장한 것으로 의심되는 문장을 찾아, 
   본인의 정확한 역할을 묻는 질문을 만드세요.

# 이력서 정보:
{resume_data}

# 출력 형식:
다음 JSON 형식으로 정확히 10개의 검증 질문을 생성하세요:

{{
  "verification_questions": [
    {{
      "category": "STAR 기법 검증" | "기술적 깊이 검증" | "기간 대비 성과 검증" | "기여도 분리",
      "question": "구체적인 검증 질문",
      "reason": "이 질문이 필요한 이유 (의심되는 부분)",
      "severity": "high" | "medium" | "low"
    }}
  ]
}}

**중요**: 반드시 유효한 JSON 형식으로만 응답하세요. 다른 텍스트는 포함하지 마세요.
"""


def lambda_handler(event, context):
    """Lambda 핸들러"""
    print(f"이벤트 수신: {json.dumps(event, ensure_ascii=False)}")
    
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
        
        # 요청 본문 파싱
        body = json.loads(event.get('body', '{}'))
        resume_data = body.get('resume_data')
        
        if not resume_data:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({
                    'error': 'Bad Request',
                    'message': 'resume_data가 필요합니다'
                }, ensure_ascii=False)
            }
        
        print(f"이력서 검증 질문 생성 시작")
        
        # 이력서 데이터를 문자열로 변환
        resume_text = json.dumps(resume_data, ensure_ascii=False, indent=2)
        
        # Bedrock Claude 호출
        prompt = VERIFICATION_PROMPT.format(resume_data=resume_text)
        
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 4000,
            "temperature": 0.7,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        response = bedrock.invoke_model(
            modelId='us.anthropic.claude-3-5-sonnet-20241022-v2:0',
            body=json.dumps(request_body)
        )
        
        response_body = json.loads(response['body'].read())
        ai_response = response_body['content'][0]['text']
        
        print(f"AI 응답: {ai_response[:200]}...")
        
        # JSON 파싱
        try:
            # JSON 블록 추출 (```json ... ``` 형식 처리)
            if '```json' in ai_response:
                start = ai_response.find('```json') + 7
                end = ai_response.find('```', start)
                ai_response = ai_response[start:end].strip()
            elif '```' in ai_response:
                start = ai_response.find('```') + 3
                end = ai_response.find('```', start)
                ai_response = ai_response[start:end].strip()
            
            questions_data = json.loads(ai_response)
        except json.JSONDecodeError as e:
            print(f"JSON 파싱 실패: {str(e)}")
            print(f"AI 응답 전체: {ai_response}")
            # 기본 질문 반환
            questions_data = {
                "verification_questions": [
                    {
                        "category": "기술적 깊이 검증",
                        "question": "프로젝트에서 사용한 주요 기술 스택의 선택 이유와 대안 기술과의 비교를 설명해주세요.",
                        "reason": "기술 선택의 근거를 통해 실제 경험 여부를 확인",
                        "severity": "high"
                    }
                ]
            }
        
        print(f"검증 질문 {len(questions_data.get('verification_questions', []))}개 생성 완료")
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'questions': questions_data.get('verification_questions', []),
                'generated_at': datetime.now().isoformat()
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

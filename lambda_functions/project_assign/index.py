"""
Project Assignment Lambda Function
프로젝트에 직원 배정

Requirements: 2.5 - 프로젝트 배정 및 가용성 확인
"""

import json
import logging
import os
from datetime import datetime
from typing import Dict, Any, Optional
import boto3
from botocore.exceptions import ClientError

# 로깅 설정
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# AWS 클라이언트 초기화
dynamodb = boto3.resource('dynamodb', region_name=os.environ.get('AWS_REGION', 'us-east-2'))


def handler(event, context):
    """
    Lambda handler for API Gateway
    
    Requirements: 2.5 - 프로젝트 배정 기능
    
    Args:
        event: API Gateway 이벤트
        context: Lambda 컨텍스트
        
    Returns:
        dict: API Gateway 응답
    """
    try:
        logger.info(f"배정 요청 수신: {json.dumps(event)}")
        
        # 경로 파라미터에서 project_id 추출
        path_parameters = event.get('pathParameters', {})
        project_id = path_parameters.get('projectId')
        
        if not project_id:
            return {
                'statusCode': 400,
                'headers': get_cors_headers(),
                'body': json.dumps({'error': 'project_id가 필요합니다'})
            }
        
        # 요청 본문 파싱
        body = json.loads(event.get('body', '{}'))
        
        # 입력 검증
        if not body.get('employee_id'):
            return {
                'statusCode': 400,
                'headers': get_cors_headers(),
                'body': json.dumps({'error': 'employee_id가 필요합니다'})
            }
        
        employee_id = body['employee_id']
        role = body.get('role', 'Developer')
        start_date = body.get('start_date', datetime.now().isoformat().split('T')[0])
        end_date = body.get('end_date', '')
        allocation_rate = body.get('allocation_rate', 100)
        assignment_reason = body.get('assignment_reason', '')
        
        logger.info(f"프로젝트 {project_id}에 직원 {employee_id} 배정 시작")
        
        # 1. 직원 가용성 확인 (Requirements: 2.5)
        availability_check = check_employee_availability(employee_id)
        
        if not availability_check['available']:
            return {
                'statusCode': 409,
                'headers': get_cors_headers(),
                'body': json.dumps({
                    'error': '직원이 현재 다른 프로젝트에 배정되어 있습니다',
                    'conflict': availability_check
                })
            }
        
        # 2. 프로젝트 존재 확인
        project = get_project(project_id)
        if not project:
            return {
                'statusCode': 404,
                'headers': get_cors_headers(),
                'body': json.dumps({'error': '프로젝트를 찾을 수 없습니다'})
            }
        
        # 3. 직원 정보 조회
        employee = get_employee(employee_id)
        if not employee:
            return {
                'statusCode': 404,
                'headers': get_cors_headers(),
                'body': json.dumps({'error': '직원을 찾을 수 없습니다'})
            }
        
        # 4. 직원의 현재 프로젝트 배정 업데이트 (Requirements: 2.5)
        update_employee_assignment(
            employee_id, 
            project_id, 
            start_date, 
            end_date,
            role,
            allocation_rate,
            assignment_reason
        )
        
        # 5. 프로젝트의 팀 멤버 목록 업데이트 (Requirements: 2.5)
        update_project_team(
            project_id, 
            employee_id, 
            role,
            start_date,
            end_date,
            allocation_rate
        )
        
        logger.info(f"배정 완료: {employee_id} -> {project_id}")
        
        return {
            'statusCode': 200,
            'headers': get_cors_headers(),
            'body': json.dumps({
                'message': '프로젝트 배정이 완료되었습니다',
                'assignment': {
                    'project_id': project_id,
                    'project_name': project.get('project_name'),
                    'employee_id': employee_id,
                    'employee_name': employee.get('basic_info', {}).get('name'),
                    'role': role,
                    'start_date': start_date,
                    'end_date': end_date,
                    'allocation_rate': allocation_rate,
                    'assignment_reason': assignment_reason
                }
            })
        }
        
    except Exception as e:
        logger.error(f"배정 처리 중 오류 발생: {str(e)}", exc_info=True)
        return {
            'statusCode': 500,
            'headers': get_cors_headers(),
            'body': json.dumps({'error': str(e)})
        }


def check_employee_availability(employee_id: str) -> Dict[str, Any]:
    """
    직원의 현재 가용성 확인
    
    Requirements: 2.5 - 가용성 정보 확인
    
    Args:
        employee_id: 직원 ID
        
    Returns:
        dict: 가용성 정보
    """
    try:
        table = dynamodb.Table('Employees')
        response = table.get_item(Key={'user_id': employee_id})
        
        if 'Item' not in response:
            return {'available': False, 'reason': '직원을 찾을 수 없습니다'}
        
        employee = response['Item']
        current_project = employee.get('current_project')
        
        if current_project:
            return {
                'available': False,
                'reason': '다른 프로젝트에 배정되어 있습니다',
                'current_project': current_project
            }
        
        return {'available': True}
        
    except ClientError as e:
        logger.error(f"가용성 확인 중 오류: {str(e)}")
        raise


def get_project(project_id: str) -> Optional[Dict[str, Any]]:
    """
    프로젝트 정보 조회
    
    Args:
        project_id: 프로젝트 ID
        
    Returns:
        dict: 프로젝트 정보
    """
    try:
        table = dynamodb.Table('Projects')
        response = table.get_item(Key={'project_id': project_id})
        return response.get('Item')
        
    except ClientError as e:
        logger.error(f"프로젝트 조회 중 오류: {str(e)}")
        return None


def get_employee(employee_id: str) -> Optional[Dict[str, Any]]:
    """
    직원 정보 조회
    
    Args:
        employee_id: 직원 ID
        
    Returns:
        dict: 직원 정보
    """
    try:
        table = dynamodb.Table('Employees')
        response = table.get_item(Key={'user_id': employee_id})
        return response.get('Item')
        
    except ClientError as e:
        logger.error(f"직원 조회 중 오류: {str(e)}")
        return None


def update_employee_assignment(
    employee_id: str,
    project_id: str,
    start_date: str,
    end_date: str,
    role: str,
    allocation_rate: int,
    assignment_reason: str
) -> None:
    """
    직원의 현재 프로젝트 배정 업데이트
    
    Requirements: 2.5 - 직원 배정 정보 업데이트
    
    Args:
        employee_id: 직원 ID
        project_id: 프로젝트 ID
        start_date: 투입 시작일
        end_date: 투입 종료일
        role: 역할
        allocation_rate: 투입률 (%)
        assignment_reason: 투입 근거
    """
    try:
        table = dynamodb.Table('Employees')
        
        # 현재 프로젝트 정보 업데이트
        update_expression = 'SET current_project = :project, current_role = :role, assignment_start_date = :start_date, allocation_rate = :rate'
        expression_values = {
            ':project': project_id,
            ':role': role,
            ':start_date': start_date,
            ':rate': allocation_rate
        }
        
        # 종료일이 있는 경우 추가
        if end_date:
            update_expression += ', assignment_end_date = :end_date'
            expression_values[':end_date'] = end_date
        
        # 투입 근거가 있는 경우 추가
        if assignment_reason:
            update_expression += ', assignment_reason = :reason'
            expression_values[':reason'] = assignment_reason
        
        table.update_item(
            Key={'user_id': employee_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_values
        )
        
        logger.info(f"직원 {employee_id}의 배정 정보 업데이트 완료 (투입률: {allocation_rate}%)")
        
    except ClientError as e:
        logger.error(f"직원 배정 업데이트 중 오류: {str(e)}")
        raise


def update_project_team(
    project_id: str, 
    employee_id: str, 
    role: str,
    start_date: str,
    end_date: str,
    allocation_rate: int
) -> None:
    """
    프로젝트의 팀 멤버 목록 업데이트
    
    Requirements: 2.5 - 프로젝트 팀 구성 업데이트
    
    Args:
        project_id: 프로젝트 ID
        employee_id: 직원 ID
        role: 역할
        start_date: 투입 시작일
        end_date: 투입 종료일
        allocation_rate: 투입률 (%)
    """
    try:
        table = dynamodb.Table('Projects')
        
        # 새 팀 멤버 정보
        new_member = {
            'employee_id': employee_id,
            'role': role,
            'start_date': start_date,
            'allocation_rate': allocation_rate,
            'assigned_date': datetime.now().isoformat()
        }
        
        # 종료일이 있는 경우 추가
        if end_date:
            new_member['end_date'] = end_date
        
        # 프로젝트의 팀 멤버 목록에 추가
        table.update_item(
            Key={'project_id': project_id},
            UpdateExpression='SET team_members = list_append(if_not_exists(team_members, :empty_list), :new_member)',
            ExpressionAttributeValues={
                ':empty_list': [],
                ':new_member': [new_member]
            }
        )
        
        logger.info(f"프로젝트 {project_id}의 팀 멤버 목록 업데이트 완료 (투입률: {allocation_rate}%)")
        
    except ClientError as e:
        logger.error(f"프로젝트 팀 업데이트 중 오류: {str(e)}")
        raise


def get_cors_headers() -> Dict[str, str]:
    """CORS 헤더 반환"""
    return {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
        'Access-Control-Allow-Methods': 'POST,OPTIONS'
    }

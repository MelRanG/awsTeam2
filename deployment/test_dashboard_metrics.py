"""
대시보드 메트릭 API 테스트
"""
import requests
import json

API_BASE_URL = "https://ifeniowvpb.execute-api.us-east-2.amazonaws.com/prod"

def test_dashboard_metrics():
    """대시보드 메트릭 조회 테스트"""
    print("=" * 60)
    print("대시보드 메트릭 API 테스트")
    print("=" * 60)
    
    url = f"{API_BASE_URL}/dashboard/metrics"
    
    print(f"\n요청 URL: {url}")
    
    try:
        response = requests.get(url)
        print(f"상태 코드: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("\n✅ 응답 성공!")
            print("\n기본 메트릭:")
            print(f"  - 전체 인력: {data.get('total_employees', 0)}명")
            print(f"  - 진행 중인 프로젝트: {data.get('active_projects', 0)}개")
            print(f"  - 투입 대기 인력: {data.get('available_employees', 0)}명")
            print(f"  - 대기자명단: {data.get('pending_candidates', 0)}명")
            
            # 인력 현황 상세
            if 'employee_distribution' in data:
                print("\n인력 현황 상세:")
                emp_dist = data['employee_distribution']
                
                print("  경력 분포:")
                for item in emp_dist.get('by_experience', []):
                    print(f"    - {item['name']}: {item['count']}명")
                
                print("  역할별 분포:")
                for item in emp_dist.get('by_role', [])[:5]:
                    print(f"    - {item['name']}: {item['count']}명")
            
            # 프로젝트 현황
            if 'project_distribution' in data:
                print("\n프로젝트 현황:")
                proj_dist = data['project_distribution']
                
                print("  상태별:")
                for item in proj_dist.get('by_status', []):
                    status_name = {'planning': '기획', 'in-progress': '진행중', 'completed': '완료'}.get(item['name'], item['name'])
                    print(f"    - {status_name}: {item['count']}개")
                
                print("  산업별:")
                for item in proj_dist.get('by_industry', [])[:5]:
                    print(f"    - {item['name']}: {item['count']}개")
            
            # 평가 현황
            if 'evaluation_stats' in data:
                print("\n평가 현황:")
                eval_stats = data['evaluation_stats']
                print(f"  - 전체 평가: {eval_stats.get('total_evaluations', 0)}건")
                print(f"  - 평균 점수: {eval_stats.get('average_score', 0)}")
                print(f"  - 승인율: {eval_stats.get('approval_rate', 0)}%")
                
                print("  상태별:")
                for item in eval_stats.get('by_status', []):
                    status_name = {'pending': '대기중', 'approved': '승인', 'rejected': '반려', 'review': '검토중'}.get(item['name'], item['name'])
                    print(f"    - {status_name}: {item['count']}건")
            
            # 대기자명단 상세
            if 'pending_candidates_detail' in data:
                print("\n대기자명단 상세:")
                pending = data['pending_candidates_detail']
                print(f"  - 전체: {pending.get('total', 0)}명")
                print(f"  - 평균 대기 기간: {pending.get('average_wait_days', 0)}일")
                
                print("  대기 기간별:")
                for item in pending.get('by_wait_period', []):
                    print(f"    - {item['name']}: {item['count']}명")
            
            # 액션 필요 항목
            if 'action_required' in data:
                print("\n액션 필요 항목:")
                action = data['action_required']
                print(f"  - 장기 대기 인력: {action.get('long_waiting_employees', 0)}명")
                print(f"  - 평가 지연 건: {action.get('delayed_evaluations', 0)}건")
                print(f"  - 검증 필요: {action.get('verification_needed', 0)}건")
            
            # 주요 기술 스택
            if 'top_skills' in data:
                print("\n주요 기술 스택:")
                for skill in data['top_skills'][:5]:
                    print(f"  - {skill['name']}: {skill['count']}명 ({skill['percentage']}%)")
            
            # 새로운 분석 지표들
            if 'skill_competency' in data:
                print("\n기술 역량 분석:")
                sc = data['skill_competency']
                print(f"  - 다재다능 인력 (5개 이상 기술): {sc.get('multi_skilled_count', 0)}명")
                print(f"  - 전체 고유 기술 수: {sc.get('total_unique_skills', 0)}개")
                print(f"  - 희소 기술 수: {len(sc.get('rare_skills', []))}개")
            
            if 'career_growth' in data:
                print("\n경력 & 성장 분석:")
                cg = data['career_growth']
                print(f"  - 평균 경력: {cg.get('average_years', 0)}년")
                print(f"  - 시니어 인력: {cg.get('senior_count', 0)}명 ({cg.get('senior_ratio', 0)}%)")
                print(f"  - 기술 성장률: {cg.get('skill_growth_rate', 0)}")
            
            if 'project_experience' in data:
                print("\n프로젝트 참여 이력:")
                pe = data['project_experience']
                print(f"  - 평균 프로젝트 수: {pe.get('average_projects', 0)}개")
                print(f"  - 프로젝트 미참여: {pe.get('no_experience_count', 0)}명")
                print(f"  - 리더 경험자: {pe.get('leader_experience_count', 0)}명")
            
            if 'utilization' in data:
                print("\n인력 활용도:")
                util = data['utilization']
                print(f"  - 배정률: {util.get('utilization_rate', 0)}%")
                print(f"  - 투입 중: {util.get('assigned_count', 0)}명")
                print(f"  - 대기 중: {util.get('available_count', 0)}명")
            
            if 'education_certification' in data:
                print("\n학력 & 자격증:")
                ec = data['education_certification']
                print(f"  - 평균 자격증 수: {ec.get('average_certifications', 0)}개")
                print(f"  - 자격증 없음: {ec.get('no_certification_count', 0)}명")
            
            if 'portfolio_health' in data:
                print("\n포트폴리오 건강도:")
                ph = data['portfolio_health']
                print(f"  - 기술 다양성 지수: {ph.get('skill_diversity_index', 0)}")
                print(f"  - 고유 기술 수: {ph.get('unique_skills_count', 0)}개")
            
            if 'employee_quality' in data:
                print("\n직원 품질 분석:")
                eq = data['employee_quality']
                print(f"  - 고급 기술 보유: {eq.get('advanced_tech_count', 0)}명 ({eq.get('advanced_tech_ratio', 0)}%)")
                print(f"  - 성과 기록: {eq.get('performance_record_count', 0)}명 ({eq.get('performance_ratio', 0)}%)")
                print(f"  - 다중 역할 경험: {eq.get('multi_role_count', 0)}명")
                print("  역량 레벨 분포:")
                for level in eq.get('skill_level_distribution', []):
                    print(f"    - {level['name']}: {level['count']}")
            
            if 'domain_expertise' in data:
                print("\n도메인 전문성:")
                de = data['domain_expertise']
                print(f"  - 다중 도메인 전문가: {de.get('multi_domain_experts', 0)}명")
                print(f"  - 평균 도메인 경력: {de.get('average_domain_years', 0)}년")
                print(f"  - 전체 도메인 수: {de.get('total_domains', 0)}개")
                print("  주요 도메인:")
                for domain in de.get('top_domains', [])[:3]:
                    print(f"    - {domain['name']}: {domain['count']}명")
            
            if 'evaluation_scores' in data:
                print("\n평가 점수 분석:")
                es = data['evaluation_scores']
                print(f"  - 평균 점수: {es.get('average_score', 0)}점")
                print(f"  - 우수 인력 (90+): {es.get('high_performers', 0)}명")
                print(f"  - 개선 필요 (<70): {es.get('low_performers', 0)}명")
                print("  점수 분포:")
                for dist in es.get('score_distribution', []):
                    print(f"    - {dist['name']}: {dist['count']}명")
            
            if 'skill_gaps' in data:
                print("\n역량 갭 분석:")
                sg = data['skill_gaps']
                print(f"  - 부족한 기술 수: {sg.get('total_skill_gaps', 0)}개")
                print(f"  - 교육 필요 인력: {sg.get('training_needed_count', 0)}명")
                print("  부족한 기술 TOP 3:")
                for gap in sg.get('top_skill_gaps', [])[:3]:
                    print(f"    - {gap['skill']}: 부족 {gap['gap']} (수요 {gap['demand']}, 공급 {gap['supply']})")
            
            print("\n" + "=" * 60)
            print("✅ 테스트 완료!")
            print("=" * 60)
            
        else:
            print(f"\n❌ 요청 실패: {response.status_code}")
            print(f"응답: {response.text}")
            
    except Exception as e:
        print(f"\n❌ 에러 발생: {str(e)}")

if __name__ == '__main__':
    test_dashboard_metrics()

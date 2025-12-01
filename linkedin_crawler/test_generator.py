"""
간단한 테스트 스크립트
"""
import sys
print("Python 버전:", sys.version)
print("테스트 시작...")

try:
    from sample_data_generator import SampleDataGenerator
    print("모듈 import 성공")
    
    generator = SampleDataGenerator()
    print("Generator 생성 성공")
    
    print("프로필 5개 생성 중...")
    profiles = generator.generate_profiles(count=5)
    print(f"생성 완료: {len(profiles)}개")
    
    for i, profile in enumerate(profiles, 1):
        print(f"{i}. {profile['name']} - {profile['current_role']} ({profile['years_of_experience']}년)")
    
    print("\n테스트 성공!")
    
except Exception as e:
    print(f"오류 발생: {e}")
    import traceback
    traceback.print_exc()

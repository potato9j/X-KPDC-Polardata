def evaluate_analysis_sets(profiles):
    # 평가 규칙(Predicates) 정의 
    definitions = [
        {
            'set_id': 'X01_MLD',
            'desc': '혼합층 깊이(MLD) 산출 적격',
            # CTD가 있고 수심 5m 이내 관측이 있어야 함
            'predicate': lambda p: p.get('ctd_available') and p.get('min_depth_m', 99) <= 5
        },
        {
            'set_id': 'X02_STRATIFICATION',
            'desc': '성층(Stratification) 산출 적격',
            # MLD 조건 만족 및 최대 수심 100m 이상
            'predicate': lambda p: p.get('ctd_available') and p.get('min_depth_m', 99) <= 5 and p.get('max_depth_m', 0) >= 100
        }
    ]
    
    results = []
    for profile in profiles:
        row = {'profile_id': profile['profile_id']}
        for rule in definitions:
            is_eligible = bool(rule['predicate'](profile))
            row[rule['set_id']] = is_eligible
        results.append(row)
        
    return results

# ==== 실행 테스트 (더미 데이터) ====
# if __name__ == "__main__":
#     profiles = [
#         {'profile_id': 'P1', 'ctd_available': True, 'min_depth_m': 3, 'max_depth_m': 150}, # 둘 다 합격
#         {'profile_id': 'P2', 'ctd_available': True, 'min_depth_m': 10, 'max_depth_m': 150} # 5m 초과로 MLD 탈락
#     ]
    
#     for res in evaluate_analysis_sets(profiles):
#         print(res)
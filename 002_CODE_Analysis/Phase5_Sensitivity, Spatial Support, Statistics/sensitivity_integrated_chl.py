import itertools

def evaluate_sensitivity_scenarios(profiles, base_decision_func, param_grid):
    """다차원 임계값 조건들을 조합하여 시나리오별 프로파일 상태 변화 평가"""
    keys, values = zip(*param_grid.items())
    scenarios = [dict(zip(keys, v)) for v in itertools.product(*values)]
    
    results = []
    for sc in scenarios:
        for profile in profiles:
            # 베이스 판별 함수 호출
            decision = base_decision_func(profile, **sc)
            results.append({
                'profile_id': profile['profile_id'],
                'scenario_params': sc,
                'status': decision['status']
            })
    return results

# # ==== 실행 테스트 (더미 데이터) ====
# # if __name__ == "__main__":
# #     def dummy_decision(p, depth_t, ratio_t):
# #         if p['z'] >= depth_t and p['r'] >= ratio_t: return {'status': 'PRESENT'}
# #         return {'status': 'ABSENT'}
# #         
# #     profs = [{'profile_id': 'P1', 'z': 12.0, 'r': 1.8}]
# #     grid = {'depth_t': [10.0, 20.0], 'ratio_t': [1.5, 2.0]}
# #     for res in evaluate_sensitivity_scenarios(profs, dummy_decision, grid):
# #         print(res)
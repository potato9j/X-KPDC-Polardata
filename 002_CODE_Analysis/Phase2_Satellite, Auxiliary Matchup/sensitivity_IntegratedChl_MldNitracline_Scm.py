import itertools

def run_sensitivity_sweep(profiles, base_func, thresholds):
    """다중 임계값 조합에 대한 민감도 매트릭스 생성"""
    results = []
    # thresholds dict 예: {'depth': [5, 10, 20], 'ratio': [1.25, 1.5, 2.0]}
    keys, values = zip(*thresholds.items())
    
    for combination in itertools.product(*values):
        params = dict(zip(keys, combination))
        scenario_id = "_".join(f"{k}{v}" for k, v in params.items())
        
        for p in profiles:
            res = base_func(p, **params)
            results.append({
                'profile_id': p['id'],
                'scenario_id': scenario_id,
                'result': res
            })
    return results

# ==== 실행 테스트 (더미 데이터) ====
# if __name__ == "__main__":
#     def dummy_scm_check(profile, depth, ratio):
#         return profile['z'] >= depth and profile['r'] >= ratio
#         
#     profiles = [{'id': 'P1', 'z': 12, 'r': 1.6}]
#     params = {'depth': [10.0, 15.0], 'ratio': [1.5, 2.0]}
#     
#     for r in run_sensitivity_sweep(profiles, dummy_scm_check, params):
#         print(r)
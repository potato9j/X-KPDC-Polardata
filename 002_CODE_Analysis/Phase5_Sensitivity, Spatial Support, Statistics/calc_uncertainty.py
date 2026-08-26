import numpy as np
import pandas as pd

def cluster_bootstrap_proportions(df, cluster_col, metric_cols, seed=20260712, B=2000):
    """항차(Cruise) 단위로 복원 추출하여 이진 위험 지표의 신뢰구간 산출"""
    clusters = df[cluster_col].unique()
    rng = np.random.default_rng(seed)
    results = {col: [] for col in metric_cols}
    
    for _ in range(B):
        sampled = rng.choice(clusters, size=len(clusters), replace=True)
        boot = pd.concat([df[df[cluster_col] == c] for c in sampled])
        
        for col in metric_cols:
            results[col].append(boot[col].mean())
            
    ci_results = {}
    for col in metric_cols:
        vals = results[col]
        ci_results[col] = {
            'estimate': df[col].mean(),
            'ci_lower': float(np.quantile(vals, 0.025, method='linear')),
            'ci_upper': float(np.quantile(vals, 0.975, method='linear'))
        }
    return ci_results

# # ==== 실행 테스트 (더미 데이터) ====
# # if __name__ == "__main__":
# #     df = pd.DataFrame({
# #         'cruise_id': ['C1', 'C1', 'C2', 'C2', 'C3'],
# #         'high_error': [True, False, True, True, False]
# #     })
# #     print(cluster_bootstrap_proportions(df, 'cruise_id', ['high_error']))
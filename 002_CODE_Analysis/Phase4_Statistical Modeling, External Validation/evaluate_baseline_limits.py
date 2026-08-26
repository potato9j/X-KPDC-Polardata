import numpy as np
import pandas as pd

def bootstrap_summary(g: pd.DataFrame, seed: int):
    """항차(Cruise) 단위 군집 부트스트랩을 수행하여 95% 신뢰구간(CI) 산출"""
    cruise_rows = []
    for _, z in g.groupby('cruise_id', sort=True, observed=False):
        e = z['log_error_prediction_minus_observation'].astype(float).to_numpy()
        cruise_rows.append({
            'n': float(len(z)), 
            'sum_e': float(e.sum()), 
            'sum_abs_e': float(np.abs(e).sum()), 
            'sum_sq_e': float(np.square(e).sum())
        })
        
    g_count = len(cruise_rows)
    if g_count < 4: return {'bootstrap_status': 'NOT_COMPUTED'}
    
    keys = list(cruise_rows[0])
    arr = np.array([[r[k] for k in keys] for r in cruise_rows], dtype=float)
    col = {k: i for i, k in enumerate(keys)}
    
    rng = np.random.default_rng(seed)
    # 복원추출을 통한 항차 단위 부트스트래핑
    sample_idx = rng.integers(0, g_count, size=(2000, g_count))
    sums = arr[sample_idx].sum(axis=1)
    
    n = sums[:, col['n']]
    metrics = {
        'bias_log': sums[:, col['sum_e']] / n,
        'mae_log': sums[:, col['sum_abs_e']] / n,
        'rmse_log': np.sqrt(sums[:, col['sum_sq_e']] / n)
    }
    
    out = {'valid_bootstrap_n': 2000}
    for key, values in metrics.items():
        lo, hi = np.quantile(values, [0.025, 0.975], method='linear')
        out[f'{key}_ci_lower'] = float(lo)
        out[f'{key}_ci_upper'] = float(hi)
        
    return out

# # ==== 실행 테스트 (더미 데이터) ====
# # if __name__ == "__main__":
# #     df = pd.DataFrame({
# #         'cruise_id': ['A', 'A', 'B', 'B', 'C', 'D'],
# #         'log_error_prediction_minus_observation': [0.1, -0.2, 0.05, 0.15, -0.1, 0.3]
# #     })
# #     print("Bootstrap CI:", bootstrap_summary(df, seed=42))
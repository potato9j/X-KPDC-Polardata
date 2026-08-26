import numpy as np
from sklearn.model_selection import GroupKFold
import math

def design_matrices(train, test, kind):
    """모델 종류에 따라 선형대수 적합을 위한 설계 행렬(Design Matrix) 생성"""
    if kind == 'fixed': return (None, None, [], {})
    
    cols_tr, cols_te = [np.ones(len(train))], [np.ones(len(test))]
    terms, scale = ['intercept'], {}
    
    if kind == 'null': return (np.column_stack(cols_tr), np.column_stack(cols_te), terms, scale)
    
    cols_tr.append(np.asarray([r['log_c_surface'] for r in train], dtype=float))
    cols_te.append(np.asarray([r['log_c_surface'] for r in test], dtype=float))
    terms.append('log_c_surface')
    
    return (np.column_stack(cols_tr), np.column_stack(cols_te), terms, scale)

def fit_predict(train, test, kind):
    """행렬 연산을 이용한 최적선형적합(OLS) 및 테스트셋 예측"""
    if kind == 'fixed':
        pred = np.asarray([math.log(100.0 * float(r['c_surface'])) for r in test], dtype=float)
        return (pred, {}, {}, None, None)
        
    xtr, xte, terms, scale = design_matrices(train, test, kind)
    ytr = np.asarray([r['observed_log_i'] for r in train], dtype=float)
    
    # LSTSQ(최소제곱법) 적합
    beta, _, rank, s = np.linalg.lstsq(xtr, ytr, rcond=None)
    cond = float(np.linalg.cond(xtr)) if xtr.size else None
    
    return (xte @ beta, {t: float(b) for t, b in zip(terms, beta)}, scale, int(rank), cond)

def inner_oof_residuals(train, kind):
    """GroupKFold를 이용해 Inner OOF 잔차를 생성하여 예측 구간(PI) 산출에 활용"""
    groups = np.asarray([r['cruise_id'] for r in train], dtype=object)
    k = min(5, len(set(groups.tolist())))
    
    pred = np.full(len(train), np.nan, dtype=float)
    splitter = GroupKFold(n_splits=k)
    idx = np.arange(len(train))
    
    for tr_idx, va_idx in splitter.split(idx, groups=groups):
        tr = [train[i] for i in tr_idx]
        va = [train[i] for i in va_idx]
        p, _, _, _, _ = fit_predict(tr, va, kind)
        pred[va_idx] = p
        
    y = np.asarray([r['observed_log_i'] for r in train], dtype=float)
    return y - pred, k, []

# # ==== 실행 테스트 (더미 데이터) ====
# # if __name__ == "__main__":
# #     train_data = [{'log_c_surface': 0.1, 'observed_log_i': 1.0, 'cruise_id': 'A'}, 
# #                   {'log_c_surface': 0.5, 'observed_log_i': 1.5, 'cruise_id': 'B'}]
# #     test_data  = [{'log_c_surface': 0.3, 'observed_log_i': 1.2, 'cruise_id': 'C'}]
# #     preds, coefs, _, _, _ = fit_predict(train_data, test_data, 'surface')
# #     print(f"Predictions: {preds}, Coefficients: {coefs}")
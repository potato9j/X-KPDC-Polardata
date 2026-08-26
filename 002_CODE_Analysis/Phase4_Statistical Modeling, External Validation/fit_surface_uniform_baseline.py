import math
import statistics
import numpy as np

def interval_score(y, lower, upper, alpha=0.1):
    """예측 구간의 품질을 평가하는 Interval Score 산출 (낮을수록 우수)"""
    score = upper - lower
    if y < lower:
        score += 2.0 / alpha * (lower - y)
    elif y > upper:
        score += 2.0 / alpha * (y - upper)
    return score

def calibration(y, pred):
    """기울기 고정 편향(Fixed Intercept) 및 자유 기울기(Slope) 캘리브레이션 진단"""
    if not y: return (None, None, None, None)
    fixed_slope_intercept = statistics.mean((yy - pp for yy, pp in zip(y, pred)))
    if len(y) < 2: return (fixed_slope_intercept, None, None, None)
    
    yy, xx = np.asarray(y, dtype=float), np.asarray(pred, dtype=float)
    if np.var(xx) <= 0: return (fixed_slope_intercept, None, None, None)
    
    slope, free_intercept = np.polyfit(xx, yy, 1)
    r = float(np.corrcoef(xx, yy)[0, 1]) if np.var(yy) > 0 else None
    return (fixed_slope_intercept, float(free_intercept), float(slope), r)

def metric_values(rows, use_fold_reference=True):
    """관측치(y)와 예측치(p)를 바탕으로 다차원 오차 지표 계산"""
    if not rows: return {}
    y = [float(r['observed_log_i_0_100']) for r in rows]
    p = [float(r['predicted_log_i_surface']) for r in rows]
    e = [pp - yy for pp, yy in zip(p, y)]
    
    medae = statistics.median([abs(v) for v in e])
    
    if use_fold_reference and all('train_mean_observed_log' in r for r in rows):
        denom = sum(((float(r['observed_log_i_0_100']) - float(r['train_mean_observed_log'])) ** 2 for r in rows))
    else:
        ybar = statistics.mean(y)
        denom = sum(((v - ybar) ** 2 for v in y))
        
    sse = sum((v * v for v in e))
    r2 = 1.0 - sse / denom if denom > 0 else None
    
    return {
        'mae_log': statistics.mean(abs(v) for v in e),
        'rmse_log': math.sqrt(statistics.mean(v * v for v in e)),
        'bias_log': statistics.mean(e),
        'medae_log': medae,
        'r2_oof': r2
    }

# # ==== 실행 테스트 (더미 데이터) ====
# # if __name__ == "__main__":
# #     dummy_rows = [
# #         {'observed_log_i_0_100': 1.0, 'predicted_log_i_surface': 1.1, 'train_mean_observed_log': 1.5},
# #         {'observed_log_i_0_100': 2.0, 'predicted_log_i_surface': 1.8, 'train_mean_observed_log': 1.5}
# #     ]
# #     print("Metrics:", metric_values(dummy_rows))
import numpy as np

def calc_window_statistics(vals, fill_value=-32767.0, vmin=0.001, vmax=100.0):
    """추출된 반경 내 픽셀(vals)의 유효성 검사 및 공간 통계량 산출"""
    valid = np.isfinite(vals) & (vals != fill_value) & (vals > 0) & (vals >= vmin) & (vals <= vmax)
    n = int(np.count_nonzero(valid))
    frac = n / vals.size if vals.size else 0.0
    
    vv = vals[valid]
    med = float(np.median(vv)) if n else None
    mean = float(np.mean(vv)) if n else None
    cv = (float(np.std(vv, ddof=0)) / mean) if n and mean and mean > 0 else None
    
    # 윈도우 품질 게이트 평가
    hard_gate = (n >= 2) and (frac >= 0.25) and (cv is not None and cv <= 1.0)
    strict_gate = (n >= 3) and (frac >= 0.50) and (cv is not None and cv <= 0.3)
    
    return {
        'valid_count': n, 'valid_fraction': frac,
        'median_chl': med, 'cv': cv,
        'hard_gate_pass': hard_gate, 'strict_gate_pass': strict_gate
    }

# # ==== 실행 테스트 (더미 데이터) ====
# # if __name__ == "__main__":
# #     # 반경 내 픽셀 배열 더미
# #     pixels = np.array([[1.1, -32767.0], [1.2, 1.5]])
# #     print("Window Stats:", calc_window_statistics(pixels))
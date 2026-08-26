import numpy as np
import math

BINS = [
    ('D00_10', '0–10', 0.0, 10.0), ('D10_20', '>10–20', 10.0, 20.0),
    ('D20_30', '>20–30', 20.0, 30.0), ('D30_40', '>30–40', 30.0, 40.0),
    ('D40_50', '>40–50', 40.0, 50.0), ('D50_60', '>50–60', 50.0, 60.0),
    ('D60_70', '>60–70', 60.0, 70.0), ('D70_80', '>70–80', 70.0, 80.0),
    ('D80_90', '>80–90', 80.0, 90.0), ('D90_100', '>90–100', 90.0, 100.0)
]

def region(d):
    """해저 수심을 기반으로 대륙붕, 사면, 분지 해역을 분류"""
    return ('SHELF_LE_200_M', '대륙붕 수심대') if d <= 200 else \
           ('SLOPE_200_TO_2000_M', '사면 수심대') if d <= 2000 else \
           ('BASIN_GT_2000_M', '분지 수심대')

def bin_for(z):
    """관측 수심에 해당하는 수심 Bin 반환"""
    if z < 0 or z > 100:
        return None
    for i, (bid, label, lo, hi) in enumerate(BINS):
        if i == 0 and lo <= z <= hi or (i > 0 and lo < z <= hi):
            return (bid, label, lo, hi)
    return None

def desc(vals):
    """결측치를 제외한 Numpy 배열의 기초 기술 통계 산출"""
    a = np.asarray(list(vals), float)
    a = a[np.isfinite(a)]
    n = len(a)
    if n == 0:
        return {'n': 0, 'mean': None, 'sd': None, 'median': None, 'q25': None, 'q75': None, 'iqr': None, 'p05': None, 'p95': None, 'min': None, 'max': None}
    q = np.quantile(a, [0.05, 0.25, 0.5, 0.75, 0.95], method='linear')
    return {
        'n': n, 'mean': float(a.mean()), 'sd': float(a.std(ddof=1)) if n > 1 else None, 
        'median': float(q[2]), 'q25': float(q[1]), 'q75': float(q[3]), 
        'iqr': float(q[3] - q[1]), 'p05': float(q[0]), 'p95': float(q[4]), 
        'min': float(a.min()), 'max': float(a.max())
    }

# # ==== 실행 테스트 (더미 데이터) ====
# # if __name__ == "__main__":
# #     print("해역 분류:", region(1500))
# #     print("수심 Bin:", bin_for(15.5))
# #     print("기초 통계량:", desc([1.2, 1.5, np.nan, 2.0, 3.1, 2.5]))
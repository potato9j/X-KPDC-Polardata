import math
import numpy as np
import statistics
from sklearn.linear_model import HuberRegressor

def lopo_cross_validation(rows):
    """단일 프로파일을 제외하며 Huber 회귀 모델을 평가하여 절대로그오차 중앙값(MdALE) 산출"""
    profiles = sorted({r['profile_id'] for r in rows})
    if len(profiles) < 2: return None
    
    errors = []
    for held in profiles:
        tr = [r for r in rows if r['profile_id'] != held]
        te = [r for r in rows if r['profile_id'] == held]
        
        m = HuberRegressor(epsilon=1.35, fit_intercept=True)
        m.fit(np.array([[r['fluor']] for r in tr]), np.array([r['bottle'] for r in tr]))
        inter, slope = float(m.intercept_), float(m.coef_[0])
        
        for r in te:
            p = inter + slope * r['fluor']
            if p > 0:
                errors.append(math.log(p / r['bottle']))
                
    return {
        'lopo_median_absolute_log_error': statistics.median((abs(x) for x in errors)) if errors else None,
        'lopo_median_log_bias': statistics.median(errors) if errors else None
    }

# # ==== 실행 테스트 (더미 데이터) ====
# # if __name__ == "__main__":
# #     data = [
# #         {'profile_id': 'P1', 'fluor': 100, 'bottle': 1.1},
# #         {'profile_id': 'P2', 'fluor': 200, 'bottle': 2.3},
# #         {'profile_id': 'P3', 'fluor': 150, 'bottle': 1.5}
# #     ]
# #     print("LOPO Result:", lopo_cross_validation(data))
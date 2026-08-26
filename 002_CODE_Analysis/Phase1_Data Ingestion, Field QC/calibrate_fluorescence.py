import numpy as np
import statistics
from sklearn.linear_model import HuberRegressor

def pair_and_calibrate_fluorescence(bottle_rows, ctd_rows, tolerance_m=2.0):
    pairs = []
    
    # 1. 허용 오차 내 수심 짝짓기 및 중앙값 추출
    for b in bottle_rows:
        candidates = [
            c['fluorescence_raw'] for c in ctd_rows 
            if c['profile_id'] == b['profile_id'] 
            and abs(c['depth_m'] - b['depth_m']) <= tolerance_m
        ]
        
        if candidates:
            pairs.append({
                'fluorescence_median': statistics.median(candidates),
                'bottle_chl': b['chl_mg_m3']
            })
            
    if len(pairs) < 2:
        return None, None
        
    # 2. Huber 회귀 (이상치에 강건한 모델 피팅)
    X = np.array([[p['fluorescence_median']] for p in pairs])
    y = np.array([p['bottle_chl'] for p in pairs])
    
    model = HuberRegressor(epsilon=1.35, fit_intercept=True)
    model.fit(X, y)
    
    return model.intercept_, model.coef_[0]

# ==== 실행 테스트 (더미 데이터) ====
# if __name__ == "__main__":
#     bottles = [{'profile_id': 'P1', 'depth_m': 10, 'chl_mg_m3': 2.5}]
#     ctds = [
#         {'profile_id': 'P1', 'depth_m': 9.5, 'fluorescence_raw': 100},
#         {'profile_id': 'P1', 'depth_m': 10.5, 'fluorescence_raw': 110}
#     ]
    
#     intercept, slope = pair_and_calibrate_fluorescence(bottles, ctds)
#     print(f"Calibration Model: y = {slope:.4f}x + {intercept:.4f}")
import numpy as np
import gsw

def find_mld_crossing(nodes, ref_depth, ref_sigma, threshold):
    """밀도 차이가 threshold를 교차하는 수심을 선형 보간하여 탐색"""
    valid_nodes = [n for n in nodes if n['z'] > ref_depth]
    for lower, upper in zip([{'z': ref_depth, 'sigma': ref_sigma}] + valid_nodes, valid_nodes):
        d0, d1 = lower['sigma'] - ref_sigma, upper['sigma'] - ref_sigma
        if d0 < threshold <= d1: # 임계값 교차 지점
            mld = lower['z'] + (threshold - d0) / (d1 - d0) * (upper['z'] - lower['z']) if d1 != d0 else upper['z']
            return mld
    return None

def compute_n2(sa, ct, p, lat):
    """TEOS-10 기반 N^2 (부력진동수) 계산"""
    n2, p_mid = gsw.Nsquared(sa, ct, p, lat)
    return n2, p_mid

# ==== 실행 테스트 (더미 데이터) ====
# if __name__ == "__main__":
#     nodes = [{'z': 5.0, 'sigma': 24.0}, {'z': 10.0, 'sigma': 24.02}, {'z': 15.0, 'sigma': 24.08}]
#     mld = find_mld_crossing(nodes, 5.0, 24.0, 0.05)
#     print(f"Calculated MLD: {mld} m")
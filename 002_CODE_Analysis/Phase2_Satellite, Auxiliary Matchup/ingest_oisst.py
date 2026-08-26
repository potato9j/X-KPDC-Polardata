from datetime import date
import numpy as np

def processing_era(d):
    """관측 일자에 따라 OISST 버전 업데이트 이력(Era) 분류"""
    if d <= date(2015, 12, 31): return ('E1', 'legacy_v2_equivalent_repackaged_v2.1')
    if d <= date(2021, 9, 30): return ('E2', 'v2.1_improved_2016plus')
    if d <= date(2023, 3, 31): return ('E3', 'v2.1a_ACSPO_input')
    return ('E4', 'v2.1b_monthly_ship_bias')

def primary_sst_qc(raw, fill=-999, valid_min=-300, valid_max=4500, scale=0.01, offset=0.0):
    """Raw SST 값을 스케일링하고 유효 범위를 검사"""
    if raw is None: return 'Q2', None
    
    raw_float = float(raw)
    if not np.isfinite(raw_float) or int(raw_float) == fill:
        return 'Q2', None
        
    if raw_float < valid_min or raw_float > valid_max:
        return 'Q2', None
        
    decoded = raw_float * scale + offset
    return 'Q0', decoded

# ==== 실행 테스트 (더미 데이터) ====
# if __name__ == "__main__":
#     print("Processing Era (2022-01-01):", processing_era(date(2022, 1, 1)))
#     qc_flag, sst_celsius = primary_sst_qc(1500) # 1500 * 0.01 = 15.0도
#     print(f"QC: {qc_flag}, SST: {sst_celsius} °C")
def grade_modis_window(n, nt, cv):
    """유효 픽셀 수(n), 전체 픽셀 수(nt), 변동계수(cv)에 따른 등급 판별"""
    frac = n / nt if nt else 0
    if n < 2 or frac < 0.25 or cv is None or not math.isfinite(cv) or cv > 1:
        return 'EXCLUDE_Q2' # 하드 게이트 탈락
    if n >= 3 and frac >= 0.5 and cv <= 0.5:
        return 'TIER_A_Q0'  # 고품질 창
    return 'TIER_B_Q1'      # 조건부 승인

def modis_missing_reason(row):
    """매치업 실패 시 주요 원인을 계층적으로 진단"""
    if not str(row.get('calendar_date_matching_eligible', '')).lower() in {'true', '1'}:
        return 'DATE_YEAR_CONFLICT_NOT_APPLICABLE'
        
    n = int(float(row.get('modis_window_valid_count', 0)))
    vf = float(row.get('modis_window_valid_fraction', 0.0))
    cv = float(row.get('modis_window_cv_raw', 999.0))
    
    if not str(row.get('modis_hard_gate_pass', '')).lower() in {'true', '1'}:
        if n == 0: return 'NO_VALID_PIXEL_IN_8KM'
        if n < 2: return 'VALID_PIXEL_N_LT2'
        if vf < 0.25: return 'VALID_FRACTION_LT0_25'
        if cv > 1.0: return 'CV_GT1_OR_UNDEFINED'
        return 'HARD_WINDOW_OTHER_FAILURE'
        
    # 하드 게이트는 통과했으나 빙염(Sea Ice) 필터에 걸린 경우
    return {
        'UNAVAILABLE_QA_INVALID': 'NSIDC_QA_INVALID_AFTER_HARD_WINDOW_PASS', 
        'EXCLUDE_GE30': 'SIC_GE30_AFTER_HARD_WINDOW_PASS', 
        'MARGINAL_15_TO_LT30': 'SIC_15_TO_LT30_PRIMARY_EXCLUDED'
    }.get(row.get('nsidc_modis_day_gate', ''), 'UNKNOWN_DAY_GATE')

# ==== 실행 테스트 (더미 데이터) ====
# if __name__ == "__main__":
#     print("MODIS Window Grade:", grade_modis_window(n=4, nt=10, cv=0.4))
#     
#     dummy_row = {
#         'calendar_date_matching_eligible': 'True',
#         'modis_hard_gate_pass': 'False',
#         'modis_window_valid_count': '1',
#         'modis_window_valid_fraction': '0.1'
#     }
#     print("Missing Reason:", modis_missing_reason(dummy_row))
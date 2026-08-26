def detect_scm(z_peak, c_peak, c_surface, min_depth=10.0, min_ratio=1.5, min_delta=0.1, min_peak=0.11):
    """SCM 성립 조건 4가지를 검사하여 존재 여부 판별"""
    if any(v is None for v in [z_peak, c_peak, c_surface]) or c_surface <= 0:
        return False, "INDETERMINATE"
        
    ratio = c_peak / c_surface
    delta = c_peak - c_surface
    
    pass_depth = z_peak >= min_depth
    pass_ratio = ratio >= min_ratio
    pass_delta = delta >= min_delta
    pass_peak = c_peak >= min_peak
    
    if pass_depth and pass_ratio and pass_delta and pass_peak:
        return True, "PRESENT"
    return False, "ABSENT_DEFINITION_FAIL"

# ==== 실행 테스트 (더미 데이터) ====
# if __name__ == "__main__":
#     is_scm, status = detect_scm(z_peak=25.0, c_peak=1.8, c_surface=0.5)
#     print(f"SCM Detected: {is_scm} ({status})")
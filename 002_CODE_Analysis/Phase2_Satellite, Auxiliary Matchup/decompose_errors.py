import math

def calculate_error_decomposition(i_0_100, c_surface, c_sat):
    """총 오차를 수직 대표성 오차와 산출 오차로 분해 (로그 스케일)"""
    metrics = {}
    
    if i_0_100 and c_surface and i_0_100 > 0 and c_surface > 0:
        metrics['e_vert_ln'] = math.log(i_0_100 / (100.0 * c_surface))
        
    if c_surface and c_sat and c_surface > 0 and c_sat > 0:
        metrics['e_ret_ln'] = math.log(c_surface / c_sat)
        
    if i_0_100 and c_sat and i_0_100 > 0 and c_sat > 0:
        metrics['e_total_ln'] = math.log(i_0_100 / (100.0 * c_sat))
        
    # 분해 항등식 검증: E_total ≈ E_vert + E_ret
    if all(k in metrics for k in ['e_vert_ln', 'e_ret_ln', 'e_total_ln']):
        metrics['identity_diff'] = abs(metrics['e_total_ln'] - (metrics['e_vert_ln'] + metrics['e_ret_ln']))
        
    return metrics

# ==== 실행 테스트 (더미 데이터) ====
# if __name__ == "__main__":
#     err = calculate_error_decomposition(i_0_100=150.0, c_surface=0.5, c_sat=0.4)
#     print(f"E_vert: {err.get('e_vert_ln'):.4f}, E_ret: {err.get('e_ret_ln'):.4f}, E_total: {err.get('e_total_ln'):.4f}")
def nsidc_qa(raw, mask, qa, spatial, temporal):
    """8-bit QA 플래그를 해독하여 등급(Q0, Q1, Q2) 및 상세 사유 분류"""
    flags = []
    melt = bool(qa & 128) # 7번째 비트: 해빙(Melt) 시작 여부
    
    if raw == 255 or raw < 0 or raw > 100:
        flags.append('CONC_FILL_OR_OUT_OF_RANGE')
    if mask != 50: # 50 = Ocean
        flags.append(f'NON_OCEAN_MASK_{mask}')
        
    # 1, 2, 4, 16 비트 검사 (치명적 오류 및 필터링)
    for bit, name in [(1, 'BT_WEATHER_FILTER'), (2, 'NT_WEATHER_FILTER'), 
                      (4, 'LAND_SPILLOVER_FILTER'), (16, 'INVALID_ICE_MASK')]:
        if qa & bit:
            flags.append(name)
            
    hard_bad = bool(flags)
    caution = False
    
    spatial_valid = 1 <= spatial <= 63
    temporal_valid = 1 <= temporal <= 55
    
    # 32, 64 비트 검사 (공간/시간 보간 적용 여부)
    if qa & 32:
        if spatial_valid:
            flags.append('SPATIAL_INTERPOLATION')
            caution = True
        else:
            flags.append('INVALID_SPATIAL_INTERPOLATION_FLAG')
            hard_bad = True
            
    if qa & 64:
        if temporal_valid:
            flags.append('TEMPORAL_INTERPOLATION')
            caution = True
        else:
            flags.append('INVALID_TEMPORAL_INTERPOLATION_FLAG')
            hard_bad = True
            
    if melt:
        flags.append('MELT_START_DETECTED')
        
    if hard_bad: return ('Q2', flags, melt)
    if caution: return ('Q1', flags or ['INTERPOLATION_CAUTION'], melt)
    return ('Q0', flags or ['PASS'], melt)

# ==== 실행 테스트 (더미 데이터) ====
# if __name__ == "__main__":
#     # qa = 160 (128 + 32: 해빙 감지 및 공간 보간 적용)
#     qclass, flags, is_melt = nsidc_qa(raw=90, mask=50, qa=160, spatial=5, temporal=0)
#     print(f"Class: {qclass}, Flags: {flags}, Melt: {is_melt}")
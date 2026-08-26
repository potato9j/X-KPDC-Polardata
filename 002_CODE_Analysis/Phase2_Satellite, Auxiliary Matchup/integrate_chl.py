def trapezoidal_integration_0_to_100(knots):
    """주어진 수심(z)과 농도(c) 노드들을 바탕으로 사다리꼴 적분 수행"""
    # knots는 {'depth_m': z, 'chl_mg_m3': c} 형태의 정렬된 리스트로 가정
    cumulative_area = 0.0
    segments = []
    
    for a, b in zip(knots, knots[1:]):
        za, zb = a['depth_m'], b['depth_m']
        ca, cb = a['chl_mg_m3'], b['chl_mg_m3']
        thickness = zb - za
        area = 0.5 * (ca + cb) * thickness
        cumulative_area += area
        segments.append({'z_start': za, 'z_end': zb, 'area': area})
        
    return cumulative_area, segments

# ==== 실행 테스트 (더미 데이터) ====
# if __name__ == "__main__":
#     knots = [
#         {'depth_m': 0.0, 'chl_mg_m3': 1.0},
#         {'depth_m': 50.0, 'chl_mg_m3': 2.0},
#         {'depth_m': 100.0, 'chl_mg_m3': 0.5}
#     ]
#     integral, segs = trapezoidal_integration_0_to_100(knots)
#     print(f"Integrated Chl (0-100m): {integral} mg/m^2")
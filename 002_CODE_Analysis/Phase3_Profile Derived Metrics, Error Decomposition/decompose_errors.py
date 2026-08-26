import math

def field_metrics(i_0_100, c_surface):
    if i_0_100 is None or c_surface is None or i_0_100 <= 0 or c_surface <= 0:
        return None
    i_surface = c_surface * 100.0
    e_vert = math.log(i_0_100 / i_surface)
    r_blind = i_0_100 / i_surface
    u_rel = (i_0_100 - i_surface) / i_0_100 * 100.0
    return {'i_surface_mg_m2': i_surface, 'e_vert_ln': e_vert, 'r_blind': r_blind, 'u_rel_pct': u_rel}

def satellite_metrics(i_0_100, c_surface, c_sat):
    e_ret = math.log(c_surface / c_sat) if c_surface and c_sat and (c_surface > 0) and (c_sat > 0) else None
    e_total = math.log(i_0_100 / (100.0 * c_sat)) if i_0_100 and c_sat and (i_0_100 > 0) and (c_sat > 0) else None
    e_vert = math.log(i_0_100 / (100.0 * c_surface)) if i_0_100 and c_surface and (i_0_100 > 0) and (c_surface > 0) else None
    identity = abs(e_total - (e_vert + e_ret)) if e_total is not None and e_vert is not None and e_ret is not None else None
    return {'e_ret_ln': e_ret, 'e_total_ln': e_total, 'e_vert_ln': e_vert, 'identity_absdiff': identity}

# # ==== 실행 테스트 (더미 데이터) ====
# # if __name__ == "__main__":
# #     print("Field Metrics:", field_metrics(150.0, 0.5))
# #     print("Satellite Metrics:", satellite_metrics(150.0, 0.5, 0.4))
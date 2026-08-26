def interpolate_100(points):
    exact = [p for p in points if abs(float(p['depth_m']) - 100.0) <= 1e-12]
    if exact: return exact[0]
    
    lower = max([p for p in points if float(p['depth_m']) < 100.0], key=lambda p: float(p['depth_m']), default=None)
    upper = min([p for p in points if float(p['depth_m']) > 100.0], key=lambda p: float(p['depth_m']), default=None)
    if not lower or not upper: return None
    
    zl, zu = float(lower['depth_m']), float(upper['depth_m'])
    cl, cu = float(lower['chl_mg_m3']), float(upper['chl_mg_m3'])
    c100 = cl + (cu - cl) * (100.0 - zl) / (zu - zl)
    return {'depth_m': 100.0, 'chl_mg_m3': c100, 'origin': 'BOTTOM_LINEAR_INTERPOLATION_100M'}

def structural_screen(pts, surface_max_depth_m=5.0, min_unique_depths=4, max_gap_m=40.0):
    if not pts: return {'eligible': False, 'reasons': ['NO_POINTS']}
    
    zmin, zmax = float(pts[0]['depth_m']), float(pts[-1]['depth_m'])
    in_domain = [dict(p) for p in pts if 0.0 <= float(p['depth_m']) <= 100.0]
    
    reasons = []
    if zmin > surface_max_depth_m: reasons.append('MIN_DEPTH_GT_LIMIT')
    if zmax < 100.0: reasons.append('MAX_DEPTH_LT_100_M')
    if len(in_domain) < min_unique_depths: reasons.append('N_UNIQUE_DEPTH_LT_LIMIT')
    
    review_knots = [dict(p) for p in in_domain]
    if review_knots:
        if zmin > 0 and zmin <= surface_max_depth_m:
            first = review_knots[0]
            review_knots.insert(0, {'depth_m': 0.0, 'chl_mg_m3': float(first['chl_mg_m3']), 'origin': 'TOP_CONSTANT_EXTENSION_0M'})
        if zmax >= 100.0:
            p100 = interpolate_100(pts)
            if p100: review_knots = [p for p in review_knots if float(p['depth_m']) < 100.0] + [p100]
            
    max_gap = max([float(b['depth_m']) - float(a['depth_m']) for a, b in zip(review_knots, review_knots[1:])]) if len(review_knots) >= 2 else None
    if max_gap and max_gap > max_gap_m + 1e-12: reasons.append('MAX_GAP_GT_LIMIT')
    
    eligible = not reasons
    integral = sum(0.5 * (float(a['chl_mg_m3']) + float(b['chl_mg_m3'])) * (float(b['depth_m']) - float(a['depth_m'])) for a, b in zip(review_knots, review_knots[1:])) if eligible else None
    
    return {'eligible': eligible, 'knots': review_knots, 'integral': integral, 'reasons': reasons}

# # ==== 실행 테스트 (더미 데이터) ====
# # if __name__ == "__main__":
# #     points = [{'depth_m': 2.0, 'chl_mg_m3': 1.0}, {'depth_m': 50.0, 'chl_mg_m3': 2.0}, {'depth_m': 110.0, 'chl_mg_m3': 0.5}]
# #     print("Integration Screen:", structural_screen(points))
import math
import statistics
from collections import defaultdict

def peak_candidate(points):
    grouped = defaultdict(list)
    for z, v in points: grouped[z].append(v)
    pts = sorted([(z, statistics.median(vals)) for z, vals in grouped.items()])
    
    if not pts: return {'status': 'NO_VALID_POINTS', 'points': []}
    
    maximum = max((v for _, v in pts))
    idx = [i for i, (_, v) in enumerate(pts) if v == maximum]
    contiguous = idx == list(range(min(idx), max(idx) + 1))
    
    shallower, deeper = (min(idx) > 0, max(idx) < len(pts) - 1)
    if not contiguous: boundary = 'AMBIGUOUS_NONCONTIGUOUS_GLOBAL_MAXIMA'
    elif not shallower: boundary = 'SURFACE_OR_FIRST_MAXIMUM'
    elif not deeper: boundary = 'RIGHT_CENSORED_DEEPEST_MAXIMUM'
    else: boundary = 'INTERIOR_MAXIMUM'
    
    return {'points': pts, 'z_peak': (pts[min(idx)][0] + pts[max(idx)][0]) / 2.0, 'c_peak': maximum, 'boundary': boundary}

def definition_decision(candidate, c_surface, complete_primary, depth_threshold=10.0, ratio_threshold=1.5, delta_threshold=0.1, peak_min=0.11):
    z_peak, c_peak = candidate.get('z_peak'), candidate.get('c_peak')
    ratio = c_peak / c_surface if c_peak and c_surface and c_surface > 0 else None
    delta = c_peak - c_surface if c_peak and c_surface else None
    
    criteria = {
        'z': z_peak is not None and z_peak >= depth_threshold - 1e-12,
        'ratio': ratio is not None and ratio >= ratio_threshold - 1e-12,
        'delta': delta is not None and delta >= delta_threshold - 1e-12,
        'peak_min': c_peak is not None and c_peak >= peak_min - 1e-12
    }
    
    if c_surface is None or c_surface <= 0: primary_status = 'INDETERMINATE_SURFACE_NOT_QUANTIFIED'
    elif candidate.get('boundary') == 'SURFACE_OR_FIRST_MAXIMUM': primary_status = 'ABSENT_SURFACE_MAXIMUM'
    elif candidate.get('boundary') == 'INTERIOR_MAXIMUM' and all(criteria.values()): primary_status = 'PRESENT'
    elif candidate.get('boundary') == 'INTERIOR_MAXIMUM': primary_status = 'ABSENT_DEFINITION_FAIL'
    else: primary_status = 'INDETERMINATE_OR_UNRECOGNIZED'
    
    return {'primary_status': primary_status, 'ratio': ratio, 'delta': delta}

# # ==== 실행 테스트 (더미 데이터) ====
# # if __name__ == "__main__":
# #     cand = peak_candidate([(0, 0.1), (20, 0.4), (50, 0.08)])
# #     print("Decision:", definition_decision(cand, c_surface=0.1, complete_primary=True))
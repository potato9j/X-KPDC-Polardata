import math
import statistics
import numpy as np
import gsw

def find_mld_crossing(rows, reference_depth_m, reference_sigma0, threshold_kg_m3, sigma_field='sigma0_kg_m3', max_crossing_gap_m=2.0):
    nodes = [{'depth_m': reference_depth_m, 'sigma0': reference_sigma0, 'density_inversion_flag': False}]
    for row in rows:
        if float(row['depth_bin_m']) <= reference_depth_m or row.get(sigma_field) is None:
            continue
        nodes.append({
            'depth_m': float(row['depth_bin_m']), 
            'sigma0': float(row[sigma_field]), 
            'density_inversion_flag': row.get('density_inversion_flag', False)
        })
        
    if len(nodes) < 2: return {'status': 'UNRESOLVED_NO_DATA_BELOW_REFERENCE'}
    
    crossings = []
    for lower, upper in zip(nodes, nodes[1:]):
        d0, d1 = lower['sigma0'] - reference_sigma0, upper['sigma0'] - reference_sigma0
        if d0 < threshold_kg_m3 <= d1:
            gap = upper['depth_m'] - lower['depth_m']
            mld = lower['depth_m'] + (threshold_kg_m3 - d0) / (d1 - d0) * gap if d1 != d0 else upper['depth_m']
            crossings.append({
                'mld_m': float(mld), 'crossing_gap_m': gap, 
                'crossing_inversion_flag': bool(upper['density_inversion_flag'])
            })
            
    if crossings:
        first = crossings[0]
        if first['crossing_gap_m'] > max_crossing_gap_m: return {**first, 'mld_m': None, 'status': 'UNRESOLVED_CROSSING_BRACKET_GT_2M'}
        if first['crossing_inversion_flag']: return {**first, 'mld_m': None, 'status': 'UNRESOLVED_CROSSING_INVERSION_FLAGGED'}
        return {**first, 'status': 'RESOLVED'}
        
    max_delta = max((node['sigma0'] - reference_sigma0 for node in nodes))
    if max_delta < threshold_kg_m3:
        return {'mld_m': None, 'status': 'RIGHT_CENSORED_NO_THRESHOLD_CROSSING', 'max_observed_delta_sigma0_kg_m3': max_delta}
    return {'mld_m': None, 'status': 'UNRESOLVED_NO_UPWARD_CROSSING'}

# # ==== 실행 테스트 (더미 데이터) ====
# # if __name__ == "__main__":
# #     dummy_rows = [
# #         {'depth_bin_m': 6.0, 'sigma0_kg_m3': 24.02},
# #         {'depth_bin_m': 7.0, 'sigma0_kg_m3': 24.08, 'density_inversion_flag': False}
# #     ]
# #     print(find_mld_crossing(dummy_rows, 5.0, 24.0, 0.05))
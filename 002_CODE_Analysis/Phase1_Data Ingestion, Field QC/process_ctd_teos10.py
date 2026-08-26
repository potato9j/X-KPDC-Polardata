import gsw
import numpy as np
import statistics
import math
from collections import defaultdict

def fnum(v):
    """숫자로 변환 가능한지 확인하고 유한한 값만 반환"""
    if v is None or isinstance(v, bool): return None
    try: x = float(v)
    except (TypeError, ValueError): return None
    return x if math.isfinite(x) else None

def med(vals):
    """유효한 값들의 중앙값 산출"""
    a = [float(v) for v in vals if fnum(v) is not None]
    return statistics.median(a) if a else None

def process_ctd_core(raw_data):
    # 1. 원시 데이터 전처리 및 물리량 추정 (수심/압력 변환 및 1m bin 할당)
    processed_raw = []
    for r in raw_data:
        lat, lon = fnum(r.get('lat')), fnum(r.get('lon'))
        z, p = fnum(r.get('depth')), fnum(r.get('pressure'))
        t, S = fnum(r.get('temp')), fnum(r.get('salinity'))

        p10 = p if p is not None else (float(gsw.p_from_z(-z, lat)) if z is not None and lat is not None else None)
        zb = z if z is not None else (float(-gsw.z_from_p(p10, lat)) if p10 is not None and lat is not None else None)

        if all(v is not None for v in (lat, lon, p10, zb, t, S)) and (-2.5 <= t <= 35) and (0 <= S <= 42):
            processed_raw.append({
                'profile_id': r.get('profile_id', 'unknown'),
                'lat': lat, 'lon': lon, 'p10': p10, 'z': zb, 't': t, 'S': S,
                'depth_bin_m': int(math.floor(zb + 0.5)),
                'temp_type': r.get('temp_type', 'in_situ_temperature')
            })

    # 2. 1m 단위 수심 병합 (Binning - 구간 내 중앙값 추출)
    grouped = defaultdict(list)
    for r in processed_raw:
        grouped[r['profile_id'], r['depth_bin_m']].append(r)

    bins = []
    for (pid, z_bin), g in sorted(grouped.items()):
        bins.append({
            'profile_id': pid, 'depth_bin_m': z_bin,
            'lat': med(r['lat'] for r in g), 'lon': med(r['lon'] for r in g),
            'p': med(r['p10'] for r in g), 't': med(r['t'] for r in g),
            'S': med(r['S'] for r in g), 'temp_type': g[0]['temp_type']
        })

    if not bins: return []

    # 3. TEOS-10 열역학 변수 고속 산출 (gsw & numpy)
    SP, pres = np.array([b['S'] for b in bins]), np.array([b['p'] for b in bins])
    lon_arr, lat_arr = np.array([b['lon'] for b in bins]), np.array([b['lat'] for b in bins])
    temp = np.array([b['t'] for b in bins])

    SA = np.asarray(gsw.SA_from_SP(SP, pres, lon_arr, lat_arr))
    CT, pt0 = np.full_like(SA, np.nan), np.full_like(SA, np.nan)
    ins = np.array([b['temp_type'] == 'in_situ_temperature' for b in bins])

    if np.any(ins):
        CT[ins] = gsw.CT_from_t(SA[ins], temp[ins], pres[ins])
        pt0[ins] = gsw.pt0_from_t(SA[ins], temp[ins], pres[ins])
    if np.any(~ins):
        CT[~ins] = gsw.CT_from_pt(SA[~ins], temp[~ins])
        pt0[~ins] = temp[~ins]

    sig = np.asarray(gsw.sigma0(SA, CT))

    for j, b in enumerate(bins):
        b.update({'SA': float(SA[j]), 'CT': float(CT[j]), 'sigma0': float(sig[j])})

    # 4. 수직 안정도 및 품질 평가 (밀도 역전 현상 검출)
    bysp = defaultdict(list)
    for b in bins: bysp[b['profile_id']].append(b)

    for pid, g in bysp.items():
        g.sort(key=lambda x: x['depth_bin_m'])
        prev = None
        for b in g:
            b['density_inversion'] = False
            if prev and (b['depth_bin_m'] - prev['depth_bin_m'] == 1):
                delta_sig = b['sigma0'] - prev['sigma0']
                if delta_sig < -0.03: # 밀도 차이가 -0.03 미만일 경우 역전으로 판별
                    b['density_inversion'] = True
            prev = b

    return bins

# ==== 실행 테스트 (더미 데이터) ====
# if __name__ == "__main__":
#     dummy_observations = [
#         {'profile_id': 'Station_A', 'lat': 35.0, 'lon': 130.0, 'depth': 1.1, 'pressure': 1.11, 'temp': 15.0, 'salinity': 34.0},
#         {'profile_id': 'Station_A', 'lat': 35.0, 'lon': 130.0, 'depth': 1.2, 'pressure': 1.21, 'temp': 15.1, 'salinity': 34.0},
#         {'profile_id': 'Station_A', 'lat': 35.0, 'lon': 130.0, 'depth': 2.0, 'pressure': 2.02, 'temp': 14.8, 'salinity': 34.2},
#         # 수심 3m에서 온도가 급상승, 염분이 급감하여 밀도가 낮아지는 상황 (역전 현상 유발)
#         {'profile_id': 'Station_A', 'lat': 35.0, 'lon': 130.0, 'depth': 3.0, 'pressure': 3.03, 'temp': 18.0, 'salinity': 33.0} 
#     ]
    
#     results = process_ctd_core(dummy_observations)
    
#     print("수심(m) | 실용염분(SP) | 절대염분(SA) | 밀도(Sigma0) | 밀도 역전(QC)")
#     print("-" * 65)
#     for r in results:
#         print(f"  {r['depth_bin_m']:2d}m   |    {r['S']:.2f}    |    {r['SA']:.2f}    |    {r['sigma0']:.3f}   |   {r['density_inversion']}")
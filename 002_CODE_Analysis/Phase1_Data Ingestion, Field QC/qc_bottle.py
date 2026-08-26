import statistics

def classify_chl(value):
    """문자열 값을 수치형태 및 QC 상태로 분류"""
    text_val = str(value).strip().lower()
    if not text_val: return 'MISSING_BLANK', None, 'Q2'
    if '<' in text_val or 'bdl' in text_val: return 'BDL_CENSORED', None, 'Q2'
    
    try:
        num = float(value)
        if num > 0: return 'QUANTITATIVE_POSITIVE', num, 'Q0'
        if num == 0: return 'ZERO_CENSORED', 0.0, 'Q2'
    except ValueError:
        pass
    return 'INVALID', None, 'Q3'

def aggregate_chl_replicates(raw_rows):
    # 수심별 정렬 후 0.5m 이내 데이터 그룹핑
    ordered = sorted(raw_rows, key=lambda x: x['depth_m'])
    groups, current_group = [], []
    
    for row in ordered:
        if not current_group or (row['depth_m'] - current_group[0]['depth_m']) <= 0.5:
            current_group.append(row)
        else:
            groups.append(current_group)
            current_group = [row]
    if current_group: groups.append(current_group)
    
    results = []
    for g in groups:
        vals = [r['val'] for r in g if r['state'] == 'QUANTITATIVE_POSITIVE']
        if not vals: continue
        
        mean, sd = statistics.mean(vals), (statistics.stdev(vals) if len(vals) > 1 else None)
        cv = sd / mean if sd and mean > 0 else None
        
        results.append({
            'depth_m': statistics.median(d['depth_m'] for d in g),
            'chl_median': statistics.median(vals),
            'replicate_n': len(vals),
            'cv': cv,
            'qc': 'Q1' if cv and cv > 0.2 else 'Q0' # CV 20% 초과시 경고
        })
    return results

# ==== 실행 테스트 (더미 데이터) ====
# if __name__ == "__main__":
#     # 동일 수심(10m, 10.1m) 반복 측정 데이터 테스트
#     data = [
#         {'depth_m': 10.0, 'val': 2.0, 'state': classify_chl(2.0)[0]},
#         {'depth_m': 10.1, 'val': 2.8, 'state': classify_chl(2.8)[0]},
#         {'depth_m': 50.0, 'val': '<BDL', 'state': classify_chl('<BDL')[0]}
#     ]
#     print(aggregate_chl_replicates(data))
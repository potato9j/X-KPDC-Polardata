from datetime import date, timedelta
import statistics

def daterange(start, end):
    cur = start
    while cur <= end:
        yield cur
        cur += timedelta(days=1)

def max_missing_gap(records, start, end):
    max_gap, cur = 0, 0
    for d in daterange(start, end):
        if records.get(d) is None:
            cur += 1
            max_gap = max(max_gap, cur)
        else: cur = 0
    return max_gap

def retreat_metric(records, obs_date, threshold_pct=10.0, persistence_days=1, min_coverage=0.9, max_gap_days=2):
    start = date(obs_date.year, 1, 1)
    days = list(daterange(start, obs_date))
    vals = [records.get(d) for d in days]
    
    valid_count = sum((v is not None for v in vals))
    coverage = valid_count / len(days)
    gap = max_missing_gap(records, start, obs_date)
    
    if records.get(start) is None: return {'status': 'UNCERTAIN_JAN1_MISSING'}
    if records.get(start) < threshold_pct: return {'status': 'LEFT_CENSORED_AT_JAN1'}
    if coverage < min_coverage or gap > max_gap_days: return {'status': 'UNCERTAIN_COVERAGE_OR_GAP'}
    
    for i, d in enumerate(days):
        run_days = days[i:i+persistence_days]
        if len(run_days) < persistence_days: break
        run_vals = [records.get(x) for x in run_days]
        if all((v is not None and v < threshold_pct for v in run_vals)):
            return {'retreat_date': d, 'status': 'RESOLVED'}
            
    return {'retreat_date': None, 'status': 'NOT_RETREATED'}

# # ==== 실행 테스트 (더미 데이터) ====
# # if __name__ == "__main__":
# #     obs = date(2020, 1, 10)
# #     records = {d: 90.0 for d in daterange(date(2020, 1, 1), obs)}
# #     records[date(2020, 1, 6)] = 9.0
# #     print("Retreat Metric:", retreat_metric(records, obs))
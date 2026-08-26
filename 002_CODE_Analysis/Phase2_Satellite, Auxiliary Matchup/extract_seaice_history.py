from datetime import timedelta

def calculate_retreat_date(daily_records, start_date, end_date, threshold=10.0, persistence=1):
    """해빙 농도가 임계값 미만으로 persistence일 이상 유지되는 첫 날짜 반환"""
    current = start_date
    days = []
    while current <= end_date:
        days.append(current)
        current += timedelta(days=1)
        
    for i, d in enumerate(days):
        run_days = days[i:i+persistence]
        if len(run_days) < persistence: break
        
        # 지정된 기간 동안 모두 임계값 미만인지 확인
        if all(daily_records.get(rd) is not None and daily_records.get(rd) < threshold for rd in run_days):
            return d
    return None

# ==== 실행 테스트 (더미 데이터) ====
# from datetime import date
# if __name__ == "__main__":
#     records = {date(2020,1,1): 90.0, date(2020,1,2): 8.0, date(2020,1,3): 5.0}
#     retreat = calculate_retreat_date(records, date(2020,1,1), date(2020,1,3))
#     print(f"Ice Retreat Date: {retreat}")
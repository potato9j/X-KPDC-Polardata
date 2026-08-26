import cdsapi
import os
import concurrent.futures

c = cdsapi.Client()
dataset = "-"

save_dir = "-"
os.makedirs(save_dir, exist_ok=True)

years = [str(y) for y in range(2016, 2025)]
months = [f"{m:02d}" for m in range(5, 11)]
days = [f"{d:02d}" for d in range(1, 32)]

boxes = [
    {"name": "Box A", "area": [82, 150, 65, 180], "prefix": "-"},
    {"name": "Box B", "area": [82, -180, 65, -140], "prefix": "-"}
]

# 1. 다운로드할 일거리(Task) 목록을 한 번에 생성
download_tasks = []
for box in boxes:
    for year in years:
        for month in months:
            file_name = os.path.join(save_dir, f"{box['prefix']}_{year}_{month}.nc")
            
            # 이미 다운로드 완료된 파일은 목록에서 자동 제외
            if not os.path.exists(file_name):
                download_tasks.append({
                    "box": box,
                    "year": year,
                    "month": month,
                    "file_name": file_name
                })

print(f"총 {len(download_tasks)}개의 남은 작업을 병렬로 시작합니다\n")

# 2. 개별 다운로드를 수행할 함수
def download_data(task):
    year_str = task['year']
    month_str = task['month']
    box_name = task['box']['name']
    
    print(f"▶ 서버 요청 시작: {year_str}년 {month_str}월 ({box_name})")
    
    request = {
        "product_type": "reanalysis",
        "variable": [
            "10m_u_component_of_wind", "10m_v_component_of_wind",
            "2m_temperature", "mean_sea_level_pressure", "total_cloud_cover"
        ],
        "year": [year_str],
        "month": [month_str],
        "day": days,
        "daily_statistic": "daily_mean",
        "time_zone": "utc+00:00",
        "frequency": "1_hourly",
        "area": task['box']['area'],
        "format": "netcdf",
    }
    
    try:
        c.retrieve(dataset, request).download(task['file_name'])
        print(f"✅ 다운로드 완료: {year_str}년 {month_str}월 ({box_name})")
    except Exception as e:
        print(f"❌ 실패: {year_str}년 {month_str}월 ({box_name}) - {e}")

# 3. 멀티스레딩 실행 
MAX_WORKERS = 3 

if download_tasks:
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        executor.map(download_data, download_tasks)
    print("\n모든 데이터 다운로드가 완료되었습니다")
else:
    print("\n더 이상 다운로드할 파일이 없습니다.")
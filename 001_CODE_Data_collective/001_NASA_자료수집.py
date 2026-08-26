import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import concurrent.futures

# 저장할 폴더 경로를 지정하세요 
save_dir = "-" 

# 사이트 기본 주소 
base_url = "-"

os.makedirs(save_dir, exist_ok=True)

# 1. 2016년~2024년의 YYYYMM 형태 폴더명 리스트 생성
target_folders = []
for year in range(2016, 2025):
    for month in range(1, 13):
        target_folders.append(f"{year}{month:02d}") 

download_tasks = []
print("다운로드할 파일 목록을 수집 중입니다. 잠시만 기다려주세욥.")

# 2. 각 YYYYMM 폴더를 돌며 .nc 파일 목록 수집
for folder in target_folders:
    folder_url = f"{base_url}{folder}/"
    
    try:
        response = requests.get(folder_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for link in soup.find_all('a'):
            href = link.get('href')
            # .nc 파일 타겟팅 (일별 NetCDF)
            if href and href.endswith('.nc'):
                full_file_url = urljoin(folder_url, href)
                file_name = os.path.join(save_dir, href)
                
                # 기존재 파일 제외
                if not os.path.exists(file_name):
                    download_tasks.append((full_file_url, file_name))
    except Exception as e:
        print(f"경고: {folder} 폴더 접근 실패 ({e})")

print(f"총 {len(download_tasks)}개의 새 파일을 찾았습니다. 병렬 다운로드를 시작합니다!\n")

# 3. 개별 파일 다운로드 함수
def download_file(task):
    url, file_path = task
    file_name = os.path.basename(file_path)
    
    try:
        with requests.get(url, stream=True, timeout=30) as r:
            r.raise_for_status()
            with open(file_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"다운로드 완료: {file_name}")
    except Exception as e:
        print(f"다운로드 실패 ({file_name}): {e}")

# 4. 멀티스레딩 다운로드 실행 (8개 동시 다운로드)
MAX_WORKERS = 8 

if download_tasks:
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        executor.map(download_file, download_tasks)
    print("\n모든 다운로드가 완료되었습니다!")
else:
    print("\n새로 다운로드할 파일이 없습니다. (모든 파일이 이미 완료)")
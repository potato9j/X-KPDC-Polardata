import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import concurrent.futures

# 저장할 폴더 경로를 지정하세요
save_dir = "-" 
base_url = "-"

os.makedirs(save_dir, exist_ok=True)
target_years = range(2016, 2025)

# 1. 다운로드할 파일 목록 먼저 싹 수집하기
download_tasks = []
print("다운로드할 파일 목록을 수집 중입니다. 잠시만 기다려주세요.")

for year in target_years:
    year_url = f"{base_url}{year}/"
    try:
        response = requests.get(year_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and href.endswith('.nc'):
                full_file_url = urljoin(year_url, href)
                file_name = os.path.join(save_dir, href)
                
                # 기존재 파일 목록에서 제외
                if not os.path.exists(file_name):
                    download_tasks.append((full_file_url, file_name))
    except Exception as e:
        print(f"경고: {year}년 페이지 스크래핑 실패 ({e})")

print(f"총 {len(download_tasks)}개의 새 파일을 찾았습니다. 병렬 다운로드를 시작합니다!\n")

# 2. 개별 파일 다운로드를 담당할 함수
def download_file(task):
    url, file_path = task
    file_name = os.path.basename(file_path)
    
    try:
        # timeout을 설정해 멈춤 현상 방지
        with requests.get(url, stream=True, timeout=30) as r:
            r.raise_for_status()
            with open(file_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"다운로드 완료: {file_name}")
    except Exception as e:
        print(f"다운로드 실패 ({file_name}): {e}")

# 3. 멀티스레딩 (여러 파일을 동시에 다운로드)
MAX_WORKERS = 8 

if download_tasks:
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # download_tasks에 있는 작업들을 일꾼들에게 나눠줌
        executor.map(download_file, download_tasks)
    print("\n모든 다운로드가 완료되었습니다")
else:
    print("\n새로 다운로드할 파일이 없습니다. (모든 파일이 이미 존재합니다)")
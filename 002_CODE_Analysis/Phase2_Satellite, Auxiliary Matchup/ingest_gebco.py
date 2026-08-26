import math

def normalize_lon(lon):
    if not math.isfinite(lon): raise ValueError('nonfinite longitude')
    if abs(lon - 180.0) < 1e-12: return -180.0
    return (lon + 180.0) % 360.0 - 180.0

def route_tile(lat, lon):
    """위경도 좌표를 기반으로 GEBCO 타일 분류"""
    if not (math.isfinite(lat) and math.isfinite(lon)): return 'Q3'
    lon = normalize_lon(lon)
    if lat < 65.0 or lat > 82.0: return 'Q2' # 범위를 벗어난 위도
    
    if -180.0 <= lon < -140.0: return 'WEST'
    if 150.0 <= lon < 180.0: return 'EAST'
    return 'Q2'

def elevation_qc(value, fill=-32767):
    """해수면 기준 고도(Elevation)를 평가하여 해양(수심) 여부 판별"""
    try: x = float(value)
    except: return 'Q3'
    
    if not math.isfinite(x) or int(x) == fill: return 'Q3'
    if x < 0: return 'Q0' # 음수 고도 = 해양
    return 'Q2'           # 양수/0 고도 = 육지 또는 해안선

# ==== 실행 테스트 (더미 데이터) ====
# if __name__ == "__main__":
#     print("Tile Routing (70N, -160E):", route_tile(70.0, -160.0))
#     print("Elevation QC (-500m):", elevation_qc(-500))
#     print("Elevation QC (10m):", elevation_qc(10))
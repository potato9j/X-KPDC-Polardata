from decimal import Decimal
from collections import defaultdict

def create_vertical_master(ctd_data, chl_data, nox_data):
    # (profile_id, depth)를 키로 사용하여 데이터를 병합할 딕셔너리
    vertical = defaultdict(dict)
    
    def canonical_depth(val):
        return Decimal(str(val)).quantize(Decimal('0.000001'))

    # 1. CTD 데이터 할당
    for row in ctd_data:
        key = (row['profile_id'], canonical_depth(row['depth_m']))
        vertical[key].update({'CTD': True, 'temperature': row['temperature']})
        
    # 2. 엽록소(Bottle Chl) 데이터 할당
    for row in chl_data:
        key = (row['profile_id'], canonical_depth(row['depth_m']))
        vertical[key].update({'BOTTLE_CHL': True, 'chl_mg_m3': row['chl']})

    # 3. 영양염(NOX) 데이터 할당
    for row in nox_data:
        key = (row['profile_id'], canonical_depth(row['depth_m']))
        vertical[key].update({'NOX': True, 'nox_umol_L': row['nox']})

    # 병합 결과 정리
    master_table = []
    for (pid, depth), data in sorted(vertical.items()):
        layers = [k for k in ['CTD', 'BOTTLE_CHL', 'NOX'] if data.get(k)]
        row = {
            'profile_id': pid,
            'depth_m': float(depth),
            'layers_present': ';'.join(layers),
            **data
        }
        master_table.append(row)
        
    return master_table

# ==== 실행 테스트 (더미 데이터) ====
# if __name__ == "__main__":
#     ctd = [{'profile_id': 'A1', 'depth_m': 10, 'temperature': 15.2}]
#     chl = [{'profile_id': 'A1', 'depth_m': 10.0, 'chl': 1.5}] # 동일 수심 병합 테스트
#     nox = [{'profile_id': 'A1', 'depth_m': 20, 'nox': 5.0}]
    
#     print(create_vertical_master(ctd, chl, nox))
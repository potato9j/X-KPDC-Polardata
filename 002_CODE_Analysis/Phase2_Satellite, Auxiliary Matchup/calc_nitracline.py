def find_nitracline_gradient(points, threshold=0.1):
    """인접한 두 수심 간의 영양염 변화율이 임계값을 넘는 첫 구간의 중간 수심 반환"""
    for a, b in zip(points, points[1:]):
        gap = b['z'] - a['z']
        if gap <= 0: continue
        
        grad = (b['v'] - a['v']) / gap
        if grad > threshold:
            return {'z_mid': (a['z'] + b['z']) / 2, 'gradient': grad}
    return None

# ==== 실행 테스트 (더미 데이터) ====
# if __name__ == "__main__":
#     nox_points = [{'z': 5.0, 'v': 0.1}, {'z': 10.0, 'v': 0.2}, {'z': 20.0, 'v': 2.5}]
#     nitracline = find_nitracline_gradient(nox_points)
#     print(f"Nitracline Depth: {nitracline['z_mid']} m (Gradient: {nitracline['gradient']})")
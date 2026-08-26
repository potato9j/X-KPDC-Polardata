import statistics

def first_gradient(points, threshold):
    for i, (a, b) in enumerate(zip(points, points[1:]), start=1):
        gap = b['z'] - a['z']
        if gap <= 0: continue
        grad = (b['v'] - a['v']) / gap
        if grad > threshold:
            return {'index': i, 'z': (a['z'] + b['z']) / 2, 'g': grad, 'z0': a['z'], 'z1': b['z'], 'v0': a['v'], 'v1': b['v']}
    return None

def nox_one_crossing(points):
    if points[0]['v'] >= 1.0:
        return {'status': 'LEFT_CENSORED_AT_SHALLOWEST', 'z': None}
    for a, b in zip(points, points[1:]):
        if a['v'] < 1.0 <= b['v'] and b['v'] != a['v']:
            frac = (1.0 - a['v']) / (b['v'] - a['v'])
            return {'status': 'RESOLVED', 'z': a['z'] + frac * (b['z'] - a['z'])}
    return {'status': 'NOT_RESOLVED_COMPLETE_PROFILE', 'z': None}

def median3_gradient(points):
    if len(points) < 5: return None
    centered = []
    for i in range(1, len(points) - 1):
        centered.append({'z': points[i]['z'], 'v': statistics.median([points[i - 1]['v'], points[i]['v'], points[i + 1]['v']])})
    return first_gradient(centered, 0.1)

# # ==== 실행 테스트 (더미 데이터) ====
# # if __name__ == "__main__":
# #     pts = [{'z': 5.0, 'v': 0.1}, {'z': 10.0, 'v': 1.1}, {'z': 20.0, 'v': 2.5}]
# #     print("Gradient:", first_gradient(pts, 0.1))
# #     print("Crossing:", nox_one_crossing(pts))
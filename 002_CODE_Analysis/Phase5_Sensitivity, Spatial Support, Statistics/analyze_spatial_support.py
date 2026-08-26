import numpy as np
from scipy.spatial.distance import cdist

def deterministic_kmeans(x, k=5, seed=20260712, n_init=100, max_iter=300):
    """결정론적 난수 시드를 적용한 K-Means 클러스터링 기반 공간 분할"""
    rng = np.random.default_rng(seed)
    n = len(x)
    best = None
    for _ in range(n_init):
        centers = np.empty((k, x.shape[1]))
        centers[0] = x[int(rng.integers(n))]
        d2 = np.sum((x - centers[0]) ** 2, axis=1)
        for j in range(1, k):
            probs = d2 / d2.sum()
            centers[j] = x[int(rng.choice(n, p=probs))]
            d2 = np.minimum(d2, np.sum((x - centers[j]) ** 2, axis=1))
            
        labels = np.full(n, -1, int)
        for _it in range(max_iter):
            nl = np.sum((x[:, None, :] - centers[None, :, :]) ** 2, axis=2).argmin(1)
            if np.array_equal(nl, labels): break
            labels = nl
            for j in range(k):
                pts = x[labels == j]
                centers[j] = pts.mean(0) if len(pts) else x[int(rng.integers(n))]
                
        inertia = float(np.sum((x - centers[labels]) ** 2))
        if best is None or inertia < best[0]:
            best = (inertia, labels.copy(), centers.copy())
    return best[1], best[2], best[0]

def calc_cross_group_distances(coords, groups):
    """프로파일 간 거리 행렬을 생성하고 타 항차(그룹)와의 최단 거리를 추출"""
    d = cdist(coords, coords)
    np.fill_diagonal(d, np.inf)
    cross_distances = []
    for i in range(len(coords)):
        mask = groups != groups[i]
        if mask.any():
            cross_distances.append(float(d[i, mask].min()))
    return np.array(cross_distances)

# # ==== 실행 테스트 (더미 데이터) ====
# # if __name__ == "__main__":
# #     coords = np.array([[0, 0], [10, 10], [10, 12], [50, 50], [52, 50]])
# #     groups = np.array(['A', 'A', 'B', 'C', 'C'])
# #     labels, centers, inertia = deterministic_kmeans(coords, k=2)
# #     print(f"K-Means Labels: {labels}")
# #     print(f"Cross-group Distances: {calc_cross_group_distances(coords, groups)}")
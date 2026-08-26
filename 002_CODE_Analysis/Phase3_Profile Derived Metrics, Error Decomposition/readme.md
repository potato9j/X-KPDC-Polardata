| file name | subject | summary |
| --- | --- | --- |
| calc_mld_stratification.py | MLD 및 성층화 지수 계산 | 밀도 역전 플래그를 확인하고 교차점을 보간하는 로직 | 
| calc_nitracline.py | 질산염약층 깊이 탐색 | 구배(Gradient), 최대 양수 구배, 1.0교차점 등 원본 탐색 함수 |
| decompose_errors.py | 위성-현장 오차 분해 | 수직 오차 및 위성 산출 오차를 로그 스케틸로 연산하는 알고리즘 | 
| detect_scm.py | SCM 판별 및 분류 | `peak_candidate`와 복합 조건을 검사하는 `definition_decision`함수 | 
| extract_seaice_history.py | 해빙 이력 지표 | 연속된 날짜 생성 및 과거 기간과 퇴각일을 연산 |
| integrate_chl.py | 사다리꼴 적분 구조 스크리닝 | 수심에 따른 매듭(Knots)을 설정하고, 사다리꼴 면적을 합산해 0~100m의 엽록소를 적분하는 핵심 연산 및 스크리닝 로직 | 

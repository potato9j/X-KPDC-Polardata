| file name | subject | summary |
| --- | --- | --- |
| analyze_spatial_support.py | 공간 지지(Spatial Support) 및 K-Means 군집화 | 지리적 좌표를 바탕으로 볼록 껍질(Convenx Hull) 및 거리를 계산하고, 공간 구조를 5개의 폴드(K-Means K=5)로 분할 |
| calc_uncertainty.py | 불확실성 산출 및 이진 부트스트랩 | 항차 단위 부트스트랩을 수행하여, 특정 위험 요인(과소대표성)의 발생 비율에 대한 95% 신뢰구간을 평가 | 
| sensitivity_external_sensors.py | 외부 센서 민감도 및 LOPO 교차검증 | 형광 센서 데이터를 검증하기 위해 단일 프로파일을 제외하면서 Huber회귀를 반복 적합하여 성능 편향을 산출 |
| sensitivity_satellite_matchup.py | 위성 매치업 윈도우 통계 | 지정된 반경 내부의 위성 픽셀 배열을 평가하여 유효 픽셀 수, 중앙값, 변동계수를 도출하고 엄격한 품질 게이트를 적용 |
| sensitivity_integrated_chl.py | 민감도 매트릭스 순회 평가 | 항목 평가 간, 여러 개의 임계값 배열을 카테시안 곱으로 생성하여 각 조건 하에서 결과하 어떻게 변화하는지 일괄 평가 |
| sensitivity_mld_nitracline.py | 민감도 매트릭스 순회 평가 | 항목 평가 간, 여러 개의 임계값 배열을 카테시안 곱으로 생성하여 각 조건 하에서 결과하 어떻게 변화하는지 일괄 평가 |
| sensitivity_scm.py | 민감도 매트릭스 순회 평가 | 항목 평가 간, 여러 개의 임계값 배열을 카테시안 곱으로 생성하여 각 조건 하에서 결과하 어떻게 변화하는지 일괄 평가 |

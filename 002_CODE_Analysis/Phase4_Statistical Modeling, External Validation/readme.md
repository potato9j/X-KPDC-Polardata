| file name | subject | summary |
| --- | --- | --- |
| analyze_vertical_structure.py | 수직 구조 요약 및 계층화 | 수심과 수심대에 따라 프로파일 데이터를 계층화하고, 관측값들의 기초 통계량(평균, 중앙값, 사분위수 등)을 산출 |
| evaluate_baseline_limits.py | 크루즈 기반 군집 부트스트랩 및 신뢰구간 평가 | 단일 프로파일 단위의 과대적합 신뢰성을 보완하기 위해 독립 관측 단위인 '항차'단위로 재표본추출을 수행하여 통계적 신뢰구간과 편향을 진단 | 
| fit_simple_regression.py | 표층 회귀모형 적합 및 OOF 잔차 산출 | 행렬곱(np.linalg.listsq)을 통해 OLS회귀식을 적합하고, 항차 단위로 분할된 GroupKFold를 활용해 과적합을 배제한 Out-Of-Fold 잔차를 도출하는 예측 로직 | 
| fir_surface_uniform_baseline.py | 기준모형 평가 및 성능 지표 산출 | 예측값과 실제 관측값을 바탕으로 MAE, RMSE, 구간점수 등 예측 모형을 주요 평가 지표로 산출하고 캘리브레이션 편향을 진단 | 

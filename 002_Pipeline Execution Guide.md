# KPDC SCM Pipeline Execution Guide

## 1. Environment & Prerequisites

- Raw binary datasets are not included in this code bundle.
- Note: Legacy scripts contain absolute path references (`H:\A0_\...` or `/mnt/data/...`). Set up a symbolic link or update root path variables in the scripts before execution.

## 2. Pipeline Execution Order

### Phase 1: Data Ingestion & Field QC
1. `04_code/01_ingest_qc/build_profile_master.py`
2. `04_code/01_ingest_qc/process_ctd_teos10.py`
3. `04_code/01_ingest_qc/qc_bottle_chl.py`
4. `04_code/01_ingest_qc/qc_nutrients.py`
5. `04_code/01_ingest_qc/calibrate_fluorescence.py`
6. `04_code/01_ingest_qc/apply_field_qc.py`

### Phase 2: Satellite & Auxiliary Matchup
7. `04_code/03_matching/ingest_modis.py`
8. `04_code/03_matching/ingest_nsidc.py`
9. `04_code/03_matching/ingest_oisst.py`
10. `04_code/03_matching/ingest_gebco.py`
11. `04_code/03_matching/match_station_grid.py`
12. `04_code/03_matching/calc_match_rates.py`

### Phase 3: Profile Derived Metrics & Error Decomposition
13. `04_code/02_profile_metrics/calc_mld_stratification.py`
14. `04_code/02_profile_metrics/calc_nitracline.py`
15. `04_code/02_profile_metrics/detect_scm.py`
16. `04_code/02_profile_metrics/extract_seaice_history.py`
17. `04_code/02_profile_metrics/integrate_chl.py`
18. `04_code/02_profile_metrics/decompose_errors.py`

### Phase 4: Statistical Modeling & External Validation
19. `04_code/04_modeling/analyze_vertical_structure.py`
20. `04_code/04_modeling/fit_surface_uniform_baseline.py`
21. `04_code/04_modeling/fit_simple_regression.py`
22. `04_code/04_modeling/evaluate_baseline_limits.py`

### Phase 5: Sensitivity, Spatial Support & Statistics
23. `04_code/02_profile_metrics/sensitivity_scm.py`
24. `04_code/02_profile_metrics/sensitivity_mld_nitracline.py`
25. `04_code/02_profile_metrics/sensitivity_integrated_chl.py`
26. `04_code/03_matching/sensitivity_satellite_matchup.py`
27. `04_code/03_matching/sensitivity_external_sensors.py`
28. `04_code/04_modeling/analyze_spatial_support.py`
29. `04_code/04_modeling/calc_uncertainty.py`
30. `04_code/05_tables/export_final_stats.py`
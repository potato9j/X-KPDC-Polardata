<div align="center">

# 서부 북극해 엽록소의 대표성과 위성 관측 한계

### [어쩌다 북극해]

2015–2023년 KPDC/ARAON 서부 북극해 하계 항차의 200개 수직 프로파일을 이용하여 표층 Chl-a의 수주 대표성, SCM 수직구조, 항차 외부 예측성능과 MODIS 위성 관측가능성을 평가한 데이터 분석 연구 프로젝트입니다.

 규정에 따라, 신원을 유추 또는 확인할 수 있는 정보는 포함되지 않았습니다. 

</div>

> [!IMPORTANT]
> 이 공개 저장소는 **문서화와 통제된 산출물 공개를 위한 저장소**입니다. 약 **14,263개·18.1 GB** 규모의 원자료 전체는 비공개 저장공간에 보관하며 본 공개 저장소에 포함하지 않습니다. 따라서 이 저장소만으로 원자료부터 최종 결과까지 완전하게 구현할 수 없습니다.

---

## 🛠️ Tech Stack & Environment

본 프로젝트의 분석 및 파이프라인 구축에 사용된 핵심 환경과 제3자 패키지 라이브러리 명세입니다. 이 패키지 목록은 기준 분석환경이며, 내부 스냅샷 및 폐쇄형 모듈에 의존하므로 라이브러리 설치만으로 전체 실행환경을 복구할 수 없습니다.

* **Development Environment:** Windows 10, Python 3.13.5, Visual Studio Code, Codex
  * (Codex-5.5 : 사용자가 사전에 설정한 파이프 라인에 따른 코드 초안 작성)
  * (GPU 가속 프레임워크나 CUDA 연산은 사용하지 않은 CPU 기반 연산 환경입니다.)
* **Core Numerical & Scientific Stack:**
  * `numpy == 2.3.5`
  * `pandas == 2.2.3`
  * `scipy == 1.17.0`
  * `scikit-learn == 1.8.0`
* **Oceanography & Geospatial Libraries:**
  * `gsw == 3.6.23` (TEOS-10 기반 해양물리량 계산)
  * `pyproj == 3.7.2` (EPSG:3413 좌표계 변환)
  * `shapely == 2.1.2` (공간기하와 관측지원 분석)
  * `rasterio == 1.5.0` / `h5py == 3.15.1`
* **Visualization & Inspection:**
  * `matplotlib == 3.10.8` / `basemap == 2.0.0`

---

## 🔒 Code Non-Disclosure & Security Governance

본 저장소에는 연구결과와 분석 거버넌스의 감사가능성(auditability) 및 추적가능성(traceability)을 제공하기 위한 문서가 포함되어 있으며, **원본 실행 스크립트 모듈은 통제된 비공개 상태 혹은 중요 보안 요소가 정제된 임시 공개 상태로 관리됩니다.** 코드를 제한하거나 비공개로 유지하는 구체적인 시스템 요구사항 및 기술적 사유는 다음과 같습니다.

### 1. 인프라 정보 노출에 따른 서버 보안 취약점 (Information Disclosure Vulnerability)
소스 코드 내부에는 연구 전용 서버의 절대 마운트 경로(e.g., `/mnt/data/...`), 내부 파일명 규칙 및 입출력 배치가 포함되어 있습니다. 
* **발생 문제:** 이 코드가 무분별하게 퍼블릭으로 노출될 경우 물리적·논리적 저장영역의 배치, 외부자료와 내부자료가 결합되는 처리 지점 등이 노출됩니다. 이는 공격자가 시스템의 구조를 사전 정찰하는 데 사용되어 시스템 침투 공격의 표면(Attack Surface)을 확대하는 정보노출 취약성을 발생시킵니다.

### 2. 오케스트레이션 및 파이프라인 무결성 훼손 (Control Plane Integrity Issue)
본 파이프라인은 단순 스크립트가 아니라, 데이터 오염과 환각(Hallucination)을 막기 위해 각 분석단계의 개방·차단, 검증순서, 상위 산출물 권위를 관리하는 **프로젝트 전용 제어면**입니다.
* **발생 문제:** 소스 코드에는 Stage-Gate 제어, 자동 검증 레코드(`V001`~`V050`), 생산 코드와 독립 검증기의 이중 확인 로직이 통합되어 있습니다. 제어 로직이 실행 맥락과 분리된 상태로 공개되면, 파이프라인 무결성이 훼손될 수 있습니다.

### 3. 폐쇄형 런타임 종속성으로 인한 계보 단절 및 허위 재현성 (Runtime Confounding & False Reproducibility)
스크립트 일부는 범용 파이썬 환경이 아닌, 내부 파일시스템 구조, 승인 스냅샷과 상태관리 JSON, 그리고 실행환경 전용 모듈(예: `artifact_tool`)에 하드코딩 수준으로 결합되어 있습니다.
* **발생 문제:** 단순 경로 치환만으로는 내부 런타임 의존성이 복원되지 않습니다. 실행 불가능한 소스 코드 일부를 퍼블릭에 방치하는 것은 오히려 분석계보 단절과 허위 재현성 주장을 유발할 수 있으므로 정제되지 않은 소스 공개를 제한하는 것으로 결정하였습니다.

### 4. 데이터 거버넌스 컴플라이언스 및 사전 유출 리스크 (Compliance & Pre-disclosure Governance)
아라온호/극지데이터센터(KPDC) 관측 데이터와 내부 검증기록은 목적 제한, 최소 공개 및 역할분리 원칙에 따라 관리됩니다.
* **발생 문제:** -

### 5. 외부 데이터 프로바이더 인증 자산 보호 및 어뷰징 차단 (Provider Credential & Quota Protection)
본 파이프라인은 위성 관측 자료(NASA Earthdata, Copernicus 등)의 자동화된 수집을 위해 외부 데이터 플랫폼의 API와 통신하며, 이 과정에서 고유 인증 토큰(Access Token/API Key) 및 세션 자격 증명이 사용됩니다.
* **발생 문제:** 데이터 자체는 오픈 데이터(Open Data)이나, 이를 호출하는 개인 인증 키가 퍼블릭 레포지토리에 노출될 경우 제3자의 무단 트래픽 도용 및 대규모 쿼터(Quota) 초과 어뷰징의 타겟이 됩니다. 이는 데이터 제공 기관의 보안 정책(Terms of Service)을 심각하게 위반하는 행위이며 시스템 접근 권한이 영구 차단(Ban)되는 보안 사고로 직결되므로, 인증 자산이 완전 정제(Scrubbing) 및 추상화되지 않은 원본 수집 스크립트의 노출을 엄격히 금지합니다.

---

## 🛠️ Code Access & Original Source Release Policy

본 저장소의 코드 및 관련 자료는 심사 및 평가와 관련한 공식적인 요청이 있는 경우에 한해, 내부 시스템 경로 및 오케스트레이션 로직 등 그 어떠한 정보도 삭제하지 않은 **원본 코드(Original Source Code) 전체를 아래 조건에 따라 제공**할 수 있습니다. (단, 외부 API 통신을 위한 개인 자격증명 및 인증 토큰은 보안상 제외됩니다.)

### 📌 원본 코드 제공 및 열람 조건 (Conditions for Access)

1. **자격 증명 (Identity Verification & Authorization)**
   * 담당자 등 정당한 검증 및 평가 목적을 가진 인가된 대상자임을 확인할 수 있어야 합니다.

2. **통제된 비공개 접근 (Controlled Private Access)**
   * 원본 코드는 퍼블릭(Public) 저장소로 전환되거나 불특정 다수에게 파일 형태로 배포되지 않습니다. 
   * 권한이 확인된 평가자에게 **GitHub Private Repository의 읽기 전용(Read-only) 협업자 권한**을 부여하거나, 만료 기한이 설정된 **보안 컨테이너/패키지 형태**로만 제한적으로 제공됩니다. 

3. **목적 제한 및 취약점 악용 금지 (Purpose Limitation & No Exploitation)**
   * 제공된 코드는 본 프로젝트의 통계적 타당성, 파이프라인 무결성, 그리고 재현성 검증 용도로만 열람 및 실행되어야 합니다.
   * 노출된 서버 내부 마운트 경로, 체계, 오케스트레이션 아키텍처를 시스템 취약점 스캐닝에 악용하거나 타 연구/상업적 파이프라인에 도용하는 행위를 엄격히 금지합니다.

4. **비밀유지 및 무단 배포 금지 (Strict Non-Disclosure)**
   * 평가자는 검토 과정에서 취득한 내부 디렉토리 토폴로지, 파이프라인 제어 로직, 검증 알고리즘 등 일체의 기술적 자산을 제3자에게 유출하거나 2차 배포할 수 없습니다.

5. **원시 데이터 연동에 관한 고지 (Raw Data Provisioning Notice)**
   * 원본 코드를 완전하게 종단간(End-to-End) 재실행하기 위해서는 약 18.1 GB 규모의 대용량 원시 데이터 및 내부 스냅샷이 필요합니다. 전체 파이프라인 구동이 필수적인 심사 단계일 경우, 해당 원시 데이터의 안전한 전달 및 마운트 방식은 별도로 협의해야 합니다.
  
---

## 📢 LICENSE

모든 일정이 종료되기 전까지 다음의 `LICENSE`를 따릅니다. 
```
Copyright (c) 2026 [일정 종료까지 비공개 / 어쩌다 북극해]. All rights reserved.

No part of this software, including source code, pipeline architecture, and metadata, 
may be reproduced, distributed, or transmitted in any form or by any means, 
without the prior written permission of the copyright holder.
```

(모든 일정 종료 후, MIT/Apache2.0 변경 예정)

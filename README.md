<div align="center">
  <img src="https://raw.githubusercontent.com/MatthewJakubowski/Universal-Lab-Converter/main/going_dark_cover.jpg" width="100%" alt="System Status: Going Dark. Deep Work Protocol.">

# 🏥 Clinical-Telemetry-Pipeline

### Master End-to-End Architecture: Hardware ASTM Stream Parsing, Real-Time PBRTQC, Westgard IQC & MLOps Reagent Drift Governance

[![CI - Pytest Suite](https://github.com/MatthewJakubowski/Clinical-Telemetry-Pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/MatthewJakubowski/Clinical-Telemetry-Pipeline/actions/workflows/ci.yml)
[![Python Version](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3b82f6?logo=python&logoColor=white)](https://github.com/MatthewJakubowski/Clinical-Telemetry-Pipeline)
[![Standard](https://img.shields.io/badge/Standards-ASTM%20%7C%20ISO%2015189%20%7C%20CLSI-8b5cf6)](https://github.com/MatthewJakubowski/Clinical-Telemetry-Pipeline)
[![Research & PoC](https://img.shields.io/badge/Status-Educational%20%2F%20PoC-f59e0b)](https://github.com/MatthewJakubowski/Clinical-Telemetry-Pipeline)
[![License: MIT](https://img.shields.io/badge/License-MIT-06b6d4.svg)](https://opensource.org/licenses/MIT)

> **The Capstone Architecture of #FromPipetteToPython**  
> An integrated, deterministic healthcare telemetry and data governance engine linking low-level analyzer byte streams to automated MLOps lot verification.

---

### 🌐 Ecosystem & Professional Profiles

[🌐 Portfolio Hub](https://mateusz-jakubowski.ai.studio/) • [🚀 Project Showroom](https://from-pipette-to-python.ai.studio/) • [💼 LinkedIn](https://www.linkedin.com/in/mateuszjakubowski) • [🐙 GitHub](https://github.com/MatthewJakubowski)  
[🏆 Kaggle](https://www.kaggle.com/matthewjakubowski) • [🤗 Hugging Face](https://huggingface.co/matthewjakubowski) • [𝕏 Twitter / X](https://x.com/M_S_Jakubowski) • [🍷 Vivino](http://www.vivino.com/users/mateusz.jakubowski/)

</div>

---

## 🏗️ Master System Architecture

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ 🏥 CLINICAL TELEMETRY & METROLOGY PIPELINE (#FromPipetteToPython)           │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                         [Raw ASTM Byte Stream]
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1️⃣ MedBridge-ASTM-Parser                                                    │
│    • Low-level ASTM E1381 / E1394 stream ingestion                          │
│    • Modulo 256 checksum verification & frame unescaping                    │
│    • DataFrame serialization (MCV = 91.2 fL, Potassium = 4.45 mmol/L)       │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                [Parsed Telemetry]
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 2️⃣ Moving-Averages-PBRTQC                                                   │
│    • Truncation filtering (physiological boundary clipping: 60–120 fL)       │
│    • Bull's Algorithm (XB) tracking red blood cell indices (MCV)            │
│    • Real-time batch deviation check: Target 90.0 fL ➔ +0.16% [STABLE]      │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                             [Parallel IQC Stream]
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 3️⃣ Lab-QC-Guardian                                                          │
│    • Multi-rule Westgard validation (1-3s, 2-2s, R-4s, 4-1s)                │
│    • Dynamic analytical error detection (Target = 4.50, SD = 0.15)          │
│    • Quality control evaluation: 4.58 mmol/L ➔ Status: PASS                 │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                         [Reagent Lot Transition Audit]
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 4️⃣ LabDrift-Scikit-Guard                                                    │
│    • Reagent Lot-to-Lot comparison (Baseline vs. Candidate)                 │
│    • Population Stability Index (PSI = 0.0150 < 0.10 ➔ STABLE)              │
│    • Two-Sample Kolmogorov-Smirnov Test (p = 0.7583)                        │
│    • Metrological decision matrix: ACCEPT (GO) [ISO 15189 Aligned]          │
└─────────────────────────────────────────────────────────────────────────────┘
```
## 📦 Integrated Core Libraries

This capstone pipeline connects the 4 core libraries developed under the **#FromPipetteToPython** initiative:

* [**MedBridge-ASTM-Parser**](https://github.com/MatthewJakubowski/MedBridge-ASTM-Parser) — Hardware telemetry and ASTM stream decoding.
* [**Moving-Averages-PBRTQC**](https://github.com/MatthewJakubowski/Moving-Averages-PBRTQC) — Real-time moving average algorithms (Bull $X_B$, EWMA, CUSUM).
* [**Lab-QC-Guardian**](https://github.com/MatthewJakubowski/Lab-QC-Guardian) — Multi-rule Westgard IQC and Six Sigma metrology.
* [**LabDrift-Scikit-Guard**](https://github.com/MatthewJakubowski/LabDrift-Scikit-Guard) — Population Stability Index (PSI) and reagent drift governance.

## ​⚡ Execution
​Run the master pipeline directly:
```bash
python pipeline.py
```
## 🧪 Unit Testing
​Execute the automated test suite:
```bash
pytest tests/ -v
```
## 👨‍💻 About the Author

**Matthew (Mateusz) Jakubowski**  
*Senior Laboratory Technologist & Healthcare Data Engineer*  
Creator of the **#FromPipetteToPython** initiative.

With over 15 years in medical laboratory diagnostics, I focus on building transparent, deterministic, and explainable software solutions that safeguard clinical AI pipelines from silent distribution shifts and hardware telemetry corruption.

* **Engineering Stack:** Python, NumPy, Pandas, Scipy, Pytest, FastAPI, Docker.
* **Environment:** 100% Mobile-First on **Samsung DeX** (Galaxy S24 Ultra & Tab S11 Ultra).

---

## ⚖️ Legal & Medical Device Disclaimer

> **IMPORTANT NOTICE / NON-MEDICAL SOFTWARE DISCLAIMER:**
>
> * **Educational & Research Proof of Concept (PoC):** This repository is developed solely for educational, technical demonstrative, and scientific research purposes under the **#FromPipetteToPython** initiative.
> * **Not a Certified Medical Device:** This software is **NOT** a certified Medical Device (neither CE-IVD, IVDR 2017/746, nor FDA 510(k)/SaMD certified). It is not intended, designed, or approved for clinical decision-making, direct patient diagnosis, or live medical diagnostic execution without human verification.
> * **No Clinical Liability:** All data processed in examples or unit tests are synthetic or anonymized mock datasets.
> * **Provided "AS IS":** The software is provided under the terms of the MIT License, without warranty of any kind.

---

## 🛡️ License

Distributed under the **MIT License**.


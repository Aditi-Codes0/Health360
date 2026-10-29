# HEALTH 360: Chronic Disease Analytics, Risk Factor Analysis, and Predictive Insights

[![Python Version](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Tableau Compatible](https://img.shields.io/badge/Tableau-Ready-orange.svg)](https://www.tableau.com/)
[![Tests](https://img.shields.io/badge/tests-18%20passed-brightgreen.svg)](tests/)

An end-to-end healthcare data analytics, machine learning, and Tableau visualization platform investigating the epidemiological prevalence, biomarker divergences, lifestyle behavioral risks, and predictive patterns of three major chronic conditions: **Coronary Heart Disease**, **Diabetes Mellitus**, and **Cerebrovascular Stroke**.

---

## 1. PROJECT ABSTRACT & MOTIVATION

Chronic non-communicable diseases (NCDs)—specifically cardiovascular disorders, type 2 diabetes, and stroke—constitute the predominant drivers of mortality, long-term physical impairment, and escalating healthcare expenditures worldwide. In clinical and public health operations, interventions frequently occur at late stages after irreversible vascular or metabolic damage has manifested.

**Health 360** addresses this challenge through an integrated computational framework that couples robust Python epidemiological analytics with interactive Tableau business intelligence dashboards. The system processes patient demographics, clinical vitals, lifestyle exposures, and acute symptoms to uncover disease patterns, quantify statistical associations, identify high-burden demographic segments, and generate calibrated predictive risk insights.

> **Clinical & Governance Disclaimer**: Health 360 is an academic and analytical platform designed for population surveillance, clinical risk triage, and healthcare resource planning. It is not an automated medical diagnostic tool. All model predictions represent **model-estimated statistical risk** and must not supersede qualified clinical evaluation.

---

## 2. SYSTEM ARCHITECTURE

```
+----------------------------------------------------------------------------------------------------+
|                                    HEALTH 360 ARCHITECTURE                                         |
+----------------------------------------------------------------------------------------------------+
                                      [ RAW HEALTH DATA ]
                                               │
                                               ▼
                         ┌───────────────────────────────────────────┐
                         │  STAGE 1: Ingestion & Schema Discovery    │
                         │  - Format parsing (CSV/XLSX)              │
                         │  - Data Dictionary & Capabilities Matrix  │
                         └─────────────────────┬─────────────────────┘
                                               ▼
                         ┌───────────────────────────────────────────┐
                         │  STAGE 2: Validation & Clinical Audit     │
                         │  - Duplicate detection (Patient & Row)    │
                         │  - Clinical plausibility boundary checks  │
                         │  - Outlier profiling (IQR & Z-Score)      │
                         └─────────────────────┬─────────────────────┘
                                               ▼
                         ┌───────────────────────────────────────────┐
                         │  STAGE 3: Preprocessing & Standardization │
                         │  - Defensible median/category imputation  │
                         │  - Derived CDC Age Groups & WHO BMI Tiers │
                         │  - Data Quality Audit Log Export          │
                         └─────────────────────┬─────────────────────┘
                                               ▼
                         ┌───────────────────────────────────────────┐
                         │  STAGE 4: Exploratory & Statistical EDA   │
                         │  - Parametric & Nonparametric summaries   │
                         │  - Pearson/Spearman Correlation Matrices  │
                         │  - High-res distribution & heatmap plots  │
                         └─────────────────────┬─────────────────────┘
                                               ▼
                         ┌───────────────────────────────────────────┐
                         │  STAGE 5: Epidemiology & Stratification   │
                         │  - Population prevalence (95% Wilson CI)  │
                         │  - Comorbidity & multimorbidity burden    │
                         │  - Biomarker contrasts (SBP, Glucose, BMI)│
                         └─────────────────────┬─────────────────────┘
                                               ▼
                         ┌───────────────────────────────────────────┐
                         │  STAGE 6: Lifestyle, Symptoms & Inference │
                         │  - Behavioral exposure cross-tabulation   │
                         │  - Contingency Odds Ratios (95% CI)       │
                         │  - Chi-Square, Welch's t-test, Mann-Whit. │
                         │  - Benjamini-Hochberg FDR Corrections     │
                         └─────────────────────┬─────────────────────┘
                                               ▼
                         ┌───────────────────────────────────────────┐
                         │  STAGE 7: Machine Learning Risk Modeling  │
                         │  - Target validation & leakage prevention │
                         │  - ColumnTransformer & Pipeline scaling   │
                         │  - Stratified 5-Fold Cross-Validation     │
                         │  - Balanced class weights (Recall/F1 focus│
                         │  - ROC-AUC, PR-AUC, Subgroup Fairness     │
                         └─────────────────────┬─────────────────────┘
                                               ▼
                         ┌───────────────────────────────────────────┐
                         │  STAGE 8: Python-to-Tableau Data Pipeline │
                         │  - 13 Granular & aggregated CSV exports   │
                         │  - Tableau Export Manifest JSON           │
                         │  - Native XML Tableau Workbook (.twb)     │
                         └─────────────────────┬─────────────────────┘
                                               ▼
                         ┌───────────────────────────────────────────┐
                         │  STAGE 9: Academic Findings & Dashboards  │
                         │  - Executive Markdown Findings Report     │
                         │  - Dashboard 1: Clinical Risk Assessment  │
                         │  - Dashboard 2: Lifestyle & Risk Factors  │
                         │  - Dashboard 3: Population Health Insights│
                         └───────────────────────────────────────────┘
```

---

## 3. TECHNOLOGY STACK

- **Core Analytics & Processing**: Python 3.11+, Pandas 3+, NumPy 2+, SciPy 1.18+, Statsmodels 0.15+
- **Machine Learning**: Scikit-Learn 1.9+, Joblib 1.6+
- **Visualization**: Matplotlib 3.11+, Seaborn 0.13+, Plotly 7.1+
- **Business Intelligence & Reporting**: Tableau Desktop / Tableau Public, Native XML `.twb`, Markdown
- **Quality Assurance**: Pytest 9.1+, Type Hints, Logging Infrastructure

---

## 4. DATASETS & DATA PROVENANCE

Health 360 enforces rigorous data provenance, distinguishing between the unified population surveillance cohort and independent clinical benchmark datasets:

### A. Primary Surveillance Cohort (`data/raw/health360_primary_cohort.csv`)
- **Sample Size**: 10,000 verified patient records (`P00001` to `P10000`).
- **Provenance**: Modeled and calibrated directly against the joint empirical distributions of the CDC Behavioral Risk Factor Surveillance System (BRFSS) and the National Health and Nutrition Examination Survey (NHANES).
- **Attributes Captured**:
  - *Demographics*: `patient_id`, `age` (18–88), `sex` (Male/Female), `region` (Northeast, Midwest, South, West), `observation_year` (2023–2025).
  - *Clinical Vitals*: `bmi` (continuous kg/m²), `systolic_bp` (mmHg), `diastolic_bp` (mmHg), `cholesterol` (total mg/dL), `fasting_glucose` (mg/dL).
  - *Lifestyle Behaviors*: `smoking_status` (Never, Former, Current), `alcohol_consumption` (Non-drinker, Moderate, Heavy), `physical_activity` (Sedentary, Moderate, Active).
  - *Reported Symptoms*: `fatigue` (0/1), `chest_pain` (0/1), `dizziness` (0/1).
  - *Validated Outcomes*: `heart_disease` (0/1), `diabetes` (0/1), `stroke` (0/1).
- **Realistic Data Integrity**: Injected ~1.5% non-critical missingness to validate preprocessing, median imputation, and audit reporting.

### B. Independent Benchmark Datasets
- **`benchmark_stroke.csv`** (Kaggle/McKinsey Healthcare, N = 5,110): Real clinical stroke observations with demographics, hypertension, glucose, BMI, and stroke outcomes.
- **`benchmark_heart.csv`** (UCI Cleveland Clinic, N = 303): Classic Detrano et al. coronary heart disease dataset with chest pain types, resting BP, cholesterol, ECG, and exercise-induced angina.
- **`benchmark_diabetes.csv`** (Pima Indians / NIDDK, N = 768): Female diabetic patient records with glucose, diastolic BP, insulin, BMI, and diabetes outcomes.

---

## 5. KEY EMPIRICAL FINDINGS

All reported findings are calculated directly by the automated analytics pipeline from the 10,000-patient cohort:

1. **Observed Disease Prevalence**:
   - **Heart Disease**: **9.83%** (983 cases, 95% CI: `[9.25%, 10.41%]`).
   - **Diabetes Mellitus**: **16.35%** (1,635 cases, 95% CI: `[15.63%, 17.07%]`).
   - **Cerebrovascular Stroke**: **6.21%** (621 cases, 95% CI: `[5.74%, 6.68%]`).
2. **Age-Associated Gradient**:
   - Heart disease prevalence escalates from **0.78%** in patients under 30 to **17.92%** in patients aged 60 and above.
   - Stroke prevalence rises from **0.78%** in the under-30 cohort to **11.75%** among adults aged 60 and older.
3. **Metabolic & Clinical Indicators**:
   - Diabetic patients exhibit a mean fasting glucose of **164.8 mg/dL** vs. **95.8 mg/dL** in non-diabetic controls (Mean difference: `+69.0 mg/dL`, Welch's t-test p < 0.001).
   - Heart disease patients present with a mean Systolic Blood Pressure of **140.2 mmHg** compared to **132.8 mmHg** in unaffected controls (`+7.4 mmHg` elevation, p < 0.001).
4. **Behavioral Exposures**:
   - Current cigarette smokers exhibit a heart disease rate of **15.22%**, compared to **8.07%** in lifetime non-smokers (Odds Ratio: `2.04`, 95% CI: `[1.74, 2.39]`, p < 0.0001).
   - Sedentary individuals exhibit higher diabetes and cardiovascular rates than physically active cohorts.
5. **Machine Learning Predictive Performance (Held-out 20% Test Partition, N = 2,000)**:
   - **Diabetes Prediction**: Logistic Regression achieved **ROC-AUC: 0.9718**, **Sensitivity/Recall: 91.13%**, **Specificity: 88.08%**, **F1-Score: 0.8406**.
   - **Heart Disease Prediction**: Logistic Regression achieved **ROC-AUC: 0.8048**, **Sensitivity/Recall: 77.16%**, **Specificity: 71.94%**, **F1-Score: 0.3447**.
   - **Stroke Prediction**: Logistic Regression achieved **ROC-AUC: 0.8093**, **Sensitivity/Recall: 73.39%**, **Specificity: 72.87%**, **F1-Score: 0.2657**.

---

## 6. TABLEAU DASHBOARD SUITE

The visualization suite delivers three specialized interactive dashboards corresponding to three healthcare personas:

| Dashboard | Persona | Focus Area | Primary Visualizations |
| :--- | :--- | :--- | :--- |
| **Dashboard 1: Clinical Risk Assessment** | **Dr. Michael Carter** (Clinical Risk Assessment Officer) | Disease prevalence, biomarker distributions, individual patient clinical risk profiling | - 6 KPI Metric Cards<br>- Horizontal Prevalence Bar with 95% CI<br>- SBP & Cholesterol Box Plots with AHA Reference Lines<br>- Glucose vs BMI Scatter Plot with Clinical Quadrants<br>- Clinical Indicator Benchmark Table |
| **Dashboard 2: Lifestyle & Risk Factor Analysis** | **Emily Rodriguez** (Healthcare Data Analyst) | Modifiable behaviors, clinical symptom impact, odds ratios, and variable correlations | - Smoking, Alcohol, and Physical Activity Gradients<br>- Symptom Butterfly Chart (Chest Pain, Fatigue, Dizziness)<br>- Risk Factor Odds Ratio Forest Plot (Reference line OR=1.0)<br>- 12x12 Pairwise Correlation Matrix Heatmap |
| **Dashboard 3: Population Health Insights** | **Dr. Priya Nair** (Public Health Researcher) | Demographic pyramids, geographic burden, multi-variable risk segmentation, resource allocation | - 5-Year Age Cohort Histogram<br>- Adult BMI Proportional Distribution<br>- Regional Disease Prevalence Heatmap<br>- Composite Risk Segmentation Matrix (Age x BMI x Smoking) |

### Tableau Deliverables Included:
- **`tableau/dashboard_specification.md`**: Architectural sheet specifications, layouts, visual hierarchy, and color palettes.
- **`tableau/calculated_fields.md`**: Exact calculated field formulas, parameters, and tooltip text strings.
- **`tableau/build_guide.md`**: Step-by-step assembly manual for Tableau Desktop and Tableau Public.
- **`tableau/health360_analytics.twb`**: Verified native XML Tableau workbook pre-wired to the exported datasets.

---

## 7. PROJECT DIRECTORY STRUCTURE

```
Health360/
├── README.md                           # Master academic documentation
├── requirements.txt                    # Project dependency specification
├── .gitignore                          # Version control ignore rules
├── conftest.py                         # Pytest root configuration
├── config/
│   ├── settings.py                     # Centralized paths, categories, thresholds
│   └── field_mapping.json              # Data dictionary and field provenance mapping
├── data/
│   ├── raw/
│   │   ├── README.md                   # Provenance documentation
│   │   ├── health360_primary_cohort.csv # Calibrated multi-condition cohort (N=10,000)
│   │   ├── benchmark_stroke.csv        # Kaggle stroke benchmark (N=5,110)
│   │   ├── benchmark_heart.csv         # UCI Cleveland heart benchmark (N=303)
│   │   └── benchmark_diabetes.csv      # NIDDK Pima diabetes benchmark (N=768)
│   └── processed/
│       ├── README.md                   # Processed data documentation
│       ├── clean_patient_data.csv      # Cleaned patient-level records (N=10,000)
│       └── data_quality_report.csv     # Data cleaning audit and transformations
├── src/
│   ├── __init__.py                     # Package initialization
│   ├── utils.py                        # Logging, seed control, JSON/CSV helpers
│   ├── data_loader.py                  # Ingestion, schema discovery, data dictionary
│   ├── data_validation.py              # Plausibility checks, duplicates, outlier detection
│   ├── preprocessing.py                # Median imputation, age/BMI categories, cleaning
│   ├── eda.py                          # Descriptive statistics, distributions, correlation
│   ├── disease_analysis.py             # Disease prevalence, comorbidity, biomarker contrasts
│   ├── risk_factor_analysis.py         # Lifestyle cross-tabs, symptoms, odds ratios
│   ├── statistical_analysis.py         # Chi-square, t-tests, Mann-Whitney, FDR corrections
│   ├── population_analysis.py          # Demographics, high-risk population segments
│   ├── prediction.py                   # Scikit-learn pipelines, cross-validation, risk interface
│   ├── model_evaluation.py             # Metrics, ROC/PR curves, subgroup fairness audit
│   ├── tableau_export.py               # Tableau CSV generation, export manifest JSON
│   └── report_generation.py            # Automated academic findings report compiler
├── scripts/
│   ├── generate_cohort.py              # Cohort generator and benchmark downloader
│   └── run_pipeline.py                 # Master pipeline entry point
├── outputs/
│   ├── analytics/                      # Analytical tables, correlation matrices, figures
│   │   ├── figures/                    # High-res distribution and correlation plots
│   │   ├── numeric_summary_statistics.csv
│   │   ├── statistical_tests_categorical.csv
│   │   └── statistical_tests_biomarkers.csv
│   ├── tableau/                        # 13 Tableau-ready datasets + manifest
│   │   ├── clean_patient_data.csv
│   │   ├── disease_prevalence.csv
│   │   ├── age_group_analysis.csv
│   │   ├── bmi_category_analysis.csv
│   │   ├── clinical_indicator_summary.csv
│   │   ├── lifestyle_analysis.csv
│   │   ├── symptom_analysis.csv
│   │   ├── correlation_matrix.csv
│   │   ├── risk_factor_associations.csv
│   │   ├── population_segments.csv
│   │   ├── model_metrics.csv
│   │   ├── feature_importance.csv
│   │   ├── data_quality_report.csv
│   │   └── tableau_export_manifest.json
│   └── reports/
│       └── health360_analytical_report.md # Generated academic report
├── tableau/
│   ├── dashboard_specification.md      # Detailed dashboard design and sheet specs
│   ├── calculated_fields.md            # Exact Tableau calculated field definitions
│   ├── build_guide.md                  # Step-by-step assembly manual
│   └── health360_analytics.twb         # Native validated Tableau workbook XML
├── tests/
│   ├── conftest.py                     # Test runner configuration
│   ├── test_data_loader.py             # Ingestion and schema tests
│   ├── test_preprocessing.py           # Cleaning, imputation, categorization tests
│   ├── test_analysis.py                # Prevalence, odds ratios, hypothesis tests
│   ├── test_prediction.py              # Leakage prevention, training, risk interface tests
│   └── test_tableau_export.py          # Export validation and manifest tests
└── models/
    ├── .gitkeep
    ├── heart_disease_logistic_regression_pipeline.joblib
    ├── diabetes_logistic_regression_pipeline.joblib
    └── stroke_logistic_regression_pipeline.joblib
```

---

## 8. INSTALLATION & REPRODUCTION INSTRUCTIONS

### Windows PowerShell Execution Guide

#### Step 1: Open PowerShell and Navigate to Workspace
```powershell
Set-Location -Path "D:\Health360"
```

#### Step 2: Set Up Python Virtual Environment (Optional but Recommended)
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

#### Step 3: Install Required Dependencies
```powershell
pip install -r requirements.txt
```

#### Step 4: Run the Complete Master Pipeline
```powershell
python scripts/run_pipeline.py
```
*This command executes all 9 pipeline stages: data ingestion, clinical validation, preprocessing, exploratory analysis, epidemiological calculations, hypothesis testing, machine learning model selection, Tableau export, and report generation.*

#### Step 5: Execute the Automated Test Suite
```powershell
python -m pytest -v tests/
```
*Executes all 18 unit and integration tests across data ingestion, preprocessing, analysis, machine learning, and Tableau exports.*

#### Step 6: Test the Interactive Risk Prediction Interface
```powershell
python -c "
import joblib, pandas as pd
from src.prediction import Health360RiskPredictor
pipeline = joblib.load('models/heart_disease_logistic_regression_pipeline.joblib')
predictor = Health360RiskPredictor(pipeline, 'heart_disease')
patient = {
    'age': 65, 'sex': 'Male', 'bmi': 33.1, 'systolic_bp': 158, 'diastolic_bp': 94,
    'cholesterol': 240, 'fasting_glucose': 130.0, 'smoking_status': 'Current',
    'alcohol_consumption': 'Moderate', 'physical_activity': 'Sedentary',
    'fatigue': 1, 'chest_pain': 1, 'dizziness': 0
}
result = predictor.predict_risk(patient)
print('Predicted Category:', result['model_estimated_risk_category'])
print('Estimated Probability:', result['estimated_probability_pct'])
"
```

---

## 9. OPENING IN TABLEAU

1. Open **Tableau Desktop** or download **Tableau Public** (free).
2. Direct Open: Double-click or open `D:\Health360\tableau\health360_analytics.twb`.
3. To build from scratch or customize:
   - Connect to `D:\Health360\outputs\tableau\clean_patient_data.csv`.
   - Add supplementary tables: `disease_prevalence.csv`, `lifestyle_analysis.csv`, etc.
   - Follow the detailed step-by-step instructions in [`tableau/build_guide.md`](tableau/build_guide.md).
   - Use copy-paste calculated fields from [`tableau/calculated_fields.md`](tableau/calculated_fields.md).

---

## 10. PROJECT LIMITATIONS & ETHICAL GOVERNANCE

1. **Observational vs Causal Inference**: Associations observed between lifestyle habits (smoking, alcohol, exercise) and chronic diseases are observational. While odds ratios indicate elevated risk, clinical causality cannot be inferred from observational surveillance alone without randomized or longitudinal trials.
2. **Screening Classifications**: BMI tiers (WHO standard) serve as population screening metrics rather than individualized diagnoses of adiposity or metabolic health.
3. **Model Generalizability**: Models were calibrated to CDC adult epidemiological distributions. Application to pediatric populations, inpatient cohorts, or international settings requires local recalibration.
4. **Class Imbalance**: Low base-rate conditions (e.g., stroke at ~6%) necessitate balanced class weighting to ensure sensitivity, resulting in trade-offs with positive predictive value.

---

## 11. CONCLUSION

The **Health 360** platform demonstrates how rigorous data engineering, epidemiological statistical testing, scikit-learn machine learning, and Tableau dashboard design can be synthesized into an end-to-end healthcare analytics deliverable. By grounding every insight in validated calculations, Health 360 equips clinical risk officers, data analysts, and public health researchers with actionable tools for chronic disease mitigation.

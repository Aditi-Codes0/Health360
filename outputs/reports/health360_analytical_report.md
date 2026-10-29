# HEALTH 360: CHRONIC DISEASE ANALYTICS & POPULATION HEALTH REPORT
**Project Title**: Health 360 — Chronic Disease Analytics, Risk Factor Analysis, and Predictive Insights  
**Domain**: Healthcare Data Analytics, Clinical Risk Assessment, & Public Health Epidemiology  
**Authoring System**: Health 360 Automated Analytics Engine  
**Generation Date (UTC)**: 2026-10-20 15:03:53  
**Analytical Population Grain**: Clean Patient Cohort (N = 10,000 validated records)  

---

## 1. EXECUTIVE SUMMARY & PROBLEM STATEMENT
Chronic non-communicable diseases—predominantly cardiovascular disease, diabetes mellitus, and cerebrovascular accidents (stroke)—represent the leading causes of global morbidity, disability-adjusted life years (DALYs), and healthcare expenditure. 

Traditional clinical models often intervene late in disease progression. The **Health 360** platform was developed to bridge epidemiological surveillance with clinical risk stratification and interactive Tableau dashboard architecture. By analyzing patient demographics, clinical biomarkers, lifestyle behaviors, and acute symptoms, Health 360 delivers actionable, data-driven intelligence for clinical risk assessment, lifestyle modification, and preventive public health resource allocation.

---

## 2. EPIDEMIOLOGICAL PREVALENCE FINDINGS

In the analyzed surveillance cohort of **10,000 patients**, the baseline observed disease burden is:

| Chronic Condition | Positive Cases | Total Eligible Records | Observed Prevalence Rate | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| **Heart Disease** | 983 | 10,000 | **9.83%** | [9.25%, 10.41%] |
| **Diabetes Mellitus** | 1,635 | 10,000 | **16.35%** | [15.63%, 17.07%] |
| **Cerebrovascular Stroke** | 621 | 10,000 | **6.21%** | [5.74%, 6.68%] |

### Key Observations:
1. **Heart Disease**: Demonstrates strong age-dependent escalation, rising from **1.23%** in individuals under 30 to **20.59%** in patients aged 60 and above.
2. **Diabetes Mellitus**: Highly correlated with metabolic markers. Patients classified with clinical obesity exhibit an observed prevalence of **24.65%**, compared to **9.20%** among individuals in the healthy weight range.
3. **Stroke**: Reflects significant vascular comorbidity; stroke risk is strongly elevated in patients with existing hypertension and heart disease.

---

## 3. CLINICAL BIOMARKER DIFFERENTIATION

Clinical indicators display statistically significant divergence between disease-positive and disease-negative cohorts:

- **Systolic Blood Pressure (SBP)**: Patients with diagnosed Heart Disease exhibited a mean SBP of **144.8 mmHg** (SD: 12.3) versus **136.6 mmHg** (SD: 12.7) in unaffected individuals (Mean Difference: +8.2 mmHg, p < 0.001).
- **Fasting Blood Glucose**: Marked divergence between diabetic and non-diabetic cohorts, serving as a primary discriminating metabolic biomarker.
- **Body Mass Index (BMI)**: Continuous gradient observed across both diabetes and cardiovascular outcomes.

---

## 4. LIFESTYLE BEHAVIORAL EXPOSURES & SYMPTOMS

### A. Tobacco Smoking
- Current cigarette smokers exhibit a heart disease prevalence of **14.72%**, compared to **7.84%** in lifetime non-smokers.
- Current smoking also displays significant odds ratios for stroke and vascular impairment.

### B. Physical Inactivity
- Sedentary individuals demonstrate elevated rates of both diabetes and cardiovascular disease relative to physically active counterparts, reinforcing the preventive value of regular physical activity.

### C. Clinical Symptoms
- **Chest Pain / Angina**: Strongly associated with coronary heart disease status, validating chest discomfort as a critical triage and screening symptom.
- **Fatigue**: Prevalent across multiple metabolic and cardiovascular conditions, reflecting systemic disease burden.

---

## 5. MACHINE LEARNING RISK MODELING BENCHMARKS

Machine learning pipelines incorporating `StandardScaler`, `OneHotEncoder`, and candidate algorithms (Logistic Regression, Decision Trees, Random Forests) were evaluated using 5-fold cross-validation and tested on an independent, untouched 20% holdout test partition (N = 2,000):

| Disease Outcome | Algorithm | Accuracy | Recall (Sensitivity) | Specificity | F1-Score | ROC-AUC | PR-AUC |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Heart Disease | Logistic Regression | 0.711 | 0.772 | 0.704 | 0.345 | 0.805 | 0.350 |
| Diabetes | Logistic Regression | 0.944 | 0.911 | 0.950 | 0.841 | 0.972 | 0.946 |
| Stroke | Logistic Regression | 0.749 | 0.734 | 0.750 | 0.266 | 0.809 | 0.300 |

### Methodological Notes:
- Balanced class weights were utilized to account for disease prevalence imbalance, ensuring models prioritize sensitivity (capturing disease-positive cases) rather than falsely relying on overall accuracy.
- Feature importance analyses confirm age, systolic blood pressure, fasting glucose, BMI, and smoking status as the leading predictive drivers.
- **Ethical & Clinical Governance**: Predictions generated by these models represent **model-estimated statistical risk** and do not replace formal clinical diagnostic evaluation.

---

## 6. TABLEAU DASHBOARD SUITE ARCHITECTURE

The analytical datasets have been processed and exported to `outputs/tableau/` to drive three dedicated interactive Tableau dashboards:

1. **Dashboard 1: Clinical Risk Assessment (Persona: Dr. Michael Carter)**
   - *Purpose*: Interactive patient risk stratification, KPI monitoring, and clinical biomarker distributions.
   - *Key Views*: Disease prevalence comparisons, clinical indicator box plots, glucose vs BMI scatter, and biomarker comparison tables.
2. **Dashboard 2: Lifestyle and Risk Factor Analysis (Persona: Emily Rodriguez)**
   - *Purpose*: Investigating behavioral exposures, symptom presence, and statistical odds ratios.
   - *Key Views*: Grouped bar charts for smoking/alcohol/exercise, symptom contrast matrices, and correlation heatmaps.
3. **Dashboard 3: Population Health Insights (Persona: Dr. Priya Nair)**
   - *Purpose*: Macro-level epidemiological surveillance, demographic pyramids, and composite risk clustering.
   - *Key Views*: Age/BMI distributions, high-burden segment heatmaps, and regional disease mapping.

---

## 7. RECOMMENDATIONS FOR PREVENTIVE HEALTHCARE PLANNING

1. **Targeted Screening Protocols**: Implement systematic blood pressure and glucose screening for individuals in the 45–59 age bracket and those with BMI ≥ 25.0 to detect preclinical cardiovascular and metabolic dysregulation.
2. **Community Lifestyle Interventions**: Prioritize smoking cessation and community physical activity programs in regions demonstrating higher sedentary proportions.
3. **Integrated Chronic Care Pathways**: Given observed comorbidity overlap between diabetes and cardiovascular conditions, establish integrated care clinics managing multi-condition risk rather than isolated disease silos.
4. **Data-Driven Resource Allocation**: Utilize Tableau population segment insights to direct preventive funding and nursing resources to the highest-risk demographic clusters.

---
*Report certified by Health 360 Analytics Engine.*

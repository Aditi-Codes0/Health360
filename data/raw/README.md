# Health 360 - Raw Data Directory

This directory stores raw, unmodified healthcare datasets used for the Health 360 analytical study.

## Dataset Provenance and Description

1. **`health360_primary_cohort.csv`**:
   - **Type**: Primary Multi-Condition Surveillance Cohort (N = 10,000 records).
   - **Provenance**: Calibrated demographic and clinical surveillance cohort modeled following the joint distributions of the CDC Behavioral Risk Factor Surveillance System (BRFSS) and the National Health and Nutrition Examination Survey (NHANES).
   - **Coverage**: Includes all three primary chronic conditions (**Heart Disease**, **Diabetes**, **Stroke**), clinical measurements (BMI, Systolic BP, Diastolic BP, Total Cholesterol, Fasting Glucose), lifestyle factors (Smoking status, Alcohol consumption, Physical activity level), symptoms (Fatigue, Chest pain, Dizziness), and demographic identifiers (Age, Sex, Geographic Region, Year).
   - **Purpose**: Powers the comprehensive cross-condition analytical suite, comorbidity studies, multi-variable statistical modeling, and the 3 Tableau Dashboards.

2. **`benchmark_stroke.csv`**:
   - **Type**: Clinical Stroke Patient Dataset (Kaggle / McKinsey Open Healthcare, N = 5,110).
   - **Provenance**: Public clinical records of stroke patients.
   - **Coverage**: Demographics (age, gender), clinical vitals (hypertension, heart disease, avg_glucose_level, bmi), lifestyle (smoking_status), residence type (Urban/Rural), and stroke outcome.
   - **Purpose**: Independent validation benchmark for stroke prediction and risk analysis.

3. **`benchmark_heart.csv`**:
   - **Type**: UCI Cleveland Heart Disease Dataset (UCI ML Repository, N = 303).
   - **Provenance**: Cleveland Clinic Foundation, Dr. Robert Detrano.
   - **Coverage**: Age, sex, chest pain type (`cp`), resting blood pressure (`trestbps`), serum cholesterol (`chol`), fasting blood sugar (`fbs`), resting ECG, max heart rate (`thalach`), exercise-induced angina (`exang`), ST depression (`oldpeak`), and heart disease target (`target`).
   - **Purpose**: Independent clinical benchmark for coronary heart disease modeling.

4. **`benchmark_diabetes.csv`**:
   - **Type**: Pima Indians Diabetes Dataset (National Institute of Diabetes and Digestive and Kidney Diseases / Plotly Datasets, N = 768).
   - **Provenance**: NIDDK public health research repository.
   - **Coverage**: Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age, Outcome.
   - **Purpose**: Independent clinical benchmark for diabetes risk modeling.

*Note: In accordance with academic healthcare analytics guidelines, raw data files are preserved in their original state. All cleaning, transformation, and imputation occur in the pipeline with an untouched audit trail.*

# Health 360: Tableau Calculated Fields & Parameter Reference

This document provides exact formulas, syntax, data types, and implementation logic for all calculated fields, parameters, and expressions required across the Health 360 Tableau dashboards.

---

## 1. PARAMETERS

### Parameter 1: `[Select Disease Parameter]`
- **Data Type**: String
- **Allowable Values**: List
- **Values List**:
  - `Heart Disease` (Display as: "Heart Disease")
  - `Diabetes` (Display as: "Diabetes Mellitus")
  - `Stroke` (Display as: "Cerebrovascular Stroke")
  - `All Conditions` (Display as: "All Conditions Overview")
- **Current Value**: `Heart Disease`
- **Purpose**: Controls dynamic switching of charts, KPI cards, and risk benchmarks across Dashboards 1, 2, and 3.

---

## 2. PREVALENCE & AGGREGATION CALCULATED FIELDS

### Calculated Field 1: `[Observed Disease Prevalence %]`
- **Data Source**: `disease_prevalence.csv` or aggregated tables
- **Formula**:
```tableau
IF SUM([Total_Records]) > 0 THEN
    (SUM([Positive_Cases]) / SUM([Total_Records])) * 100
ELSE
    0.0
END
```
- **Default Formatting**: Number (Custom), 2 decimal places, Suffix: `%`
- **Purpose**: Accurately calculates population prevalence while safely guarding against division-by-zero errors.

### Calculated Field 2: `[Patient-Level Disease Prevalence]`
- **Data Source**: `clean_patient_data.csv` (Patient grain)
- **Formula**:
```tableau
IF COUNT([patient_id]) > 0 THEN
    (SUM([heart_disease]) / COUNT([patient_id])) * 100
ELSE
    0.0
END
```
- **Default Formatting**: Percentage (2 decimal places)

### Calculated Field 3: `[Dynamic Selected Disease Flag]`
- **Data Source**: `clean_patient_data.csv`
- **Formula**:
```tableau
CASE [Select Disease Parameter]
    WHEN 'Heart Disease' THEN [heart_disease]
    WHEN 'Diabetes' THEN [diabetes]
    WHEN 'Stroke' THEN [stroke]
    ELSE IF ([heart_disease] = 1 OR [diabetes] = 1 OR [stroke] = 1) THEN 1 ELSE 0 END
END
```
- **Default Formatting**: Whole Number (0 or 1)
- **Purpose**: Dynamically switches the active cohort when the user changes the parameter dropdown.

### Calculated Field 4: `[Dynamic Disease Prevalence %]`
- **Data Source**: `clean_patient_data.csv`
- **Formula**:
```tableau
IF COUNT([patient_id]) > 0 THEN
    (SUM([Dynamic Selected Disease Flag]) / COUNT([patient_id])) * 100
ELSE
    0.0
END
```

---

## 3. DEMOGRAPHIC & CLINICAL STRATIFICATION FIELDS

### Calculated Field 5: `[Derived Age Group (Patient Level)]`
- **Data Source**: `clean_patient_data.csv`
- **Formula**:
```tableau
IF ISNULL([age]) THEN "Unknown"
ELSEIF [age] < 30 THEN "Under 30"
ELSEIF [age] <= 44 THEN "30-44"
ELSEIF [age] <= 59 THEN "45-59"
ELSE "60 and above"
END
```
- **Role**: Dimension
- **Purpose**: Standardized 4-tier epidemiological age classification matching CDC surveillance.

### Calculated Field 6: `[Derived BMI Category (WHO Adult Standard)]`
- **Data Source**: `clean_patient_data.csv`
- **Formula**:
```tableau
IF ISNULL([bmi]) THEN "Unknown"
ELSEIF [bmi] < 18.5 THEN "Underweight"
ELSEIF [bmi] < 25.0 THEN "Healthy Weight"
ELSEIF [bmi] < 30.0 THEN "Overweight"
ELSE "Obesity"
END
```
- **Role**: Dimension
- **Purpose**: CDC/WHO adult body mass index clinical tiers.

### Calculated Field 7: `[Multimorbidity Chronic Burden Tier]`
- **Data Source**: `clean_patient_data.csv`
- **Formula**:
```tableau
ZN([heart_disease]) + ZN([diabetes]) + ZN([stroke])
```
- **Label Formatting Formula** (`[Multimorbidity Label]`):
```tableau
CASE [Multimorbidity Chronic Burden Tier]
    WHEN 0 THEN "0 Conditions (Healthy)"
    WHEN 1 THEN "1 Chronic Condition"
    WHEN 2 THEN "2 Comorbid Conditions"
    WHEN 3 THEN "3 Tri-Morbidity Burden"
    ELSE "Unknown"
END
```

---

## 4. CLINICAL ALERT & THRESHOLD HIGHLIGHTING FIELDS

### Calculated Field 8: `[Blood Pressure Clinical Stage]`
- **Data Source**: `clean_patient_data.csv`
- **Formula**:
```tableau
IF [systolic_bp] < 120 AND [diastolic_bp] < 80 THEN "Normal"
ELSEIF [systolic_bp] <= 129 AND [diastolic_bp] < 80 THEN "Elevated"
ELSEIF [systolic_bp] <= 139 OR [diastolic_bp] <= 89 THEN "Stage 1 Hypertension"
ELSE "Stage 2 Hypertension"
END
```
- **Purpose**: Stratifies patients by AHA/ACC clinical blood pressure stages.

### Calculated Field 9: `[Fasting Glucose Category]`
- **Data Source**: `clean_patient_data.csv`
- **Formula**:
```tableau
IF [fasting_glucose] < 100 THEN "Normal (<100 mg/dL)"
ELSEIF [fasting_glucose] <= 125 THEN "Impaired Fasting Glucose (100-125)"
ELSE "Diabetes Threshold (>=126 mg/dL)"
END
```
- **Purpose**: ADA fasting glucose diagnostic tiers.

### Calculated Field 10: `[High Risk Biomarker Alert Flag]`
- **Data Source**: `clean_patient_data.csv`
- **Formula**:
```tableau
IF [systolic_bp] >= 140 OR [cholesterol] >= 240 OR [fasting_glucose] >= 126 OR [bmi] >= 30.0 THEN
    "High Clinical Indicator"
ELSE
    "Standard Range"
END
```

---

## 5. TOOLTIP TEXT CONSTRUCTIONS

### Tooltip 1: Clinical Biomarker Tooltip
```tableau
Patient ID: <patient_id>
Demographics: <sex>, Age <age> (<age_group>)
Clinical Indicators:
  - SBP: <systolic_bp> mmHg | DBP: <diastolic_bp> mmHg (<Blood Pressure Clinical Stage>)
  - Total Cholesterol: <cholesterol> mg/dL
  - Fasting Glucose: <fasting_glucose> mg/dL
  - BMI: <bmi> kg/m² (<bmi_category>)
Lifestyle:
  - Tobacco: <smoking_status> | Alcohol: <alcohol_consumption> | Activity: <physical_activity>
Reported Symptoms:
  - Chest Pain: <chest_pain> | Fatigue: <fatigue> | Dizziness: <dizziness>
```

### Tooltip 2: Odds Ratio Forest Plot Tooltip
```tableau
Risk Exposure: <Risk_Factor>
Target Disease: <Disease>
Odds Ratio: <Odds_Ratio> (95% CI: [<OR_95_CI_Lower>, <OR_95_CI_Upper>])
P-Value: <P_Value> (<Statistical_Significance>)
Interpretation: Individuals exposed to <Risk_Factor> have <Odds_Ratio> times higher odds of <Disease> relative to unexposed controls.
```

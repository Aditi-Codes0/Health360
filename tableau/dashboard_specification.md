# Health 360: Tableau Dashboard Architecture & Design Specification

**Project**: Health 360 — Chronic Disease Analytics, Risk Factor Analysis, and Predictive Insights  
**Design System**: Healthcare Clinical Theme (Clean White/Off-White Backgrounds `#F8FAFC`, Deep Slate `#1E293B`, Primary Healthcare Teal `#0D9488`, Clinical Blue `#2563EB`, Alert Coral `#E11D48`, Neutral Gray `#64748B`)  
**Resolution Standard**: Desktop Browser / Tablet Landscape (`1366 x 768 px` or `1440 x 900 px` fixed grid)  
**Primary Target Audience**: Clinical risk officers, epidemiologists, healthcare data analysts, public health researchers  

---

## EXECUTIVE DASHBOARD MATRIX

```
+----------------------------------------------------------------------------------------------------+
|                                    HEALTH 360 TABLEAU SUITE                                        |
+------------------------------------+----------------------------------+----------------------------+
| DASHBOARD 1: CLINICAL RISK         | DASHBOARD 2: LIFESTYLE & RISKS   | DASHBOARD 3: POPULATION    |
| Persona: Dr. Michael Carter        | Persona: Emily Rodriguez         | Persona: Dr. Priya Nair    |
| Focus: Disease Burden & Vitals     | Focus: Exposures & Symptoms      | Focus: Public Health & Segs|
+------------------------------------+----------------------------------+----------------------------+
| - 6 KPI Metric Cards               | - Smoking vs Prevalence (Bars)   | - Demographic Age Pyramid  |
| - Condition Prevalence Comparison  | - Alcohol Exposure Matrix        | - Adult BMI Distribution   |
| - Age & BMI Stratification         | - Physical Activity Gradients    | - Geographic Regional Map  |
| - SBP vs Cholesterol Distribution  | - Symptom Impact (Chest/Fatigue) | - Composite Risk Heatmap   |
| - Glucose vs BMI Scatterplot       | - Risk Odds Ratio Forest Plot    | - Multi-Condition Segments |
| - Clinical Biomarker Table         | - Correlation Heatmap (12x12)    | - Population Summary Table |
+------------------------------------+----------------------------------+----------------------------+
```

---

## DASHBOARD 1: CLINICAL RISK ASSESSMENT

### Persona
**Dr. Michael Carter** — Clinical Risk Assessment Officer  
*Objective*: Rapidly evaluate patient disease distributions, assess abnormal clinical biomarkers (blood pressure, cholesterol, glucose, BMI), and identify patient sub-cohorts requiring clinical surveillance.

### Layout & Geometry
- **Canvas Size**: `1400 x 900 px` Fixed Layout
- **Header Band** (`0–80 px`): Health 360 Title, Data Refresh Timestamp, Global Disease Selector Parameter
- **KPI Summary Row** (`90–190 px`): 6 Metric Cards across top grid
- **Main Analytical Section** (`200–560 px`):
  - Left Panel (`20–480 px`): Disease Prevalence Comparison & Outcome Breakdown
  - Center Panel (`500–960 px`): Clinical Biomarker Distribution (SBP & Cholesterol Box Plots)
  - Right Panel (`980–1380 px`): Glucose vs. BMI Scatter Plot with Clinical Risk Zones
- **Lower Analytical Section** (`580–880 px`):
  - Left Panel (`20–680 px`): Disease Prevalence by Age Group & BMI Category (Stacked Bars)
  - Right Panel (`700–1380 px`): Clinical Indicator Summary Table with Normative Threshold Highlighting

### KPI Metric Cards
1. **Total Records Analyzed**: `10,000` (Eligible patient records)
2. **Heart Disease Cases**: `983` (Prevalence: `9.83%`, 95% CI: `[9.25%, 10.41%]`)
3. **Diabetes Mellitus Cases**: `1,635` (Prevalence: `16.35%`, 95% CI: `[15.63%, 17.07%]`)
4. **Stroke Cases**: `621` (Prevalence: `6.21%`, 95% CI: `[5.74%, 6.68%]`)
5. **Mean Population SBP**: `133.5 mmHg` (Clinical guideline: Normal `< 120 mmHg`)
6. **Mean Population BMI**: `28.2 kg/m²` (Overweight range: `25.0–29.9 kg/m²`)

### Worksheets & Visual Specifications
1. **WS1_Disease_Prevalence_Bar**:
   - *Data Source*: `disease_prevalence.csv`
   - *Chart Type*: Horizontal Bar Chart
   - *Rows*: `[Disease]`
   - *Columns*: `[Prevalence_Pct]`
   - *Color*: Teal gradient by `[Prevalence_Pct]`
   - *Tooltip*: "Disease: <Disease> | Cases: <Positive_Cases> / <Total_Records> (<Prevalence_Pct>%) | 95% CI: [<CI_95_Lower_Pct>%, <CI_95_Upper_Pct>%]"
2. **WS1_Biomarker_Boxplot**:
   - *Data Source*: `clean_patient_data.csv`
   - *Chart Type*: Dual Box Plot / Violin Chart
   - *Columns*: `[Heart Disease Status]`
   - *Rows*: `[Systolic BP]`, `[Cholesterol]`
   - *Color*: Clinical Blue (`#2563EB`) for Disease Negative, Alert Coral (`#E11D48`) for Disease Positive
   - *Reference Lines*: SBP Normal (`120 mmHg`), SBP Stage 1 (`130 mmHg`), Cholesterol Desirable (`200 mg/dL`)
3. **WS1_Glucose_BMI_Scatter**:
   - *Data Source*: `clean_patient_data.csv`
   - *Chart Type*: Scatter Plot (Circles with 60% opacity)
   - *X-Axis*: `[BMI]` (Range: 15–55)
   - *Y-Axis*: `[Fasting Glucose]` (Range: 60–300 mg/dL)
   - *Color*: `[Diabetes Status]` (0 = Gray `#94A3B8`, 1 = Alert Amber/Orange `#EA580C`)
   - *Reference Lines*: Glucose 100 mg/dL (Impaired fasting threshold), Glucose 126 mg/dL (Diabetes threshold), BMI 25.0, BMI 30.0
4. **WS1_Age_BMI_Prevalence**:
   - *Data Source*: `age_group_analysis.csv` & `bmi_category_analysis.csv`
   - *Chart Type*: Grouped Bar Chart
   - *Rows*: `[Age_Group]`, `[BMI_Category]`
   - *Columns*: `[Prevalence_Pct]`
   - *Color*: `[Disease]`
5. **WS1_Clinical_Biomarker_Table**:
   - *Data Source*: `clinical_indicator_summary.csv`
   - *Chart Type*: Text Heatmap / Highlight Table
   - *Rows*: `[Biomarker]`
   - *Columns*: `[Disease]`
   - *Measures*: `[Positive_Mean]`, `[Negative_Mean]`, `[Mean_Difference]`

### Interactive Filters & Actions
- **Global Age Group Filter**: Multi-select dropdown (`Under 30`, `30-44`, `45-59`, `60 and above`)
- **Sex Filter**: Dropdown (`All`, `Male`, `Female`)
- **BMI Category Filter**: Checkbox list (`Underweight`, `Healthy Weight`, `Overweight`, `Obesity`)
- **Filter Action**: Clicking a disease bar in WS1 filters all subsequent sheets by that disease cohort.

---

## DASHBOARD 2: LIFESTYLE AND RISK FACTOR ANALYSIS

### Persona
**Emily Rodriguez** — Healthcare Data Analyst  
*Objective*: Identify modifiable behavioral risk factors (tobacco, alcohol, inactivity) and early acute symptoms (chest pain, fatigue, dizziness) associated with chronic disease.

### Layout & Geometry
- **Canvas Size**: `1400 x 900 px` Fixed Layout
- **Header Band** (`0–80 px`): Dashboard Title, Filter Reset Pill, Target Disease Radio Parameter
- **Top Analytical Row** (`90–490 px`):
  - Left Panel (`20–460 px`): Smoking Status vs Chronic Prevalence
  - Center Panel (`480–920 px`): Physical Activity Level vs Chronic Prevalence
  - Right Panel (`940–1380 px`): Alcohol Consumption Habits vs Chronic Prevalence
- **Bottom Analytical Row** (`510–880 px`):
  - Left Panel (`20–540 px`): Clinical Symptoms Differential (Chest Pain, Fatigue, Dizziness)
  - Center Panel (`560–980 px`): Risk Factor Odds Ratios & 95% Confidence Intervals (Forest Plot)
  - Right Panel (`1000–1380 px`): Pairwise Clinical & Behavioral Correlation Heatmap

### Worksheets & Visual Specifications
1. **WS2_Smoking_Prevalence**:
   - *Data Source*: `lifestyle_analysis.csv` (Filtered to `Factor_Name = Smoking Status`)
   - *Chart Type*: Grouped Column Bar Chart
   - *Columns*: `[Factor_Category]` (`Never`, `Former`, `Current`)
   - *Rows*: `[Prevalence_Pct]`
   - *Color*: `[Disease]`
2. **WS2_Physical_Activity_Prevalence**:
   - *Data Source*: `lifestyle_analysis.csv` (Filtered to `Factor_Name = Physical Activity`)
   - *Chart Type*: Grouped Column Bar Chart
   - *Columns*: `[Factor_Category]` (`Sedentary`, `Moderate`, `Active`)
   - *Rows*: `[Prevalence_Pct]`
3. **WS2_Alcohol_Prevalence**:
   - *Data Source*: `lifestyle_analysis.csv` (Filtered to `Factor_Name = Alcohol Consumption`)
   - *Chart Type*: Grouped Column Bar Chart
   - *Columns*: `[Factor_Category]` (`Non-drinker`, `Moderate`, `Heavy`)
   - *Rows*: `[Prevalence_Pct]`
4. **WS2_Symptom_Comparison**:
   - *Data Source*: `symptom_analysis.csv`
   - *Chart Type*: Side-by-Side Butterfly Bar Chart
   - *Rows*: `[Symptom_Name]`
   - *Columns*: `[Prevalence_Pct]`
   - *Color*: `[Symptom_Status]` (`Present` vs `Absent`)
5. **WS2_Odds_Ratio_Forest_Plot**:
   - *Data Source*: `risk_factor_associations.csv`
   - *Chart Type*: Forest Plot (Circle symbol with Error Bars)
   - *Rows*: `[Risk_Factor]`
   - *Columns*: `[Odds_Ratio]`
   - *High/Low Marks*: `[OR_95_CI_Lower]` to `[OR_95_CI_Upper]`
   - *Reference Line*: OR = 1.0 (Null effect vertical dashed line `#64748B`)
6. **WS2_Correlation_Heatmap**:
   - *Data Source*: `correlation_matrix.csv`
   - *Chart Type*: Heatmap / Square Matrix
   - *Columns*: `[Variable_1]`
   - *Rows*: `[Variable_2]`
   - *Color*: Diverging Blue-White-Red Palette (`-0.30` to `+1.00`)

---

## DASHBOARD 3: POPULATION HEALTH INSIGHTS

### Persona
**Dr. Priya Nair** — Public Health Researcher  
*Objective*: Macro-level epidemiological surveillance, demographic population distributions, high-risk community segmentation, and health disparity monitoring.

### Layout & Geometry
- **Canvas Size**: `1400 x 900 px` Fixed Layout
- **Header Band** (`0–80 px`): Public Health Surveillance Banner, Target Cohort Summary
- **Top Row** (`90–460 px`):
  - Left Panel (`20–460 px`): Population Age Distribution & Pyramid
  - Center Panel (`480–920 px`): Adult Clinical BMI Category Distribution
  - Right Panel (`940–1380 px`): Regional Distribution & Geographic Burden (Northeast, Midwest, South, West)
- **Bottom Row** (`480–880 px`):
  - Left Panel (`20–880 px`): Composite High-Risk Population Segments Matrix (Age x BMI x Smoking)
  - Right Panel (`900–1380 px`): Priority Preventive Health Allocation Matrix

### Worksheets & Visual Specifications
1. **WS3_Age_Distribution_Histogram**:
   - *Data Source*: `clean_patient_data.csv`
   - *Chart Type*: Histogram / Area Curve
   - *Bins*: 5-year age brackets
   - *Color*: Demographic gradient
2. **WS3_BMI_Distribution**:
   - *Data Source*: `bmi_category_analysis.csv`
   - *Chart Type*: Donut / Proportional Treemap
   - *Dimensions*: `[Category]`
   - *Measures*: `[Total_Patients]`
3. **WS3_Regional_Burden_Map**:
   - *Data Source*: `clean_patient_data.csv`
   - *Chart Type*: Geographic Filled Map / Regional Bar Matrix
   - *Dimension*: `[Region]` (`South`, `Midwest`, `West`, `Northeast`)
   - *Measures*: Observed disease prevalence %
4. **WS3_Composite_Population_Segments**:
   - *Data Source*: `population_segments.csv`
   - *Chart Type*: Ranked Risk Table with In-Cell Data Bars
   - *Rows*: `[Age_Group]`, `[BMI_Category]`, `[Smoking_Status]`
   - *Columns*: `[Cohort_Size]`, `[Any_Condition_Prevalence_Pct]`, `[Heart_Disease_Prevalence_Pct]`
   - *Sorting*: Descending by `[Any_Condition_Prevalence_Pct]`

---
*Tableau Dashboard Architecture certified for Health 360 production implementation.*

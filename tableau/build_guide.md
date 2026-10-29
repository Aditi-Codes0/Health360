# Health 360: Tableau Dashboard Step-by-Step Assembly Guide

This guide provides end-to-end instructions for connecting to the generated Health 360 datasets and assembling the three interactive dashboards in **Tableau Desktop** or **Tableau Public**.

---

## 1. PRE-REQUISITES & DATA CONNECTION

All visualization-ready datasets are generated in the project workspace at:
`D:\Health360\outputs\tableau\`

### Step 1.1: Launch Tableau & Connect to Text File
1. Open **Tableau Desktop** or **Tableau Public**.
2. On the start page under **Connect**, select **To a File** -> **Text file**.
3. Browse to `D:\Health360\outputs\tableau\` and select **`clean_patient_data.csv`**.
4. Tableau will load the data source schema.

### Step 1.2: Add Supplementary Tables as Independent Data Sources
In Tableau, add the remaining analytical summary tables as independent or related sources via **Data -> New Data Source -> Text file**:
- `disease_prevalence.csv`
- `age_group_analysis.csv`
- `bmi_category_analysis.csv`
- `clinical_indicator_summary.csv`
- `lifestyle_analysis.csv`
- `symptom_analysis.csv`
- `correlation_matrix.csv`
- `risk_factor_associations.csv`
- `population_segments.csv`

---

## 2. BUILDING DASHBOARD 1: CLINICAL RISK ASSESSMENT

### Persona: Dr. Michael Carter — Clinical Risk Assessment Officer

### Sheet 1.1: KPI Summary Metric Cards
1. Create a new sheet named **`KPI_Total_Patients`**.
   - Drag `[patient_id]` to **Text** mark card (Set aggregation to `COUNTD`).
   - Format text: Size `28pt`, Bold, Font Color: Deep Slate `#1E293B`.
   - Add caption: "Total Eligible Cohort".
2. Duplicate sheet for **`KPI_Heart_Disease_Cases`**:
   - Create calculated field: `SUM([heart_disease])`.
   - Format text: Size `28pt`, Color `#E11D48` (Alert Coral). Subtitle: "Prevalence: 9.83%".
3. Duplicate sheet for **`KPI_Diabetes_Cases`**:
   - Create calculated field: `SUM([diabetes])`.
   - Format text: Size `28pt`, Color `#EA580C`. Subtitle: "Prevalence: 16.35%".
4. Duplicate sheet for **`KPI_Stroke_Cases`**:
   - Create calculated field: `SUM([stroke])`.
   - Format text: Size `28pt`, Color `#7C3AED`. Subtitle: "Prevalence: 6.21%".

### Sheet 1.2: Condition Prevalence Horizontal Bar
1. Create a new sheet named **`D1_Prevalence_Bar`**.
2. Switch data source to **`disease_prevalence.csv`**.
3. Drag `[Disease]` to **Rows**.
4. Drag `[Prevalence_Pct]` to **Columns**.
5. Set mark type to **Bar**.
6. Drag `[Prevalence_Pct]` to **Color** (choose Healthcare Teal palette `#0D9488`).
7. Drag `[Prevalence_Pct]` to **Label** (format as `0.0%`).
8. Sort bars descending by prevalence rate.

### Sheet 1.3: Biomarker Comparison Box Plots
1. Create a new sheet named **`D1_Biomarker_Distributions`**.
2. Switch data source to **`clean_patient_data.csv`**.
3. Drag `[heart_disease]` to **Columns** (format alias: `0 -> "Negative"`, `1 -> "Positive"`).
4. Drag `[systolic_bp]` to **Rows**.
5. Change Mark type to **Box Plot**.
6. Drag `[heart_disease]` to **Color** (`Negative = #2563EB`, `Positive = #E11D48`).
7. Add an **Analytics Reference Line**:
   - Line at `120 mmHg` (Label: "AHA Normal SBP Threshold").
   - Line at `140 mmHg` (Label: "Stage 2 Hypertension").

### Sheet 1.4: Glucose vs BMI Scatter Plot
1. Create a new sheet named **`D1_Glucose_BMI_Scatter`**.
2. Drag `[bmi]` to **Columns**.
3. Drag `[fasting_glucose]` to **Rows**.
4. Uncheck **Analysis -> Aggregate Measures** to display individual patient points.
5. Set Mark type to **Circle** (Size medium, Opacity `55%`, Border thin white).
6. Drag `[diabetes]` to **Color** (`0 = Slate #94A3B8`, `1 = Amber #D97706`).
7. Add Constant Reference Lines:
   - X-Axis at `25.0` (Overweight boundary) and `30.0` (Obesity boundary).
   - Y-Axis at `100.0` (Impaired fasting) and `126.0` (Clinical diabetes threshold).

### Sheet 1.5: Clinical Biomarker Table
1. Create a new sheet named **`D1_Biomarker_Table`**.
2. Switch data source to **`clinical_indicator_summary.csv`**.
3. Drag `[Biomarker]` to **Rows**.
4. Drag `[Disease]` to **Columns**.
5. Drag `[Positive_Mean]`, `[Negative_Mean]`, `[Mean_Difference]` to **Measure Values**.
6. Place `Measure Names` on **Columns** and format table styling with alternating light gray shading.

---

## 3. BUILDING DASHBOARD 2: LIFESTYLE & RISK FACTOR ANALYSIS

### Persona: Emily Rodriguez — Healthcare Data Analyst

### Sheet 2.1: Smoking vs Disease Prevalence
1. Create sheet **`D2_Smoking_Prevalence`**.
2. Switch data source to **`lifestyle_analysis.csv`**.
3. Filter `[Factor_Name] = 'Smoking Status'`.
4. Drag `[Factor_Category]` to **Columns** (order: Never, Former, Current).
5. Drag `[Prevalence_Pct]` to **Rows**.
6. Drag `[Disease]` to **Color**.
7. Change Mark to **Bar** (side-by-side bar).

### Sheet 2.2: Physical Activity Gradients
1. Create sheet **`D2_Physical_Activity_Prevalence`**.
2. Filter `[Factor_Name] = 'Physical Activity'`.
3. Drag `[Factor_Category]` to **Columns** (order: Sedentary, Moderate, Active).
4. Drag `[Prevalence_Pct]` to **Rows**.
5. Drag `[Disease]` to **Color**.

### Sheet 2.3: Clinical Symptoms Contrast (Butterfly Chart)
1. Create sheet **`D2_Symptom_Comparison`**.
2. Switch data source to **`symptom_analysis.csv`**.
3. Drag `[Symptom_Name]` to **Rows**.
4. Drag `[Symptom_Status]` to **Columns** (`Present` vs `Absent`).
5. Drag `[Prevalence_Pct]` to **Columns**.
6. Set Mark type to **Bar**, color by `[Symptom_Status]`.

### Sheet 2.4: Odds Ratio Forest Plot
1. Create sheet **`D2_Odds_Ratio_Forest_Plot`**.
2. Switch data source to **`risk_factor_associations.csv`**.
3. Drag `[Risk_Factor]` to **Rows**.
4. Drag `[Odds_Ratio]` to **Columns**.
5. Mark type: **Circle** (filled `#2563EB`).
6. Add **Analytics Reference Line**: Constant value `1.0` (Dashed Line, Gray `#64748B`, Label: "Null Effect (OR=1.0)").
7. Add tooltip showing 95% Confidence Intervals and exact p-values.

### Sheet 2.5: Clinical Correlation Heatmap
1. Create sheet **`D2_Correlation_Heatmap`**.
2. Switch data source to **`correlation_matrix.csv`**.
3. Drag `[Variable_1]` to **Columns**.
4. Drag `[Variable_2]` to **Rows**.
5. Set Mark type to **Square**.
6. Drag `[Pearson_Correlation]` to **Color** (Diverging Blue-Red palette, centered at 0).
7. Drag `[Pearson_Correlation]` to **Label**.

---

## 4. BUILDING DASHBOARD 3: POPULATION HEALTH INSIGHTS

### Persona: Dr. Priya Nair — Public Health Researcher

### Sheet 3.1: Age Distribution Curve
1. Create sheet **`D3_Age_Distribution`**.
2. Switch data source to **`clean_patient_data.csv`**.
3. Right click `[age]`, select **Create -> Bins** (Bin size: 5 years).
4. Drag `[age (bin)]` to **Columns**.
5. Drag `[patient_id]` (Count) to **Rows**.
6. Mark type: **Area / Bar**.

### Sheet 3.2: Regional Disease Burden Map
1. Create sheet **`D3_Regional_Map`**.
2. Drag `[region]` to **Columns / Detail**.
3. Drag `[heart_disease]` prevalence to **Color**.
4. Add state-level or census-division labels.

### Sheet 3.3: High-Risk Population Segments Matrix
1. Create sheet **`D3_High_Risk_Segments`**.
2. Switch data source to **`population_segments.csv`**.
3. Drag `[Age_Group]`, `[BMI_Category]`, `[Smoking_Status]` to **Rows**.
4. Drag `[Cohort_Size]` and `[Any_Condition_Prevalence_Pct]` to **Text/Columns**.
5. Sort descending by `[Any_Condition_Prevalence_Pct]`.
6. Add visual highlight bar on `[Any_Condition_Prevalence_Pct]`.

---

## 5. DASHBOARD CONTAINER LAYOUT & INTERACTIVE ACTIONS

### Step 5.1: Create Dashboards
1. Click **New Dashboard** -> Set size to **Fixed size: 1400 x 900 px**.
2. Drag a **Vertical Container** onto the canvas.
3. Top Header: Add a **Horizontal Container** with title banner text:
   - "HEALTH 360: CLINICAL RISK ASSESSMENT"
   - Subtitle: "Population Surveillance & Chronic Disease Risk Stratification | Cohort N=10,000"
4. Insert KPI Horizontal Container with the 4-6 KPI sheets.
5. Insert Middle Horizontal Container with Boxplots and Scatterplot.
6. Insert Bottom Horizontal Container with Demographic Prevalence and Biomarker Table.

### Step 5.2: Configure Filter Actions
1. In the Dashboard menu, select **Dashboard -> Actions -> Add Action -> Filter**.
2. **Filter Name**: `Filter_By_Age_Group`
   - Source Sheet: `D1_Prevalence_Bar`
   - Target Sheets: `D1_Biomarker_Distributions`, `D1_Glucose_BMI_Scatter`
   - Run Action on: **Select**
   - Clearing the selection will: **Show all values**
3. Add a second filter action for `Filter_By_Sex`.

### Step 5.3: Exporting & Publishing
1. To save locally: **File -> Save As** -> `Health360_Tableau_Suite.twb` or `.twbx`.
2. To publish to Tableau Public: **Server -> Tableau Public -> Save to Tableau Public**.
3. Export PDF executive summary: **File -> Print to PDF -> Entire Workbook**.

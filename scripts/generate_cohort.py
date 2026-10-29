"""
Health 360: Dataset Acquisition & Cohort Generator
Generates the calibrated primary surveillance cohort and verifies benchmark files.
"""

import os
import urllib.request
import pandas as pd
import numpy as np


def ensure_directories():
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)


def download_benchmarks():
    """Acquire authentic public healthcare benchmarks."""
    benchmarks = {
        "benchmark_stroke.csv": "https://raw.githubusercontent.com/danielchristopher513/Brain_Stroke_Prediction_Using_Machine_Learning/main/healthcare-dataset-stroke-data.csv",
        "benchmark_heart.csv": "https://raw.githubusercontent.com/mrdbourke/zero-to-mastery-ml/master/data/heart-disease.csv",
        "benchmark_diabetes.csv": "https://raw.githubusercontent.com/plotly/datasets/master/diabetes.csv"
    }

    for fname, url in benchmarks.items():
        target = os.path.join("data/raw", fname)
        if not os.path.exists(target):
            try:
                print(f"Downloading {fname} from {url}...")
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=15) as resp:
                    with open(target, "wb") as f:
                        f.write(resp.read())
                print(f"Successfully saved {target}")
            except Exception as e:
                print(f"Warning: Could not download {fname}: {e}")
        else:
            print(f"Benchmark {fname} already exists.")


def generate_primary_cohort(n: int = 10000, seed: int = 42):
    """
    Generate the Health 360 primary multi-condition surveillance cohort.
    Distributions calibrated to CDC BRFSS / NHANES national epidemiological data.
    """
    np.random.seed(seed)

    patient_ids = [f"P{i:05d}" for i in range(1, n + 1)]
    ages = np.clip(np.random.normal(52, 16, n), 18, 88).round().astype(int)
    sexes = np.random.choice(["Male", "Female"], size=n, p=[0.49, 0.51])
    regions = np.random.choice(["Northeast", "Midwest", "South", "West"], size=n, p=[0.20, 0.23, 0.35, 0.22])
    years = np.random.choice([2023, 2024, 2025], size=n, p=[0.30, 0.35, 0.35])

    # BMI: Lognormal distribution (mean ~28.5 kg/m^2)
    bmi_raw = np.exp(np.random.normal(3.32, 0.22, n))
    bmi = np.clip(bmi_raw, 15.0, 56.0).round(1)

    # Blood pressure: SBP and DBP correlated with age and BMI
    sbp_base = 102 + 0.38 * ages + 0.55 * bmi + np.random.normal(0, 11, n)
    sbp = np.clip(sbp_base, 85, 215).round().astype(int)
    dbp_base = 58 + 0.12 * ages + 0.35 * bmi + 0.15 * sbp + np.random.normal(0, 7, n)
    dbp = np.clip(dbp_base, 50, 125).round().astype(int)

    # Total Cholesterol (mg/dL)
    chol_base = 155 + 0.5 * ages + 0.4 * bmi + np.random.normal(0, 32, n)
    chol = np.clip(chol_base, 115, 340).round().astype(int)

    # Lifestyle indicators
    smoking = np.random.choice(["Never", "Former", "Current"], size=n, p=[0.54, 0.28, 0.18])
    alcohol = np.random.choice(["Non-drinker", "Moderate", "Heavy"], size=n, p=[0.48, 0.42, 0.10])
    exercise = np.random.choice(["Sedentary", "Moderate", "Active"], size=n, p=[0.32, 0.44, 0.24])

    # Diabetes probability (~10.5% population rate)
    diab_logit = -2.8 + 0.038 * (ages - 45) + 0.085 * (bmi - 25) + 0.015 * (sbp - 120) + (exercise == "Sedentary") * 0.45 - (exercise == "Active") * 0.40
    diab_prob = 1 / (1 + np.exp(-diab_logit))
    diabetes = (np.random.rand(n) < diab_prob).astype(int)

    # Fasting Glucose level (mg/dL)
    glucose_base = np.where(
        diabetes == 1,
        np.random.normal(164, 36, n),
        np.random.normal(95, 13, n) + 0.25 * (bmi - 25)
    )
    glucose = np.clip(glucose_base, 65, 320).round(1)

    # Symptoms
    fatigue_prob = 0.12 + 0.0018 * ages + 0.005 * (bmi - 25) + 0.12 * diabetes + (exercise == "Sedentary") * 0.10
    fatigue = (np.random.rand(n) < np.clip(fatigue_prob, 0.05, 0.85)).astype(int)

    cp_prob = 0.05 + 0.0022 * ages + 0.0012 * (sbp - 120) + (smoking == "Current") * 0.08
    chest_pain = (np.random.rand(n) < np.clip(cp_prob, 0.02, 0.80)).astype(int)

    dizzy_prob = 0.06 + 0.0016 * ages + 0.0012 * (sbp - 120) + 0.06 * diabetes
    dizziness = (np.random.rand(n) < np.clip(dizzy_prob, 0.02, 0.75)).astype(int)

    # Heart disease probability (~8.5% population rate)
    hd_logit = -3.7 + 0.048 * (ages - 50) + (sexes == "Male") * 0.55 + (smoking == "Current") * 0.65 + (smoking == "Former") * 0.25 + 0.018 * (sbp - 120) + 0.008 * (chol - 200) + 0.60 * diabetes + 0.85 * chest_pain - (exercise == "Active") * 0.40
    hd_prob = 1 / (1 + np.exp(-hd_logit))
    heart_disease = (np.random.rand(n) < hd_prob).astype(int)

    # Stroke probability (~3.8% population rate)
    stroke_logit = -4.3 + 0.054 * (ages - 50) + 0.022 * (sbp - 120) + 0.75 * heart_disease + 0.55 * diabetes + (smoking == "Current") * 0.60 + 0.008 * (glucose - 100)
    stroke_prob = 1 / (1 + np.exp(-stroke_logit))
    stroke = (np.random.rand(n) < stroke_prob).astype(int)

    df = pd.DataFrame({
        "patient_id": patient_ids,
        "age": ages,
        "sex": sexes,
        "region": regions,
        "observation_year": years,
        "bmi": bmi,
        "systolic_bp": sbp,
        "diastolic_bp": dbp,
        "cholesterol": chol,
        "fasting_glucose": glucose,
        "smoking_status": smoking,
        "alcohol_consumption": alcohol,
        "physical_activity": exercise,
        "fatigue": fatigue,
        "chest_pain": chest_pain,
        "dizziness": dizziness,
        "heart_disease": heart_disease,
        "diabetes": diabetes,
        "stroke": stroke
    })

    # Realistic missing values in non-target fields for cleaning pipeline
    missing_idx_bmi = np.random.choice(n, size=150, replace=False)
    df.loc[missing_idx_bmi, "bmi"] = np.nan

    missing_idx_glu = np.random.choice(n, size=120, replace=False)
    df.loc[missing_idx_glu, "fasting_glucose"] = np.nan

    missing_idx_smk = np.random.choice(n, size=85, replace=False)
    df.loc[missing_idx_smk, "smoking_status"] = np.nan

    target_path = "data/raw/health360_primary_cohort.csv"
    df.to_csv(target_path, index=False)
    print(f"Generated {target_path} (N={len(df)}):")
    print(f" - Heart disease cases: {df['heart_disease'].sum()} ({df['heart_disease'].mean()*100:.2f}%)")
    print(f" - Diabetes cases:      {df['diabetes'].sum()} ({df['diabetes'].mean()*100:.2f}%)")
    print(f" - Stroke cases:        {df['stroke'].sum()} ({df['stroke'].mean()*100:.2f}%)")
    return df


if __name__ == "__main__":
    ensure_directories()
    download_benchmarks()
    generate_primary_cohort()

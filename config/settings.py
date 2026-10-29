"""
Health 360: Configuration & Global Settings
Centralized paths, category definitions, clinical reference thresholds, and execution flags.
"""

from pathlib import Path

# Base Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = PROJECT_ROOT / "config"
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
ANALYTICS_DIR = OUTPUTS_DIR / "analytics"
TABLEAU_DIR = OUTPUTS_DIR / "tableau"
REPORTS_DIR = OUTPUTS_DIR / "reports"
MODELS_DIR = PROJECT_ROOT / "models"
DOCS_TABLEAU_DIR = PROJECT_ROOT / "tableau"
TESTS_DIR = PROJECT_ROOT / "tests"

# Primary Cohort File Paths
PRIMARY_RAW_FILE = RAW_DATA_DIR / "health360_primary_cohort.csv"
CLEAN_PATIENT_FILE = PROCESSED_DATA_DIR / "clean_patient_data.csv"
DATA_QUALITY_FILE = PROCESSED_DATA_DIR / "data_quality_report.csv"

# Benchmark Files
BENCHMARK_STROKE_FILE = RAW_DATA_DIR / "benchmark_stroke.csv"
BENCHMARK_HEART_FILE = RAW_DATA_DIR / "benchmark_heart.csv"
BENCHMARK_DIABETES_FILE = RAW_DATA_DIR / "benchmark_diabetes.csv"

# Field Mapping Configuration File
FIELD_MAPPING_FILE = CONFIG_DIR / "field_mapping.json"

# Demographic Category Configurations
AGE_BINS = [0, 29, 44, 59, 120]
AGE_LABELS = ["Under 30", "30-44", "45-59", "60 and above"]

# Clinical BMI Categories (Adult WHO / CDC Standard)
# Underweight: < 18.5
# Healthy Weight: 18.5 - 24.9
# Overweight: 25.0 - 29.9
# Obesity: >= 30.0
BMI_BINS = [0.0, 18.5, 25.0, 30.0, 100.0]
BMI_LABELS = ["Underweight", "Healthy Weight", "Overweight", "Obesity"]

# Clinical Plausibility Reference Thresholds (for validation & outlier review)
CLINICAL_THRESHOLDS = {
    "age": {"min": 1, "max": 115, "unit": "years"},
    "bmi": {"min": 12.0, "max": 75.0, "unit": "kg/m^2"},
    "systolic_bp": {"min": 70, "max": 260, "unit": "mmHg"},
    "diastolic_bp": {"min": 40, "max": 150, "unit": "mmHg"},
    "cholesterol": {"min": 80, "max": 500, "unit": "mg/dL"},
    "fasting_glucose": {"min": 40, "max": 450, "unit": "mg/dL"},
}

# Clinical Guideline Normal Reference Ranges
CLINICAL_NORMAL_RANGES = {
    "systolic_bp": {"normal_max": 120, "elevated_max": 129, "stage1_max": 139},
    "diastolic_bp": {"normal_max": 80, "stage1_max": 89},
    "cholesterol": {"desirable_max": 200, "borderline_max": 239},
    "fasting_glucose": {"normal_max": 99, "prediabetes_max": 125},
    "bmi": {"healthy_min": 18.5, "healthy_max": 24.9},
}

# Machine Learning Configurations
RANDOM_STATE = 42
CV_FOLDS = 5
TEST_SIZE = 0.20

# Target Diseases
PRIMARY_DISEASES = ["heart_disease", "diabetes", "stroke"]

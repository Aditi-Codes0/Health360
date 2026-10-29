"""
Health 360: Data Preprocessing & Cleaning Pipeline
Transforms raw clinical observations into standardized, quality-audited patient records.
"""

from pathlib import Path
from typing import Tuple, Dict, Any, Optional
import numpy as np
import pandas as pd
from config import settings
from src.utils import setup_logger

logger = setup_logger("health360.preprocessing")


class Preprocessor:
    """Preprocesses and standardizes clinical cohorts for analytics and Tableau visualization."""

    def __init__(self):
        self.audit_log: Dict[str, Any] = {
            "transformations_applied": [],
            "imputations": {},
            "rows_excluded": 0,
            "exclusion_reasons": []
        }

    def create_age_groups(self, df: pd.DataFrame, age_col: str = "age") -> pd.DataFrame:
        """
        Constructs standardized epidemiological age categories.
        Categories: 'Under 30', '30-44', '45-59', '60 and above'.
        """
        df = df.copy()
        if age_col not in df.columns:
            logger.warning(f"Age column '{age_col}' not found. Skipping age group derivation.")
            return df

        # Coerce to numeric
        valid_age = pd.to_numeric(df[age_col], errors="coerce")
        df["age_group"] = pd.cut(
            valid_age,
            bins=settings.AGE_BINS,
            labels=settings.AGE_LABELS,
            right=True,
            include_lowest=True
        )
        # Fallback for null or extreme ages
        df["age_group"] = df["age_group"].astype(str).replace({"nan": "Unknown", "None": "Unknown"})
        self.audit_log["transformations_applied"].append("Derived standardized 'age_group' classification")
        return df

    def create_bmi_categories(self, df: pd.DataFrame, bmi_col: str = "bmi") -> pd.DataFrame:
        """
        Constructs WHO/CDC adult clinical BMI categories.
        Categories:
          - Underweight: < 18.5
          - Healthy Weight: 18.5 to < 25.0
          - Overweight: 25.0 to < 30.0
          - Obesity: >= 30.0
        """
        df = df.copy()
        if bmi_col not in df.columns:
            logger.warning(f"BMI column '{bmi_col}' not found. Skipping BMI categorization.")
            return df

        valid_bmi = pd.to_numeric(df[bmi_col], errors="coerce")
        df["bmi_category"] = pd.cut(
            valid_bmi,
            bins=settings.BMI_BINS,
            labels=settings.BMI_LABELS,
            right=False,
            include_lowest=True
        )
        df["bmi_category"] = df["bmi_category"].astype(str).replace({"nan": "Unknown", "None": "Unknown"})
        self.audit_log["transformations_applied"].append("Derived standardized 'bmi_category' classification")
        return df

    def handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Applies clinically defensible imputation without indiscriminately dropping rows.
        - Continuous vitals (bmi, glucose, bp, chol): Median imputation
        - Categorical lifestyle: 'Unknown' category to preserve observation auditability
        """
        df = df.copy()

        # Numeric clinical metrics: Impute with median
        numeric_clinical = ["bmi", "systolic_bp", "diastolic_bp", "cholesterol", "fasting_glucose", "age"]
        for col in numeric_clinical:
            if col in df.columns and df[col].isnull().any():
                missing_count = int(df[col].isnull().sum())
                med_val = df[col].median()
                df[col] = df[col].fillna(med_val)
                self.audit_log["imputations"][col] = {
                    "missing_count": missing_count,
                    "imputed_value": round(float(med_val), 2),
                    "method": "median"
                }
                logger.info(f"Imputed {missing_count} missing values in '{col}' with median={med_val:.2f}")

        # Categorical lifestyle fields: Mark as Unknown
        cat_fields = ["smoking_status", "alcohol_consumption", "physical_activity", "region", "sex"]
        for col in cat_fields:
            if col in df.columns and df[col].isnull().any():
                missing_count = int(df[col].isnull().sum())
                df[col] = df[col].fillna("Unknown")
                self.audit_log["imputations"][col] = {
                    "missing_count": missing_count,
                    "imputed_value": "Unknown",
                    "method": "explicit_category"
                }
                logger.info(f"Imputed {missing_count} missing values in '{col}' with category 'Unknown'")

        # Symptoms and binary targets: fillna with 0 if null
        binary_fields = ["fatigue", "chest_pain", "dizziness"]
        for col in binary_fields:
            if col in df.columns and df[col].isnull().any():
                missing_count = int(df[col].isnull().sum())
                df[col] = df[col].fillna(0).astype(int)
                self.audit_log["imputations"][col] = {
                    "missing_count": missing_count,
                    "imputed_value": 0,
                    "method": "absence_zero"
                }

        return df

    def normalize_categories(self, df: pd.DataFrame) -> pd.DataFrame:
        """Normalizes casing, whitespace, and formatting across text fields."""
        df = df.copy()
        str_cols = df.select_dtypes(include=["object", "string"]).columns

        for col in str_cols:
            if col in ["patient_id"]:
                continue
            df[col] = df[col].astype(str).str.strip().str.title()
            # Normalize specific strings
            df[col] = df[col].replace({"Nan": "Unknown", "None": "Unknown", "": "Unknown"})

        self.audit_log["transformations_applied"].append("Normalized categorical strings and standardized casing")
        return df

    def clean(self, df_raw: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Executes full preprocessing pipeline and returns (clean_df, data_quality_report_df).
        """
        logger.info(f"Initiating preprocessing pipeline on raw dataset (N={len(df_raw)} rows, {len(df_raw.columns)} cols)")
        df = df_raw.copy()

        # Step 1: Remove exact row duplicates if any
        initial_count = len(df)
        df = df.drop_duplicates()
        dups_removed = initial_count - len(df)
        if dups_removed > 0:
            self.audit_log["rows_excluded"] += dups_removed
            self.audit_log["exclusion_reasons"].append(f"Removed {dups_removed} duplicate records")

        # Step 2: Handle missing values with documented strategies
        df = self.handle_missing_values(df)

        # Step 3: Categorical normalization
        df = self.normalize_categories(df)

        # Step 4: Derive epidemiological categories
        df = self.create_age_groups(df)
        df = self.create_bmi_categories(df)

        # Build Data Quality Report DataFrame
        quality_rows = []
        for col in df_raw.columns:
            raw_nulls = int(df_raw[col].isnull().sum())
            clean_nulls = int(df[col].isnull().sum()) if col in df.columns else 0
            impute_info = self.audit_log["imputations"].get(col, {})
            strategy = impute_info.get("method", "None (Complete)" if raw_nulls == 0 else "preserved")

            quality_rows.append({
                "Column Name": col,
                "Raw Missing Count": raw_nulls,
                "Cleaned Missing Count": clean_nulls,
                "Imputation Strategy": strategy,
                "Imputed Value": str(impute_info.get("imputed_value", "N/A")),
                "Raw Data Type": str(df_raw[col].dtype),
                "Cleaned Data Type": str(df[col].dtype) if col in df.columns else "N/A"
            })

        # Add derived columns to report
        for derived_col in ["age_group", "bmi_category"]:
            if derived_col in df.columns and derived_col not in df_raw.columns:
                quality_rows.append({
                    "Column Name": derived_col,
                    "Raw Missing Count": 0,
                    "Cleaned Missing Count": int(df[derived_col].isnull().sum()),
                    "Imputation Strategy": "Derived Categorical Variable",
                    "Imputed Value": "N/A",
                    "Raw Data Type": "Not in Raw",
                    "Cleaned Data Type": str(df[derived_col].dtype)
                })

        quality_report_df = pd.DataFrame(quality_rows)
        logger.info(f"Preprocessing completed. Cleaned dataset has {len(df)} rows and {len(df.columns)} columns.")
        return df, quality_report_df

    def save_clean_data(self, clean_df: pd.DataFrame, quality_df: pd.DataFrame,
                        clean_path: Optional[Path] = None, report_path: Optional[Path] = None) -> None:
        """Exports cleaned dataset and data quality audit to disk."""
        target_clean = clean_path or settings.CLEAN_PATIENT_FILE
        target_report = report_path or settings.DATA_QUALITY_FILE

        target_clean.parent.mkdir(parents=True, exist_ok=True)
        target_report.parent.mkdir(parents=True, exist_ok=True)

        clean_df.to_csv(target_clean, index=False)
        quality_df.to_csv(target_report, index=False)
        logger.info(f"Saved clean patient dataset to: {target_clean}")
        logger.info(f"Saved data quality audit report to: {target_report}")

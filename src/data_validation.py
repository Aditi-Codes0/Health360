"""
Health 360: Data Validation & Quality Verification
Provides rigorous integrity checks, clinical range checks, duplicate detection, and outlier audits.
"""

from typing import Dict, Any, List, Tuple
import numpy as np
import pandas as pd
from config import settings
from src.utils import setup_logger

logger = setup_logger("health360.validation")


class DataValidator:
    """Performs comprehensive clinical validation and quality auditing on healthcare datasets."""

    def __init__(self, thresholds: Dict[str, Dict[str, Any]] = None):
        self.thresholds = thresholds or settings.CLINICAL_THRESHOLDS

    def check_duplicates(self, df: pd.DataFrame, id_col: str = "patient_id") -> Dict[str, Any]:
        """Identifies duplicate rows and duplicate identifier values."""
        full_dups = int(df.duplicated().sum())
        id_dups = 0
        if id_col in df.columns:
            id_dups = int(df.duplicated(subset=[id_col]).sum())

        logger.info(f"Duplicate validation: {full_dups} duplicate rows, {id_dups} duplicate '{id_col}' values.")
        return {
            "total_duplicate_rows": full_dups,
            "duplicate_ids": id_dups,
            "has_duplicates": (full_dups > 0 or id_dups > 0)
        }

    def check_missingness(self, df: pd.DataFrame) -> pd.DataFrame:
        """Profiles missing values across all columns."""
        counts = df.isnull().sum()
        pcts = (df.isnull().mean() * 100).round(2)
        summary = pd.DataFrame({
            "column": df.columns,
            "missing_count": counts.values,
            "missing_pct": pcts.values
        })
        summary = summary[summary["missing_count"] > 0].sort_values(by="missing_count", ascending=False)
        return summary

    def validate_clinical_ranges(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Validates numeric fields against physiological plausibility thresholds.
        Does not automatically delete, but flags out-of-range observations.
        """
        range_violations = {}
        for col, bounds in self.thresholds.items():
            if col in df.columns:
                series = pd.to_numeric(df[col], errors="coerce").dropna()
                min_val = bounds.get("min")
                max_val = bounds.get("max")
                unit = bounds.get("unit", "")

                under_min = (series < min_val).sum()
                over_max = (series > max_val).sum()
                total_invalid = int(under_min + over_max)

                if total_invalid > 0:
                    logger.warning(
                        f"Field '{col}' has {total_invalid} values outside clinical bounds "
                        f"[{min_val}, {max_val}] {unit}."
                    )

                range_violations[col] = {
                    "valid_range": f"[{min_val}, {max_val}] {unit}",
                    "under_min_count": int(under_min),
                    "over_max_count": int(over_max),
                    "total_out_of_range": total_invalid,
                    "observed_min": float(series.min()) if len(series) > 0 else None,
                    "observed_max": float(series.max()) if len(series) > 0 else None
                }

        return range_violations

    def detect_outliers(self, df: pd.DataFrame, method: str = "iqr", factor: float = 1.5) -> Dict[str, Any]:
        """
        Detects statistical outliers using IQR or Z-score method on continuous clinical variables.
        """
        outlier_report = {}
        numeric_cols = df.select_dtypes(include=[np.number]).columns

        for col in numeric_cols:
            if col in ["patient_id", "observation_year", "heart_disease", "diabetes", "stroke", "fatigue", "chest_pain", "dizziness"]:
                continue
            series = df[col].dropna()
            if len(series) < 10:
                continue

            if method == "iqr":
                q25 = series.quantile(0.25)
                q75 = series.quantile(0.75)
                iqr = q75 - q25
                lower_bound = q25 - factor * iqr
                upper_bound = q75 + factor * iqr
                outliers = series[(series < lower_bound) | (series > upper_bound)]
            elif method == "zscore":
                mean = series.mean()
                std = series.std()
                if std == 0:
                    continue
                z = (series - mean) / std
                outliers = series[np.abs(z) > 3.0]
                lower_bound = mean - 3 * std
                upper_bound = mean + 3 * std
            else:
                raise ValueError(f"Unknown outlier method: {method}")

            outlier_report[col] = {
                "outlier_count": int(len(outliers)),
                "outlier_pct": round(float(len(outliers) / len(series) * 100), 2),
                "lower_bound": round(float(lower_bound), 2),
                "upper_bound": round(float(upper_bound), 2),
                "method": method
            }

        return outlier_report

    def run_full_validation_audit(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Runs the complete validation audit and returns a consolidated report."""
        logger.info("Executing comprehensive data validation audit...")
        dups = self.check_duplicates(df)
        missing_df = self.check_missingness(df)
        range_violations = self.validate_clinical_ranges(df)
        outliers = self.detect_outliers(df)

        audit_summary = {
            "total_records_checked": len(df),
            "columns_checked": len(df.columns),
            "duplicates": dups,
            "missing_columns_count": len(missing_df),
            "columns_with_missing": missing_df.to_dict(orient="records"),
            "clinical_range_violations": range_violations,
            "statistical_outliers": outliers
        }
        logger.info(f"Validation complete: {audit_summary['missing_columns_count']} columns with missingness.")
        return audit_summary

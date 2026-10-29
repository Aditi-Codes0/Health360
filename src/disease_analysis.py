"""
Health 360: Chronic Disease Epidemiology & Prevalence Analysis
Examines prevalence, comorbidity burden, age-stratification, and clinical biomarker contrasts.
"""

from pathlib import Path
from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np
from config import settings
from src.utils import setup_logger

logger = setup_logger("health360.disease_analysis")


class DiseaseAnalyzer:
    """Performs epidemiological prevalence and biomarker stratification across chronic diseases."""

    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = output_dir or settings.ANALYTICS_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def calculate_overall_prevalence(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculates population-level prevalence for Heart Disease, Diabetes, and Stroke.
        Includes total eligible count, positive count, observed prevalence %, and 95% CI.
        """
        records = []
        n_total = len(df)

        for disease in settings.PRIMARY_DISEASES:
            if disease in df.columns:
                series = df[disease].dropna()
                n_eligible = len(series)
                n_pos = int(series.sum())
                prev = n_pos / n_eligible if n_eligible > 0 else 0.0
                
                # Wilson score or Wald 95% Confidence Interval
                se = np.sqrt(prev * (1 - prev) / n_eligible) if n_eligible > 0 else 0.0
                ci_lower = max(0.0, prev - 1.96 * se)
                ci_upper = min(1.0, prev + 1.96 * se)

                disease_label = disease.replace("_", " ").title()
                records.append({
                    "Disease": disease_label,
                    "Disease_Key": disease,
                    "Total_Records": n_eligible,
                    "Positive_Cases": n_pos,
                    "Prevalence_Rate": round(prev, 4),
                    "Prevalence_Pct": round(prev * 100, 2),
                    "CI_95_Lower_Pct": round(ci_lower * 100, 2),
                    "CI_95_Upper_Pct": round(ci_upper * 100, 2)
                })

        summary_df = pd.DataFrame(records)
        target_path = self.output_dir / "disease_prevalence.csv"
        summary_df.to_csv(target_path, index=False)
        logger.info(f"Overall disease prevalence computed:\n{summary_df[['Disease', 'Positive_Cases', 'Prevalence_Pct']]}")
        return summary_df

    def analyze_comorbidity_burden(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Evaluates multimorbidity (patients having 0, 1, 2, or 3 chronic conditions).
        """
        available = [d for d in settings.PRIMARY_DISEASES if d in df.columns]
        if len(available) < 2:
            logger.info("Insufficient disease targets for multimorbidity analysis.")
            return pd.DataFrame()

        df_calc = df.copy()
        df_calc["comorbidity_count"] = df_calc[available].sum(axis=1)

        counts = df_calc["comorbidity_count"].value_counts().sort_index().reset_index()
        counts.columns = ["Conditions_Count", "Patient_Count"]
        counts["Percentage"] = (counts["Patient_Count"] / len(df) * 100).round(2)

        # Label counts
        labels = {
            0: "No Chronic Conditions",
            1: "Single Chronic Condition",
            2: "Dual Comorbidity",
            3: "Triple Multimorbidity"
        }
        counts["Burden_Category"] = counts["Conditions_Count"].map(labels).fillna("Multiple Conditions")
        return counts

    def analyze_by_demographic(self, df: pd.DataFrame, stratifier: str = "age_group") -> pd.DataFrame:
        """
        Calculates disease prevalence stratified by demographic dimensions (age_group, sex, region).
        """
        if stratifier not in df.columns:
            logger.warning(f"Stratifier '{stratifier}' not present in dataset.")
            return pd.DataFrame()

        rows = []
        for group, sub_df in df.groupby(stratifier, observed=False):
            n_sub = len(sub_df)
            for disease in settings.PRIMARY_DISEASES:
                if disease in sub_df.columns:
                    pos = int(sub_df[disease].sum())
                    prev_pct = round(pos / n_sub * 100, 2) if n_sub > 0 else 0.0
                    rows.append({
                        "Stratifier": stratifier,
                        "Category": str(group),
                        "Disease": disease.replace("_", " ").title(),
                        "Total_Patients": n_sub,
                        "Positive_Cases": pos,
                        "Prevalence_Pct": prev_pct
                    })

        res_df = pd.DataFrame(rows)
        return res_df

    def compare_clinical_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Compares continuous clinical biomarkers (BMI, BP, Cholesterol, Glucose)
        between disease-positive and disease-negative cohorts.
        """
        biomarkers = ["bmi", "systolic_bp", "diastolic_bp", "cholesterol", "fasting_glucose"]
        available_bio = [b for b in biomarkers if b in df.columns]

        rows = []
        for disease in settings.PRIMARY_DISEASES:
            if disease not in df.columns:
                continue

            for bio in available_bio:
                pos_series = df[df[disease] == 1][bio].dropna()
                neg_series = df[df[disease] == 0][bio].dropna()

                rows.append({
                    "Disease": disease.replace("_", " ").title(),
                    "Biomarker": bio.replace("_", " ").title(),
                    "Positive_Count": int(len(pos_series)),
                    "Positive_Mean": round(float(pos_series.mean()), 2),
                    "Positive_Std": round(float(pos_series.std()), 2),
                    "Positive_Median": round(float(pos_series.median()), 2),
                    "Negative_Count": int(len(neg_series)),
                    "Negative_Mean": round(float(neg_series.mean()), 2),
                    "Negative_Std": round(float(neg_series.std()), 2),
                    "Negative_Median": round(float(neg_series.median()), 2),
                    "Mean_Difference": round(float(pos_series.mean() - neg_series.mean()), 2)
                })

        summary_df = pd.DataFrame(rows)
        target_path = self.output_dir / "clinical_indicator_summary.csv"
        summary_df.to_csv(target_path, index=False)
        return summary_df

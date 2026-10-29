"""
Health 360: Population Health Insights & Demographic Segmentation
Identifies vulnerable demographic cohorts and multi-variable population segments.
"""

from pathlib import Path
from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np
from config import settings
from src.utils import setup_logger

logger = setup_logger("health360.population")


class PopulationAnalyzer:
    """Evaluates population-level patterns, demographic strata, and high-risk segments."""

    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = output_dir or settings.ANALYTICS_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def analyze_age_and_bmi_distribution(self, df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """Calculates demographic proportions across age brackets and BMI classes."""
        age_dist = df["age_group"].value_counts(dropna=False).reset_index()
        age_dist.columns = ["Age_Group", "Count"]
        age_dist["Percentage"] = (age_dist["Count"] / len(df) * 100).round(2)

        bmi_dist = df["bmi_category"].value_counts(dropna=False).reset_index()
        bmi_dist.columns = ["BMI_Category", "Count"]
        bmi_dist["Percentage"] = (bmi_dist["Count"] / len(df) * 100).round(2)

        return {"age_distribution": age_dist, "bmi_distribution": bmi_dist}

    def analyze_population_segments(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Segments the population across composite demographic & behavioral risk profiles:
        Age Group x BMI Category x Smoking Status.
        Computes sample size, disease counts, and composite disease prevalence.
        """
        required = ["age_group", "bmi_category", "smoking_status"]
        if not all(c in df.columns for c in required):
            logger.warning("Missing columns for composite population segmentation.")
            return pd.DataFrame()

        segments = []
        for (age_grp, bmi_cat, smk), sub in df.groupby(required, observed=False):
            n_sub = len(sub)
            if n_sub < 15:  # Filter sparse sub-cells for statistical reliability
                continue

            hd_cases = int(sub["heart_disease"].sum()) if "heart_disease" in sub.columns else 0
            diab_cases = int(sub["diabetes"].sum()) if "diabetes" in sub.columns else 0
            stroke_cases = int(sub["stroke"].sum()) if "stroke" in sub.columns else 0

            hd_pct = round(hd_cases / n_sub * 100, 2)
            diab_pct = round(diab_cases / n_sub * 100, 2)
            stroke_pct = round(stroke_cases / n_sub * 100, 2)

            # Combined chronic burden score (% of individuals with at least one condition)
            any_disease = ((sub["heart_disease"] == 1) | (sub["diabetes"] == 1) | (sub["stroke"] == 1)).sum()
            any_disease_pct = round(any_disease / n_sub * 100, 2)

            segments.append({
                "Age_Group": str(age_grp),
                "BMI_Category": str(bmi_cat),
                "Smoking_Status": str(smk),
                "Cohort_Size": n_sub,
                "Heart_Disease_Cases": hd_cases,
                "Heart_Disease_Prevalence_Pct": hd_pct,
                "Diabetes_Cases": diab_cases,
                "Diabetes_Prevalence_Pct": diab_pct,
                "Stroke_Cases": stroke_cases,
                "Stroke_Prevalence_Pct": stroke_pct,
                "Any_Condition_Prevalence_Pct": any_disease_pct
            })

        seg_df = pd.DataFrame(segments)
        # Sort by composite disease burden descending
        if len(seg_df) > 0:
            seg_df = seg_df.sort_values(by="Any_Condition_Prevalence_Pct", ascending=False)
            target_path = self.output_dir / "population_segments.csv"
            seg_df.to_csv(target_path, index=False)
            logger.info(f"Generated {len(seg_df)} population segments saved to {target_path}")

        return seg_df

    def analyze_symptom_demographics(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Profiles symptom prevalence across age categories and sex.
        """
        symptoms = ["fatigue", "chest_pain", "dizziness"]
        available_syms = [s for s in symptoms if s in df.columns]

        rows = []
        for age_grp, sub in df.groupby("age_group", observed=False):
            n_sub = len(sub)
            for sym in available_syms:
                cnt = int(sub[sym].sum())
                pct = round(cnt / n_sub * 100, 2) if n_sub > 0 else 0.0
                rows.append({
                    "Age_Group": str(age_grp),
                    "Symptom": sym.replace("_", " ").title(),
                    "Cases": cnt,
                    "Total": n_sub,
                    "Prevalence_Pct": pct
                })

        sym_demo_df = pd.DataFrame(rows)
        return sym_demo_df

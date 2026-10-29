"""
Health 360: Lifestyle & Risk Factor Analysis
Evaluates behavioral exposures (smoking, alcohol, physical activity) and clinical symptoms.
"""

from pathlib import Path
from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np
from scipy import stats
from config import settings
from src.utils import setup_logger

logger = setup_logger("health360.risk_factor_analysis")


class RiskFactorAnalyzer:
    """Investigates associations between lifestyle choices, clinical symptoms, and chronic outcomes."""

    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = output_dir or settings.ANALYTICS_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def analyze_lifestyle_factors(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Cross-tabulates lifestyle behaviors against each chronic disease outcome.
        Computes group patient count, disease cases, and observed prevalence %.
        """
        lifestyle_factors = ["smoking_status", "alcohol_consumption", "physical_activity"]
        available_factors = [f for f in lifestyle_factors if f in df.columns]

        rows = []
        for factor in available_factors:
            for group, sub_df in df.groupby(factor, observed=False):
                n_group = len(sub_df)
                for disease in settings.PRIMARY_DISEASES:
                    if disease in sub_df.columns:
                        pos = int(sub_df[disease].sum())
                        prev_pct = round(pos / n_group * 100, 2) if n_group > 0 else 0.0
                        rows.append({
                            "Factor_Type": "Lifestyle",
                            "Factor_Name": factor.replace("_", " ").title(),
                            "Factor_Category": str(group),
                            "Disease": disease.replace("_", " ").title(),
                            "Total_Patients": n_group,
                            "Positive_Cases": pos,
                            "Prevalence_Pct": prev_pct
                        })

        summary_df = pd.DataFrame(rows)
        target_path = self.output_dir / "lifestyle_analysis.csv"
        summary_df.to_csv(target_path, index=False)
        return summary_df

    def analyze_symptoms(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Analyzes reported clinical symptoms (Fatigue, Chest Pain, Dizziness) against disease outcomes.
        Calculates prevalence when symptom is Present (1) vs Absent (0).
        """
        symptoms = ["fatigue", "chest_pain", "dizziness"]
        available_symptoms = [s for s in symptoms if s in df.columns]

        rows = []
        for sym in available_symptoms:
            for val in [0, 1]:
                sub_df = df[df[sym] == val]
                n_sub = len(sub_df)
                status_label = "Present" if val == 1 else "Absent"
                for disease in settings.PRIMARY_DISEASES:
                    if disease in sub_df.columns:
                        pos = int(sub_df[disease].sum())
                        prev_pct = round(pos / n_sub * 100, 2) if n_sub > 0 else 0.0
                        rows.append({
                            "Factor_Type": "Symptom",
                            "Symptom_Name": sym.replace("_", " ").title(),
                            "Symptom_Status": status_label,
                            "Disease": disease.replace("_", " ").title(),
                            "Total_Patients": n_sub,
                            "Positive_Cases": pos,
                            "Prevalence_Pct": prev_pct
                        })

        summary_df = pd.DataFrame(rows)
        target_path = self.output_dir / "symptom_analysis.csv"
        summary_df.to_csv(target_path, index=False)
        return summary_df

    def calculate_odds_ratios(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Computes 2x2 contingency Odds Ratios (OR) and 95% Confidence Intervals for key binary/dichotomized risks.
        """
        # Dichotomize exposures for standard epidemiological odds ratio calculation
        df_exp = df.copy()
        exposures = {}

        if "smoking_status" in df.columns:
            df_exp["exp_smoking_current"] = (df["smoking_status"] == "Current").astype(int)
            exposures["Current Smoking"] = "exp_smoking_current"

        if "physical_activity" in df.columns:
            df_exp["exp_sedentary"] = (df["physical_activity"] == "Sedentary").astype(int)
            exposures["Sedentary Lifestyle"] = "exp_sedentary"

        if "bmi" in df.columns:
            df_exp["exp_obesity"] = (df["bmi"] >= 30.0).astype(int)
            exposures["Obesity (BMI >= 30)"] = "exp_obesity"

        if "systolic_bp" in df.columns:
            df_exp["exp_hypertension_stage2"] = (df["systolic_bp"] >= 140).astype(int)
            exposures["Stage 2 Hypertension (SBP >= 140)"] = "exp_hypertension_stage2"

        if "chest_pain" in df.columns:
            exposures["Chest Pain Symptom"] = "chest_pain"

        if "fatigue" in df.columns:
            exposures["Fatigue Symptom"] = "fatigue"

        rows = []
        for exp_label, exp_col in exposures.items():
            for disease in settings.PRIMARY_DISEASES:
                if disease not in df_exp.columns:
                    continue

                # 2x2 contingency table:
                # a = Exposed & Disease+, b = Exposed & Disease-
                # c = Unexposed & Disease+, d = Unexposed & Disease-
                a = int(((df_exp[exp_col] == 1) & (df_exp[disease] == 1)).sum())
                b = int(((df_exp[exp_col] == 1) & (df_exp[disease] == 0)).sum())
                c = int(((df_exp[exp_col] == 0) & (df_exp[disease] == 1)).sum())
                d = int(((df_exp[exp_col] == 0) & (df_exp[disease] == 0)).sum())

                # Prevent division by zero with Haldane-Anscombe correction (+0.5) if any cell is 0
                if 0 in (a, b, c, d):
                    a_c, b_c, c_c, d_c = a + 0.5, b + 0.5, c + 0.5, d + 0.5
                else:
                    a_c, b_c, c_c, d_c = a, b, c, d

                odds_ratio = (a_c * d_c) / (b_c * c_c)
                se_ln_or = np.sqrt(1/a_c + 1/b_c + 1/c_c + 1/d_c)
                ci_lower = np.exp(np.log(odds_ratio) - 1.96 * se_ln_or)
                ci_upper = np.exp(np.log(odds_ratio) + 1.96 * se_ln_or)

                # Fisher exact or Chi-Square p-value
                res = stats.fisher_exact([[a, b], [c, d]]) if (a + b + c + d) < 1000 else stats.chi2_contingency([[a, b], [c, d]])
                p_val = res[1] if isinstance(res, tuple) else res.pvalue

                rows.append({
                    "Risk_Factor": exp_label,
                    "Disease": disease.replace("_", " ").title(),
                    "Exposed_Positive": a,
                    "Exposed_Negative": b,
                    "Unexposed_Positive": c,
                    "Unexposed_Negative": d,
                    "Odds_Ratio": round(odds_ratio, 2),
                    "OR_95_CI_Lower": round(ci_lower, 2),
                    "OR_95_CI_Upper": round(ci_upper, 2),
                    "P_Value": round(p_val, 6),
                    "Statistical_Significance": "Significant (p < 0.05)" if p_val < 0.05 else "Not Significant"
                })

        or_df = pd.DataFrame(rows)
        target_path = self.output_dir / "risk_factor_associations.csv"
        or_df.to_csv(target_path, index=False)
        return or_df

"""
Health 360: Inferential Statistical Analysis Module
Provides hypothesis testing, effect size estimations, and multiple-testing corrections.
"""

from pathlib import Path
from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.stats.multitest import multipletests
from config import settings
from src.utils import setup_logger

logger = setup_logger("health360.statistical")


class StatisticalAnalyzer:
    """Performs rigorous hypothesis testing, effect size estimation, and FDR corrections."""

    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = output_dir or settings.ANALYTICS_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def calculate_cramers_v(confusion_matrix: np.ndarray) -> float:
        """Calculates Cramér's V measure of nominal association."""
        chi2 = stats.chi2_contingency(confusion_matrix)[0]
        n = confusion_matrix.sum()
        phi2 = chi2 / n
        r, k = confusion_matrix.shape
        phi2corr = max(0, phi2 - ((k - 1) * (r - 1)) / (n - 1))
        rcorr = r - ((r - 1) ** 2) / (n - 1)
        kcorr = k - ((k - 1) ** 2) / (n - 1)
        denom = min((kcorr - 1), (rcorr - 1))
        if denom <= 0:
            return 0.0
        return float(np.sqrt(phi2corr / denom))

    @staticmethod
    def calculate_cohens_d(group1: pd.Series, group2: pd.Series) -> float:
        """Calculates Cohen's d effect size for two independent continuous groups."""
        n1, n2 = len(group1), len(group2)
        if n1 < 2 or n2 < 2:
            return 0.0
        var1, var2 = group1.var(), group2.var()
        pooled_std = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
        if pooled_std == 0:
            return 0.0
        return float((group1.mean() - group2.mean()) / pooled_std)

    def test_categorical_associations(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Executes Chi-Square tests of independence for categorical factors across diseases.
        Computes Chi2 statistic, degrees of freedom, unadjusted p-value, and Cramér's V.
        """
        cat_factors = ["smoking_status", "alcohol_consumption", "physical_activity", "age_group", "bmi_category", "sex", "region"]
        available_factors = [f for f in cat_factors if f in df.columns]

        tests = []
        for factor in available_factors:
            for disease in settings.PRIMARY_DISEASES:
                if disease not in df.columns:
                    continue

                cont_table = pd.crosstab(df[factor], df[disease])
                if cont_table.shape[0] < 2 or cont_table.shape[1] < 2:
                    continue

                chi2, p_val, dof, _ = stats.chi2_contingency(cont_table)
                cramer_v = self.calculate_cramers_v(cont_table.values)

                tests.append({
                    "Factor": factor,
                    "Disease": disease,
                    "Test_Type": "Chi-Square Independence",
                    "Statistic": round(float(chi2), 3),
                    "Degrees_Freedom": int(dof),
                    "P_Value_Raw": p_val,
                    "Effect_Size_Type": "Cramer's V",
                    "Effect_Size": round(cramer_v, 3)
                })

        tests_df = pd.DataFrame(tests)
        if len(tests_df) > 0:
            # Apply Benjamini-Hochberg False Discovery Rate correction
            reject_fdr, pvals_corrected, _, _ = multipletests(tests_df["P_Value_Raw"], alpha=0.05, method="fdr_bh")
            tests_df["P_Value_Adjusted_FDR"] = pvals_corrected.round(6)
            tests_df["Significant_FDR"] = reject_fdr
        return tests_df

    def test_continuous_biomarkers(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Executes Independent Samples T-Tests and Mann-Whitney U tests for clinical biomarkers.
        """
        biomarkers = ["bmi", "systolic_bp", "diastolic_bp", "cholesterol", "fasting_glucose", "age"]
        available_bio = [b for b in biomarkers if b in df.columns]

        tests = []
        for bio in available_bio:
            for disease in settings.PRIMARY_DISEASES:
                if disease not in df.columns:
                    continue

                pos = df[df[disease] == 1][bio].dropna()
                neg = df[df[disease] == 0][bio].dropna()

                if len(pos) < 5 or len(neg) < 5:
                    continue

                # Parametric T-Test (Welch's unequal variances)
                t_stat, t_pval = stats.ttest_ind(pos, neg, equal_var=False)
                # Nonparametric Mann-Whitney U test
                u_stat, u_pval = stats.mannwhitneyu(pos, neg, alternative="two-sided")
                cohen_d = self.calculate_cohens_d(pos, neg)

                tests.append({
                    "Biomarker": bio,
                    "Disease": disease,
                    "T_Statistic": round(float(t_stat), 3),
                    "T_Test_P_Value": t_pval,
                    "Mann_Whitney_U": round(float(u_stat), 1),
                    "MWU_P_Value": u_pval,
                    "Cohens_d": round(cohen_d, 3),
                    "Positive_Mean": round(float(pos.mean()), 2),
                    "Negative_Mean": round(float(neg.mean()), 2)
                })

        tests_df = pd.DataFrame(tests)
        if len(tests_df) > 0:
            # FDR multiple testing correction on parametric p-values
            reject, adj_p, _, _ = multipletests(tests_df["T_Test_P_Value"], alpha=0.05, method="fdr_bh")
            tests_df["T_Test_P_Adjusted_FDR"] = adj_p.round(6)
            tests_df["Significant_FDR"] = reject
        return tests_df

    def run_complete_statistical_suite(self, df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """Runs the entire inferential suite and exports summary outputs."""
        logger.info("Executing comprehensive inferential statistical testing suite...")
        cat_results = self.test_categorical_associations(df)
        cont_results = self.test_continuous_biomarkers(df)

        cat_path = self.output_dir / "statistical_tests_categorical.csv"
        cont_path = self.output_dir / "statistical_tests_biomarkers.csv"

        cat_results.to_csv(cat_path, index=False)
        cont_results.to_csv(cont_path, index=False)
        logger.info(f"Saved inferential test results to {cat_path} and {cont_path}")

        return {
            "categorical_tests": cat_results,
            "biomarker_tests": cont_results
        }

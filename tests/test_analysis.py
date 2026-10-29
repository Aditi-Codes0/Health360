"""
Health 360: Unit Tests for Epidemiology, Risk Factors & Statistical Analytics
"""

import pytest
import pandas as pd
import numpy as np
from src.disease_analysis import DiseaseAnalyzer
from src.risk_factor_analysis import RiskFactorAnalyzer
from src.statistical_analysis import StatisticalAnalyzer


@pytest.fixture
def clean_cohort():
    return pd.DataFrame({
        "patient_id": [f"P{i}" for i in range(100)],
        "age": np.random.randint(20, 80, 100),
        "age_group": np.random.choice(["Under 30", "30-44", "45-59", "60 and above"], 100),
        "bmi": np.random.uniform(18.0, 38.0, 100),
        "bmi_category": np.random.choice(["Healthy Weight", "Overweight", "Obesity"], 100),
        "systolic_bp": np.random.randint(100, 180, 100),
        "fasting_glucose": np.random.uniform(70, 220, 100),
        "smoking_status": np.random.choice(["Never", "Former", "Current"], 100),
        "physical_activity": np.random.choice(["Sedentary", "Moderate", "Active"], 100),
        "fatigue": np.random.choice([0, 1], 100),
        "chest_pain": np.random.choice([0, 1], 100),
        "heart_disease": np.random.choice([0, 1], 100, p=[0.85, 0.15]),
        "diabetes": np.random.choice([0, 1], 100, p=[0.88, 0.12]),
        "stroke": np.random.choice([0, 1], 100, p=[0.94, 0.06]),
        "sex": np.random.choice(["Male", "Female"], 100),
        "region": np.random.choice(["North", "South", "East", "West"], 100)
    })


def test_calculate_prevalence(clean_cohort):
    """Verify disease prevalence calculations and confidence intervals."""
    analyzer = DiseaseAnalyzer()
    prev_df = analyzer.calculate_overall_prevalence(clean_cohort)
    assert len(prev_df) == 3
    assert "Prevalence_Pct" in prev_df.columns
    assert "CI_95_Lower_Pct" in prev_df.columns
    assert (prev_df["Prevalence_Pct"] >= 0).all()
    assert (prev_df["Prevalence_Pct"] <= 100).all()


def test_prevalence_zero_denominator():
    """Verify safe handling of empty dataframes without ZeroDivisionError."""
    analyzer = DiseaseAnalyzer()
    empty_df = pd.DataFrame(columns=["heart_disease", "diabetes", "stroke"])
    prev_df = analyzer.calculate_overall_prevalence(empty_df)
    assert len(prev_df) == 3
    assert (prev_df["Positive_Cases"] == 0).all()
    assert (prev_df["Prevalence_Pct"] == 0.0).all()


def test_risk_factor_odds_ratios(clean_cohort):
    """Verify contingency odds ratio calculations."""
    rf_analyzer = RiskFactorAnalyzer()
    or_df = rf_analyzer.calculate_odds_ratios(clean_cohort)
    assert len(or_df) > 0
    assert "Odds_Ratio" in or_df.columns
    assert "OR_95_CI_Lower" in or_df.columns
    assert (or_df["Odds_Ratio"] >= 0).all()


def test_statistical_hypothesis_tests(clean_cohort):
    """Verify inferential chi-square and t-test execution."""
    stat_analyzer = StatisticalAnalyzer()
    res = stat_analyzer.run_complete_statistical_suite(clean_cohort)
    assert "categorical_tests" in res
    assert "biomarker_tests" in res
    assert len(res["categorical_tests"]) > 0
    assert "P_Value_Adjusted_FDR" in res["categorical_tests"].columns

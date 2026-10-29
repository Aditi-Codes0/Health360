"""
Health 360: Unit Tests for Preprocessing & Data Cleaning
"""

import pytest
import pandas as pd
import numpy as np
from src.preprocessing import Preprocessor


@pytest.fixture
def preprocessor():
    return Preprocessor()


@pytest.fixture
def dirty_patient_df():
    return pd.DataFrame({
        "patient_id": ["P1", "P2", "P3", "P4", "P5", "P5"],  # P5 is duplicate
        "age": [22, 35, 52, 68, np.nan, np.nan],
        "sex": ["male ", " Female", "MALE", "female", "Male", "Male"],
        "bmi": [17.5, 23.0, 27.5, 34.0, np.nan, np.nan],
        "systolic_bp": [110, 125, 140, 160, np.nan, np.nan],
        "smoking_status": ["Never", "former", "Current", np.nan, "Never", "Never"],
        "heart_disease": [0, 0, 1, 1, 0, 0]
    })


def test_create_age_groups(preprocessor):
    """Verify age groups match CDC surveillance bands."""
    df = pd.DataFrame({"age": [18, 29, 30, 44, 45, 59, 60, 85]})
    res = preprocessor.create_age_groups(df)
    assert res["age_group"].tolist() == [
        "Under 30", "Under 30", "30-44", "30-44", "45-59", "45-59", "60 and above", "60 and above"
    ]


def test_create_bmi_categories(preprocessor):
    """Verify adult WHO BMI category classifications."""
    df = pd.DataFrame({"bmi": [17.0, 18.4, 18.5, 24.9, 25.0, 29.9, 30.0, 45.0]})
    res = preprocessor.create_bmi_categories(df)
    assert res["bmi_category"].tolist() == [
        "Underweight", "Underweight",
        "Healthy Weight", "Healthy Weight",
        "Overweight", "Overweight",
        "Obesity", "Obesity"
    ]


def test_handle_missing_values(preprocessor, dirty_patient_df):
    """Verify median imputation for numeric and category for text."""
    clean = preprocessor.handle_missing_values(dirty_patient_df)
    assert clean["bmi"].isnull().sum() == 0
    assert clean["systolic_bp"].isnull().sum() == 0
    assert clean["smoking_status"].isnull().sum() == 0
    assert "Unknown" in clean["smoking_status"].values


def test_full_clean_pipeline(preprocessor, dirty_patient_df):
    """Verify full preprocessing pipeline drops duplicates and derives columns."""
    clean_df, quality_df = preprocessor.clean(dirty_patient_df)
    # 6 initial rows minus 1 duplicate = 5 rows
    assert len(clean_df) == 5
    assert "age_group" in clean_df.columns
    assert "bmi_category" in clean_df.columns
    assert len(quality_df) > 0

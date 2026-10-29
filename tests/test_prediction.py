"""
Health 360: Unit Tests for Machine Learning Modeling & Risk Prediction
"""

import pytest
import pandas as pd
import numpy as np
from src.prediction import HealthRiskModelManager, Health360RiskPredictor
from src.model_evaluation import ModelEvaluator


@pytest.fixture
def ml_cohort():
    np.random.seed(42)
    n = 200
    return pd.DataFrame({
        "patient_id": [f"P{i:04d}" for i in range(n)],
        "age": np.random.randint(30, 80, n),
        "age_group": np.random.choice(["30-44", "45-59", "60 and above"], n),
        "sex": np.random.choice(["Male", "Female"], n),
        "region": np.random.choice(["South", "Midwest", "West", "Northeast"], n),
        "bmi": np.random.uniform(19.0, 36.0, n),
        "bmi_category": np.random.choice(["Healthy Weight", "Overweight", "Obesity"], n),
        "systolic_bp": np.random.randint(100, 180, n),
        "diastolic_bp": np.random.randint(60, 100, n),
        "cholesterol": np.random.randint(140, 280, n),
        "fasting_glucose": np.random.uniform(70, 200, n),
        "smoking_status": np.random.choice(["Never", "Former", "Current"], n),
        "alcohol_consumption": np.random.choice(["Non-drinker", "Moderate"], n),
        "physical_activity": np.random.choice(["Sedentary", "Active"], n),
        "fatigue": np.random.choice([0, 1], n),
        "chest_pain": np.random.choice([0, 1], n),
        "dizziness": np.random.choice([0, 1], n),
        "heart_disease": np.random.choice([0, 1], n, p=[0.80, 0.20]),
        "diabetes": np.random.choice([0, 1], n, p=[0.85, 0.15]),
        "stroke": np.random.choice([0, 1], n, p=[0.90, 0.10])
    })


def test_prepare_features_leakage_prevention(ml_cohort):
    """Verify other disease targets and patient identifiers are excluded from features."""
    manager = HealthRiskModelManager()
    X, y, num_cols, cat_cols = manager.prepare_features(ml_cohort, target_col="heart_disease")
    assert "heart_disease" not in X.columns
    assert "diabetes" not in X.columns
    assert "stroke" not in X.columns
    assert "patient_id" not in X.columns
    assert len(X) == len(y)


def test_invalid_target_exception(ml_cohort):
    """Verify ValueError is raised if target column is missing."""
    manager = HealthRiskModelManager()
    with pytest.raises(ValueError):
        manager.prepare_features(ml_cohort, target_col="non_existent_target")


def test_train_and_evaluate_model(ml_cohort):
    """Verify end-to-end model training, CV selection, and metric computation."""
    manager = HealthRiskModelManager()
    evaluator = ModelEvaluator()
    res = manager.train_and_select_best_model(ml_cohort, target_col="heart_disease")
    assert res["best_pipeline"] is not None
    assert res["best_model_name"] in ["Logistic_Regression", "Decision_Tree", "Random_Forest"]

    test_metrics = evaluator.evaluate_test_set(res)
    assert "ROC_AUC" in test_metrics
    assert "Sensitivity_Recall" in test_metrics
    assert 0.0 <= test_metrics["Accuracy"] <= 1.0


def test_risk_prediction_interface(ml_cohort):
    """Verify prediction interface accepts features and returns model-estimated risk."""
    manager = HealthRiskModelManager()
    res = manager.train_and_select_best_model(ml_cohort, target_col="heart_disease")
    predictor = Health360RiskPredictor(res["best_pipeline"], target_name="heart_disease")

    patient = {
        "age": 60, "sex": "Male", "bmi": 31.0, "systolic_bp": 150, "diastolic_bp": 90,
        "cholesterol": 230, "fasting_glucose": 110.0, "smoking_status": "Current",
        "alcohol_consumption": "Moderate", "physical_activity": "Sedentary",
        "fatigue": 1, "chest_pain": 1, "dizziness": 0
    }
    prediction = predictor.predict_risk(patient)
    assert "model_estimated_risk_category" in prediction
    assert "estimated_probability" in prediction
    assert "clinical_disclaimer" in prediction
    assert "NOT constitute a clinical diagnosis" in prediction["clinical_disclaimer"]

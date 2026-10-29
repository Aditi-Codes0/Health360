"""
Health 360: Machine Learning Disease Risk Prediction Module
Implements pipelines with ColumnTransformer, Stratified Cross-Validation, and Risk Interface.
"""

from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_validate, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier

from config import settings
from src.utils import setup_logger

logger = setup_logger("health360.prediction")


class HealthRiskModelManager:
    """Manages training, cross-validation, and inference pipelines for chronic disease outcomes."""

    def __init__(self, models_dir: Optional[Path] = None):
        self.models_dir = models_dir or settings.MODELS_DIR
        self.models_dir.mkdir(parents=True, exist_ok=True)
        self.trained_pipelines: Dict[str, Pipeline] = {}
        self.feature_columns: Dict[str, List[str]] = {}

    def get_candidate_models(self) -> Dict[str, Any]:
        """Returns baseline candidate classifiers."""
        return {
            "Logistic_Regression": LogisticRegression(
                max_iter=1000,
                class_weight="balanced",
                random_state=settings.RANDOM_STATE
            ),
            "Decision_Tree": DecisionTreeClassifier(
                max_depth=5,
                class_weight="balanced",
                random_state=settings.RANDOM_STATE
            ),
            "Random_Forest": RandomForestClassifier(
                n_estimators=100,
                max_depth=6,
                class_weight="balanced",
                random_state=settings.RANDOM_STATE
            )
        }

    def prepare_features(self, df: pd.DataFrame, target_col: str) -> Tuple[pd.DataFrame, pd.Series, List[str], List[str]]:
        """
        Validates target and isolates non-leaking predictors.
        Excludes patient identifiers, targets, and derived labels.
        """
        if target_col not in df.columns:
            raise ValueError(f"Target column '{target_col}' not present in dataset.")

        y = df[target_col].dropna().astype(int)
        valid_indices = y.index

        # Exclude IDs, target, other disease targets, and post-diagnostic derivations
        leakage_cols = [
            "patient_id", "observation_year", target_col, 
            "heart_disease", "diabetes", "stroke"
        ]
        
        feature_df = df.loc[valid_indices].drop(columns=[c for c in leakage_cols if c in df.columns], errors="ignore")

        numeric_features = feature_df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_features = feature_df.select_dtypes(include=["object", "string", "category"]).columns.tolist()

        logger.info(f"Target '{target_col}': {len(numeric_features)} numeric features, {len(categorical_features)} categorical features.")
        return feature_df, y, numeric_features, categorical_features

    def build_pipeline(self, model: Any, numeric_cols: List[str], categorical_cols: List[str]) -> Pipeline:
        """Constructs an end-to-end preprocessing and modeling pipeline."""
        numeric_transformer = Pipeline(steps=[
            ("scaler", StandardScaler())
        ])

        categorical_transformer = Pipeline(steps=[
            ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
        ])

        preprocessor = ColumnTransformer(
            transformers=[
                ("num", numeric_transformer, numeric_cols),
                ("cat", categorical_transformer, categorical_cols)
            ]
        )

        return Pipeline(steps=[
            ("preprocessor", preprocessor),
            ("classifier", model)
        ])

    def train_and_select_best_model(self, df: pd.DataFrame, target_col: str) -> Dict[str, Any]:
        """
        Performs stratified 80/20 train/test split, 5-fold cross validation on training data,
        selects top performing model by ROC-AUC, and evaluates on held-out test data.
        """
        X, y, num_cols, cat_cols = self.prepare_features(df, target_col)

        # Stratified Train/Test Split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=settings.TEST_SIZE, stratify=y, random_state=settings.RANDOM_STATE
        )

        candidates = self.get_candidate_models()
        cv = StratifiedKFold(n_splits=settings.CV_FOLDS, shuffle=True, random_state=settings.RANDOM_STATE)
        
        cv_results = {}
        best_name = None
        best_score = -1.0
        best_pipe = None

        logger.info(f"Training and cross-validating models for target: '{target_col}'")
        for name, model in candidates.items():
            pipe = self.build_pipeline(model, num_cols, cat_cols)
            scores = cross_validate(
                pipe, X_train, y_train, cv=cv,
                scoring=["roc_auc", "f1", "recall", "precision"],
                return_train_score=False
            )
            mean_auc = scores["test_roc_auc"].mean()
            mean_f1 = scores["test_f1"].mean()
            mean_rec = scores["test_recall"].mean()

            cv_results[name] = {
                "cv_roc_auc_mean": round(float(mean_auc), 4),
                "cv_roc_auc_std": round(float(scores["test_roc_auc"].std()), 4),
                "cv_f1_mean": round(float(mean_f1), 4),
                "cv_recall_mean": round(float(mean_rec), 4)
            }

            if mean_auc > best_score:
                best_score = mean_auc
                best_name = name
                best_pipe = pipe

        # Fit best pipeline on full training set
        logger.info(f"Selected best model for {target_col}: '{best_name}' (CV ROC-AUC: {best_score:.4f})")
        best_pipe.fit(X_train, y_train)

        # Save model pipeline artifact
        model_filename = f"{target_col}_{best_name.lower()}_pipeline.joblib"
        model_path = self.models_dir / model_filename
        joblib.dump(best_pipe, model_path)
        logger.info(f"Saved model artifact to {model_path}")

        self.trained_pipelines[target_col] = best_pipe
        self.feature_columns[target_col] = X.columns.tolist()

        return {
            "target": target_col,
            "best_model_name": best_name,
            "best_pipeline": best_pipe,
            "model_path": str(model_path),
            "cv_benchmarks": cv_results,
            "X_train": X_train,
            "X_test": X_test,
            "y_train": y_train,
            "y_test": y_test,
            "numeric_cols": num_cols,
            "categorical_cols": cat_cols
        }


class Health360RiskPredictor:
    """
    Python prediction interface providing patient risk estimates and feature explanations.
    Uses strictly the terminology 'model-estimated risk' rather than 'medical diagnosis'.
    """

    def __init__(self, pipeline: Pipeline, target_name: str = "heart_disease"):
        self.pipeline = pipeline
        self.target_name = target_name

    def predict_risk(self, patient_features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Computes model-estimated risk for a patient observation.
        Automatically derives age_group and bmi_category if raw age and bmi are supplied.
        """
        features = patient_features.copy()

        # Auto-derive age_group if absent but age present
        if "age_group" not in features and "age" in features:
            age_val = features["age"]
            if age_val <= 29:
                features["age_group"] = "Under 30"
            elif age_val <= 44:
                features["age_group"] = "30-44"
            elif age_val <= 59:
                features["age_group"] = "45-59"
            else:
                features["age_group"] = "60 and above"

        # Auto-derive bmi_category if absent but bmi present
        if "bmi_category" not in features and "bmi" in features:
            bmi_val = features["bmi"]
            if bmi_val < 18.5:
                features["bmi_category"] = "Underweight"
            elif bmi_val < 25.0:
                features["bmi_category"] = "Healthy Weight"
            elif bmi_val < 30.0:
                features["bmi_category"] = "Overweight"
            else:
                features["bmi_category"] = "Obesity"

        if "region" not in features:
            features["region"] = "Unknown"

        input_df = pd.DataFrame([features])

        try:
            pred_class = int(self.pipeline.predict(input_df)[0])
            pred_proba = float(self.pipeline.predict_proba(input_df)[0][1])
        except Exception as e:
            logger.error(f"Prediction execution error: {e}")
            raise

        risk_tier = "High Risk" if pred_proba >= 0.50 else ("Moderate Risk" if pred_proba >= 0.25 else "Low Risk")

        return {
            "target_disease": self.target_name.replace("_", " ").title(),
            "model_estimated_risk_category": risk_tier,
            "predicted_binary_class": pred_class,
            "estimated_probability": round(pred_proba, 4),
            "estimated_probability_pct": f"{pred_proba * 100:.1f}%",
            "provided_patient_features": patient_features,
            "clinical_disclaimer": (
                "IMPORTANT: This output represents a model-estimated statistical risk based on "
                "observational population data. It is for research and educational purposes only "
                "and does NOT constitute a clinical diagnosis or medical recommendation. "
                "Individual healthcare decisions should be made with a licensed physician."
            )
        }

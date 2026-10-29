"""
Health 360: Machine Learning Evaluation & Subgroup Audit
Computes test metrics, confusion matrices, ROC/PR-AUC, feature importances, and fairness audits.
"""

from pathlib import Path
from typing import Dict, Any, List, Optional
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, average_precision_score, confusion_matrix,
    classification_report, roc_curve, precision_recall_curve
)
from config import settings
from src.utils import setup_logger

logger = setup_logger("health360.evaluation")


class ModelEvaluator:
    """Evaluates machine learning models with performance metrics, feature importances, and subgroup analysis."""

    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = output_dir or settings.ANALYTICS_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def evaluate_test_set(self, trained_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluates the best pipeline on the untouched held-out test set.
        """
        target = trained_info["target"]
        pipeline = trained_info["best_pipeline"]
        model_name = trained_info["best_model_name"]
        X_test = trained_info["X_test"]
        y_test = trained_info["y_test"]

        y_pred = pipeline.predict(X_test)
        y_prob = pipeline.predict_proba(X_test)[:, 1] if hasattr(pipeline, "predict_proba") else y_pred

        cm = confusion_matrix(y_test, y_pred)
        tn, fp, fn, tp = cm.ravel()

        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, zero_division=0)
        recall = recall_score(y_test, y_pred, zero_division=0)
        specificity = tn / (tn + fp) if (tn + fp) > 0 else 0.0
        f1 = f1_score(y_test, y_pred, zero_division=0)
        roc_auc = roc_auc_score(y_test, y_prob)
        pr_auc = average_precision_score(y_test, y_prob)

        metrics = {
            "Disease": target.replace("_", " ").title(),
            "Disease_Key": target,
            "Model_Algorithm": model_name.replace("_", " "),
            "Test_Sample_Size": len(y_test),
            "True_Positives": int(tp),
            "False_Positives": int(fp),
            "True_Negatives": int(tn),
            "False_Negatives": int(fn),
            "Accuracy": round(float(accuracy), 4),
            "Sensitivity_Recall": round(float(recall), 4),
            "Specificity": round(float(specificity), 4),
            "Precision": round(float(precision), 4),
            "F1_Score": round(float(f1), 4),
            "ROC_AUC": round(float(roc_auc), 4),
            "PR_AUC": round(float(pr_auc), 4)
        }

        # Subgroup audit across demographics (e.g. Sex)
        subgroup_results = []
        if "sex" in X_test.columns:
            for sex_grp in X_test["sex"].unique():
                idx = X_test[X_test["sex"] == sex_grp].index
                sub_y_true = y_test.loc[idx]
                sub_y_pred = y_pred[X_test.index.get_indexer(idx)]
                sub_y_prob = y_prob[X_test.index.get_indexer(idx)]
                if len(sub_y_true.unique()) > 1:
                    sub_auc = roc_auc_score(sub_y_true, sub_y_prob)
                    sub_rec = recall_score(sub_y_true, sub_y_pred, zero_division=0)
                    subgroup_results.append({
                        "Subgroup": f"Sex: {sex_grp}",
                        "Sample_Size": len(sub_y_true),
                        "ROC_AUC": round(float(sub_auc), 4),
                        "Recall": round(float(sub_rec), 4)
                    })

        metrics["Subgroup_Audit"] = subgroup_results
        logger.info(f"Test evaluation for {target} ({model_name}): ROC-AUC={roc_auc:.4f}, Recall={recall:.4f}, F1={f1:.4f}")
        return metrics

    def extract_feature_importance(self, trained_info: Dict[str, Any]) -> pd.DataFrame:
        """
        Extracts feature importances or standardized coefficients from the trained pipeline.
        """
        target = trained_info["target"]
        pipeline = trained_info["best_pipeline"]
        preprocessor = pipeline.named_steps["preprocessor"]
        classifier = pipeline.named_steps["classifier"]

        # Get transformed feature names
        try:
            feature_names = preprocessor.get_feature_names_out()
        except Exception:
            feature_names = [f"feat_{i}" for i in range(100)]

        # Extract weights
        importance_vals = None
        imp_type = "Importance"

        if hasattr(classifier, "feature_importances_"):
            importance_vals = classifier.feature_importances_
            imp_type = "Gini_Importance"
        elif hasattr(classifier, "coef_"):
            importance_vals = np.abs(classifier.coef_[0])
            imp_type = "Absolute_Coefficient"

        if importance_vals is not None and len(feature_names) == len(importance_vals):
            clean_names = [f.replace("num__", "").replace("cat__", "").replace("_", " ").title() for f in feature_names]
            imp_df = pd.DataFrame({
                "Disease": target.replace("_", " ").title(),
                "Feature_Raw": feature_names,
                "Feature_Name": clean_names,
                "Importance_Score": importance_vals.round(4),
                "Metric_Type": imp_type
            }).sort_values(by="Importance_Score", ascending=False)
            return imp_df
        return pd.DataFrame()

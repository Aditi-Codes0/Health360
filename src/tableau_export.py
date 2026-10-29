"""
Health 360: Tableau Data Export Pipeline & Manifest Generator
Prepares, formats, and exports visualization-ready datasets and metadata manifests for Tableau.
"""

from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional
import pandas as pd
from config import settings
from src.utils import setup_logger, save_json

logger = setup_logger("health360.tableau_export")


class TableauExporter:
    """Prepares and validates export datasets tailored specifically for Tableau Desktop/Public."""

    def __init__(self, export_dir: Optional[Path] = None):
        self.export_dir = export_dir or settings.TABLEAU_DIR
        self.export_dir.mkdir(parents=True, exist_ok=True)
        self.manifest_entries: List[Dict[str, Any]] = []

    def export_dataset(self, df: pd.DataFrame, filename: str, description: str,
                       grain: str, target_dashboard: str) -> Path:
        """
        Saves a clean CSV formatted for Tableau and logs its metadata to the manifest.
        """
        out_path = self.export_dir / filename
        # Ensure clean CSV formatting without unnecessary indexes
        df.to_csv(out_path, index=False)

        manifest_entry = {
            "file_name": filename,
            "target_path": str(out_path),
            "description": description,
            "analytical_grain": grain,
            "target_dashboard": target_dashboard,
            "row_count": len(df),
            "column_count": len(df.columns),
            "columns": list(df.columns),
            "generated_at_utc": datetime.now(timezone.utc).isoformat()
        }
        self.manifest_entries.append(manifest_entry)
        logger.info(f"Exported Tableau dataset: {filename} ({len(df)} rows, {len(df.columns)} cols)")
        return out_path

    def export_all_tableau_tables(self,
                                  clean_patient_df: pd.DataFrame,
                                  disease_prev_df: pd.DataFrame,
                                  age_analysis_df: pd.DataFrame,
                                  bmi_analysis_df: pd.DataFrame,
                                  clinical_summary_df: pd.DataFrame,
                                  lifestyle_df: pd.DataFrame,
                                  symptom_df: pd.DataFrame,
                                  corr_df: pd.DataFrame,
                                  risk_associations_df: pd.DataFrame,
                                  pop_segments_df: pd.DataFrame,
                                  model_metrics_df: pd.DataFrame,
                                  feature_imp_df: pd.DataFrame,
                                  data_quality_df: pd.DataFrame) -> Dict[str, Path]:
        """
        Exports all 13 core Tableau-ready datasets and compiles the manifest.
        """
        exported = {}

        # 1. Primary Patient-Level Grain (Core engine for Dashboards 1, 2, 3)
        exported["clean_patient_data"] = self.export_dataset(
            clean_patient_df,
            "clean_patient_data.csv",
            "Granular patient-level cohort containing demographic, clinical, lifestyle, and disease outcomes for interactive slicing.",
            "Patient Grain (1 row per patient)",
            "Dashboard 1, 2, 3"
        )

        # 2. Disease Prevalence Summary
        exported["disease_prevalence"] = self.export_dataset(
            disease_prev_df,
            "disease_prevalence.csv",
            "Summary prevalence counts, rates, and 95% confidence intervals for Heart Disease, Diabetes, and Stroke.",
            "Disease Grain (1 row per disease)",
            "Dashboard 1: Clinical Risk Assessment"
        )

        # 3. Age Group Stratification
        exported["age_group_analysis"] = self.export_dataset(
            age_analysis_df,
            "age_group_analysis.csv",
            "Prevalence and case distribution of chronic diseases across standardized demographic age brackets.",
            "Age Group x Disease Grain",
            "Dashboard 1 & 3: Clinical Risk & Population Insights"
        )

        # 4. BMI Category Stratification
        exported["bmi_category_analysis"] = self.export_dataset(
            bmi_analysis_df,
            "bmi_category_analysis.csv",
            "Chronic disease prevalence across adult WHO/CDC BMI categories (Underweight, Healthy, Overweight, Obesity).",
            "BMI Category x Disease Grain",
            "Dashboard 1 & 3: Clinical Risk & Population Insights"
        )

        # 5. Clinical Biomarker Comparison
        exported["clinical_indicator_summary"] = self.export_dataset(
            clinical_summary_df,
            "clinical_indicator_summary.csv",
            "Comparative central tendency (mean, median, standard deviation) for biomarkers between disease-positive and negative groups.",
            "Biomarker x Disease Status Grain",
            "Dashboard 1: Clinical Risk Assessment"
        )

        # 6. Lifestyle Exposure Analysis
        exported["lifestyle_analysis"] = self.export_dataset(
            lifestyle_df,
            "lifestyle_analysis.csv",
            "Disease prevalence cross-tabulated against smoking habits, alcohol consumption, and physical activity levels.",
            "Lifestyle Factor x Category x Disease Grain",
            "Dashboard 2: Lifestyle & Risk Factor Analysis"
        )

        # 7. Symptom Association Analysis
        exported["symptom_analysis"] = self.export_dataset(
            symptom_df,
            "symptom_analysis.csv",
            "Disease outcomes stratified by presence vs absence of clinical symptoms (Chest Pain, Fatigue, Dizziness).",
            "Symptom x Status x Disease Grain",
            "Dashboard 2: Lifestyle & Risk Factor Analysis"
        )

        # 8. Clinical Correlation Matrix
        # Flatten correlation matrix for easy Tableau heatmap rendering
        corr_flat = corr_df.reset_index().melt(id_vars="index", var_name="Variable_2", value_name="Pearson_Correlation")
        corr_flat.columns = ["Variable_1", "Variable_2", "Pearson_Correlation"]
        exported["correlation_matrix"] = self.export_dataset(
            corr_flat,
            "correlation_matrix.csv",
            "Pairwise Pearson correlation coefficients among continuous clinical indicators and disease flags.",
            "Variable Pair Grain",
            "Dashboard 2: Lifestyle & Risk Factor Analysis"
        )

        # 9. Risk Factor Odds Ratios & Statistical Associations
        exported["risk_factor_associations"] = self.export_dataset(
            risk_associations_df,
            "risk_factor_associations.csv",
            "Contingency odds ratios, 95% confidence intervals, and hypothesis test p-values for major risk factors.",
            "Risk Factor x Disease Grain",
            "Dashboard 2: Lifestyle & Risk Factor Analysis"
        )

        # 10. Composite Population Segments
        exported["population_segments"] = self.export_dataset(
            pop_segments_df,
            "population_segments.csv",
            "Demographic and behavioral risk clusters identifying high-burden population sub-segments.",
            "Age x BMI x Smoking Segment Grain",
            "Dashboard 3: Population Health Insights"
        )

        # 11. Machine Learning Performance Metrics
        exported["model_metrics"] = self.export_dataset(
            model_metrics_df,
            "model_metrics.csv",
            "Predictive model performance on held-out test data (Accuracy, Recall, Specificity, F1, ROC-AUC, PR-AUC).",
            "Model x Disease Grain",
            "Model Performance Specification & Validation"
        )

        # 12. Feature Importance / Risk Predictors
        exported["feature_importance"] = self.export_dataset(
            feature_imp_df,
            "feature_importance.csv",
            "Relative feature importances and standardized risk predictor weights extracted from trained algorithms.",
            "Feature x Disease Grain",
            "Predictive Insights & Feature Drivers"
        )

        # 13. Data Quality Audit Log
        exported["data_quality_report"] = self.export_dataset(
            data_quality_df,
            "data_quality_report.csv",
            "Data cleansing and transformation audit log detailing missingness treatment, derivations, and data types.",
            "Column Grain",
            "Data Governance & Audit"
        )

        # Save the full Tableau Export Manifest
        manifest_path = self.export_dir / "tableau_export_manifest.json"
        save_json({
            "project_name": "Health 360",
            "pipeline_version": "1.0.0",
            "generated_timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "exported_files_count": len(self.manifest_entries),
            "manifest": self.manifest_entries
        }, manifest_path)
        logger.info(f"Tableau Export Manifest generated with {len(self.manifest_entries)} tables at {manifest_path}")

        return exported

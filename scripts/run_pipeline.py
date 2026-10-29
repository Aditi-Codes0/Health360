"""
Health 360: Master End-to-End Pipeline
Executes data ingestion, validation, preprocessing, exploratory analytics,
statistical hypothesis testing, machine learning modeling, Tableau export,
and academic findings generation.
"""

import argparse
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
from config import settings
from src.utils import setup_logger, set_seed
from src.data_loader import DataLoader
from src.data_validation import DataValidator
from src.preprocessing import Preprocessor
from src.eda import ExploratoryDataAnalysis
from src.disease_analysis import DiseaseAnalyzer
from src.risk_factor_analysis import RiskFactorAnalyzer
from src.statistical_analysis import StatisticalAnalyzer
from src.population_analysis import PopulationAnalyzer
from src.prediction import HealthRiskModelManager, Health360RiskPredictor
from src.model_evaluation import ModelEvaluator
from src.tableau_export import TableauExporter
from src.report_generation import ReportGenerator

logger = setup_logger("health360.master_pipeline")


def run_pipeline(raw_file_path: Path = settings.PRIMARY_RAW_FILE, seed: int = settings.RANDOM_STATE):
    """
    Executes the full 9-stage Health 360 data analytics and Tableau export lifecycle.
    """
    logger.info("=" * 80)
    logger.info("STARTING HEALTH 360: CHRONIC DISEASE ANALYTICS & TABLEAU PIPELINE")
    logger.info("=" * 80)
    set_seed(seed)

    # ---------------------------------------------------------
    # STAGE 1: DATA INGESTION & DISCOVERY
    # ---------------------------------------------------------
    logger.info("\n--- [STAGE 1/9] DATA INGESTION & METADATA DISCOVERY ---")
    loader = DataLoader()
    raw_df = loader.load_dataset(raw_file_path)
    profile = loader.inspect_dataset(raw_df, dataset_name=raw_file_path.stem)
    data_dict_df = loader.generate_data_dictionary(raw_df)
    data_dict_path = settings.ANALYTICS_DIR / "data_dictionary.csv"
    data_dict_df.to_csv(data_dict_path, index=False)
    logger.info(f"Dataset Data Dictionary saved to: {data_dict_path}")

    # ---------------------------------------------------------
    # STAGE 2: DATA VALIDATION & AUDIT
    # ---------------------------------------------------------
    logger.info("\n--- [STAGE 2/9] DATA VALIDATION & INTEGRITY AUDITING ---")
    validator = DataValidator()
    validation_audit = validator.run_full_validation_audit(raw_df)

    # ---------------------------------------------------------
    # STAGE 3: PREPROCESSING & QUALITY CONTROL
    # ---------------------------------------------------------
    logger.info("\n--- [STAGE 3/9] DATA CLEANING & REPRODUCIBLE PREPROCESSING ---")
    preprocessor = Preprocessor()
    clean_df, quality_df = preprocessor.clean(raw_df)
    preprocessor.save_clean_data(clean_df, quality_df)

    # ---------------------------------------------------------
    # STAGE 4: EXPLORATORY DATA ANALYSIS (EDA)
    # ---------------------------------------------------------
    logger.info("\n--- [STAGE 4/9] EXPLORATORY DATA ANALYSIS & VISUALIZATION ---")
    eda = ExploratoryDataAnalysis()
    numeric_stats = eda.compute_summary_statistics(clean_df)
    corr_matrix = eda.compute_correlation_matrix(clean_df)
    eda.plot_distributions(clean_df)

    # ---------------------------------------------------------
    # STAGE 5: EPIDEMIOLOGICAL & DISEASE ANALYSIS
    # ---------------------------------------------------------
    logger.info("\n--- [STAGE 5/9] CHRONIC DISEASE PREVALENCE & BIOMARKER CONTRASTS ---")
    disease_analyzer = DiseaseAnalyzer()
    prevalence_df = disease_analyzer.calculate_overall_prevalence(clean_df)
    comorbidity_df = disease_analyzer.analyze_comorbidity_burden(clean_df)
    age_analysis_df = disease_analyzer.analyze_by_demographic(clean_df, stratifier="age_group")
    bmi_analysis_df = disease_analyzer.analyze_by_demographic(clean_df, stratifier="bmi_category")
    clinical_summary_df = disease_analyzer.compare_clinical_indicators(clean_df)

    # ---------------------------------------------------------
    # STAGE 6: RISK FACTOR & INFERENTIAL STATISTICAL TESTING
    # ---------------------------------------------------------
    logger.info("\n--- [STAGE 6/9] LIFESTYLE, SYMPTOMS & INFERENTIAL HYPOTHESIS TESTING ---")
    rf_analyzer = RiskFactorAnalyzer()
    lifestyle_df = rf_analyzer.analyze_lifestyle_factors(clean_df)
    symptom_df = rf_analyzer.analyze_symptoms(clean_df)
    risk_associations_df = rf_analyzer.calculate_odds_ratios(clean_df)

    stat_analyzer = StatisticalAnalyzer()
    inferential_results = stat_analyzer.run_complete_statistical_suite(clean_df)

    # Population segmentation
    pop_analyzer = PopulationAnalyzer()
    pop_segments_df = pop_analyzer.analyze_population_segments(clean_df)

    # ---------------------------------------------------------
    # STAGE 7: MACHINE LEARNING RISK MODELING & EVALUATION
    # ---------------------------------------------------------
    logger.info("\n--- [STAGE 7/9] MACHINE LEARNING RISK PREDICTION & SUBGROUP AUDIT ---")
    model_mgr = HealthRiskModelManager()
    evaluator = ModelEvaluator()

    all_metrics = []
    all_feature_imps = []

    # Train and evaluate models across available chronic targets
    for disease in settings.PRIMARY_DISEASES:
        if disease in clean_df.columns:
            logger.info(f"Building predictive modeling pipeline for: {disease.upper()}")
            trained_info = model_mgr.train_and_select_best_model(clean_df, target_col=disease)
            test_metrics = evaluator.evaluate_test_set(trained_info)
            feat_imp = evaluator.extract_feature_importance(trained_info)

            # Store metrics excluding nested dicts
            clean_metric = {k: v for k, v in test_metrics.items() if k != "Subgroup_Audit"}
            all_metrics.append(clean_metric)
            if not feat_imp.empty:
                all_feature_imps.append(feat_imp)

    model_metrics_df = pd.DataFrame(all_metrics)
    model_metrics_path = settings.ANALYTICS_DIR / "model_metrics.csv"
    model_metrics_df.to_csv(model_metrics_path, index=False)

    feature_imp_df = pd.concat(all_feature_imps, ignore_index=True) if all_feature_imps else pd.DataFrame()
    feature_imp_path = settings.ANALYTICS_DIR / "feature_importance.csv"
    feature_imp_df.to_csv(feature_imp_path, index=False)

    # Demonstrate prediction interface
    if "heart_disease" in model_mgr.trained_pipelines:
        predictor = Health360RiskPredictor(model_mgr.trained_pipelines["heart_disease"], "heart_disease")
        sample_patient = {
            "age": 62, "sex": "Male", "region": "South", "bmi": 32.4, "systolic_bp": 155, "diastolic_bp": 92,
            "cholesterol": 245, "fasting_glucose": 135.0, "smoking_status": "Current",
            "alcohol_consumption": "Moderate", "physical_activity": "Sedentary",
            "fatigue": 1, "chest_pain": 1, "dizziness": 0
        }
        demo_risk = predictor.predict_risk(sample_patient)
        logger.info(f"Sample Patient Model-Estimated Risk Output:\n"
                    f" - Category: {demo_risk['model_estimated_risk_category']}\n"
                    f" - Probability: {demo_risk['estimated_probability_pct']}\n"
                    f" - Binary Class: {demo_risk['predicted_binary_class']}")

    # ---------------------------------------------------------
    # STAGE 8: PYTHON-TO-TABLEAU DATA PIPELINE EXPORT
    # ---------------------------------------------------------
    logger.info("\n--- [STAGE 8/9] PYTHON-TO-TABLEAU DATA EXPORT & MANIFEST GENERATION ---")
    tableau_exporter = TableauExporter()
    exported_files = tableau_exporter.export_all_tableau_tables(
        clean_patient_df=clean_df,
        disease_prev_df=prevalence_df,
        age_analysis_df=age_analysis_df,
        bmi_analysis_df=bmi_analysis_df,
        clinical_summary_df=clinical_summary_df,
        lifestyle_df=lifestyle_df,
        symptom_df=symptom_df,
        corr_df=corr_matrix,
        risk_associations_df=risk_associations_df,
        pop_segments_df=pop_segments_df,
        model_metrics_df=model_metrics_df,
        feature_imp_df=feature_imp_df,
        data_quality_df=quality_df
    )

    # ---------------------------------------------------------
    # STAGE 9: ACADEMIC FINDINGS & EXECUTIVE REPORT GENERATION
    # ---------------------------------------------------------
    logger.info("\n--- [STAGE 9/9] ACADEMIC FINDINGS & EXECUTIVE REPORT COMPILATION ---")
    reporter = ReportGenerator()
    report_file = reporter.generate_executive_report(
        clean_df=clean_df,
        prevalence_df=prevalence_df,
        age_df=age_analysis_df,
        bmi_df=bmi_analysis_df,
        clinical_df=clinical_summary_df,
        lifestyle_df=lifestyle_df,
        symptom_df=symptom_df,
        risk_associations_df=risk_associations_df,
        model_metrics_df=model_metrics_df,
        quality_df=quality_df
    )

    logger.info("=" * 80)
    logger.info("HEALTH 360 PIPELINE EXECUTION COMPLETED SUCCESSFULLY!")
    logger.info(f"Clean Patient Data:    {settings.CLEAN_PATIENT_FILE}")
    logger.info(f"Tableau Exports:       {settings.TABLEAU_DIR} ({len(exported_files)} datasets)")
    logger.info(f"Analytical Report:     {report_file}")
    logger.info("=" * 80)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Health 360 Master Analytics Pipeline")
    parser.add_argument("--raw-file", type=str, default=str(settings.PRIMARY_RAW_FILE),
                        help="Path to raw patient cohort CSV")
    parser.add_argument("--seed", type=int, default=settings.RANDOM_STATE,
                        help="Random seed for reproducibility")
    args = parser.parse_args()

    run_pipeline(raw_file_path=Path(args.raw_file), seed=args.seed)

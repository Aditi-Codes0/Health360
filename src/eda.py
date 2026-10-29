"""
Health 360: Exploratory Data Analysis (EDA) Module
Calculates descriptive statistics, distributions, and produces summary figures.
"""

from pathlib import Path
from typing import Dict, Any, List, Optional
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for server/script safety
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from config import settings
from src.utils import setup_logger

logger = setup_logger("health360.eda")


class ExploratoryDataAnalysis:
    """Performs structured exploratory data analysis on cleaned patient cohorts."""

    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = output_dir or settings.ANALYTICS_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)
        # Apply standard healthcare visual theme
        sns.set_theme(style="whitegrid", palette="Blues_r")

    def compute_summary_statistics(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculates comprehensive summary statistics for numeric variables.
        Includes count, mean, std, median, IQR, min, max, skewness, and kurtosis.
        """
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        stats_list = []

        for col in numeric_cols:
            if col in ["patient_id"]:
                continue
            series = df[col].dropna()
            q25 = series.quantile(0.25)
            q75 = series.quantile(0.75)
            stats_list.append({
                "Variable": col,
                "Observations": int(len(series)),
                "Mean": round(float(series.mean()), 2),
                "Std Dev": round(float(series.std()), 2),
                "Median": round(float(series.median()), 2),
                "IQR": round(float(q75 - q25), 2),
                "Min": round(float(series.min()), 2),
                "Max": round(float(series.max()), 2),
                "Skewness": round(float(series.skew()), 3),
                "Kurtosis": round(float(series.kurtosis()), 3)
            })

        summary_df = pd.DataFrame(stats_list)
        summary_path = self.output_dir / "numeric_summary_statistics.csv"
        summary_df.to_csv(summary_path, index=False)
        logger.info(f"Summary statistics calculated and saved to {summary_path}")
        return summary_df

    def compute_categorical_distributions(self, df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """Calculates value counts and proportions for all categorical variables."""
        cat_cols = df.select_dtypes(include=["object", "string", "category"]).columns
        dist_dict = {}

        for col in cat_cols:
            if col == "patient_id":
                continue
            counts = df[col].value_counts(dropna=False).reset_index()
            counts.columns = [col, "Count"]
            counts["Percentage"] = (counts["Count"] / len(df) * 100).round(2)
            dist_dict[col] = counts

        return dist_dict

    def compute_correlation_matrix(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculates Pearson correlation matrix for numeric clinical variables.
        """
        numeric_clinical = [
            col for col in ["age", "bmi", "systolic_bp", "diastolic_bp", "cholesterol", "fasting_glucose", 
                            "heart_disease", "diabetes", "stroke", "fatigue", "chest_pain", "dizziness"]
            if col in df.columns
        ]
        corr_matrix = df[numeric_clinical].corr(method="pearson").round(3)
        corr_path = self.output_dir / "correlation_matrix.csv"
        corr_matrix.to_csv(corr_path)
        logger.info(f"Correlation matrix computed and saved to {corr_path}")
        return corr_matrix

    def plot_distributions(self, df: pd.DataFrame, figures_dir: Optional[Path] = None) -> List[Path]:
        """Generates distribution plots for clinical variables."""
        save_dir = figures_dir or (self.output_dir / "figures")
        save_dir.mkdir(parents=True, exist_ok=True)
        generated_plots = []

        clinical_vars = ["age", "bmi", "systolic_bp", "diastolic_bp", "cholesterol", "fasting_glucose"]
        available_vars = [v for v in clinical_vars if v in df.columns]

        # 1. Multi-panel Histogram / KDE
        fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(15, 9))
        axes = axes.flatten()

        for idx, col in enumerate(available_vars):
            sns.histplot(df[col], kde=True, ax=axes[idx], color="#1E88E5", bins=25)
            axes[idx].set_title(f"Distribution of {col.replace('_', ' ').title()}", fontsize=12, fontweight="bold")
            axes[idx].set_xlabel(col)
            axes[idx].set_ylabel("Patient Count")

        plt.tight_layout()
        dist_plot_path = save_dir / "clinical_distributions.png"
        plt.savefig(dist_plot_path, dpi=300)
        plt.close()
        generated_plots.append(dist_plot_path)

        # 2. Correlation Heatmap
        corr = self.compute_correlation_matrix(df)
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr, annot=True, cmap="Blues", fmt=".2f", cbar=True, vmin=-0.2, vmax=1.0)
        plt.title("Health 360: Clinical Variable Correlation Heatmap", fontsize=14, fontweight="bold", pad=12)
        plt.tight_layout()
        corr_plot_path = save_dir / "correlation_heatmap.png"
        plt.savefig(corr_plot_path, dpi=300)
        plt.close()
        generated_plots.append(corr_plot_path)

        logger.info(f"Generated {len(generated_plots)} EDA visual figures in {save_dir}")
        return generated_plots

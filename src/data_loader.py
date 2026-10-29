"""
Health 360: Data Ingestion & Metadata Discovery
Handles multi-format ingestion, provenance tracking, and column schema discovery.
"""

from pathlib import Path
from typing import Dict, Any, Tuple, Optional
import pandas as pd
from config import settings
from src.utils import setup_logger, load_json

logger = setup_logger("health360.data_loader")


class DataLoader:
    """Manages robust loading, schema discovery, and validation of raw healthcare datasets."""

    def __init__(self, field_mapping_path: Optional[Path] = None):
        self.field_mapping_path = field_mapping_path or settings.FIELD_MAPPING_FILE
        self.field_mapping = self._load_field_mapping()

    def _load_field_mapping(self) -> Dict[str, Any]:
        """Loads field mapping configuration."""
        try:
            return load_json(self.field_mapping_path)
        except Exception as e:
            logger.warning(f"Could not load field mapping from {self.field_mapping_path}: {e}")
            return {"datasets": {}}

    def load_dataset(self, file_path: Path) -> pd.DataFrame:
        """
        Loads CSV or Excel data file into a Pandas DataFrame with validation.
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"Requested dataset file does not exist: {file_path}")

        logger.info(f"Loading dataset from: {file_path}")
        suffix = file_path.suffix.lower()

        try:
            if suffix in [".csv", ".txt"]:
                df = pd.read_csv(file_path)
            elif suffix in [".xlsx", ".xls"]:
                df = pd.read_excel(file_path)
            else:
                raise ValueError(f"Unsupported file format '{suffix}'. Supported formats: .csv, .xlsx, .xls")
        except Exception as err:
            logger.error(f"Failed to read dataset file {file_path}: {err}")
            raise

        logger.info(f"Successfully loaded dataset with shape: {df.shape[0]} rows, {df.shape[1]} columns.")
        return df

    def inspect_dataset(self, df: pd.DataFrame, dataset_name: str = "primary_cohort") -> Dict[str, Any]:
        """
        Inspects dataset schema, types, missing values, and identifies available capabilities.
        """
        cols = df.columns.tolist()
        missing_counts = df.isnull().sum().to_dict()
        missing_pcts = (df.isnull().mean() * 100).round(2).to_dict()
        dtypes = {col: str(dtype) for col, dtype in df.dtypes.items()}

        # Check target variables
        targets_present = [d for d in settings.PRIMARY_DISEASES if d in cols]
        
        # Check clinical indicators
        clinical_keys = ["bmi", "systolic_bp", "diastolic_bp", "cholesterol", "fasting_glucose"]
        clinical_present = [c for c in clinical_keys if c in cols]

        # Check lifestyle indicators
        lifestyle_keys = ["smoking_status", "alcohol_consumption", "physical_activity"]
        lifestyle_present = [l for l in lifestyle_keys if l in cols]

        # Check symptoms
        symptom_keys = ["fatigue", "chest_pain", "dizziness"]
        symptoms_present = [s for s in symptom_keys if s in cols]

        # Demographic indicators
        demo_keys = ["patient_id", "age", "sex", "region", "observation_year"]
        demo_present = [dm for dm in demo_keys if dm in cols]

        capabilities = {
            "can_analyze_disease_prevalence": len(targets_present) > 0,
            "target_diseases": targets_present,
            "can_analyze_clinical_vitals": len(clinical_present) > 0,
            "available_clinical": clinical_present,
            "can_analyze_lifestyle": len(lifestyle_present) > 0,
            "available_lifestyle": lifestyle_present,
            "can_analyze_symptoms": len(symptoms_present) > 0,
            "available_symptoms": symptoms_present,
            "can_stratify_demographics": "age" in cols,
            "can_train_ml_model": len(targets_present) > 0 and len(clinical_present) > 0
        }

        profile = {
            "dataset_name": dataset_name,
            "rows": len(df),
            "columns_count": len(cols),
            "columns": cols,
            "dtypes": dtypes,
            "missing_counts": missing_counts,
            "missing_percentages": missing_pcts,
            "capabilities": capabilities
        }

        logger.info(f"Dataset profile summary for '{dataset_name}': {len(targets_present)} disease targets, "
                    f"{len(clinical_present)} clinical fields, {len(lifestyle_present)} lifestyle fields.")
        return profile

    def generate_data_dictionary(self, df: pd.DataFrame, dataset_key: str = "health360_primary_cohort") -> pd.DataFrame:
        """
        Generates a documented data dictionary table for the loaded dataset.
        """
        meta_dict = {}
        if "datasets" in self.field_mapping and dataset_key in self.field_mapping["datasets"]:
            meta_dict = {
                f["source_column"]: f 
                for f in self.field_mapping["datasets"][dataset_key].get("fields", [])
            }

        dict_rows = []
        for col in df.columns:
            meta = meta_dict.get(col, {})
            non_null = df[col].dropna()
            sample_val = str(non_null.iloc[0]) if len(non_null) > 0 else "N/A"
            unique_count = df[col].nunique()
            missing_pct = round(df[col].isnull().mean() * 100, 2)

            dict_rows.append({
                "Column Name": col,
                "Standardized Name": meta.get("standardized_name", col),
                "Data Type": str(df[col].dtype),
                "Units": meta.get("units", "unspecified"),
                "Description": meta.get("description", "Observation measurement"),
                "Missing %": f"{missing_pct}%",
                "Unique Values": unique_count,
                "Sample Value": sample_val,
                "Treatment Strategy": meta.get("missing_value_treatment", "impute_or_flag")
            })

        return pd.DataFrame(dict_rows)

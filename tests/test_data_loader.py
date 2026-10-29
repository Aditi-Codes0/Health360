"""
Health 360: Unit Tests for Data Ingestion & Metadata Discovery
"""

import pytest
import pandas as pd
from pathlib import Path
from src.data_loader import DataLoader
from src.data_validation import DataValidator
from config import settings


@pytest.fixture
def loader():
    return DataLoader()


@pytest.fixture
def sample_raw_df():
    return pd.DataFrame({
        "patient_id": ["P001", "P002", "P003", "P004"],
        "age": [25, 45, 65, 75],
        "sex": ["Male", "Female", "Male", "Female"],
        "bmi": [22.4, 28.1, 33.5, None],
        "systolic_bp": [115, 130, 155, 140],
        "heart_disease": [0, 0, 1, 1],
        "diabetes": [0, 1, 1, 0],
        "stroke": [0, 0, 1, 0]
    })


def test_load_dataset_nonexistent(loader):
    """Verify FileNotFoundError is raised when file does not exist."""
    with pytest.raises(FileNotFoundError):
        loader.load_dataset(Path("non_existent_file.csv"))


def test_inspect_dataset_capabilities(loader, sample_raw_df):
    """Verify schema profiling and capability detection."""
    profile = loader.inspect_dataset(sample_raw_df, dataset_name="sample")
    assert profile["rows"] == 4
    assert profile["columns_count"] == 8
    assert profile["capabilities"]["can_analyze_disease_prevalence"] is True
    assert "heart_disease" in profile["capabilities"]["target_diseases"]
    assert profile["capabilities"]["can_train_ml_model"] is True


def test_data_dictionary_generation(loader, sample_raw_df):
    """Verify data dictionary generation has all columns."""
    dict_df = loader.generate_data_dictionary(sample_raw_df)
    assert len(dict_df) == len(sample_raw_df.columns)
    assert "Column Name" in dict_df.columns
    assert "Data Type" in dict_df.columns


def test_validator_duplicates():
    """Verify duplicate detection."""
    validator = DataValidator()
    df_dup = pd.DataFrame({
        "patient_id": ["P1", "P1", "P2"],
        "val": [10, 10, 20]
    })
    res = validator.check_duplicates(df_dup, id_col="patient_id")
    assert res["has_duplicates"] is True
    assert res["duplicate_ids"] == 1

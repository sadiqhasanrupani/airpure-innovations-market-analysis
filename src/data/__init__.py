"""
AirPure Innovations Data Processing Package

This package contains data cleaning and processing utilities for the AirPure Innovations project.

Modules:
    - pipeline: Main data cleaning pipeline
    - validators: Data validation utilities
    - transformers: Data transformation utilities
    - io_utils: Input/output utilities

Author: Sadiq (Solo Data Analyst)
Date: July 13, 2025
"""

from .pipeline import (
    DataCleaningPipeline,
    run_cleaning_pipeline,
    clean_idsp_dataset,
    clean_aqi_dataset,
    clean_population_dataset,
    clean_vahan_dataset
)

from .validators import (
    validate_dataframe_structure,
    check_logical_consistency,
    validate_date_columns,
    detect_outliers
)

from .transformers import (
    standardize_dates,
    handle_missing_values,
    normalize_text_columns,
    derive_date_features
)

from .io_utils import (
    safe_read_csv,
    detect_encoding,
    export_data_quality_report,
    save_cleaned_data
)

__version__ = "1.0.0"
__author__ = "Sadiq (Solo Data Analyst)"

# Package-level configuration
DEFAULT_CONFIG = {
    "inconsistency_threshold": 0.2,
    "output_dir": "cleaned",
    "inconsistency_dir": "inconsistencies",
    "log_level": "INFO",
    "memory_threshold_mb": 1000,
}

__all__ = [
    # Main pipeline
    "DataCleaningPipeline",
    "run_cleaning_pipeline",
    
    # Dataset-specific cleaners
    "clean_idsp_dataset",
    "clean_aqi_dataset", 
    "clean_population_dataset",
    "clean_vahan_dataset",
    
    # Validators
    "validate_dataframe_structure",
    "check_logical_consistency",
    "validate_date_columns",
    "detect_outliers",
    
    # Transformers
    "standardize_dates",
    "handle_missing_values",
    "normalize_text_columns",
    "derive_date_features",
    
    # I/O utilities
    "safe_read_csv",
    "detect_encoding",
    "export_data_quality_report",
    "save_cleaned_data",
    
    # Configuration
    "DEFAULT_CONFIG",
]

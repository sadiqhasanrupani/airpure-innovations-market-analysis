"""
Enhanced Data Cleaning Pipeline for AirPure Innovations
Author: Sadiq (Solo Data Analyst)
Date: July 13, 2025

This enhanced version includes:
- Improved error handling and logging
- Configuration management
- Comprehensive data validation
- Memory optimization
- Extended data profiling
"""

import pandas as pd
import numpy as np
import os
import logging
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any
import chardet
import warnings

warnings.filterwarnings("ignore")

# 📋 Configuration
CONFIG = {
    "inconsistency_threshold": 0.2,
    "output_dir": "cleaned",
    "inconsistency_dir": "inconsistencies",
    "log_level": "INFO",
    "memory_threshold_mb": 1000,
}

# 📁 Setup directories and logging
def setup_environment():
    """Initialize directories and logging configuration"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create necessary directories
    for dir_name in [CONFIG["output_dir"], CONFIG["inconsistency_dir"], "logs"]:
        dir_path = os.path.join(base_dir, dir_name)
        os.makedirs(dir_path, exist_ok=True)
    
    # Setup logging
    log_file = os.path.join(base_dir, "logs", f"data_cleaning_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    logging.basicConfig(
        level=getattr(logging, CONFIG["log_level"]),
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    return base_dir

# 📂 File path management
def get_file_paths(base_dir: str) -> Dict[str, str]:
    """Get absolute file paths for all datasets"""
    data_dir = os.path.join(base_dir, "../../data/raw")
    return {
        "aqi": os.path.join(data_dir, "aqi.csv"),
        "idsp": os.path.join(data_dir, "idsp.csv"),
        "pp": os.path.join(data_dir, "population_projection.csv"),
        "vahan": os.path.join(data_dir, "vahan.csv"),
    }

# 🔍 Enhanced encoding detection
def detect_encoding(path: str) -> str:
    """Detect file encoding with enhanced error handling"""
    try:
        with open(path, "rb") as f:
            result = chardet.detect(f.read(100000))
        encoding = result.get("encoding", "utf-8")
        confidence = result.get("confidence", 0)
        
        logging.info(f"Detected encoding: {encoding} (confidence: {confidence:.2f})")
        return encoding
    except Exception as e:
        logging.warning(f"Encoding detection failed: {e}. Using utf-8 as fallback.")
        return "utf-8"

def safe_read_csv(path: str) -> pd.DataFrame:
    """Read CSV with multiple encoding fallbacks and validation"""
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    
    encodings = [detect_encoding(path), "utf-8", "latin1", "cp1252"]
    
    for encoding in encodings:
        try:
            df = pd.read_csv(path, encoding=encoding)
            logging.info(f"Successfully read {path} with {encoding} encoding")
            return df
        except UnicodeDecodeError:
            continue
        except Exception as e:
            logging.error(f"Failed to read {path}: {e}")
            raise
    
    raise ValueError(f"Could not read {path} with any encoding")

# 📊 Data profiling and validation
def profile_dataframe(df: pd.DataFrame, name: str) -> Dict[str, Any]:
    """Generate comprehensive data profile"""
    profile = {
        "name": name,
        "shape": df.shape,
        "memory_usage_mb": df.memory_usage(deep=True).sum() / (1024**2),
        "missing_values": df.isnull().sum().to_dict(),
        "duplicate_rows": df.duplicated().sum(),
        "dtypes": df.dtypes.to_dict(),
        "numeric_columns": df.select_dtypes(include=[np.number]).columns.tolist(),
        "datetime_columns": df.select_dtypes(include=['datetime64']).columns.tolist(),
        "object_columns": df.select_dtypes(include=['object']).columns.tolist(),
    }
    
    # Add basic statistics for numeric columns
    if profile["numeric_columns"]:
        profile["numeric_stats"] = df[profile["numeric_columns"]].describe().to_dict()
    
    logging.info(f"Data profile for {name}: {profile['shape'][0]} rows, {profile['shape'][1]} columns")
    return profile

def validate_dataframe_structure(df: pd.DataFrame, expected_columns: List[str], name: str) -> bool:
    """Validate dataframe has expected structure"""
    missing_cols = set(expected_columns) - set(df.columns)
    extra_cols = set(df.columns) - set(expected_columns)
    
    if missing_cols:
        logging.warning(f"{name}: Missing columns: {missing_cols}")
    if extra_cols:
        logging.info(f"{name}: Extra columns found: {extra_cols}")
    
    return len(missing_cols) == 0

# 🧼 Enhanced logical consistency checker
def check_and_fix_logical_inconsistency(
    df: pd.DataFrame, 
    col_a: str, 
    col_b: str, 
    condition: callable, 
    name: str, 
    swap: bool = False, 
    threshold: float = None
) -> pd.DataFrame:
    """Enhanced logical consistency checker with better reporting"""
    threshold = threshold or CONFIG["inconsistency_threshold"]
    
    if col_a not in df.columns or col_b not in df.columns:
        logging.error(f"Columns {col_a} or {col_b} not found in dataframe")
        return df
    
    mask = condition(df)
    count = mask.sum()
    ratio = count / len(df) if len(df) > 0 else 0
    
    logging.info(f"🔎 Checking logical consistency: {name}")
    logging.info(f"Found {count} inconsistent rows out of {len(df)} ({ratio*100:.2f}%)")
    
    inconsistent_rows = df[mask].copy()
    
    if ratio >= threshold:
        logging.warning("⚠️ HIGH INCONSISTENCY WARNING!")
        logging.warning(f"❌ Skipping auto-fix: {ratio*100:.2f}% inconsistency rate exceeds threshold ({threshold*100}%)")
        
        # Export inconsistent rows
        output_file = os.path.join(CONFIG["inconsistency_dir"], f"{name.replace(' ', '_').lower()}_inconsistent.csv")
        inconsistent_rows.to_csv(output_file, index=False)
        logging.info(f"Exported inconsistent rows to: {output_file}")
        return df
    
    if swap and count > 0:
        # Only swap non-null values
        valid_swap_mask = mask & df[col_a].notna() & df[col_b].notna()
        df.loc[valid_swap_mask, [col_a, col_b]] = df.loc[valid_swap_mask, [col_b, col_a]].values
        logging.info(f"✅ Fixed {valid_swap_mask.sum()} rows by swapping values")
    
    return df

# 🧹 Enhanced duplicate handler
def handle_duplicates(df: pd.DataFrame, subset_cols: List[str], name: str) -> pd.DataFrame:
    """Enhanced duplicate detection and handling"""
    logging.info(f"🔍 Checking for duplicates in {name} based on: {subset_cols}")
    
    # Check if subset columns exist
    missing_cols = set(subset_cols) - set(df.columns)
    if missing_cols:
        logging.warning(f"Subset columns not found: {missing_cols}. Skipping duplicate check.")
        return df
    
    initial_count = len(df)
    
    # Handle exact duplicates
    exact_dupes = df.duplicated()
    exact_dupe_count = exact_dupes.sum()
    
    if exact_dupe_count > 0:
        df = df[~exact_dupes]
        logging.info(f"📌 Removed {exact_dupe_count} exact duplicates")
    
    # Handle partial duplicates
    partial_dupes = df.duplicated(subset=subset_cols, keep=False)
    partial_dupe_count = partial_dupes.sum()
    
    if partial_dupe_count > 0:
        logging.warning(f"⚠️ Found {partial_dupe_count} partial duplicates")
        output_file = os.path.join(CONFIG["inconsistency_dir"], f"{name.lower()}_partial_duplicates.csv")
        df[partial_dupes].to_csv(output_file, index=False)
        logging.info(f"Exported partial duplicates to: {output_file}")
    
    final_count = len(df)
    logging.info(f"Duplicate handling complete: {initial_count} -> {final_count} rows")
    
    return df

# 📅 Enhanced week validator
def add_week_validation_flag(df: pd.DataFrame) -> pd.DataFrame:
    """Enhanced week validation with better error handling"""
    if "reporting_date" not in df.columns:
        logging.warning("reporting_date column not found. Skipping week validation.")
        return df
    
    if not pd.api.types.is_datetime64_any_dtype(df["reporting_date"]):
        logging.warning("reporting_date is not datetime type. Skipping week validation.")
        return df
    
    # Calculate ISO week
    df["iso_week"] = df["reporting_date"].dt.isocalendar().week
    df["week_is_valid"] = df["week"] == df["iso_week"]
    
    valid_count = df["week_is_valid"].sum()
    total_count = len(df)
    mismatch_rate = 1 - (valid_count / total_count) if total_count > 0 else 0
    
    logging.info(f"🗓️ Week validation: {valid_count}/{total_count} valid ({(1-mismatch_rate)*100:.2f}%)")
    
    if mismatch_rate >= CONFIG["inconsistency_threshold"]:
        logging.warning("❌ High week mismatch rate. Exporting for manual review.")
        output_file = os.path.join(CONFIG["inconsistency_dir"], "week_mismatch.csv")
        df[~df["week_is_valid"]].to_csv(output_file, index=False)
        logging.info(f"Exported week mismatches to: {output_file}")
    else:
        df["original_week"] = df["week"]
        df["week"] = df["iso_week"]
        logging.info("✅ Week column corrected using ISO week")
    
    return df

# 🔧 Memory monitoring
def monitor_memory_usage(df: pd.DataFrame, stage: str):
    """Monitor and log memory usage"""
    memory_mb = df.memory_usage(deep=True).sum() / (1024**2)
    logging.info(f"Memory usage at {stage}: {memory_mb:.2f} MB")
    
    if memory_mb > CONFIG["memory_threshold_mb"]:
        logging.warning(f"High memory usage detected: {memory_mb:.2f} MB")

# 🧪 Enhanced data cleaning pipeline
def clean_idsp_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Clean IDSP dataset with comprehensive validation"""
    logging.info("📊 Starting IDSP dataset cleaning")
    monitor_memory_usage(df, "IDSP initial")
    
    # Expected columns for IDSP
    expected_cols = ["year", "week", "outbreak_starting_date", "reporting_date", 
                    "state", "district", "disease_illness_name", "status", "cases", "deaths"]
    
    validate_dataframe_structure(df, expected_cols, "IDSP")
    
    # Convert date columns
    date_columns = ["reporting_date", "outbreak_starting_date"]
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
            null_dates = df[col].isnull().sum()
            if null_dates > 0:
                logging.warning(f"Found {null_dates} null dates in {col}")
    
    # Logical consistency checks
    df = check_and_fix_logical_inconsistency(
        df=df,
        col_a="reporting_date",
        col_b="outbreak_starting_date",
        condition=lambda df: df["reporting_date"] < df["outbreak_starting_date"],
        name="Reporting Date vs Outbreak Starting Date",
        swap=True
    )
    
    df = check_and_fix_logical_inconsistency(
        df=df,
        col_a="deaths",
        col_b="cases",
        condition=lambda df: df["deaths"] > df["cases"],
        name="Deaths vs Cases",
        swap=False  # Don't swap deaths and cases, just flag
    )
    
    # Week validation
    if "week" in df.columns:
        df = add_week_validation_flag(df)
    
    # Handle duplicates
    df = handle_duplicates(df, 
                          subset_cols=["reporting_date", "outbreak_starting_date", 
                                     "state", "district", "disease_illness_name"],
                          name="IDSP")
    
    monitor_memory_usage(df, "IDSP final")
    logging.info("✅ IDSP dataset cleaning complete")
    
    return df

def run_enhanced_cleaning_pipeline():
    """Run the enhanced data cleaning pipeline"""
    start_time = datetime.now()
    logging.info("🚀 Starting Enhanced Data Cleaning Pipeline")
    
    # Setup environment
    base_dir = setup_environment()
    file_paths = get_file_paths(base_dir)
    
    # Initialize results dictionary
    results = {
        "start_time": start_time,
        "datasets_processed": [],
        "profiles": {},
        "errors": []
    }
    
    try:
        # Load datasets
        logging.info("📂 Loading datasets...")
        datasets = {}
        
        for name, path in file_paths.items():
            try:
                if os.path.exists(path):
                    datasets[name] = safe_read_csv(path)
                    results["datasets_processed"].append(name)
                    
                    # Generate profile
                    profile = profile_dataframe(datasets[name], name)
                    results["profiles"][name] = profile
                    
                    logging.info(f"✅ Loaded {name}: {profile['shape']}")
                else:
                    logging.warning(f"⚠️ File not found: {path}")
            except Exception as e:
                error_msg = f"Failed to load {name}: {str(e)}"
                logging.error(error_msg)
                results["errors"].append(error_msg)
        
        # Clean IDSP dataset (primary focus)
        if "idsp" in datasets:
            datasets["idsp_cleaned"] = clean_idsp_dataset(datasets["idsp"])
            
            # Save cleaned dataset
            output_path = os.path.join(base_dir, CONFIG["output_dir"], "cleaned_idsp.csv")
            datasets["idsp_cleaned"].to_csv(output_path, index=False)
            logging.info(f"💾 Saved cleaned IDSP dataset to: {output_path}")
        
        # Generate final report
        end_time = datetime.now()
        duration = end_time - start_time
        
        results.update({
            "end_time": end_time,
            "duration_seconds": duration.total_seconds(),
            "success": len(results["errors"]) == 0
        })
        
        # Save processing report
        report_path = os.path.join(base_dir, "logs", f"cleaning_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        with open(report_path, 'w') as f:
            f.write(f"Data Cleaning Pipeline Report\n")
            f.write(f"Started: {start_time}\n")
            f.write(f"Completed: {end_time}\n")
            f.write(f"Duration: {duration}\n")
            f.write(f"Datasets Processed: {', '.join(results['datasets_processed'])}\n")
            f.write(f"Errors: {len(results['errors'])}\n")
            for error in results["errors"]:
                f.write(f"  - {error}\n")
        
        logging.info(f"🎉 Pipeline completed successfully in {duration}")
        return results
        
    except Exception as e:
        error_msg = f"Pipeline failed: {str(e)}"
        logging.error(error_msg)
        results["errors"].append(error_msg)
        results["success"] = False
        return results

# 🔧 Main execution
if __name__ == "__main__":
    results = run_enhanced_cleaning_pipeline()
    
    if results["success"]:
        print("✅ Data cleaning pipeline completed successfully!")
    else:
        print("❌ Data cleaning pipeline completed with errors:")
        for error in results["errors"]:
            print(f"  - {error}")

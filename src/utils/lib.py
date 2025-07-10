import pandas as pd
import numpy as np

def detailed_data_quality_report(df, table_name='Dataset', target_col=None, expected_categories=None):
    rows = []
    total_rows = len(df)
    total_cells = df.size

    # 1. Missing Values
    for col in df.columns:
        missing_count = df[col].isnull().sum()
        if missing_count > 0:
            rows.append({
                'Table': table_name,
                'Column': col,
                'Issue': 'Missing Values',
                'Row Count': int(missing_count),
                'Magnitude (%)': round((missing_count / total_rows) * 100, 2),
                'Solvable?': 'Yes',
                'Resolution Suggestion': 'Impute with mean/median/mode or drop rows'
            })

    # 2. Duplicate Rows
    dup_count = df.duplicated().sum()
    if dup_count > 0:
        rows.append({
            'Table': table_name,
            'Column': 'ALL',
            'Issue': 'Duplicate Rows',
            'Row Count': int(dup_count),
            'Magnitude (%)': round((dup_count / total_rows) * 100, 2),
            'Solvable?': 'Yes',
            'Resolution Suggestion': 'Use df.drop_duplicates()'
        })

    # 3. Outliers (Numerical Columns using IQR)
    numeric_cols = df.select_dtypes(include=[np.number])
    for col in numeric_cols.columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        outliers = df[(df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)]
        outlier_count = len(outliers)
        if outlier_count > 0:
            rows.append({
                'Table': table_name,
                'Column': col,
                'Issue': 'Outliers',
                'Row Count': outlier_count,
                'Magnitude (%)': round((outlier_count / total_rows) * 100, 2),
                'Solvable?': 'Yes',
                'Resolution Suggestion': 'Cap, transform, or remove extreme values'
            })

    # 4. Inconsistent Categories
    if expected_categories:
        for col, expected_vals in expected_categories.items():
            if col in df.columns:
                actual_vals = set(df[col].dropna().unique())
                unexpected = actual_vals - set(expected_vals)
                if unexpected:
                    count_unexpected = df[col].isin(unexpected).sum()
                    rows.append({
                        'Table': table_name,
                        'Column': col,
                        'Issue': f'Inconsistent Categories: {list(unexpected)}',
                        'Row Count': count_unexpected,
                        'Magnitude (%)': round((count_unexpected / total_rows) * 100, 2),
                        'Solvable?': 'Yes',
                        'Resolution Suggestion': f'Map or replace with valid categories: {expected_vals}'
                    })

    # 5. Class Imbalance (Optional)
    if target_col and target_col in df.columns:
        value_counts = df[target_col].value_counts(normalize=True) * 100
        imbalance = value_counts.max() - value_counts.min()
        if imbalance > 40:  # Heuristic threshold
            rows.append({
                'Table': table_name,
                'Column': target_col,
                'Issue': 'Class Imbalance',
                'Row Count': None,
                'Magnitude (%)': round(imbalance, 2),
                'Solvable?': 'Yes',
                'Resolution Suggestion': 'Apply resampling: SMOTE, oversampling, or undersampling'
            })

    # Return as DataFrame
    return pd.DataFrame(rows)

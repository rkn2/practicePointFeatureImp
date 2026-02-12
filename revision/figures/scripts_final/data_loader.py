"""
Helper function for loading data with robust path checking.
This can be imported by all figure generation scripts.
"""
import pandas as pd
import os

def load_processed_data():
    """
    Load processed_data.csv from multiple possible locations.
    Returns DataFrame if found, None otherwise.
    """
    data_paths = [
        '../../../processed_data.csv',        # From scripts_final (3 levels up to root)
        '../../processed_data.csv',           # From scripts_final (2 levels up)
        '../processed_data.csv',              # One level up
        'processed_data.csv',                 # Current directory
    ]
    
    for path in data_paths:
        if os.path.exists(path):
            df = pd.read_csv(path)
            print(f"✓ Loaded data from: {path}")
            return df
    
    print("✗ Error: processed_data.csv not found in any expected location.")
    print("  Searched:", data_paths)
    return None

def load_heritage_data():
    """
    Load heritage_data.csv from multiple possible locations.
    Returns DataFrame if found, None otherwise.
    """
    data_paths = [
        '../../../heritage_data.csv',         # From scripts_final (3 levels up to root)
        '../../heritage_data.csv',            # From scripts_final (2 levels up)
        '../heritage_data.csv',               # One level up
        'heritage_data.csv',                  # Current directory
    ]
    
    for path in data_paths:
        if os.path.exists(path):
            df = pd.read_csv(path)
            print(f"✓ Loaded data from: {path}")
            return df
    
    print("✗ Error: heritage_data.csv not found in any expected location.")
    print("  Searched:", data_paths)
    return None

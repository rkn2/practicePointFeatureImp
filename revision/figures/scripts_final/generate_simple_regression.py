"""
Generate simple_regression.png
Shows simple linear regression of Condition Rating vs Crack Width.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os

def generate_simple_regression():
    # Load data - check multiple locations
    data_paths = [
        '../../processed_data.csv',           # From scripts_final
        '../../../processed_data.csv',        # From scripts_final (alternative)
        'processed_data.csv',                 # Current directory
        '../processed_data.csv',              # One level up
    ]
    
    df = None
    for path in data_paths:
        if os.path.exists(path):
            df = pd.read_csv(path)
            print(f"Loaded data from: {path}")
            break
    
    if df is None:
        print("Error: processed_data.csv not found in any expected location.")
        print("Searched:", data_paths)
        return
    
    # Set style
    sns.set_style("white")
    
    # Variables
    predictor = 'Crack_Width_mm'
    outcome = 'Condition_Rating'
    
    # Prepare data (remove missing values)
    data_clean = df[[predictor, outcome]].dropna()
    X = data_clean[predictor]
    Y = data_clean[outcome]
    
    # Perform linear regression
    slope, intercept, r_value, p_value, std_err = stats.linregress(X, Y)
    
    # Create plot
    plt.figure(figsize=(10, 6))
    plt.grid(False)
    
    # Scatter plot with condition colors
    scatter = plt.scatter(X, Y, alpha=0.6, s=60, c=Y, cmap='viridis')
    
    # Plot regression line
    x_line = np.linspace(X.min(), X.max(), 100)
    y_line = slope * x_line + intercept
    plt.plot(x_line, y_line, 'r-', linewidth=3, label='Best Fit Line')
    
    plt.xlabel('Crack Width (mm)', fontsize=12)
    plt.ylabel('Condition Rating (1=Good, 5=Poor)', fontsize=12)
    plt.title(f'Simple Linear Regression: Condition Rating vs Crack Width\nR² = {r_value**2:.3f}, p = {p_value:.4f}', 
              fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(False)
    plt.tight_layout()
    
    # Save
    output_path = '../simple_regression.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved to {output_path}")
    print(f"R² = {r_value**2:.3f}, p-value = {p_value:.4f}")
    plt.close()

if __name__ == "__main__":
    generate_simple_regression()

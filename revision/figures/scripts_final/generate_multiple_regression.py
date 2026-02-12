"""
Generate multiple_regression.png
Shows actual vs predicted values from a multivariate regression model.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import os

def generate_multiple_regression():
    # Load data
    if os.path.exists('../../processed_data.csv'):
        df = pd.read_csv('../../processed_data.csv')
    elif os.path.exists('../processed_data.csv'):
        df = pd.read_csv('../processed_data.csv')
    else:
        print("Error: processed_data.csv not found.")
        return
    
    # Set style
    sns.set_style("white")
    
    # Define variables
    outcome_var = 'Condition_Rating'
    predictor_vars = [
        'Avg_Temp_C',
        'Annual_Rainfall_mm',
        'Humidity_Percent',
        'Crack_Width_mm',
        'Salt_Deposition_g_m2'
    ]
    
    # Prepare data
    data_clean = df[predictor_vars + [outcome_var]].dropna()
    X = data_clean[predictor_vars]
    y = data_clean[outcome_var]
    
    # Fit model
    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X)
    r2 = r2_score(y, y_pred)
    
    # Create plot
    plt.figure(figsize=(10, 6))
    plt.grid(False)
    
    # Scatter plot colored by actual rating
    plt.scatter(y, y_pred, alpha=0.6, s=60, c=y, cmap='viridis')
    
    # Perfect prediction line
    min_val = min(y.min(), y_pred.min())
    max_val = max(y.max(), y_pred.max())
    plt.plot([min_val, max_val], [min_val, max_val], 'r--', linewidth=2, label='Perfect Prediction')
    
    plt.xlabel(f'Actual {outcome_var}', fontsize=12)
    plt.ylabel(f'Predicted {outcome_var}', fontsize=12)
    plt.title(f'Multiple Regression: Actual vs Predicted {outcome_var}\\nR² = {r2:.3f}', 
              fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(False)
    plt.tight_layout()
    
    # Save
    output_path = '../multiple_regression.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved to {output_path}")
    print(f"R² = {r2:.3f}")
    plt.close()

if __name__ == "__main__":
    generate_multiple_regression()

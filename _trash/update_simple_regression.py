import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os
import shutil

# Set style
sns.set_style("white")

# Load data
df = pd.read_csv('processed_data.csv')

# Variables for Condition vs Crack Width
# Based on the user's image: X axis is Crack Width, Y axis is Condition Rating
predictor = 'Crack_Width_mm'
outcome = 'Condition_Rating'
color_var = 'Condition_Rating'

# Check if columns exist
required_cols = [predictor, outcome, color_var]
missing_cols = [col for col in required_cols if col not in df.columns]

if not missing_cols:
    # Prepare data (remove missing values)
    data_clean = df[required_cols].dropna()
    
    X = data_clean[predictor]
    Y = data_clean[outcome]
    C = data_clean[color_var]
    
    # Perform linear regression
    slope, intercept, r_value, p_value, std_err = stats.linregress(X, Y)
    
    # Plot
    plt.figure(figsize=(10, 6))
    
    # Remove grid
    plt.grid(False)
    
    # Scatter plot with condition colors
    # Using viridis cmap as requested
    scatter = plt.scatter(X, Y, alpha=0.6, s=60, c=C, cmap='viridis')
    # plt.colorbar(scatter, label='Condition Rating') # Colorbar might be redundant if Y is Condition Rating, but nice for consistency
    
    # Plot the regression line
    x_line = np.linspace(X.min(), X.max(), 100)
    y_line = slope * x_line + intercept
    plt.plot(x_line, y_line, 'r-', linewidth=3, label=f'Best Fit Line')
    
    plt.xlabel('Crack Width (mm)', fontsize=12)
    plt.ylabel('Condition Rating', fontsize=12)
    plt.title(f'Simple Regression: Crack Width → Condition Rating\nR² = {r_value**2:.3f}, p = {p_value:.4f}', 
              fontsize=14, fontweight='bold')
    plt.legend()
    
    # Ensure no grid
    plt.grid(False)
    
    plt.tight_layout()
    
    # Save
    if not os.path.exists('figures'):
        os.makedirs('figures')
    output_path = 'figures/simple_regression.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved {output_path}")
    
    # Copy to revision
    revision_figs = 'revision/figures'
    if not os.path.exists(revision_figs):
        os.makedirs(revision_figs)
    target_path = os.path.join(revision_figs, 'simple_regression.png')
    shutil.copy(output_path, target_path)
    print(f"Copied to {target_path}")

    # Print results
    print("=" * 70)
    print("REGRESSION RESULTS")
    print("=" * 70)
    print(f"Equation: {outcome} = {slope:.4f} × {predictor} + {intercept:.4f}")
    print(f"\nR² = {r_value**2:.3f}")
    print(f"p-value = {p_value:.4f}")
    
else:
    print(f"Error: Missing columns {missing_cols}")

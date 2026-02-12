import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import os
import shutil

# Set style
sns.set_style("white")

# Load data
df = pd.read_csv('processed_data.csv')

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

# Plot
plt.figure(figsize=(10, 6))

# Remove grid
plt.grid(False)

# Use viridis colormap for points based on actual rating
# This matches the consistency where Condition Rating dictates color
plt.scatter(y, y_pred, alpha=0.6, s=60, c=y, cmap='viridis')

# Plot perfect prediction line
min_val = min(y.min(), y_pred.min())
max_val = max(y.max(), y_pred.max())
plt.plot([min_val, max_val], [min_val, max_val], 'r--', linewidth=2, label='Perfect Prediction')

plt.xlabel(f'Actual {outcome_var}', fontsize=12)
plt.ylabel(f'Predicted {outcome_var}', fontsize=12)
plt.title(f'Multiple Regression: Actual vs Predicted {outcome_var}\nR² = {r2:.3f}', 
          fontsize=14, fontweight='bold')
plt.legend()

# Ensure no grid (redundant check)
plt.grid(False)

plt.tight_layout()

# Save
if not os.path.exists('figures'):
    os.makedirs('figures')
output_path = 'figures/multiple_regression.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"Saved {output_path}")

# Copy to revision
revision_figs = 'revision/figures'
if not os.path.exists(revision_figs):
    os.makedirs(revision_figs)
target_path = os.path.join(revision_figs, 'multiple_regression.png')
shutil.copy(output_path, target_path)
print(f"Copied to {target_path}")

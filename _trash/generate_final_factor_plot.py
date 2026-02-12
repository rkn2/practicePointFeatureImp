import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import FactorAnalysis

# Load Data
df = pd.read_csv('processed_data.csv')

# Features list
features = [
    'Construction_Year', 'Avg_Temp_C', 'Temp_Range_C', 'Annual_Rainfall_mm', 
    'Humidity_Percent', 'Freeze_Thaw_Cycles', 'Soil_Moisture_Index', 
    'Crack_Width_mm', 'Salt_Deposition_g_m2'
]
X = df[features]

# Factor Analysis
fa = FactorAnalysis(n_components=3, rotation='varimax', random_state=42)
X_fa = fa.fit_transform(X)
# Flip signs for Factors 1 and 2 so High Score = High Rain/Damage (Intuitive)
df['Factor1'] = -X_fa[:, 0]
df['Factor2'] = -X_fa[:, 1]
df['Factor3'] = X_fa[:, 2]

# Plotting
plt.figure(figsize=(9, 7))

colors = sns.color_palette("viridis", 5)


# Scatter plot colored by Condition Rating
scatter = sns.scatterplot(
    x='Factor1', y='Factor2', 
    hue='Condition_Rating', palette=colors,
    data=df, s=100, alpha=0.9, edgecolor='black', linewidth=0.5
)
# Set the style to 'white' or 'ticks' to disable grids
sns.set_style("white")


# Customize Axes Labels based on Loadings:
# Factor 1: Rainfall (was -0.82, now +0.82) -> "Groundwater Pressure"
# Factor 2: Crack Width (was -0.85, now +0.85) -> "Structural Damage"
plt.xlabel('Factor 1: Groundwater Pressure\n(High Values = High Rain/Soil Moisture)', fontsize=12)
plt.ylabel('Factor 2: Structural Damage\n(High Values = Wide Cracks)', fontsize=12)
plt.title('Factor Analysis: Environment vs. Damage', fontsize=14, pad=15)

# Add grid
plt.grid(False)

# Arrow and text removed as requested

# Legend Check
plt.legend(title='Condition Rating\n(1=Good, 5=Poor)', bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
plt.savefig('revision/figures/factor_scores_risk.png', dpi=300)
print("Plot saved to revision/figures/factor_scores_risk.png")

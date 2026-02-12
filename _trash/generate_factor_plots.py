import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import FactorAnalysis
from sklearn.preprocessing import StandardScaler

# Load Data
df = pd.read_csv('processed_data.csv')

# Reverse One-Hot Encoding for Material
material_cols = [c for c in df.columns if 'Material_Type_' in c]
def get_material(row):
    for col in material_cols:
        if row[col] == 1:
            return col.replace('Material_Type_', '')
    return 'Unknown'

df['Material'] = df.apply(get_material, axis=1)

# Select Features for Factor Analysis
# Exclude meta-data like IDs and outcomes like Condition_Rating
features = [
    'Construction_Year', 'Avg_Temp_C', 'Temp_Range_C', 'Annual_Rainfall_mm', 
    'Humidity_Percent', 'Freeze_Thaw_Cycles', 'Soil_Moisture_Index', 
    'Crack_Width_mm', 'Salt_Deposition_g_m2'
]

X = df[features]

# Factor Analysis
fa = FactorAnalysis(n_components=2, rotation='varimax', random_state=42)
X_fa = fa.fit_transform(X)
df['Factor1'] = X_fa[:, 0]
df['Factor2'] = X_fa[:, 1]

# Plotting
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Plot 1: Colored by Condition Rating (Risk)
# This shows if the factors separate Good vs Bad buildings
sns.scatterplot(
    x='Factor1', y='Factor2', 
    hue='Condition_Rating', palette='RdYlBu_r', 
    data=df, ax=axes[0], s=80, alpha=0.8
)
axes[0].set_title('Factor Scores by Condition Rating (Risk)')
axes[0].set_xlabel('Factor 1 (Likely Moisture/Soil)')
axes[0].set_ylabel('Factor 2 (Likely Thermal/Structure)')
axes[0].grid(True, linestyle='--', alpha=0.6)

# Plot 2: Colored by Material Type
# This shows if different materials define the clusters
sns.scatterplot(
    x='Factor1', y='Factor2', 
    hue='Material', palette='Set2', 
    data=df, ax=axes[1], s=80, alpha=0.8
)
axes[1].set_title('Factor Scores by Material Type')
axes[1].set_xlabel('Factor 1')
axes[1].set_ylabel('Factor 2')
axes[1].grid(True, linestyle='--', alpha=0.6)

# Plot 3: Colored by Soil Moisture (Underlying Driver)
# This confirms the physical meaning of Factor 1
norm = plt.Normalize(df['Soil_Moisture_Index'].min(), df['Soil_Moisture_Index'].max())
sm = plt.cm.ScalarMappable(cmap="Blues", norm=norm)
sm.set_array([])

sc = axes[2].scatter(
    df['Factor1'], df['Factor2'], 
    c=df['Soil_Moisture_Index'], cmap='Blues', 
    s=80, alpha=0.8, edgecolors='k', linewidth=0.5
)
axes[2].set_title('Factor Scores by Soil Moisture')
axes[2].set_xlabel('Factor 1')
axes[2].set_ylabel('Factor 2')
axes[2].grid(True, linestyle='--', alpha=0.6)
cbar = plt.colorbar(sm, ax=axes[2])
cbar.set_label('Soil Moisture Index')

plt.tight_layout()
plt.savefig('revision/figures/factor_plot_options.png', dpi=300)
print("Plots saved to revision/figures/factor_plot_options.png")

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.decomposition import FactorAnalysis

# Load Data
df = pd.read_csv('processed_data.csv')

# Features
features = [
    'Construction_Year', 'Avg_Temp_C', 'Temp_Range_C', 'Annual_Rainfall_mm', 
    'Humidity_Percent', 'Freeze_Thaw_Cycles', 'Soil_Moisture_Index', 
    'Crack_Width_mm', 'Salt_Deposition_g_m2'
]
X = df[features]

# Factor Analysis
fa = FactorAnalysis(n_components=3, rotation='varimax', random_state=42)
fa.fit(X)

# Loadings DataFrame
# Flip signs of Factors 1 and 2 for intuitive interpretation
loadings = pd.DataFrame(fa.components_.T, index=features, columns=['Factor 1', 'Factor 2', 'Factor 3'])
loadings['Factor 1'] = -loadings['Factor 1']
loadings['Factor 2'] = -loadings['Factor 2']

# Plot
plt.figure(figsize=(8, 10))
# Heatmap centered at 0
sns.heatmap(loadings, annot=True, cmap='RdBu_r', center=0, vmin=-1, vmax=1)
plt.title('Factor Loadings: Variable Contributions', fontsize=14)
plt.tight_layout()
plt.savefig('revision/figures/factor_loadings.png', dpi=300)
print("Saved revision/figures/factor_loadings.png")

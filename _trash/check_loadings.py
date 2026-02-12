import pandas as pd
from sklearn.decomposition import FactorAnalysis

# Load Data
df = pd.read_csv('processed_data.csv')

# Select Features
features = [
    'Construction_Year', 'Avg_Temp_C', 'Temp_Range_C', 'Annual_Rainfall_mm', 
    'Humidity_Percent', 'Freeze_Thaw_Cycles', 'Soil_Moisture_Index', 
    'Crack_Width_mm', 'Salt_Deposition_g_m2'
]
X = df[features]

# Factor Analysis
fa = FactorAnalysis(n_components=2, rotation='varimax', random_state=42)
fa.fit(X)

# Create Loadings DataFrame
loadings = pd.DataFrame(fa.components_.T, index=features, columns=['Factor 1', 'Factor 2'])
print("Factor Loadings:")
print(loadings)

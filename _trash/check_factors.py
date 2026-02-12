import pandas as pd
import numpy as np
from sklearn.decomposition import FactorAnalysis
from sklearn.preprocessing import StandardScaler

# Load Data
df = pd.read_csv('processed_data.csv')

# Features
features = [
    'Construction_Year', 'Avg_Temp_C', 'Temp_Range_C', 'Annual_Rainfall_mm', 
    'Humidity_Percent', 'Freeze_Thaw_Cycles', 'Soil_Moisture_Index', 
    'Crack_Width_mm', 'Salt_Deposition_g_m2'
]
X = df[features]

# Standardize
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Calculate Eigenvalues of Correlation Matrix
corr_matrix = np.corrcoef(X_scaled.T)
eigenvalues, _ = np.linalg.eig(corr_matrix)

print("Eigenvalues:", np.sort(eigenvalues)[::-1])

# Check explained variance for 2 factors vs more
fa2 = FactorAnalysis(n_components=2, rotation='varimax')
fa2.fit(X)
# There isn't a direct "explained_variance_ratio_" for FA like PCA, 
# but we can look at the noise variance or just the loadings magnitude sum.

print("\nRunning FA with n=3 to see loadings...")
fa3 = FactorAnalysis(n_components=3, rotation='varimax')
fa3.fit(X)
loadings3 = pd.DataFrame(fa3.components_.T, index=features, columns=['Factor 1', 'Factor 2', 'Factor 3'])
print(loadings3)

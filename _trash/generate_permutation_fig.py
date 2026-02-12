import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.inspection import permutation_importance

# Load data
df = pd.read_csv('heritage_data.csv')

# Prepare features and target - select only numeric columns
numeric_cols = ['Construction_Year', 'Avg_Temp_C', 'Temp_Range_C', 'Annual_Rainfall_mm', 
                'Humidity_Percent', 'Freeze_Thaw_Cycles', 'Soil_Moisture_Index', 
                'Crack_Width_mm', 'Salt_Deposition_g_m2']
X = df[numeric_cols].fillna(df[numeric_cols].mean())
y = df['Condition_Rating']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a simple Random Forest model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Calculate permutation importance
result = permutation_importance(model, X_test, y_test, n_repeats=10, random_state=42)
importances = result.importances_mean
indices = np.argsort(importances)[::-1]

# Create plot
sns.set_style('white')
plt.figure(figsize=(8,5))
plt.grid(False)
sns.barplot(x=importances[indices], y=[X_test.columns[i] for i in indices], palette='viridis')
plt.title('Permutation Importance')
plt.xlabel('Mean Decrease in Score')
plt.tight_layout()
plt.savefig('figures/permutation_importance.png', dpi=300, bbox_inches='tight')
plt.close()
print("Generated figures/permutation_importance.png")

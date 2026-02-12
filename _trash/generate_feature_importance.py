import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import r2_score, mean_absolute_error
import os
import shutil

# Set style
sns.set_style("white")

# Load data
df = pd.read_csv('processed_data.csv')

# Prepare Data
target = 'Condition_Rating'
drop_cols = ['Building_ID', 'Condition_Rating', 'Intervention_Urgency']
# Ensure columns exist before dropping
cols_to_drop = [c for c in drop_cols if c in df.columns]
X = df.drop(columns=cols_to_drop)
y = df[target]

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 1. Random Forest
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)
r2_rf = r2_score(y_test, y_pred_rf)
mae_rf = mean_absolute_error(y_test, y_pred_rf)

# 2. Gradient Boosting
gb = GradientBoostingRegressor(n_estimators=100, random_state=42)
gb.fit(X_train, y_train)
y_pred_gb = gb.predict(X_test)
r2_gb = r2_score(y_test, y_pred_gb)
mae_gb = mean_absolute_error(y_test, y_pred_gb)

# Visualization 1: Feature Importance (Random Forest)
importances = rf.feature_importances_
feature_names = X.columns
# Sort
indices = np.argsort(importances)[::-1]
sorted_importances = importances[indices]
sorted_features = feature_names[indices]

plt.figure(figsize=(10, 8))
# Create barplot
# Note: Orient 'h' for horizontal bars is easier to read labels
sns.barplot(x=sorted_importances, y=sorted_features, palette='viridis')
plt.title('Feature Importance (Random Forest)\nWhat drives deterioration?', fontsize=14, fontweight='bold')
plt.xlabel('Importance (0-1)', fontsize=12)
plt.ylabel('Feature', fontsize=12)
plt.tight_layout()

# Save Feature Importance
if not os.path.exists('figures'):
    os.makedirs('figures')
plt.savefig('figures/feature_importance.png', dpi=300, bbox_inches='tight')
print("Saved figures/feature_importance.png")

# Copy to revision
if not os.path.exists('revision/figures'):
    os.makedirs('revision/figures')
target_path = os.path.join('revision', 'figures', 'feature_importance.png')
shutil.copy('figures/feature_importance.png', target_path)
print(f"Copied to {target_path}")

# Report Top 5 Features
print("\n" + "="*50)
print("TOP 5 MOST IMPORTANT FEATURES (Random Forest)")
print("="*50)
for i in range(min(5, len(sorted_features))):
    print(f"{i+1}. {sorted_features[i]}: {sorted_importances[i]:.4f}")

# Visualization 2: Model Comparison
comparison = pd.DataFrame({
    'Model': ['Random Forest', 'Gradient Boosting'],
    'R2 Score': [r2_rf, r2_gb],
    'MAE': [mae_rf, mae_gb]
})

plt.figure(figsize=(8, 6))
sns.barplot(x='Model', y='R2 Score', data=comparison, palette='viridis')
plt.title('Model Performance Comparison (R² Score)', fontsize=14, fontweight='bold')
plt.ylim(0, 1.0)
for index, row in comparison.iterrows():
    plt.text(index, row['R2 Score'] + 0.02, f"{row['R2 Score']:.3f}", ha='center', fontsize=12)
plt.tight_layout()

# Save Model Comparison
plt.savefig('figures/model_comparison.png', dpi=300, bbox_inches='tight')
print("Saved figures/model_comparison.png")
target_path_model = os.path.join('revision', 'figures', 'model_comparison.png')
shutil.copy('figures/model_comparison.png', target_path_model)
print(f"Copied to {target_path_model}")

print("\n" + "="*50)
print("MODEL COMPARISON")
print("="*50)
print(comparison)

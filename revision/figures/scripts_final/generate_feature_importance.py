"""
Generate feature_importance.png
Shows feature importance ranking from Random Forest model.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error
import os

def generate_feature_importance():
    # Load data - check multiple locations
    data_paths = [
        '../../../processed_data.csv',        # From scripts_final (3 levels up to root)
        '../../processed_data.csv',           # From scripts_final (2 levels up)
        '../processed_data.csv',              # One level up
        'processed_data.csv',                 # Current directory
    ]
    
    df = None
    for path in data_paths:
        if os.path.exists(path):
            df = pd.read_csv(path)
            print(f"✓ Loaded data from: {path}")
            break
    
    if df is None:
        print("Error: processed_data.csv not found in any expected location.")
        print("Searched:", data_paths)
        return
    
    # Set style
    sns.set_style("white")
    
    # Prepare data
    target = 'Condition_Rating'
    drop_cols = ['Building_ID', 'Condition_Rating', 'Intervention_Urgency']
    cols_to_drop = [c for c in drop_cols if c in df.columns]
    X = df.drop(columns=cols_to_drop)
    y = df[target]
    
    # Add random noise column as benchmark
    np.random.seed(42)
    X['Random_Noise'] = np.random.randn(len(X))
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train Random Forest
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    y_pred_rf = rf.predict(X_test)
    r2_rf = r2_score(y_test, y_pred_rf)
    mae_rf = mean_absolute_error(y_test, y_pred_rf)
    
    # Get feature importances
    importances = rf.feature_importances_
    feature_names = X.columns
    
    # Sort by importance
    indices = np.argsort(importances)[::-1]
    sorted_importances = importances[indices]
    sorted_features = feature_names[indices]
    
    # Create colors: red for noise, viridis for real features
    colors = []
    for feat in sorted_features:
        if 'Random_Noise' in feat:
            colors.append('#FF6B6B')  # Red for noise
        else:
            colors.append('#4ECDC4')  # Teal for real features
    
    # Create plot
    plt.figure(figsize=(10, 10))
    bars = plt.barh(range(len(sorted_features)), sorted_importances, color=colors, alpha=0.8)
    plt.yticks(range(len(sorted_features)), sorted_features)
    plt.xlabel('Importance Score', fontsize=12)
    plt.ylabel('Feature', fontsize=12)
    plt.title('Feature Importance with Random Noise Benchmark\n(Red = Random Noise Baseline)', 
              fontsize=14, fontweight='bold')
    
    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor='#4ECDC4', label='Real Features'),
                      Patch(facecolor='#FF6B6B', label='Random Noise (Baseline)')]
    plt.legend(handles=legend_elements, loc='lower right')
    
    plt.gca().invert_yaxis()  # Highest importance at top
    plt.tight_layout()
    
    # Save
    output_path = '../feature_importance.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved to {output_path}")
    print(f"Model R² = {r2_rf:.3f}, MAE = {mae_rf:.3f}")
    print(f"\nTop 5 Features:")
    for i in range(min(5, len(sorted_features))):
        print(f"  {i+1}. {sorted_features[i]}: {sorted_importances[i]:.4f}")
    plt.close()

if __name__ == "__main__":
    generate_feature_importance()

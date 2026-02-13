"""
Generate permutation_importance.png
Shows permutation importance scores validating feature importance.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.inspection import permutation_importance
import os

def generate_permutation_importance():
    # Load data - check multiple locations
    data_paths = [
        '../../../processed_data.csv',
        '../../processed_data.csv',
        '../processed_data.csv',
        'processed_data.csv',
    ]
    
    df = None
    for path in data_paths:
        if os.path.exists(path):
            df = pd.read_csv(path)
            print(f"✓ Loaded data from: {path}")
            break
    
    if df is None:
        print("Error: processed_data.csv not found.")
        return
    
    # Prepare features and target - select only numeric columns
    numeric_cols = ['Construction_Year', 'Avg_Temp_C', 'Temp_Range_C', 'Annual_Rainfall_mm', 
                    'Humidity_Percent', 'Freeze_Thaw_Cycles', 'Soil_Moisture_Index', 
                    'Crack_Width_mm', 'Salt_Deposition_g_m2']
    
    # Check which columns exist
    available_cols = [col for col in numeric_cols if col in df.columns]
    
    X = df[available_cols].fillna(df[available_cols].mean())
    
    # Add random noise column as benchmark
    np.random.seed(42)
    X['Random_Noise'] = np.random.randn(len(X))
    
    y = df['Condition_Rating']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train Random Forest model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Calculate permutation importance
    result = permutation_importance(model, X_test, y_test, n_repeats=10, random_state=42)
    importances = result.importances_mean
    indices = np.argsort(importances)[::-1]
    
    # Set style
    sns.set_style('white')
    
    # Get feature names in sorted order
    sorted_features = [X_test.columns[i] for i in indices]
    sorted_importances = importances[indices]
    
    # Create colors: red for noise, teal for real features
    colors = []
    for feat in sorted_features:
        if 'Random_Noise' in feat:
            colors.append('#FF6B6B')  # Red for noise
        else:
            colors.append('#4ECDC4')  # Teal for real features
    
    # Create plot
    plt.figure(figsize=(10, 8))
    plt.grid(False)
    bars = plt.barh(range(len(sorted_features)), sorted_importances, color=colors, alpha=0.8)
    plt.yticks(range(len(sorted_features)), sorted_features)
    plt.xlabel('Mean Decrease in Score', fontsize=12)
    plt.ylabel('Feature', fontsize=12)
    plt.title('Permutation Importance with Random Noise Benchmark\n(Red = Random Noise Baseline)', 
              fontsize=14, fontweight='bold')
    
    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor='#4ECDC4', label='Real Features'),
                      Patch(facecolor='#FF6B6B', label='Random Noise (Baseline)')]
    plt.legend(handles=legend_elements, loc='lower right')
    
    plt.gca().invert_yaxis()  # Highest importance at top
    plt.tight_layout()
    
    # Save
    output_path = '../permutation_importance.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved to {output_path}")
    plt.close()

if __name__ == "__main__":
    generate_permutation_importance()

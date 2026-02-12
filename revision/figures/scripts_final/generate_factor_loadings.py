"""
Generate factor_loadings.png
Shows factor loadings heatmap from factor analysis.
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.decomposition import FactorAnalysis
import os

def generate_factor_loadings():
    # Load data
    if os.path.exists('../../processed_data.csv'):
        df = pd.read_csv('../../processed_data.csv')
    elif os.path.exists('../processed_data.csv'):
        df = pd.read_csv('../processed_data.csv')
    else:
        print("Error: processed_data.csv not found.")
        return
    
    # Features for factor analysis
    features = [
        'Construction_Year', 'Avg_Temp_C', 'Temp_Range_C', 'Annual_Rainfall_mm', 
        'Humidity_Percent', 'Freeze_Thaw_Cycles', 'Soil_Moisture_Index', 
        'Crack_Width_mm', 'Salt_Deposition_g_m2'
    ]
    X = df[features]
    
    # Perform Factor Analysis
    fa = FactorAnalysis(n_components=3, rotation='varimax', random_state=42)
    fa.fit(X)
    
    # Create loadings DataFrame
    # Flip signs of Factors 1 and 2 for intuitive interpretation
    loadings = pd.DataFrame(fa.components_.T, index=features, columns=['Factor 1', 'Factor 2', 'Factor 3'])
    loadings['Factor 1'] = -loadings['Factor 1']
    loadings['Factor 2'] = -loadings['Factor 2']
    
    # Create plot
    plt.figure(figsize=(8, 10))
    sns.heatmap(loadings, annot=True, cmap='RdBu_r', center=0, vmin=-1, vmax=1)
    plt.title('Factor Loadings: Variable Contributions', fontsize=14)
    plt.tight_layout()
    
    # Save
    output_path = '../factor_loadings.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved to {output_path}")
    plt.close()

if __name__ == "__main__":
    generate_factor_loadings()

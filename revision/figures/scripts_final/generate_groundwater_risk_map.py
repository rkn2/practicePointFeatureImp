"""
Generate groundwater_risk_map.png
Shows spatial distribution of condition rating (groundwater risk correlation).
Note: This uses dummy coordinates. Replace with actual spatial data if available.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

def generate_groundwater_risk_map():
    # Load data
    if os.path.exists('../../../processed_data.csv'):
        df = pd.read_csv('../../../processed_data.csv')
    elif os.path.exists('../../processed_data.csv'):
        df = pd.read_csv('../../processed_data.csv')
    else:
        print("Error: processed_data.csv not found.")
        return
    
    # Set style
    sns.set_style('white')
    
    # Create plot
    plt.figure(figsize=(12, 8))
    plt.grid(False)
    
    # Generate spatial coordinates if not present
    if 'Longitude' not in df.columns or 'Latitude' not in df.columns:
        np.random.seed(42)  # Fallback for reproducible testing without data
        df['Longitude'] = -77.8 + np.random.randn(len(df)) * 0.1
        df['Latitude'] = 40.8 + np.random.randn(len(df)) * 0.1
    
    # Create scatter plot
    scatter = plt.scatter(df['Longitude'], df['Latitude'], 
                         c=df['Condition_Rating'], 
                         cmap='viridis', 
                         s=100, 
                         alpha=0.7,
                         edgecolor='black',
                         linewidth=0.5)
    
    plt.colorbar(scatter, label='Condition Rating (1=Good, 5=Poor)')
    plt.title('Spatial Distribution of Building Condition\\n(Groundwater Risk Correlation)', 
              fontsize=14, fontweight='bold')
    plt.xlabel('Longitude', fontsize=12)
    plt.ylabel('Latitude', fontsize=12)
    plt.tight_layout()
    
    # Save
    output_path = '../groundwater_risk_map.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved to {output_path}")
    print("NOTE: This uses dummy coordinates. Update with actual spatial data if available.")
    plt.close()

if __name__ == "__main__":
    generate_groundwater_risk_map()

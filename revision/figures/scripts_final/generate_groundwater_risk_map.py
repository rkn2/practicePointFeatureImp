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
    if os.path.exists('../../processed_data.csv'):
        df = pd.read_csv('../../processed_data.csv')
    elif os.path.exists('../processed_data.csv'):
        df = pd.read_csv('../processed_data.csv')
    else:
        print("Error: processed_data.csv not found.")
        return
    
    # Set style
    sns.set_style('white')
    
    # Create plot
    plt.figure(figsize=(12, 8))
    plt.grid(False)
    
    # Generate spatial coordinates if not present
    # NOTE: Replace this with actual X/Y coordinates if available in your data
    if 'x' not in df.columns or 'y' not in df.columns:
        np.random.seed(42)  # For reproducibility
        df['x'] = np.random.rand(len(df)) * 100
        df['y'] = np.random.rand(len(df)) * 100
    
    # Create scatter plot
    scatter = plt.scatter(df['x'], df['y'], 
                         c=df['Condition_Rating'], 
                         cmap='viridis', 
                         s=100, 
                         alpha=0.7,
                         edgecolor='black',
                         linewidth=0.5)
    
    plt.colorbar(scatter, label='Condition Rating (1=Good, 5=Poor)')
    plt.title('Spatial Distribution of Building Condition\\n(Groundwater Risk Correlation)', 
              fontsize=14, fontweight='bold')
    plt.xlabel('X Coordinate', fontsize=12)
    plt.ylabel('Y Coordinate', fontsize=12)
    plt.tight_layout()
    
    # Save
    output_path = '../groundwater_risk_map.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved to {output_path}")
    print("NOTE: This uses dummy coordinates. Update with actual spatial data if available.")
    plt.close()

if __name__ == "__main__":
    generate_groundwater_risk_map()

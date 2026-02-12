"""
Generate correlation_heatmap.png
Shows correlation matrix heatmap of relationships between variables.
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

def generate_correlation_heatmap():
    # Load data
    if os.path.exists('../../processed_data.csv'):
        df = pd.read_csv('../../processed_data.csv')
    elif os.path.exists('../processed_data.csv'):
        df = pd.read_csv('../processed_data.csv')
    else:
        print("Error: processed_data.csv not found.")
        return
    
    # Select numeric columns for correlation
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    # Remove ID columns if present
    numeric_cols = [col for col in numeric_cols if 'ID' not in col]
    
    # Calculate correlation matrix
    corr = df[numeric_cols].corr()
    
    # Set style
    sns.set_style("white")
    
    # Create figure
    plt.figure(figsize=(12, 10))
    
    # Create heatmap
    sns.heatmap(corr, 
                annot=False,
                cmap='coolwarm',
                center=0,
                vmin=-1,
                vmax=1,
                square=True,
                linewidths=0.5,
                cbar_kws={'shrink': 0.8})
    
    plt.title('Correlation Matrix Heatmap', fontsize=14)
    plt.tight_layout()
    
    # Save
    output_path = '../correlation_heatmap.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved to {output_path}")
    plt.close()

if __name__ == "__main__":
    generate_correlation_heatmap()

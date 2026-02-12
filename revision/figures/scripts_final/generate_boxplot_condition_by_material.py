"""
Generate boxplot_condition_by_material.png
Shows distribution of condition ratings by material type.
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

def generate_boxplot_condition_by_material():
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
    plt.figure(figsize=(10, 6))
    plt.grid(False)
    
    # Boxplot of Condition Rating by Material Type
    sns.boxplot(x='Material_Type', y='Condition_Rating', data=df, palette='viridis')
    plt.title('Condition Rating by Material Type', fontsize=14, fontweight='bold')
    plt.xlabel('Material Type', fontsize=12)
    plt.ylabel('Condition Rating', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Save
    output_path = '../boxplot_condition_by_material.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved to {output_path}")
    plt.close()

if __name__ == "__main__":
    generate_boxplot_condition_by_material()
